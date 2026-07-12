from pathlib import Path

from engine.mvp.ingest import load_pdf, load_zip
from engine.mvp.group_detector import (
    BoundaryDetector,
)
from engine.mvp.page_orderer import (
    reorder_groups,
)
from engine.mvp.exporter import (
    export_group,
    export_metadata,
)


def process(
    input_path: str,
    output_dir: str = "output",
    temp_dir: str = "data/temp",
    verbose: bool = True,
):

    if verbose:
        print(
            f"[MVP] Processing: "
            f"{input_path}"
        )

    ext = (
        Path(input_path)
        .suffix
        .lower()
    )

    if ext == ".pdf":
        is_pdf = True
        image_paths = load_pdf(
            input_path, temp_dir
        )
    elif ext == ".zip":
        is_pdf = False
        image_paths = load_zip(
            input_path, temp_dir
        )
    else:
        raise ValueError(
            f"Unsupported format: {ext}"
        )

    if verbose:
        print(
            f"[MVP] Extracted "
            f"{len(image_paths)} images"
        )

    from engine.ocr.ocr_processor import (
        OCRProcessor,
    )

    ocr_processor = OCRProcessor()

    pages = (
        ocr_processor.process_directory(
            temp_dir
        )
    )

    if not pages:
        raise RuntimeError(
            "No pages extracted"
        )

    if verbose:
        print(
            f"[MVP] OCR completed for "
            f"{len(pages)} pages"
        )

    detector = BoundaryDetector()
    groups = detector.detect(pages)

    if verbose:
        print(
            f"[MVP] Detected "
            f"{len(groups)} groups"
        )
        for g in groups:
            print(
                f"  Group {g.group_id}: "
                f"{len(g.pages)} pages, "
                f"confidence="
                f"{g.grouping_confidence}"
            )

    groups = reorder_groups(
        groups, is_pdf=is_pdf
    )

    out_path = Path(output_dir)
    out_path.mkdir(
        parents=True, exist_ok=True
    )

    pdf_paths = []

    for group in groups:

        pdf = export_group(
            group, str(out_path)
        )
        pdf_paths.append(pdf)

        if verbose:
            print(
                f"[MVP] Exported: {pdf}"
            )

    meta = export_metadata(
        groups, str(out_path)
    )

    if verbose:
        print(
            f"[MVP] Metadata: {meta}"
        )

    return groups, pdf_paths
