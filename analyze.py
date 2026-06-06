from collections import Counter
import json

with open(
    "data/output/pages.json",
    encoding="utf-8"
) as f:
    pages = json.load(f)

counts = Counter(
    page["subject"]
    for page in pages
)

print("\n===== SUBJECT DISTRIBUTION =====\n")

for subject, count in sorted(
    counts.items(),
    key=lambda x: x[1],
    reverse=True
):
    print(f"{subject}: {count}")