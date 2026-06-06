from pathlib import Path
import shutil

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

from organizer.page_organizer import (
    PageOrganizer
)

from pdf.pdf_batch_generator import (
    PDFBatchGenerator
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

    MetadataExporter.export_pages(
        pages,
        "data/output/pages.json"
    )

    sorted_dir = Path(
        "data/output/sorted"
    )

    if sorted_dir.exists():

        shutil.rmtree(
            sorted_dir
        )

    organizer = PageOrganizer()

    organizer.organize(
        pages,
        "data/output/sorted"
    )

    pdf_dir = Path(
        "data/output/pdfs"
    )

    if pdf_dir.exists():

        shutil.rmtree(
            pdf_dir
        )

    batch_generator = (
        PDFBatchGenerator()
    )

    batch_generator.generate_all(
        "data/output/sorted",
        "data/output/pdfs"
    )

    print()

    print(
        "Metadata exported to "
        "data/output/pages.json"
    )

    print(
        "Pages organized in "
        "data/output/sorted"
    )

    print(
        "PDFs generated in "
        "data/output/pdfs"
    )


if __name__ == "__main__":
    main()