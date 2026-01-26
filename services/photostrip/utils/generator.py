from services.photostrip.utils.image import resize_and_crop_cover
import json
from pathlib import Path
from PIL import Image, ImageOps
from io import BytesIO


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


def generate_photostrip(
    template_id: str,
    photos,
    output_path: Path,
) -> Path:
    """
    photos: request.FILES (UploadedFile objects)
    """

    config = load_template_by_id(template_id)

    template_image_path = BASE_DIR / "templates" / config["location"]

    base = Image.open(template_image_path).convert("RGBA")

    for zone in config["dropzones"]:
        uploaded_file = photos.get(zone["id"])
        if not uploaded_file:
            continue

        photo = Image.open(BytesIO(uploaded_file.read()))

        # ✅ Fix EXIF rotation
        photo = ImageOps.exif_transpose(photo)

        photo = photo.convert("RGBA")

        # 🔥 THIS replaces resize()
        photo = resize_and_crop_cover(
            photo,
            zone["width"],
            zone["height"],
        )

        base.paste(photo, (zone["left"], zone["top"]), photo)

    base.save(output_path, "PNG")

    return output_path
