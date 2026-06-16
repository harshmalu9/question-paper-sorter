import re

from mvp.models import MVPPGroup

PAGE_NUM_WEIGHT = 0.40
QUESTION_CONT_WEIGHT = 0.30
SENTENCE_CONT_WEIGHT = 0.20
LAYOUT_WEIGHT = 0.10


def _extract_page_number(
    text: str,
) -> int | None:

    lines = text.strip().split("\n")

    for line in lines[:5]:

        line = line.strip()

        m = re.match(
            r"^(\d{1,3})\s*$", line
        )

        if m:
            return int(m.group(1))

        m = re.match(
            r"^Page\s*(\d{1,3})",
            line,
            re.IGNORECASE,
        )

        if m:
            return int(m.group(1))

    return None


def _page_number_score(
    pages_text: list[str],
    page_numbers: list[int],
) -> float:

    if len(pages_text) <= 1:
        return 0.95

    extracted = []
    for text in pages_text:
        n = _extract_page_number(text)
        if n is not None:
            extracted.append(n)

    if len(extracted) < 2:
        return 0.5

    correct = 0
    total = len(extracted) - 1

    for i in range(total):
        expected = extracted[i] + 1
        if extracted[i + 1] == expected:
            correct += 1
        elif extracted[i + 1] == expected + 1:
            correct += 1

    return (
        correct / total if total > 0 else 0.5
    )


def _question_continuity_score(
    pages_text: list[str],
) -> float:

    q_pattern = re.compile(
        r"\b(Q\.?\s*\d+|Question\s*\d+|\d+\.\s)",
        re.IGNORECASE,
    )

    last_question = None
    matches = 0
    total_transitions = (
        len(pages_text) - 1
    )

    if total_transitions < 1:
        return 0.95

    for i, text in enumerate(
        pages_text
    ):

        questions = q_pattern.findall(
            text
        )

        if questions and last_question:

            current = questions[0]

            last_q_num = (
                _extract_q_num(last_question)
            )
            current_q_num = (
                _extract_q_num(current)
            )

            if (
                last_q_num is not None
                and current_q_num is not None
            ):

                expected = last_q_num + 1

                if (
                    current_q_num == expected
                    or current_q_num
                    == expected + 1
                ):
                    matches += 1

        if questions:
            last_question = questions[-1]

    if total_transitions == 0:
        return 0.95

    return matches / total_transitions


def _extract_q_num(
    q_str: str,
) -> int | None:

    nums = re.findall(r"\d+", q_str)

    if nums:
        return int(nums[0])

    return None


def _sentence_continuity_score(
    pages_text: list[str],
) -> float:

    if len(pages_text) <= 1:
        return 0.95

    matches = 0
    total = len(pages_text) - 1

    for i in range(total):

        prev_sentences = (
            _split_sentences(
                pages_text[i]
            )
        )
        next_sentences = (
            _split_sentences(
                pages_text[i + 1]
            )
        )

        if (
            not prev_sentences
            or not next_sentences
        ):
            continue

        last_line = (
            prev_sentences[-1]
            .strip()
            .lower()
        )

        first_line = (
            next_sentences[0]
            .strip()
            .lower()
        )

        if (
            last_line
            and not last_line.endswith(
                "."
            )
            and not last_line.endswith(
                "?"
            )
            and not last_line.endswith(
                "!"
            )
        ):

            if (
                first_line
                and first_line[0]
                not in "0123456789"
            ):
                matches += 1

    return (
        matches / total if total > 0 else 0.5
    )


def _split_sentences(
    text: str,
) -> list[str]:

    parts = re.split(
        r"\n+", text
    )

    return [
        p.strip()
        for p in parts
        if p.strip()
    ]


def _layout_similarity_score(
    pages_text: list[str],
) -> float:

    if len(pages_text) <= 1:
        return 0.95

    matches = 0
    total = len(pages_text) - 1

    for i in range(total):

        prev_lines = pages_text[
            i
        ].strip().split("\n")
        next_lines = pages_text[
            i + 1
        ].strip().split("\n")

        if not prev_lines or not next_lines:
            continue

        plen = min(
            len(prev_lines), 5
        )
        nlen = min(
            len(next_lines), 5
        )

        if abs(plen - nlen) <= 1:
            matches += 1

    return (
        matches / total if total > 0 else 0.5
    )


def reorder_group(
    group: MVPPGroup,
) -> tuple[
    MVPPGroup, float
]:

    pages_text = [
        p.ocr_text
        for p in group.pages
    ]

    page_nums = [
        p.index
        for p in group.pages
    ]

    pn_score = (
        _page_number_score(
            pages_text, page_nums
        )
    )
    qc_score = (
        _question_continuity_score(
            pages_text
        )
    )
    sc_score = (
        _sentence_continuity_score(
            pages_text
        )
    )
    ls_score = (
        _layout_similarity_score(
            pages_text
        )
    )

    confidence = round(
        (
            pn_score
            * PAGE_NUM_WEIGHT
            + qc_score
            * QUESTION_CONT_WEIGHT
            + sc_score
            * SENTENCE_CONT_WEIGHT
            + ls_score * LAYOUT_WEIGHT
        ),
        2,
    )

    group.ordering_confidence = (
        confidence
    )

    return group, confidence


def reorder_groups(
    groups: list[MVPPGroup],
) -> list[MVPPGroup]:

    for i, group in enumerate(
        groups
    ):

        groups[i], _ = reorder_group(
            group
        )

    return groups
