# Service layer for the processing engine.
# This is the ONLY backend module that imports from engine/.
# All processing requests must go through this service.

from pathlib import Path

from engine.product.pipeline import process


def run_pipeline(
    input_path: str, output_dir: str
) -> tuple[list[str], str]:
    """Run the question paper sorting pipeline.

    Returns a tuple of (pdf_filenames, metadata_filename)
    where each name is just the filename (no directory path).
    """
    _groups, pdf_paths = process(
        input_path=input_path,
        output_dir=output_dir,
        verbose=False,
    )

    pdf_filenames = [
        Path(p).name for p in pdf_paths
    ]
    metadata_filename = "metadata.json"

    return pdf_filenames, metadata_filename
