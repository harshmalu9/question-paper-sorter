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


class TopicExtractor:

    def extract_topics(
        self,
        text: str,
        top_n: int = 10,
    ) -> list[str]:

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
            and len(w) >= 4
        ]

        counts = Counter(words)

        return [
            word
            for word, _ in counts.most_common(
                top_n
            )
        ]

    def extract_keywords(
        self,
        text: str,
        top_n: int = 10,
    ) -> list[str]:

        return self.extract_topics(
            text, top_n
        )
