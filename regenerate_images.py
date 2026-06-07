import sys

sys.path.append("src")

from ocr.pdf_loader import pdf_to_images

pdf_to_images(
    "data/input/sample.pdf",
    "data/temp"
)

print("Done")