import json
import sys

from pathlib import Path

sys.path.append("src")

from search.semantic_search import (
    SemanticSearch,
)

REPORT_PATH = "data/output/report.json"


def load_report(
    path: str,
) -> list[dict]:

    with open(path) as f:
        data = json.load(f)

    return data["groups"]


def main():

    if len(sys.argv) < 2:

        print(
            "Usage: python search_papers.py "
            '"<query>"'
        )
        sys.exit(1)

    query = " ".join(sys.argv[1:])

    report_file = Path(REPORT_PATH)

    if not report_file.exists():

        print(
            f"Report not found: "
            f"{REPORT_PATH}"
        )
        print(
            "Run the pipeline first: "
            "python run.py <pdf>"
        )
        sys.exit(1)

    print("Loading report...")

    groups = load_report(REPORT_PATH)

    print("Loading embedding model...")

    searcher = SemanticSearch()

    print("Indexing groups...")

    searcher.index(groups)

    print("Searching...")

    results = searcher.search(
        query, top_k=5
    )

    sep = "=" * 50

    print()
    print(sep)
    print(f"Search Query: {query}")
    print(sep)
    print()

    if not results:

        print("No results found.")
        return

    for i, r in enumerate(
        results, start=1
    ):

        print(f"Result {i}")
        print(
            f"Group ID: "
            f"{r['group_id']}"
        )
        print(
            f"Similarity Score: "
            f"{r['score']:.2f}"
        )
        print(
            f"Subject: "
            f"{r['subject']}"
        )
        print(
            f"Document Type: "
            f"{r['document_type']}"
        )
        print(
            f"Cluster: "
            f"{r['cluster_name']}"
        )
        print("Topics:")
        for t in r["top_topics"]:
            print(f"- {t}")
        print()


if __name__ == "__main__":
    main()
