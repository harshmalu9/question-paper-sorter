class DocumentTypeClassifier:

    RULES = {
        "Practical": [
            "practical examination",
            "gram staining",
            "ziehl",
            "specimen",
            "slide",
            "oral viva",
            "gross specimen"
        ],

        "MCQ": [
            "mcq",
            "multiple choice",
            "darken",
            "one mark",
            "circle below"
        ],

        "Communication": [
            "case scenario",
            "communicate",
            "patient care",
            "motivate the patient"
        ],

        "Theory": [
            "short answer questions",
            "long answer questions",
            "section b"
        ]
    }

    def classify(self, text: str):

        text = text.lower()

        scores = {}

        for doc_type, keywords in self.RULES.items():

            score = 0

            for keyword in keywords:

                if keyword in text:
                    score += 1

            scores[doc_type] = score

        best_type = max(
            scores,
            key=scores.get
        )

        if scores[best_type] == 0:
            return "Unknown", scores

        return best_type, scores