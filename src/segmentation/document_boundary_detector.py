from sentence_transformers.util import cos_sim

from models.page_metadata import (
    PageMetadata
)

from models.document_group import (
    DocumentGroup
)


class DocumentBoundaryDetector:

    BOUNDARY_SCORES = {
        "department of": 2,
        "internal assessment": 2,
        "question paper": 2,
        "practical examination": 2,
        "university": 1,
        "examination": 1,
    }

    def __init__(self, model):

        self.model = model

    def calculate_similarity(
        self,
        text1: str,
        text2: str
    ) -> float:

        embedding1 = self.model.encode(
            text1,
            convert_to_tensor=True
        )

        embedding2 = self.model.encode(
            text2,
            convert_to_tensor=True
        )

        return cos_sim(
            embedding1,
            embedding2
        ).item()

    def calculate_boundary_score(
        self,
        text: str
    ) -> int:

        first_lines = "\n".join(
            text.lower().split("\n")[:10]
        )

        score = 0

        for (
            keyword,
            value
        ) in self.BOUNDARY_SCORES.items():

            if keyword in first_lines:
                score += value

        return score

    def detect(
        self,
        pages: list[PageMetadata]
    ) -> list[DocumentGroup]:

        if not pages:
            return []

        groups = []

        current_pages = [pages[0]]

        previous_page = pages[0]

        for page in pages[1:]:

            similarity = (
                self.calculate_similarity(
                    previous_page.ocr_text,
                    page.ocr_text
                )
            )

            print(
                f"Similarity: "
                f"Page {previous_page.page_number}"
                f" -> "
                f"Page {page.page_number}"
            )

            print(
                f"Score: {similarity}"
            )

            boundary_score = (
                self.calculate_boundary_score(
                    page.ocr_text
                )
            )

            should_split = (
                boundary_score >= 2
                and len(current_pages) >= 2
            )

            if should_split:

                print(
                    f"Boundary detected "
                    f"at page "
                    f"{page.page_number}"
                )

                print(
                    f"Score: "
                    f"{boundary_score}"
                )

                print(
                    "Boundary reason: "
                    "keyword"
                )

                groups.append(
                    DocumentGroup(
                        pages=current_pages
                    )
                )

                current_pages = []

            current_pages.append(page)

            previous_page = page

        if current_pages:

            groups.append(
                DocumentGroup(
                    pages=current_pages
                )
            )

        return groups