import re
import string
from collections import Counter


STOPWORDS = {
    "this", "that", "with", "from", "have", "been", "were",
    "will", "would", "could", "should", "their", "there",
    "which", "when", "where", "what", "about", "into",
    "than", "then", "them", "they", "these", "those",
    "also", "after", "before", "between", "other", "over",
    "such", "only", "very", "just", "more", "some", "each",
    "both", "most", "like", "well", "even", "many", "much",
    "because", "while", "since", "until", "during", "upon",
    "being", "done", "does", "used", "using", "make", "made",
    "take", "took", "given", "said", "seen", "need", "find",
    "part", "case", "based", "shown", "known", "found",
    "also", "within", "without", "across", "along", "among",
    "first", "second", "third", "next", "last", "another",
    "still", "though", "always", "never", "every", "large",
    "must", "may", "can", "get", "way", "work", "form",
}

ACADEMIC_STOPWORDS = {
    "marks",
    "mark",
    "question",
    "questions",
    "paper",
    "answer",
    "answers",
    "write",
    "short",
    "long",
    "following",
    "describe",
    "explain",
    "discuss",
    "give",
    "mention",
    "attempt",
    "section",
    "part",
    "number",
    "medical",
    "college",
    "year",
    "syllabus",
    "your",
    "anything",
}


class TopicExtractor:

    def _is_valid_word(
        self,
        word: str,
    ) -> bool:

        if len(word) < 4:
            return False

        if any(c.isdigit() for c in word):
            return False

        alpha = sum(
            1 for c in word if c.isalpha()
        )

        if alpha / len(word) < 0.5:
            return False

        return True

    def extract_topics(
        self,
        text: str,
        top_n: int = 10,
    ) -> list[tuple[str, int]]:

        text = text.lower()

        text = re.sub(
            rf"[{re.escape(string.punctuation)}]",
            " ",
            text,
        )

        words = text.split()

        words = [
            w for w in words
            if w not in STOPWORDS
            and w not in ACADEMIC_STOPWORDS
            and self._is_valid_word(w)
        ]

        counts = Counter(words)

        return counts.most_common(
            top_n
        )

    def extract_keywords(
        self,
        text: str,
        top_n: int = 10,
    ) -> list[tuple[str, int]]:

        return self.extract_topics(
            text, top_n
        )
