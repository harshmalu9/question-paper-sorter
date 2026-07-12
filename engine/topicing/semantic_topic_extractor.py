import re
import string

import numpy as np
from sklearn.feature_extraction.text import (
    CountVectorizer,
    TfidfTransformer,
)

STOPWORDS = {
    "a", "an", "the",
    "is", "are", "was", "were",
    "with", "without",
    "from", "into", "onto",
    "that", "this", "these", "those",
    "what", "which", "when", "where", "why", "how",
    "only", "also",
    "been", "being",
    "have", "has", "had",
    "will", "would",
    "shall", "should",
    "can", "could",
    "may", "might",
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves",
    "you", "your", "yours", "yourself", "yourselves",
    "he", "him", "his", "himself",
    "she", "her", "hers", "herself",
    "it", "its", "itself",
    "they", "them", "their", "theirs", "themselves",
    "and", "but", "or", "nor", "not", "no", "neither",
    "as", "at", "by", "for", "in", "of", "on", "to", "up",
    "do", "does", "did", "doing",
    "each", "every", "all", "any", "both",
    "few", "more", "most", "other", "some", "such",
    "than", "too", "so",
    "be", "if", "because", "then", "here", "there",
    "about", "above", "after", "again", "against",
    "below", "between", "during", "before", "behind",
    "under", "over", "through", "out", "off", "down",
    "along", "around", "among", "across",
    "toward", "towards", "within",
    "am", "need", "like", "just", "much", "very",
    "get", "got", "make", "made", "take", "took",
    "say", "said", "see", "seen", "know", "known",
    "think", "thought", "come", "came",
    "give", "given", "find", "found",
    "tell", "told", "use", "used", "using",
    "upon", "enough", "almost", "quite", "really",
    "also", "always", "never", "often", "sometimes",
    "usually", "however", "although", "though",
    "while", "since", "until", "still", "already",
    "yet", "because", "therefore", "thus", "hence",
    "marks", "mark",
    "question", "questions",
    "paper",
    "answer", "answers",
    "write",
    "short", "long",
    "following",
    "describe", "explain", "discuss",
    "give", "mention", "attempt",
    "section",
    "part",
    "number",
    "medical", "college",
    "year", "syllabus",
    "your", "anything",
    "total", "time", "please",
    "page", "pages", "note", "notes",
    "first", "second", "third", "last", "next",
    "one", "two", "three", "four", "five",
    "six", "seven", "eight", "nine", "ten",
    "many", "much",
    "well", "even",
    "way", "ways",
    "new", "old",
    "due",
    "per",
    "via",
    "versus",
    "etc",
    "eg",
    "ie",
    "de",
    "la",
    "le",
    "les",
    "un", "une", "des",
    "das", "die", "der",
}

DOMAIN_TERMS = {
    "drug",
    "diagnosis",
    "therapy",
    "mechanism",
    "disease",
    "health",
    "community",
    "treatment",
    "pathology",
    "infection",
    "pharmacology",
    "medicine",
    "clinical",
}

OCR_BLACKLIST = {
    "mks",
    "que",
    "aabo",
    "iiu",
    "ihe",
    "smg",
    "hrs",
    "akola",
    "compulsory",
    "structured",
    "date",
    "batch",
}


class SemanticTopicExtractor:

    def __init__(self) -> None:

        self._abbrevs_lower: set[str] = set()

    def _is_junk_token(self, token: str) -> bool:

        if token in self._abbrevs_lower:
            return False

        if len(token) < 3:
            return True

        if re.search(r"(.)\1{2,}", token):
            return True

        if all(c in "aeiou" for c in token):
            return True

        if not any(c in "aeiou" for c in token):
            return True

        if token in OCR_BLACKLIST:
            return True

        return False

    def extract(
        self,
        text: str,
        top_n: int = 15,
    ) -> list[tuple[str, float]]:

        abbrevs = set(
            re.findall(
                r"\b[A-Z]{2,}\b", text
            )
        )

        self._abbrevs_lower = {
            a.lower() for a in abbrevs
        }

        text = text.lower()

        text = re.sub(
            rf"[{re.escape(string.punctuation)}]",
            " ",
            text,
        )

        text = re.sub(r"\d+", "", text)

        chunks = [
            c.strip()
            for c in re.split(
                r"[.!?\n]+", text
            )
            if c.strip()
        ]

        if not chunks:
            return []

        removed_tokens: set[str] = set()
        clean_chunks: list[str] = []

        for chunk in chunks:

            words = chunk.split()
            filtered: list[str] = []

            for w in words:

                if self._is_junk_token(w):
                    removed_tokens.add(w)
                    continue

                if w in STOPWORDS:
                    continue

                filtered.append(w)

            if filtered:

                clean_chunks.append(
                    " ".join(filtered)
                )

        print("Filtered tokens removed:")
        print(sorted(removed_tokens))
        print()

        if not clean_chunks:

            return []

        vectorizer = CountVectorizer(
            ngram_range=(1, 3),
            token_pattern=(
                r"(?u)\b[a-z][a-z]+\b"
            ),
            min_df=1,
        )

        count_matrix = (
            vectorizer.fit_transform(
                clean_chunks
            )
        )

        transformer = TfidfTransformer()

        tfidf_matrix = (
            transformer.fit_transform(
                count_matrix
            )
        )

        scores = np.array(
            tfidf_matrix.sum(axis=0)
        ).flatten()

        feature_names = (
            vectorizer.get_feature_names_out()
        )

        phrases: list[tuple[str, float]] = []

        for name, score in zip(
            feature_names, scores
        ):

            parts = name.split()

            if any(
                p in OCR_BLACKLIST
                for p in parts
            ):
                continue

            if any(
                p in DOMAIN_TERMS
                for p in parts
            ):
                score *= 1.2

            phrases.append((name, score))

        phrases.sort(
            key=lambda x: x[1],
            reverse=True,
        )

        result = phrases[:top_n]

        print("Final phrases:")
        for phrase, score in result:
            print(f"  {phrase}: {score:.4f}")
        print()

        return result
