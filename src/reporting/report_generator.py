import json
from collections import Counter


class ReportGenerator:

    def generate(
        self,
        pages,
        groups=None,
        output_path="data/output/report.json"
    ):

        subject_counts = Counter()

        type_counts = Counter()

        for page in pages:

            subject_counts[
                page.subject
            ] += 1

            type_counts[
                page.document_type
            ] += 1

        report = {
            "total_pages": len(pages),
            "subjects": dict(
                subject_counts
            ),
            "document_types": dict(
                type_counts
            )
        }

        if groups is not None:

            report["groups"] = [
                {
                    "group_id": i + 1,
                    "pages": [
                        p.page_number
                        for p in group.pages
                    ],
                    "subject": group.subject,
                    "document_type":
                        group.document_type,
                    "topics": group.topics,
                    "top_topic":
                        group.topics[0][0]
                        if group.topics
                        else None,
                    "embedding_size":
                        len(group.embedding)
                        if group.embedding
                        else None,
                    "keyphrases":
                        group.keyphrases,
                    "cluster_id":
                        group.cluster_id,
                    "cluster_name":
                        group.cluster_name,
                    "raw_text":
                        group.raw_text
                        if group.raw_text
                        else None,
                }
                for i, group in enumerate(
                    groups
                )
            ]

            clusters: dict[
                int, dict
            ] = {}

            for i, group in enumerate(
                groups
            ):

                cid = group.cluster_id

                if cid is None:
                    continue

                if cid not in clusters:

                    clusters[cid] = {
                        "cluster_id": cid,
                        "cluster_name":
                            group.cluster_name,
                        "groups": [],
                    }

                clusters[cid][
                    "groups"
                ].append(i + 1)

            report["clusters"] = (
                sorted(
                    clusters.values(),
                    key=lambda x: x[
                        "cluster_id"
                    ],
                )
            )

        with open(
            output_path,
            "w"
        ) as f:

            json.dump(
                report,
                f,
                indent=4
            )