from dataclasses import dataclass


@dataclass
class PaperSegment:

    segment_id: int

    start_page: int

    end_page: int

    subject: str

    document_type: str