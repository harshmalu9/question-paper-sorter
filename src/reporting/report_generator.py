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
                }
                for i, group in enumerate(
                    groups
                )
            ]

        with open(
            output_path,
            "w"
        ) as f:

            json.dump(
                report,
                f,
                indent=4
            )