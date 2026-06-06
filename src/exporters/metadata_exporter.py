import json
from dataclasses import asdict

from models.page_metadata import PageMetadata


class MetadataExporter:

    @staticmethod
    def export_pages(
        pages: list[PageMetadata],
        output_file: str
    ):

        data = [
            asdict(page)
            for page in pages
        ]

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )