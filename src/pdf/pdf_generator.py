from pathlib import Path
from PIL import Image


class PDFGenerator:

    def generate_folder_pdf(
        self,
        image_folder: str,
        output_pdf: str
    ):

        image_folder = Path(
            image_folder
        )

        images = sorted(
            image_folder.glob("*.jpg")
        )

        if not images:
            return

        pil_images = []

        for image_path in images:

            image = Image.open(
                image_path
            )

            if image.mode != "RGB":
                image = image.convert(
                    "RGB"
                )

            pil_images.append(
                image
            )

        first = pil_images[0]

        rest = pil_images[1:]

        first.save(
            output_pdf,
            save_all=True,
            append_images=rest
        )