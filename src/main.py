from ocr.ocr_processor import OCRProcessor
from classification.embedding_classifier import (
    EmbeddingClassifier
)
from exporters.metadata_exporter import (
    MetadataExporter
)


def main():

    processor = OCRProcessor()

    pages = processor.process_directory(
        "data/temp",
        max_pages=9
    )

    classifier = EmbeddingClassifier()

    for page in pages:

        subject, scores = classifier.classify(
            page.ocr_text
        )

        page.subject = subject

        page.subject_confidence = (
            max(scores.values())
        )

        print()

        print(
            f"Page {page.page_number}: "
            f"{subject}"
        )

        for name, score in sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True
        ):
            print(
                f"{name}: "
                f"{score:.4f}"
            )

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