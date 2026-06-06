from ocr.ocr_processor import OCRProcessor
from classification.subject_classifier import SubjectClassifier
from exporters.metadata_exporter import MetadataExporter


def main():

    processor = OCRProcessor()

    pages = processor.process_directory(
        "data/temp",
        max_pages=10
    )

    classifier = SubjectClassifier()

    for page in pages:

        subject, scores = classifier.classify(
            page.ocr_text
        )

        page.subject = subject

        page.subject_confidence = max(
            scores.values()
        )

        print()
        print(
            f"Page {page.page_number}: "
            f"{subject}"
        )

        print(scores)

    MetadataExporter.export_pages(
        pages,
        "data/output/pages.json"
    )

    print()
    print(
        "Metadata exported to "
        "data/output/pages.json"
    )


if __name__ == "__main__":
    main()