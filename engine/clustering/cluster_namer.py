from collections import Counter

from engine.models.document_group import (
    DocumentGroup,
)

GENERIC_PHRASES = {
    "drug",
    "drugs",
    "case",
    "patient",
    "distribution",
    "uses",
    "action",
    "mechanism",
    "theory",
    "practical",
    "question"
}


class ClusterNamer:

    def name_clusters(
        self,
        groups: list[DocumentGroup],
    ) -> list[DocumentGroup]:

        clusters: dict[
            int, list[DocumentGroup]
        ] = {}

        for group in groups:

            if group.cluster_id is None:
                continue

            clusters.setdefault(
                group.cluster_id, []
            ).append(group)

        for (
            cluster_id,
            cluster_groups,
        ) in clusters.items():

            phrase_counter: Counter = Counter()

            for g in cluster_groups:

                for phrase, score in (
                    g.topics
                ):

                    phrase_counter[
                        phrase
                    ] += score

            scored_phrases = []

            for phrase, freq in (
                phrase_counter.items()
            ):

                if (
                    phrase.lower()
                    in GENERIC_PHRASES
                ):
                    continue

                words = phrase.split()
                score = freq * len(words)
                scored_phrases.append(
                    (phrase, score)
                )

            scored_phrases.sort(
                key=lambda x: x[1],
                reverse=True,
            )

            top_phrases = [
                phrase
                for phrase, _ in
                scored_phrases[:3]
            ]

            if top_phrases:

                name = "_".join(
                    p.replace(" ", "_")
                    for p in top_phrases
                )

                if len(name) > 60:
                    name = name[:60]

            else:
                name = (
                    f"cluster_{cluster_id}"
                )

            print()
            print(
                "Cluster naming candidates:"
            )
            for phrase, score in (
                scored_phrases[:10]
            ):
                print(
                    f"  {phrase}: {score}"
                )

            print(
                f"Final cluster name: "
                f"{name}"
            )

            for g in cluster_groups:

                g.cluster_name = name

        return groups
