import json

from pathlib import Path

import numpy as np

from search.semantic_search import (
    SemanticSearch,
)


class Retriever:

    def __init__(
        self, report_path: str
    ):

        self.report_path = report_path
        self.groups = []
        self.searcher = SemanticSearch()

    def load(self) -> None:

        path = Path(self.report_path)

        if not path.exists():

            raise FileNotFoundError(
                f"Report not found: "
                f"{self.report_path}\n"
                f"Run the pipeline first: "
                f"python run.py <pdf>"
            )

        with open(path) as f:
            data = json.load(f)

        self.groups = data["groups"]
        self.searcher.index(self.groups)

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict]:

        results = self.searcher.search(
            query, top_k=top_k
        )

        result_ids = {
            r["group_id"]
            for r in results
        }

        score_map = {
            r["group_id"]: r["score"]
            for r in results
        }

        retrieved = [
            g
            for g in self.groups
            if g.get("group_id")
            in result_ids
        ]

        for g in retrieved:

            g["_score"] = score_map.get(
                g.get("group_id"), 0.0
            )

        retrieved.sort(
            key=lambda g: g["_score"],
            reverse=True,
        )

        return retrieved
