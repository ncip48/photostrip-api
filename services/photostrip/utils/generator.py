from services.photostrip.utils.image import resize_and_crop_cover
import json
from pathlib import Path
from PIL import Image, ImageOps
from io import BytesIO
import requests

BASE_DIR = Path(__file__).resolve().parent.parent


def load_template_by_id(template_id: str) -> dict:
    template_file = (
        Path(__file__).resolve().parent.parent / "templates" / "templates.json"
    )

    with open(template_file, "r") as f:
        templates = json.load(f)

    for template in templates:
        if template["id"] == template_id:
            return template

    raise ValueError(f"Template '{template_id}' not found")


def load_image(source) -> Image.Image:
    """
    source can be:
    - UploadedFile
    - URL string
    """

    # Case 1: UploadedFile (multipart)
    if hasattr(source, "read"):
        image_bytes = source.read()

    # Case 2: URL string
    elif isinstance(source, str):
        response = requests.get(source, timeout=10)
        response.raise_for_status()
        image_bytes = response.content

    else:
        raise ValueError("Unsupported image source")

    image = Image.open(BytesIO(image_bytes))
    image = ImageOps.exif_transpose(image)  # ✅ fix rotation
    return image.convert("RGBA")


def generate_photostrip(
    template_id: str,
    photos,
    output_path: Path,
) -> Path:
    """
    photos:
    {
        "zone1": UploadedFile | "https://example.com/a.jpg",
        "zone2": UploadedFile | "https://example.com/b.jpg",
    }
    """

    config = load_template_by_id(template_id)

    template_image_path = BASE_DIR / "templates" / config["location"]
    base = Image.open(template_image_path).convert("RGBA")

    for zone in config["dropzones"]:
        source = photos.get(zone["id"])
        if not source:
            continue

        # 🔥 Normalize input → PIL Image
        photo = load_image(source)

        # 🔥 COVER behavior
        photo = resize_and_crop_cover(
            photo,
            zone["width"],
            zone["height"],
        )

        base.paste(
            photo,
            (zone["left"], zone["top"]),
            photo,
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    base.save(output_path, "PNG")

    return output_path
