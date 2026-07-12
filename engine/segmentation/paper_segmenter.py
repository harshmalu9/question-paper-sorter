from engine.models.paper import Paper


class PaperSegmenter:

    def segment(self, pages):

        if not pages:
            return []

        papers = []

        current_subject = pages[0].subject

        start_page = pages[0].page_number

        paper_id = 1

        for i in range(1, len(pages)):

            if pages[i].subject != current_subject:

                papers.append(
                    Paper(
                        paper_id=paper_id,
                        subject=current_subject,
                        start_page=start_page,
                        end_page=pages[i - 1].page_number
                    )
                )

                paper_id += 1

                current_subject = pages[i].subject

                start_page = pages[i].page_number

        papers.append(
            Paper(
                paper_id=paper_id,
                subject=current_subject,
                start_page=start_page,
                end_page=pages[-1].page_number
            )
        )

        return papers