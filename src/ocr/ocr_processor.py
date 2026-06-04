from pathlib import Path

from models.page_metadata import PageMetadata
from ocr.ocr_engine import OCREngine


class OCRProcessor:

    def __init__(self):
        self.ocr_engine = OCREngine()

    def process_directory(
        self,
        image_directory: str,
        max_pages: int | None = None
    ) -> list[PageMetadata]:

        image_directory = Path(image_directory)

        image_files = sorted(
            image_directory.glob("*.jpg")
        )

        if max_pages is not None:
            image_files = image_files[:max_pages]

        pages = []

        for page_number, image_path in enumerate(
            image_files,
            start=1
        ):

            print(
                f"OCR page {page_number}/{len(image_files)}"
            )

            text = self.ocr_engine.extract_text(
                str(image_path)
            )

            pages.append(
                PageMetadata(
                    page_number=page_number,
                    image_path=str(image_path),
                    ocr_text=text
                )
            )

        return pages