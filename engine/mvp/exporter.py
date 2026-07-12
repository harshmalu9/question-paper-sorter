import json

from pathlib import Path

from PIL import Image

from engine.mvp.models import MVPPGroup


_PAGE_REORDERING_SUPPORTED = False


def export_group(
    group: MVPPGroup,
    output_dir: str = "output",
) -> str:

    output_path = Path(output_dir)
    output_path.mkdir(
        parents=True, exist_ok=True
    )

    pdf_path = (
        output_path
        / f"group_{group.group_id}.pdf"
    )

    images = []

    for page in group.pages:

        img = Image.open(
            page.image_path
        ).convert("RGB")

        images.append(img)

    if images:

        images[0].save(
            pdf_path,
            save_all=True,
            append_images=images[1:],
            quality=95,
        )

    return str(pdf_path)


def export_metadata(
    groups: list[MVPPGroup],
    output_dir: str = "output",
) -> str:

    output_path = Path(output_dir)
    output_path.mkdir(
        parents=True, exist_ok=True
    )

    metadata_path = (
        output_path / "metadata.json"
    )

    payload = []

    for group in groups:

        entry = {
            "group_id": group.group_id,
            "num_pages": len(
                group.pages
            ),
            "grouping_confidence": (
                group.grouping_confidence
            ),
            "ordering_confidence": (
                group.ordering_confidence
            ),
            "pages": [
                {
                    "index": p.index,
                    "image_path": (
                        p.image_path
                    ),
                }
                for p in group.pages
            ],
        }

        payload.append(entry)

    data = {
        "page_reordering_supported": (
            _PAGE_REORDERING_SUPPORTED
        ),
        "groups": payload,
    }

    metadata_path.write_text(
        json.dumps(
            data,
            indent=2,
            default=str,
        )
    )

    return str(metadata_path)
