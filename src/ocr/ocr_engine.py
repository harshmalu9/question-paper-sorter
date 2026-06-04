import easyocr


class OCREngine:

    def __init__(self):
        print("Loading OCR model...")

        self.reader = easyocr.Reader(
            ["en"],
            gpu=False
        )

        print("OCR model loaded.")

    def extract_text(self, image_path: str) -> str:

        result = self.reader.readtext(
            image_path,
            detail=0
        )

        return "\n".join(result)