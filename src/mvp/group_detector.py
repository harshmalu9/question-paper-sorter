from sklearn.feature_extraction.text import (
    TfidfVectorizer,
)

from models.page_metadata import (
    PageMetadata,
)

from mvp.models import MVPPPage, MVPPGroup


BOUNDARY_KEYWORDS = {
    "department of": 3,
    "internal assessment": 3,
    "question paper": 3,
    "practical examination": 3,
    "university": 2,
    "examination": 2,
    "total marks": 2,
    "total time": 2,
    "annual examination": 2,
    "supplementary examination": 2,
}

MIN_GROUP_SIZE = 3


class BoundaryDetector:

    def __init__(self):

        self._vectorizer = TfidfVectorizer(
            max_features=2000,
            ngram_range=(1, 3),
            stop_words="english",
        )

    def _keyword_boundary_score(
        self, text: str
    ) -> int:

        first_lines = "\n".join(
            text.lower().split("\n")[:15]
        )

        score = 0

        for keyword, weight in (
            BOUNDARY_KEYWORDS.items()
        ):

            if keyword in first_lines:
                score += weight

        return score

    def _compute_similarities(
        self, texts: list[str]
    ) -> list[float]:

        if len(texts) < 2:
            return []

        tfidf = self._vectorizer.fit_transform(
            texts
        )

        from sklearn.metrics.pairwise import (
            cosine_similarity,
        )

        sims = []

        for i in range(
            1, len(texts)
        ):

            s = cosine_similarity(
                tfidf[i - 1 : i],
                tfidf[i : i + 1],
            )

            sims.append(float(s[0][0]))

        return sims

    def detect(
        self,
        pages: list[PageMetadata],
    ) -> list[MVPPGroup]:

        if not pages:
            return []

        mvp_pages = [
            MVPPPage(
                index=p.page_number,
                image_path=p.image_path,
                ocr_text=p.ocr_text,
            )
            for p in pages
        ]

        texts = [p.ocr_text for p in pages]

        sims = (
            self._compute_similarities(
                texts
            )
        )

        boundary_scores = [
            self._keyword_boundary_score(
                p.ocr_text
            )
            for p in pages
        ]

        groups: list[list[MVPPPage]] = []
        current: list[MVPPPage] = [
            mvp_pages[0]
        ]

        for i in range(
            1, len(mvp_pages)
        ):

            bscore = boundary_scores[i]
            sim = sims[i - 1]

            should_split = False

            if (
                bscore >= 3
                and len(current) >= MIN_GROUP_SIZE
            ):
                should_split = True

            if should_split:
                groups.append(current)
                current = []

            current.append(mvp_pages[i])

        if current:
            groups.append(current)

        result = []

        for gid, group_pages in enumerate(
            groups, start=1
        ):

            conf = (
                self._compute_confidence(
                    group_pages, sims
                )
            )

            result.append(
                MVPPGroup(
                    group_id=gid,
                    pages=group_pages,
                    grouping_confidence=conf,
                )
            )

        return result

    def _compute_confidence(
        self,
        pages: list[MVPPPage],
        all_sims: list[float],
    ) -> float:

        if len(pages) <= 1:
            return 0.95

        conf = 0.5

        if len(pages) >= 5:
            conf += 0.2

        if len(pages) >= 10:
            conf += 0.15

        texts = [
            p.ocr_text for p in pages
        ]

        internal_sims = []

        for i in range(
            1, len(texts)
        ):

            prev_idx = pages[
                i - 1
            ].index
            cur_idx = pages[i].index

            if (
                prev_idx >= 1
                and prev_idx - 1
                < len(all_sims)
            ):

                internal_sims.append(
                    all_sims[prev_idx - 1]
                )

        if internal_sims:

            avg = (
                sum(internal_sims)
                / len(internal_sims)
            )

            conf += avg * 0.3

        return round(
            min(conf, 0.99), 2
        )
