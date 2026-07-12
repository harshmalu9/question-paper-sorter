import os
import tempfile

import cv2
import easyocr

from engine.preprocessing.image_preprocessor import (
    ImagePreprocessor
)


class OCREngine:

    MIN_ACCEPTABLE_SCORE = 300

    def __init__(self):

        print("Loading OCR model...")

        self.reader = easyocr.Reader(
            ['en'],
            gpu=True
        )

        print("OCR model loaded.")

    def calculate_text_score(
        self,
        text: str
    ) -> float:

        if not text:
            return 0

        letters = sum(
            char.isalpha()
            for char in text
        )

        words = len(
            text.split()
        )

        return letters + (words * 10)

    def run_ocr(
        self,
        image
    ) -> tuple[str, float]:

        with tempfile.NamedTemporaryFile(
            suffix=".jpg",
            delete=False
        ) as temp_file:

            temp_path = temp_file.name

        cv2.imwrite(
            temp_path,
            image
        )

        result = self.reader.readtext(
            temp_path,
            detail=0
        )

        os.remove(temp_path)

        text = "\n".join(result)

        score = self.calculate_text_score(
            text
        )

        return text, score

    def extract_text(
        self,
        image_path: str
    ) -> str:

        rotations = (
            ImagePreprocessor
            .generate_rotations(image_path)
        )

        # Try 0° first

        text, score = self.run_ocr(
            rotations[0]
        )

        if score >= self.MIN_ACCEPTABLE_SCORE:

            print(
                f"Good OCR at 0° "
                f"(score={score}), "
                f"skipping rotation checks."
            )

            return text

        # Fallback to full rotation search

        best_text = text
        best_rotation = 0
        best_score = score

        for angle in (90, 180, 270):

            text, score = self.run_ocr(
                rotations[angle]
            )

            if score > best_score:

                best_score = score
                best_text = text
                best_rotation = angle

        print(
            f"Best rotation: "
            f"{best_rotation} "
            f"(score={best_score})"
        )

        return best_text