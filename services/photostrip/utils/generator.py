from pathlib import Path
from typing import Union, IO
from io import BytesIO

import requests
from PIL import Image, ImageOps
from django.core.files.storage import default_storage

from services.photostrip.utils.image import (
    resize_and_crop_cover,
    resize_and_crop_cover_2,
)
from services.template.models import Template
from services.photobooth.models import File
import imageio.v2 as imageio
import numpy as np
from django.core.files.base import ContentFile


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


def generate_gif(file_instance, photos):

    frames = []

    TARGET_SIZE = (720, 720)

    for key in sorted(photos.keys()):
        source = photos.get(key)

        if not source:
            continue

        image = load_image(source)

        # 🔴 FIX: skip invalid frames
        if image is None:
            continue

        image = image.convert("RGB")

        # image = resize_and_crop_cover(
        #     image,
        #     TARGET_SIZE[0],
        #     TARGET_SIZE[1],
        # )

        frames.append(np.array(image))

    if not frames:
        raise ValueError("No valid frames available to generate GIF")

    # photobooth bounce animation
    frames = frames + frames[::-1]

    gif_io = BytesIO()

    # 1️⃣ Change the format to WEBP
    imageio.mimsave(
        gif_io,
        frames,
        format="WEBP",
        duration=800,
        loop=0,
    )

    gif_io.seek(0)

    file_instance.file.save(
        f"session_{file_instance.session_id}.webp",
        ContentFile(gif_io.read()),
        save=True,
    )
