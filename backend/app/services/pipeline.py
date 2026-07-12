# Service layer for the processing engine.
# This is the ONLY backend module that imports from engine/.
# All processing requests must go through this service.

from engine.product.pipeline import process


def run_pipeline(input_path: str, output_dir: str) -> None:
    """Run the question paper sorting pipeline.

    This function is the single point of contact between
    the backend and the processing engine. No other backend
    module should import from engine directly.
    """
    process(
        input_path=input_path,
        output_dir=output_dir,
        verbose=False,
    )
