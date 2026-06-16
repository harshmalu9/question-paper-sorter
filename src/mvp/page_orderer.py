from mvp.models import MVPPGroup


_PDF_ORDERING_CONFIDENCE = 1.0
_ZIP_ORDERING_CONFIDENCE = 0.5


def reorder_groups(
    groups: list[MVPPGroup],
    is_pdf: bool = True,
) -> list[MVPPGroup]:

    confidence = (
        _PDF_ORDERING_CONFIDENCE
        if is_pdf
        else _ZIP_ORDERING_CONFIDENCE
    )

    for group in groups:
        group.ordering_confidence = confidence

    return groups
