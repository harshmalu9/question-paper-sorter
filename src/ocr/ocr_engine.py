import os
import tempfile

import cv2
import easyocr

from preprocessing.image_preprocessor import (
    ImagePreprocessor
)


class OCREngine:

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

    def extract_text(
        self,
        image_path: str
    ) -> str:

        rotations = (
            ImagePreprocessor
            .generate_rotations(image_path)
        )

        best_text = ""
        best_rotation = 0
        best_score = 0

        for angle, image in rotations.items():

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

            if score > best_score:

                best_score = score
                best_text = text
                best_rotation = angle

        print(
            f"Best rotation: {best_rotation}"
        )

        return best_text