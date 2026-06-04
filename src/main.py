from ocr.ocr_engine import OCREngine


def main():

    ocr = OCREngine()

    text = ocr.extract_text(
        "data/temp/page_001.jpg"
    )

    with open(
        "data/output/page_001.txt",
        "w",
        encoding="utf-8"
    ) as file:
        file.write(text)

    print("OCR output saved.")


if __name__ == "__main__":
    main()