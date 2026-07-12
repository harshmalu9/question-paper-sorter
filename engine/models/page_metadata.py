from dataclasses import dataclass


@dataclass
class PageMetadata:

    page_number: int

    image_path: str

    ocr_text: str

    subject: str | None = None

    subject_confidence: float = 0.0

    document_type: str | None = None

    document_type_confidence: float = 0.0

    term: str | None = None

    term_confidence: float = 0.0