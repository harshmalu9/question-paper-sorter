from pathlib import Path


def analyze_ocr_cache():

    cache_dir = Path(
        "data/cache/ocr"
    )

    for file in sorted(
        cache_dir.glob("*.txt")
    ):

        text = file.read_text(
            encoding="utf-8"
        )

        words = len(text.split())

        chars = len(text)

        if chars < 100:

            print(
                f"{file.name}"
                f" | chars={chars}"
                f" | words={words}"
            )


if __name__ == "__main__":
    analyze_ocr_cache()