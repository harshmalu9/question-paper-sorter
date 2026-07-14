import json
import re

from pathlib import Path

from PIL import Image

from engine.product.models import Group


_PAGE_REORDERING_SUPPORTED = False


def _sanitise_filename(name: str) -> str:
    """Turn a paper name into a safe filesystem filename."""
    safe = re.sub(r'[<>:"/\\|?*]', "", name)
    safe = safe.strip()
    return safe if safe else "paper"


def export_group(
    group: Group,
    output_dir: str = "output",
    filename_counter: dict[str, int] | None = None,
) -> str:
    output_path = Path(output_dir)
    output_path.mkdir(
        parents=True, exist_ok=True
    )

    if filename_counter is None:
        filename_counter = {}

    base = _sanitise_filename(group.paper_name)
    key = base.lower()
    count = filename_counter.get(key, 0)
    if count > 0:
        filename_counter[key] = count + 1
        pdf_path = output_path / f"{base} ({count + 1}).pdf"
    else:
        filename_counter[key] = 1
        pdf_path = output_path / f"{base}.pdf"

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
    groups: list[Group],
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
    filename_counter: dict[str, int] = {}
    for group in groups:
        base = _sanitise_filename(
            group.paper_name
        )
        key = base.lower()
        count = filename_counter.get(key, 0)
        if count > 0:
            filename_counter[key] = count + 1
            filename = (
                f"{base} ({count + 1}).pdf"
            )
        else:
            filename_counter[key] = 1
            filename = f"{base}.pdf"

        entry = {
            "paper_name": group.paper_name,
            "filename": filename,
            "page_count": len(group.pages),
            "grouping_confidence": (
                group.grouping_confidence
            ),
            "ordering_confidence": (
                group.ordering_confidence
            ),
            "group_id": group.group_id,
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
