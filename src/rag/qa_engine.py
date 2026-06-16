import string
import re


class QAEngine:

    def _detect_intent(
        self, query: str
    ) -> str:

        q = query.lower()

        if any(
            phrase in q
            for phrase in [
                "what questions",
                "asked about",
                "question on",
                "questions were",
            ]
        ):
            return "question_extraction"

        if any(
            phrase in q
            for phrase in [
                "find",
                "topics",
                "list",
                "what topics",
            ]
        ):
            return "topic_listing"

        return "summary"

    def _extract_keywords(
        self, query: str
    ) -> list[str]:

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

    def _answer_question_extraction(
        self,
        query: str,
        context: str,
    ) -> str:

        keywords = (
            self._extract_keywords(query)
        )

        lines = context.split("\n")

        ocr_lines = []

        in_ocr = False

        for line in lines:

            stripped = line.strip()

            if stripped == "OCR:":
                in_ocr = True
                continue

            if stripped.startswith(
                "Group"
            ) or stripped.startswith(
                "Subject:"
            ):
                in_ocr = False

            if stripped == "----------":
                in_ocr = False
                continue

            if in_ocr and stripped:

                if any(
                    kw
                    in stripped.lower()
                    for kw in keywords
                ):
                    ocr_lines.append(
                        stripped
                    )

        if not ocr_lines:

            for line in lines:
                stripped = line.strip()

                if (
                    stripped
                    and not stripped.startswith(
                        "- "
                    )
                    and not stripped.startswith(
                        "Group"
                    )
                    and not stripped.startswith(
                        "Subject"
                    )
                    and not stripped.startswith(
                        "Type"
                    )
                    and not stripped.startswith(
                        "Topics"
                    )
                    and not stripped.startswith(
                        "Keyphrases"
                    )
                    and stripped
                    != "OCR:"
                    and stripped
                    != "----------"
                ):

                    if any(
                        kw
                        in stripped.lower()
                        for kw in keywords
                    ):
                        ocr_lines.append(
                            stripped
                        )

        topic_lines = []

        capture_topics = False

        for line in lines:
            stripped = line.strip()

            if stripped == "Topics:":
                capture_topics = True
                continue

            if (
                capture_topics
                and stripped.startswith(
                    "- "
                )
            ):
                topic_name = stripped[
                    2:
                ].strip()

                if any(
                    kw in topic_name.lower()
                    for kw in keywords
                ):
                    topic_lines.append(
                        topic_name
                    )
            else:
                capture_topics = False

        if ocr_lines:

            heading = (
                "Questions related to "
                + " ".join(keywords[:3])
                + ":"
            )

            result = [heading]

            for line in ocr_lines[
                :10
            ]:
                result.append(
                    f"- {line}"
                )

            return "\n".join(result)

        if topic_lines:

            heading = (
                "Topics related to "
                + " ".join(keywords[:3])
                + ":"
            )

            result = [heading]

            for topic in topic_lines[
                :10
            ]:
                result.append(
                    f"- {topic}"
                )

            return "\n".join(result)

        return (
            "No specific information "
            "found. Try rephrasing "
            "your query."
        )

    def _answer_topic_listing(
        self,
        query: str,
        context: str,
    ) -> str:

        keywords = (
            self._extract_keywords(query)
        )

        lines = context.split("\n")

        topics = []

        capture_topics = False

        for line in lines:
            stripped = line.strip()

            if stripped == "Topics:":
                capture_topics = True
                continue

            if capture_topics:
                if stripped.startswith(
                    "- "
                ):
                    topic = stripped[
                        2:
                    ].strip()

                    if not keywords or any(
                        kw in topic.lower()
                        for kw in keywords
                    ):
                        topics.append(
                            topic
                        )
                else:
                    capture_topics = False

        if not topics:
            return (
                "No topics found "
                "for your query."
            )

        seen = set()
        unique = []

        for t in topics:

            if t.lower() not in seen:
                seen.add(t.lower())
                unique.append(t)

        heading = "Topics:"

        result = [heading]

        for topic in unique[:15]:
            result.append(
                f"- {topic}"
            )

        return "\n".join(result)

    def _answer_summary(
        self,
        query: str,
        context: str,
    ) -> str:

        keywords = (
            self._extract_keywords(query)
        )

        lines = context.split("\n")

        topics = set()
        subjects = set()
        types_ = set()
        ocr_matches = []

        capture_topics = False

        for line in lines:
            stripped = line.strip()

            if stripped.startswith(
                "Subject:"
            ):
                subjects.add(
                    stripped.split(
                        ": ", 1
                    )[1]
                )

            if stripped.startswith(
                "Type:"
            ):
                types_.add(
                    stripped.split(
                        ": ", 1
                    )[1]
                )

            if stripped == "Topics:":
                capture_topics = True
                continue

            if capture_topics:
                if stripped.startswith(
                    "- "
                ):
                    topics.add(
                        stripped[
                            2:
                        ].strip()
                    )
                else:
                    capture_topics = False

            if (
                stripped
                and not stripped.startswith(
                    "- "
                )
                and not stripped.startswith(
                    "Group"
                )
                and not stripped.startswith(
                    "Subject"
                )
                and not stripped.startswith(
                    "Type"
                )
                and not stripped.startswith(
                    "Topics"
                )
                and not stripped.startswith(
                    "Keyphrases"
                )
                and stripped
                not in (
                    "OCR:",
                    "----------",
                )
            ):

                if not keywords or any(
                    kw in stripped.lower()
                    for kw in keywords
                ):
                    ocr_matches.append(
                        stripped
                    )

        parts = []

        if topics:

            parts.append(
                "Topics discussed:"
            )

            for t in sorted(topics)[
                :10
            ]:
                parts.append(f"- {t}")

            parts.append("")

        if ocr_matches:

            parts.append(
                "Key excerpts:"
            )

            for m in ocr_matches[:5]:
                parts.append(f"- {m}")

            parts.append("")

        if subjects or types_:

            meta = []

            if subjects:
                meta.append(
                    f"Subjects: "
                    f"{', '.join(subjects)}"
                )

            if types_:
                meta.append(
                    f"Document types: "
                    f"{', '.join(types_)}"
                )

            if meta:
                parts.extend(meta)

        if not parts:
            return (
                "The retrieved "
                "documents do not "
                "contain information "
                "related to your "
                "query."
            )

        return "\n".join(parts).strip()

    def answer(
        self,
        query: str,
        context: str,
    ) -> str:

        intent = self._detect_intent(
            query
        )

        if (
            intent
            == "question_extraction"
        ):
            return (
                self._answer_question_extraction(
                    query, context
                )
            )

        if intent == "topic_listing":
            return (
                self._answer_topic_listing(
                    query, context
                )
            )

        return self._answer_summary(
            query, context
        )
