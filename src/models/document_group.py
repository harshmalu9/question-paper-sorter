from dataclasses import dataclass, field

from models.page_metadata import PageMetadata


@dataclass
class DocumentGroup:

    pages: list[PageMetadata]

    subject: str | None = None

    subject_confidence: float = 0.0

    document_type: str | None = None

    document_type_confidence: float = 0.0

    topics: list[str] = field(
        default_factory=list
    )
