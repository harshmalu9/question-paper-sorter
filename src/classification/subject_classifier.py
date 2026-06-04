class SubjectClassifier:

    SUBJECT_KEYWORDS = {

        "Pharmacology": [
            "drug",
            "dose",
            "tablet",
            "prescription",
            "adverse effect",
            "pharmacokinetics",
            "atenolol",
            "paracetamol",
            "metoclopramide",
            "antibiotic"
        ],

        "Pathology": [
            "necrosis",
            "inflammation",
            "tumor",
            "carcinoma",
            "histopathology",
            "biopsy",
            "cell injury"
        ],

        "Microbiology": [
            "bacteria",
            "virus",
            "fungus",
            "culture",
            "stain",
            "gram",
            "antigen",
            "microorganism"
        ],

        "Forensic Medicine": [
            "poison",
            "autopsy",
            "injury",
            "postmortem",
            "hanging",
            "asphyxia",
            "forensic"
        ],

        "Community Medicine": [
            "epidemiology",
            "screening",
            "prevalence",
            "incidence",
            "vaccination",
            "public health",
            "survey"
        ]
    }

    def classify(self, text: str):

        text = text.lower()

        scores = {}

        for subject, keywords in self.SUBJECT_KEYWORDS.items():

            score = 0

            for keyword in keywords:

                if keyword.lower() in text:
                    score += 1

            scores[subject] = score

        best_subject = max(
            scores,
            key=scores.get
        )

        return best_subject, scores