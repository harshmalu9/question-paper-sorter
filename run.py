import sys
import shutil
from pathlib import Path

sys.path.append("src")

from ocr.pdf_loader import pdf_to_images
from main import main


def clean_temp():

    temp_dir = Path("data/temp")

    if temp_dir.exists():
        shutil.rmtree(temp_dir)

    temp_dir.mkdir(
        parents=True,
        exist_ok=True
    )


def run(pdf_path: str, config_path: str = None):

    clean_temp()

    print()
    print("Converting PDF to images...")

    pdf_to_images(
        pdf_path,
        "data/temp"
    )

    print()
    print("Running pipeline...")

    main(config_path)

    print()
    print("Finished.")


if __name__ == "__main__":

    if len(sys.argv) < 2 or len(sys.argv) > 3:

        print(
            "Usage: python run.py <pdf> [config_file]"
        )

        sys.exit(1)

    pdf = sys.argv[1]
    config = sys.argv[2] if len(sys.argv) == 3 else None

    run(pdf, config)
