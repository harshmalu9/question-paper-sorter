import json
from collections import Counter


class ReportGenerator:

    def generate(
        self,
        pages,
        output_path
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

        with open(
            output_path,
            "w"
        ) as f:

            json.dump(
                report,
                f,
                indent=4
            )