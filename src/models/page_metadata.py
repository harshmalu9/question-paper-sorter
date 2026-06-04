from dataclasses import dataclass


@dataclass
class PageMetadata:
    page_number: int
    image_path: str
    ocr_text: str

    subject: str | None = None
    term: str | None = None

    confidence: float = 0.0