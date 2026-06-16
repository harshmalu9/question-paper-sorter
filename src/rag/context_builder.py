import re


def _extract_keywords(query: str) -> list[str]:

    stop_words = {
        "what",
        "were",
        "about",
        "find",
        "list",
        "topics",
        "questions",
        "question",
        "asked",
        "give",
        "tell",
        "show",
        "get",
        "the",
        "and",
        "for",
        "are",
        "was",
        "is",
        "can",
        "how",
        "why",
        "does",
        "do",
        "did",
    }

    words = re.findall(
        r"[a-zA-Z]+", query.lower()
    )

    return [
        w
        for w in words
        if w not in stop_words
        and len(w) > 2
    ]


def _filter_ocr_lines(
    raw_text: str, keywords: list[str]
) -> str:

    if not raw_text:
        return ""

    if not keywords:
        return raw_text[:5000]

    lines = raw_text.split("\n")

    matching = [
        line
        for line in lines
        if any(
            kw in line.lower()
            for kw in keywords
        )
    ]

    if matching:
        return "\n".join(matching)

    return raw_text[:5000]


class ContextBuilder:

    def build(
        self,
        groups: list[dict],
        query: str = "",
    ) -> str:

        keywords = (
            _extract_keywords(query)
        )
        parts = []

        for g in groups:

            group_id = g.get("group_id")
            subject = g.get(
                "subject", "Unknown"
            )
            doc_type = g.get(
                "document_type",
                "Unknown",
            )
            topics = g.get("topics", [])
            raw_text = g.get(
                "raw_text"
            ) or ""

            ocr_excerpt = (
                _filter_ocr_lines(
                    raw_text, keywords
                )
            )

            parts.append(
                "----------------------------------"
            )
            parts.append(
                f"Group {group_id}"
            )
            parts.append(
                f"Subject: {subject}"
            )
            parts.append(
                f"Type: {doc_type}"
            )

            if topics:
                parts.append(
                    "Topics:"
                )

                for phrase, _ in (
                    topics[:10]
                ):
                    parts.append(
                        f"- {phrase}"
                    )

            if ocr_excerpt:
                parts.append(
                    "OCR TEXT:"
                )
                parts.append(
                    ocr_excerpt
                )

            parts.append(
                "----------------------------------"
            )

        return "\n".join(parts)
