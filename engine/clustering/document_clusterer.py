import numpy as np

from sklearn.cluster import (
    AgglomerativeClustering,
)

from engine.models.document_group import (
    DocumentGroup,
)


class DocumentClusterer:

    def _estimate_cluster_count(
        self,
        num_groups: int,
    ) -> int:

        return max(
            2,
            min(
                num_groups // 3,
                10,
            ),
        )

    def cluster(
        self,
        groups: list[DocumentGroup],
    ) -> list[DocumentGroup]:

        embeddings = np.array(
            [g.embedding for g in groups]
        )

        n_clusters = (
            self._estimate_cluster_count(
                len(groups)
            )
        )

        print(
            f"Clustering {len(groups)} groups "
            f"into {n_clusters} clusters"
        )

        model = AgglomerativeClustering(
            n_clusters=n_clusters,
        )

        labels = model.fit_predict(
            embeddings
        )

        for group, label in zip(
            groups, labels
        ):

            group.cluster_id = int(label)

        return groups
