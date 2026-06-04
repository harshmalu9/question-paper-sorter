from ocr.ocr_processor import OCRProcessor


def main():

    processor = OCRProcessor()

    pages = processor.process_directory(
        "data/temp",
        max_pages=5
    )

    print()
    print(f"Total pages: {len(pages)}")

    print()
    print("First page preview:")
    print()

    print(
        pages[0].ocr_text[:500]
    )


if __name__ == "__main__":
    main()