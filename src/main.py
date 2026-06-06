from ocr.ocr_processor import OCRProcessor

from classification.embedding_classifier import (
    EmbeddingClassifier
)

from classification.document_type_classifier import (
    DocumentTypeClassifier
)

from classification.subject_override import (
    SubjectOverride
)

from exporters.metadata_exporter import (
    MetadataExporter
)


def main():

    processor = OCRProcessor()

    pages = processor.process_directory(
        "data/temp"
    )

    subject_classifier = (
        EmbeddingClassifier()
    )

    document_classifier = (
        DocumentTypeClassifier()
    )

    override_classifier = (
        SubjectOverride()
    )

    for page in pages:

        # Subject Classification

        override_subject = (
            override_classifier.classify(
                page.ocr_text
            )
        )

        if override_subject:

            subject = override_subject

            subject_scores = {
                subject: 1.0
            }

        else:

            subject, subject_scores = (
                subject_classifier.classify(
                    page.ocr_text
                )
            )

        page.subject = subject

        page.subject_confidence = (
            max(subject_scores.values())
        )

        # Document Type Classification

        document_type, doc_scores = (
            document_classifier.classify(
                page.ocr_text
            )
        )

        page.document_type = (
            document_type
        )

        page.document_type_confidence = (
            max(doc_scores.values())
        )

        # Console Output

        print()

        print(
            f"Page {page.page_number}"
        )

        print(
            f"Subject: {subject}"
        )

        print(
            f"Type: {document_type}"
        )

        print()

        print(
            "Subject Scores:"
        )

        for name, score in sorted(
            subject_scores.items(),
            key=lambda x: x[1],
            reverse=True
        ):
            print(
                f"{name}: "
                f"{score:.4f}"
            )

        print()

        print(
            "Document Type Scores:"
        )

        for name, score in sorted(
            doc_scores.items(),
            key=lambda x: x[1],
            reverse=True
        ):
            print(
                f"{name}: {score}"
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