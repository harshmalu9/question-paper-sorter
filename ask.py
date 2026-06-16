import sys

sys.path.append("src")

from rag.retriever import Retriever
from rag.context_builder import (
    ContextBuilder,
)
from rag.qa_engine import QAEngine

REPORT_PATH = "data/output/report.json"
PAGES_PATH = "data/output/pages.json"


def main():

    if len(sys.argv) < 2:

        print(
            "Usage: python ask.py "
            '"<question>"'
        )
        sys.exit(1)

    query = " ".join(sys.argv[1:])

    retriever = Retriever(REPORT_PATH)

    try:
        retriever.load()
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

    results = retriever.retrieve(
        query, top_k=5
    )

    builder = ContextBuilder(
        pages_path=PAGES_PATH
    )

    context = builder.build(results)

    engine = QAEngine()

    answer = engine.answer(
        query, context
    )

    sep = "=" * 50

    print()
    print(sep)
    print("Query")
    print(sep)
    print()
    print(query)
    print()
    print(sep)
    print("Answer")
    print(sep)
    print()
    print(answer)
    print()
    print(sep)
    print("Sources")
    print(sep)
    print()

    for r in results:

        score = r.get("_score", 0.0)

        print(
            f"Group {r['group_id']} "
            f"(score: {score:.2f})"
        )

    print()


if __name__ == "__main__":
    main()
