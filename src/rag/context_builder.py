import json

from pathlib import Path


class ContextBuilder:

    def __init__(
        self, pages_path: str = None
    ):

        self._page_map = {}

        if pages_path is not None:
            self._load_pages(pages_path)

    def _load_pages(
        self, pages_path: str
    ) -> None:

        path = Path(pages_path)

        if not path.exists():
            return

        with open(path) as f:
            pages = json.load(f)

        for p in pages:
            self._page_map[
                p["page_number"]
            ] = p.get("ocr_text", "")

    def _get_ocr_snippet(
        self, group: dict
    ) -> str:

        page_numbers = group.get(
            "pages", []
        )

        texts = []

        for num in page_numbers:

            text = self._page_map.get(
                num
            )

            if text:
                texts.append(text)

        if not texts:
            return ""

        combined = "\n".join(texts)

        if len(combined) > 1000:
            combined = combined[:1000]

        return combined

    def build(
        self, groups: list[dict]
    ) -> str:

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
            keyphrases = g.get(
                "keyphrases", []
            )
            ocr = self._get_ocr_snippet(g)

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

            if keyphrases:
                parts.append(
                    "Keyphrases:"
                )

                for phrase, _ in (
                    keyphrases[:10]
                ):
                    parts.append(
                        f"- {phrase}"
                    )

            if ocr:
                parts.append(
                    "OCR:"
                )
                parts.append(ocr)

            parts.append(
                "----------"
            )

        return "\n".join(parts)
