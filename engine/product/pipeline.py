from pathlib import Path

from engine.ocr.ocr_processor import OCRProcessor

from engine.product.ingest import load_pdf, load_zip
from engine.product.group_detector import (
    BoundaryDetector,
)
from engine.product.page_orderer import (
    set_ordering_confidence,
)
from engine.product.paper_namer import (
    name_groups,
)
from engine.product.exporter import (
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
            f"[Product] Processing: "
            f"{input_path}"
        )

    ext = (
        Path(input_path)
        .suffix
        .lower()
    )

    is_pdf = ext == ".pdf"

    if ext == ".pdf":

        load_pdf(input_path, temp_dir)

    elif ext == ".zip":

        load_zip(input_path, temp_dir)

    else:

        raise ValueError(
            f"Unsupported format: {ext}"
        )

    ocr = OCRProcessor()
    pages = ocr.process_directory(
        temp_dir
    )

    if not pages:
        raise RuntimeError(
            "No pages extracted"
        )

    if verbose:
        print(
            f"[Product] OCR completed for "
            f"{len(pages)} pages"
        )

    detector = BoundaryDetector()
    groups = detector.detect(pages)

    if verbose:
        print(
            f"[Product] Detected "
            f"{len(groups)} groups"
        )
        for g in groups:
            print(
                f"  Group {g.group_id}: "
                f"{len(g.pages)} pages, "
                f"confidence="
                f"{g.grouping_confidence}"
            )

    groups = name_groups(groups)

    groups = set_ordering_confidence(
        groups, is_pdf=is_pdf
    )

    if verbose:
        print(
            f"[Product] Paper names:"
        )
        for g in groups:
            print(
                f"  {g.paper_name}: "
                f"{len(g.pages)} pages"
            )

    out_path = Path(output_dir)
    out_path.mkdir(
        parents=True, exist_ok=True
    )

    pdf_paths = []
    filename_counter: dict[str, int] = {}
    for group in groups:
        pdf = export_group(
            group,
            str(out_path),
            filename_counter,
        )
        pdf_paths.append(pdf)
        if verbose:
            print(
                f"[Product] Exported: {pdf}"
            )

    meta = export_metadata(
        groups, str(out_path)
    )
    if verbose:
        print(
            f"[Product] Metadata: {meta}"
        )

    return groups, pdf_paths
