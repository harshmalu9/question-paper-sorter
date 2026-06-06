import json

with open("data/output/pages.json") as f:
    pages = json.load(f)

for page in pages[:15]:

    print("\n" + "=" * 60)

    print(
        f"Page {page['page_number']}"
    )

    print(
        f"Subject: {page['subject']}"
    )

    print()

    text = page["ocr_text"]

    print(text[:400])