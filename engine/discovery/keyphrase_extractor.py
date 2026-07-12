import re
import string
from collections import Counter

from engine.discovery.topic_extractor import (
    ACADEMIC_STOPWORDS,
)


class KeyphraseExtractor:

    def _is_content_word(
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

    def _is_valid_phrase(
        self,
        phrase: str,
    ) -> bool:

        words = phrase.split()

        if not words:
            return False

        if len(words) == 1:

            word = words[0]

            if word in ACADEMIC_STOPWORDS:
                return False

            return self._is_content_word(
                word
            )

        for w in words:

            if w in ACADEMIC_STOPWORDS:
                return False

        first = words[0]
        last = words[-1]

        return (
            self._is_content_word(first)
            and self._is_content_word(last)
        )

    def extract_keyphrases(
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

        phrases: list[str] = []

        for i in range(len(words)):

            for n in (1, 2, 3):

                if i + n > len(words):
                    continue

                phrase = " ".join(
                    words[i:i + n]
                )

                if self._is_valid_phrase(
                    phrase
                ):
                    phrases.append(phrase)

        counts = Counter(phrases)

        return counts.most_common(top_n)
