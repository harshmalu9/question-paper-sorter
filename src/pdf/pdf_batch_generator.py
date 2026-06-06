from pathlib import Path

from pdf.pdf_generator import (
    PDFGenerator
)


class PDFBatchGenerator:

    def generate_all(
        self,
        sorted_root: str,
        output_root: str
    ):

        sorted_root = Path(
            sorted_root
        )

        output_root = Path(
            output_root
        )

        output_root.mkdir(
            parents=True,
            exist_ok=True
        )

        generator = PDFGenerator()

        for subject_dir in sorted_root.iterdir():

            if not subject_dir.is_dir():
                continue

            subject = subject_dir.name

            for type_dir in subject_dir.iterdir():

                if not type_dir.is_dir():
                    continue

                doc_type = type_dir.name

                pdf_name = (
                    f"{subject}_{doc_type}.pdf"
                )

                output_pdf = (
                    output_root / pdf_name
                )

                print(
                    f"Generating {pdf_name}"
                )

                generator.generate_folder_pdf(
                    str(type_dir),
                    str(output_pdf)
                )