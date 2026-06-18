import zipfile

from pathlib import Path

from ocr.pdf_loader import (
    pdf_to_images as _pdf_to_images,
)


def load_pdf(
    pdf_path: str,
    output_dir: str = "data/temp",
) -> list[str]:
    return _pdf_to_images(
        pdf_path, output_dir
    )


def load_zip(
    zip_path: str,
    output_dir: str = "data/temp",
) -> list[str]:
    output_path = Path(output_dir)
    output_path.mkdir(
        parents=True, exist_ok=True
    )

    image_extensions = {
        ".jpg",
        ".jpeg",
        ".png",
    }

    image_paths = []

    with zipfile.ZipFile(
        zip_path, "r"
    ) as zf:
        members = zf.namelist()
        for member in members:
            ext = (
                Path(member)
                .suffix
                .lower()
            )
            if ext in image_extensions:
                zf.extract(
                    member, output_path
                )
                dest = output_path / member
                image_paths.append(
                    str(dest)
                )

    if not image_paths:
        raise ValueError(
            f"No images found in ZIP: "
            f"{zip_path}"
        )

    return image_paths
