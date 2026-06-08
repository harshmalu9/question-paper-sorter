from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

from classification.subject_loader import SubjectLoader


class EmbeddingClassifier:

    def __init__(self, config_path: str = None):

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.category_embeddings = {}

        category_descriptions = SubjectLoader.load(
            config_path
        )

        for category, description in (
            category_descriptions.items()
        ):

            self.category_embeddings[category] = (
                self.model.encode(
                    description,
                    convert_to_tensor=True
                )
            )

        print("Embedding model loaded.")

    def classify(
        self,
        text: str
    ):

        text_embedding = self.model.encode(
            text,
            convert_to_tensor=True
        )

        scores = {}

        for (
            category,
            category_embedding
        ) in self.category_embeddings.items():

            similarity = cos_sim(
                text_embedding,
                category_embedding
            ).item()

            scores[category] = similarity

        best_category = max(
            scores,
            key=scores.get
        )

        best_score = scores[best_category]

        if best_score < 0.15:
            return "Unknown", scores

        return best_category, scores
