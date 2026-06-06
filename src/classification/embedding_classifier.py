from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim


class EmbeddingClassifier:

    SUBJECT_DESCRIPTIONS = {
        "Pharmacology":
            """
            Drugs, medicines, prescriptions, dosage,
            pharmacokinetics, pharmacodynamics,
            adverse effects, antibiotics,
            antihypertensives, analgesics.
            """,

        "Pathology":
            """
            Disease mechanisms, inflammation,
            necrosis, tumors, carcinoma,
            histopathology, biopsy,
            cell injury.
            """,

        "Microbiology":
            """
            Bacteria, viruses, fungi,
            microorganisms, cultures,
            gram staining, infection,
            microbiological diagnosis.
            """,

        "Forensic Medicine":
            """
            Poisoning, autopsy,
            postmortem examination,
            injury, hanging,
            asphyxia, medico-legal cases.
            """,

        "Community Medicine":
            """
            Epidemiology, public health,
            vaccination, prevalence,
            incidence, screening,
            surveys, healthcare programs.
            """
    }

    def __init__(self):

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.subject_embeddings = {}

        for subject, description in (
            self.SUBJECT_DESCRIPTIONS.items()
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

        return best_subject, scores