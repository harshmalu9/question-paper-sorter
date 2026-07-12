from pathlib import Path

from pdf2image import convert_from_path
from pdf2image.pdf2image import pdfinfo_from_path


def pdf_to_images(pdf_path: str, output_dir: str) -> list[str]:
    """
    Convert PDF pages into JPG images one page at a time.
    This avoids loading the entire PDF into memory.
    """

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    pdf_info = pdfinfo_from_path(pdf_path)
    total_pages = pdf_info["Pages"]

    image_paths = []

    for page_number in range(1, total_pages + 1):

        print(f"Processing page {page_number}/{total_pages}")

        page = convert_from_path(
            pdf_path,
            first_page=page_number,
            last_page=page_number,
            dpi=150
        )[0]

        image_path = output_path / f"page_{page_number:03d}.jpg"

        page.save(image_path, "JPEG")

        image_paths.append(str(image_path))

        del page

    return image_paths