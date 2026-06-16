import numpy as np
from sklearn.metrics.pairwise import (
    cosine_similarity,
)

from sentence_transformers import (
    SentenceTransformer,
)


class SemanticSearch:

    def __init__(
        self,
        model: SentenceTransformer = None,
    ):

        if model is None:
            self.model = SentenceTransformer(
                "all-MiniLM-L6-v2"
            )
        else:
            self.model = model

        self.groups: list[dict] = []
        self.embeddings: list[
            np.ndarray
        ] = []

    def _build_text(
        self, group: dict
    ) -> str:

        parts = []

        if group.get("topics"):

            topic_text = " ".join(
                t[0]
                for t in group["topics"]
            )
            parts.append(topic_text)

        if group.get("keyphrases"):

            kp_text = " ".join(
                k[0]
                for k in group["keyphrases"]
            )
            parts.append(kp_text)

        if group.get("subject"):
            parts.append(
                group["subject"]
            )

        if group.get("document_type"):
            parts.append(
                group["document_type"]
            )

        if group.get("cluster_name"):
            parts.append(
                group["cluster_name"]
            )

        return " ".join(parts)

    def index(
        self, groups: list[dict]
    ) -> None:

        self.groups = groups
        self.embeddings = []

        texts = [
            self._build_text(g)
            for g in groups
        ]

        vecs = self.model.encode(
            texts, show_progress_bar=True
        )

        self.embeddings = [
            v for v in vecs
        ]

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict]:

        query_vec = (
            self.model.encode([query])[0]
        )

        if not self.embeddings:
            return []

        sims = cosine_similarity(
            [query_vec],
            self.embeddings,
        )[0]

        indices = np.argsort(sims)[
            ::-1
        ][:top_k]

        results = []

        for idx in indices:

            group = self.groups[idx]

            topics = [
                t[0]
                for t in group.get(
                    "topics", []
                )
            ]

            results.append(
                {
                    "group_id": group.get(
                        "group_id"
                    ),
                    "score": float(
                        sims[idx]
                    ),
                    "pages": group.get(
                        "pages"
                    ),
                    "subject": group.get(
                        "subject"
                    ),
                    "document_type": group.get(
                        "document_type"
                    ),
                    "cluster_name": group.get(
                        "cluster_name"
                    ),
                    "top_topics": topics[:5],
                }
            )

        return results
