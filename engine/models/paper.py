from dataclasses import dataclass


@dataclass
class Paper:

    paper_id: int

    subject: str

    start_page: int

    end_page: int