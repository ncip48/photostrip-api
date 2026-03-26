from pathlib import Path
from typing import Union, IO
from io import BytesIO

import requests
from PIL import Image, ImageOps
from django.core.files.storage import default_storage

from services.photostrip.utils.image import resize_and_crop_cover
from services.template.models import Template
from services.photobooth.models import File


def load_image(source) -> Image.Image:
    """
    source can be:
    - UploadedFile
    - URL string
    - File.subid string (DB lookup)
    """

    image_bytes = None

    # Case 1: UploadedFile (multipart)
    if hasattr(source, "read"):
        image_bytes = source.read()

    # Case 2: string input
    elif isinstance(source, str):
        # Case 2A: URL
        if source.startswith("http://") or source.startswith("https://"):
            response = requests.get(source, timeout=10)
            response.raise_for_status()
            image_bytes = response.content

        # Case 2B: File.subid lookup
        else:
            file_obj = File.objects.filter(subid=source).first()

            if not file_obj:
                raise ValueError(f"File with subid '{source}' not found")

            with default_storage.open(file_obj.file.name, "rb") as f:
                image_bytes = f.read()

    else:
        raise ValueError("Unsupported image source")

    image = Image.open(BytesIO(image_bytes))
    image = ImageOps.exif_transpose(image)

    return image.convert("RGBA")


def generate_photostrip(
    template_subid: str,
    photos,
    output_path: Union[Path, IO],
):
    """
    photos example:

    {
        "zone1": UploadedFile | "https://example.com/a.jpg",
        "zone2": UploadedFile | "https://example.com/b.jpg",
    }
    """

    # 🚀 Load template + relations in one query
    template = (
        Template.objects.select_related("size")
        .prefetch_related("dropzones")
        .get(subid=template_subid)
    )

    # 🚀 Load overlay image from storage safely
    with default_storage.open(template.location.name, "rb") as f:
        template_overlay = Image.open(f).convert("RGBA")

    # create transparent canvas same size as overlay
    base = Image.new("RGBA", template_overlay.size, (0, 0, 0, 0))

    # paste photos FIRST (background)
    for index, zone in enumerate(template.dropzones.all(), start=1):
        zone_key = f"zone{index}"
        source = photos.get(zone_key)

        if not source:
            continue

        photo = load_image(source)

        photo = resize_and_crop_cover(
            photo,
            zone.width,
            zone.height,
        )

        base.paste(
            photo,
            (zone.left, zone.top),
        )

    # paste template LAST (foreground frame)
    base.paste(template_overlay, (0, 0), template_overlay)

    # save output
    if isinstance(output_path, Path):
        output_path.parent.mkdir(parents=True, exist_ok=True)
        base.save(output_path, "PNG")
    else:
        base.save(output_path, "PNG")

    return output_path
