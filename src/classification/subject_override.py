class SubjectOverride:

    RULES = {
        "Pharmacology": [
            "department of pharmacology"
        ],

        "Microbiology": [
            "department of microbiology",
            "microbiology practical"
        ],

        "Pathology": [
            "department of pathology",
            "systemic pathology"
        ],

        "Forensic Medicine": [
            "forensic medicine",
            "forensic medicine and toxicology"
        ],

        "Community Medicine": [
            "department of community medicine"
        ]
    }

    def classify(self, text):

        text = text.lower()

        for subject, keywords in self.RULES.items():

            for keyword in keywords:

                if keyword in text:
                    return subject

        return None