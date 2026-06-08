from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

from classification.subject_loader import SubjectLoader


class EmbeddingClassifier:

    def __init__(self):

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.subject_embeddings = {}

        subject_descriptions = SubjectLoader.load()

        for subject, description in (
            subject_descriptions.items()
        ):

            self.subject_embeddings[subject] = (
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
            subject,
            subject_embedding
        ) in self.subject_embeddings.items():

            similarity = cos_sim(
                text_embedding,
                subject_embedding
            ).item()

            scores[subject] = similarity

        best_subject = max(
            scores,
            key=scores.get
        )

        best_score = scores[best_subject]

        if best_score < 0.15:
            return "Unknown", scores

        return best_subject, scores