from dataclasses import dataclass, field


@dataclass
class MVPPPage:
    index: int
    image_path: str
    ocr_text: str = ""


@dataclass
class MVPPGroup:
    group_id: int
    pages: list[MVPPPage]
    grouping_confidence: float = 0.0
    ordering_confidence: float = 0.0
