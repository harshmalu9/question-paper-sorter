from engine.product.models import Group


_PDF_ORDERING_CONFIDENCE = 1.0
_ZIP_ORDERING_CONFIDENCE = 0.5


def set_ordering_confidence(
    groups: list[Group],
    is_pdf: bool = True,
) -> list[Group]:
    confidence = (
        _PDF_ORDERING_CONFIDENCE
        if is_pdf
        else _ZIP_ORDERING_CONFIDENCE
    )
    for group in groups:
        group.ordering_confidence = (
            confidence
        )
    return groups
