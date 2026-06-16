#!/usr/bin/env python3

import sys
from pathlib import Path

sys.path.insert(
    0,
    str(
        Path(__file__).resolve().parent
        / "src"
    ),
)

import argparse

from mvp.pipeline import process


_ZIP_WARNING = (
    "[WARNING] Random page reordering "
    "is not fully supported yet. "
    "Best results with mostly ordered pages."
)


def main():

    parser = argparse.ArgumentParser(
        description="MVP pipeline for "
        "question paper sorting"
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
        Path(args.input)
        .suffix
        .lower()
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
