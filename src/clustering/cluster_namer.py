from collections import Counter

from models.document_group import (
    DocumentGroup,
)


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
                    g.keyphrases
                ):

                    phrase_counter[
                        phrase
                    ] += score

            top_phrases = [
                phrase.replace(
                    " ", "_"
                )
                for phrase, _ in (
                    phrase_counter.most_common(
                        3
                    )
                )
            ]

            name = "_".join(top_phrases)

            for g in cluster_groups:

                g.cluster_name = name

        return groups
