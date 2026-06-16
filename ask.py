import sys

sys.path.append("src")

from rag.retriever import Retriever
from rag.context_builder import (
    ContextBuilder,
)
from rag.llm_engine import (
    LLMEngine,
    PROMPT_TEMPLATE,
)

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

    builder = ContextBuilder()

    context = builder.build(
        results, query=query
    )

    engine = LLMEngine()

    full_prompt = PROMPT_TEMPLATE.format(
        query=query, context=context
    )

    answer = engine.generate_answer(
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
    print("Full Prompt Sent to LLM")
    print(sep)
    print()
    print(full_prompt)
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
