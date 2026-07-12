#!/usr/bin/env python3
"""Production entrypoint for question-paper-sorter.

Usage:
    python main.py <input.pdf>
    python main.py <input.zip>
"""

import argparse
from pathlib import Path

from engine.product.pipeline import process

_ZIP_WARNING = (
    "[WARNING] ZIP uploads preserve image "
    "order from upload. For best results, "
    "upload pages in approximate document "
    "order. Fully shuffled pages may group "
    "correctly but page order is not "
    "guaranteed."
)


def main():
    parser = argparse.ArgumentParser(
        description="Question paper sorter"
    )

    parser.add_argument(
        "input",
        type=str,
        help="Path to PDF or ZIP file",
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="output",
        help="Output directory "
        "(default: output)",
    )

    parser.add_argument(
        "--temp-dir",
        type=str,
        default="data/temp",
        help="Temporary directory "
        "(default: data/temp)",
    )

    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress verbose output",
    )

    args = parser.parse_args()

    ext = (
        Path(args.input).suffix.lower()
    )

    if ext == ".zip":
        print(_ZIP_WARNING)

    process(
        input_path=args.input,
        output_dir=args.output_dir,
        temp_dir=args.temp_dir,
        verbose=not args.quiet,
    )


if __name__ == "__main__":
    main()
