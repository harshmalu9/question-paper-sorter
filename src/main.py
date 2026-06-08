from pathlib import Path
import shutil

from sentence_transformers import (
    SentenceTransformer
)

from ocr.ocr_processor import OCRProcessor

from classification.embedding_classifier import (
    EmbeddingClassifier
)

from classification.document_type_classifier import (
    DocumentTypeClassifier
)

from segmentation.document_boundary_detector import (
    DocumentBoundaryDetector
)

from discovery.topic_extractor import (
    TopicExtractor
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

from reporting.report_generator import (
    ReportGenerator
)


def main(config_path: str = None):

    processor = OCRProcessor()

    pages = processor.process_directory(
        "data/temp"
    )

    print("Loading embedding model...")

    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    print("Embedding model loaded.")

    subject_classifier = (
        EmbeddingClassifier(
            model=model,
            config_path=config_path,
        )
    )

    document_classifier = (
        DocumentTypeClassifier()
    )

    detector = DocumentBoundaryDetector(
        model=model
    )

    topic_extractor = TopicExtractor()

    groups = detector.detect(pages)

    for group_index, group in enumerate(
        groups, start=1
    ):

        combined_text = "\n".join(
            page.ocr_text
            for page in group.pages
        )

        subject, subject_scores = (
            subject_classifier.classify(
                combined_text
            )
        )

        group.subject = subject

        group.subject_confidence = (
            max(subject_scores.values())
        )

        document_type, doc_scores = (
            document_classifier.classify(
                combined_text
            )
        )

        group.document_type = document_type

        group.document_type_confidence = (
            max(doc_scores.values())
        )

        group.topics = (
            topic_extractor.extract_topics(
                combined_text
            )
        )

        for page in group.pages:

            page.subject = group.subject

            page.subject_confidence = (
                group.subject_confidence
            )

            page.document_type = (
                group.document_type
            )

            page.document_type_confidence = (
                group.document_type_confidence
            )

        page_numbers = [
            p.page_number
            for p in group.pages
        ]

        print()

        print(
            f"  Document Group {group_index}"
        )

        print()

        print(
            "  Pages:"
        )

        print(
            f"  {page_numbers}"
        )

        print()

        print(
            "  Subject:"
        )

        print(
            f"  {group.subject}"
        )

        print(
            f"  Confidence: "
            f"{group.subject_confidence}"
        )

        print()

        print(
            "  Type:"
        )

        print(
            f"  {group.document_type}"
        )

        print(
            f"  Type Confidence: "
            f"{group.document_type_confidence}"
        )

        if group.topics:

            print()

            print(
                "  Topics:"
            )

            for topic in group.topics:

                print(f"  {topic}")

    print()

    for page in pages:

        print(
            f"  Page {page.page_number}"
            f" -> {page.subject}"
        )

    # Export metadata

    MetadataExporter.export_pages(
        pages,
        "data/output/pages.json"
    )

    # Organize pages

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

    # Generate PDFs

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

    # Generate report

    report_generator = (
        ReportGenerator()
    )

    report_generator.generate(
        pages,
        groups,
        "data/output/report.json"
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

    print(
        "Report generated in "
        "data/output/report.json"
    )


if __name__ == "__main__":
    main()
