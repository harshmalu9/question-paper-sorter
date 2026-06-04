from ocr.ocr_processor import OCRProcessor
from classification.subject_classifier import SubjectClassifier


def main():

    processor = OCRProcessor()

    pages = processor.process_directory(
        "data/temp",
        max_pages=1
    )

    classifier = SubjectClassifier()

    page = pages[0]

    subject, scores = classifier.classify(
        page.ocr_text
    )

    print()
    print("Predicted Subject:")
    print(subject)

    print()
    print("Scores:")
    print(scores)


if __name__ == "__main__":
    main()