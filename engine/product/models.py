from dataclasses import dataclass


@dataclass
class Page:
    index: int
    image_path: str
    ocr_text: str = ""


@dataclass
class Group:
    group_id: int
    pages: list[Page]
    grouping_confidence: float = 0.0
    ordering_confidence: float = 0.0
