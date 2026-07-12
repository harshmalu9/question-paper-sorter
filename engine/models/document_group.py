from dataclasses import dataclass, field

from engine.models.page_metadata import PageMetadata


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

    embedding: list[float] | None = None

    keyphrases: list[tuple[str, int]] = field(
        default_factory=list
    )

    cluster_id: int | None = None

    cluster_name: str | None = None

    raw_text: str | None = None
