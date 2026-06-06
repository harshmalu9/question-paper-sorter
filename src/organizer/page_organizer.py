from pathlib import Path
import shutil


class PageOrganizer:

    def organize(
        self,
        pages,
        output_root: str
    ):

        output_root = Path(output_root)

        for page in pages:

            subject = (
                page.subject
                or "Unknown"
            )

            document_type = (
                page.document_type
                or "Unknown"
            )

            destination = (
                output_root
                / subject
                / document_type
            )

            destination.mkdir(
                parents=True,
                exist_ok=True
            )

            source = Path(
                page.image_path
            )

            shutil.copy2(
                source,
                destination / source.name
            )