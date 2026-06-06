import json

with open(
    "data/output/pages.json",
    "r"
) as f:

    pages = json.load(f)

for page in pages:

    print(
        page["page_number"],
        page["subject"]
    )