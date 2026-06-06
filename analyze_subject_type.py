import json
from collections import defaultdict

with open("data/output/pages.json") as f:
    pages = json.load(f)

groups = defaultdict(list)

for page in pages:

    key = (
        page["subject"],
        page["document_type"]
    )

    groups[key].append(
        page["page_number"]
    )

print("\n===== SUBJECT + TYPE GROUPS =====\n")

for key, page_numbers in sorted(groups.items()):

    print(
        f"{key}: "
        f"{page_numbers}"
    )