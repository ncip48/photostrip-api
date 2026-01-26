from PIL import Image


def resize_and_crop_cover(
    img: Image.Image, target_width: int, target_height: int
) -> Image.Image:
    """
    Resize image to cover target size, then center-crop.
    (Equivalent to CSS object-fit: cover)
    """

    src_width, src_height = img.size
    src_ratio = src_width / src_height
    target_ratio = target_width / target_height

    # Scale so image fully covers target
    if src_ratio > target_ratio:
        # Image is wider → scale by height
        scale = target_height / src_height
    else:
        # Image is taller → scale by width
        scale = target_width / src_width

    new_width = int(src_width * scale)
    new_height = int(src_height * scale)

    img = img.resize((new_width, new_height), Image.LANCZOS)

    # Center crop
    left = (new_width - target_width) // 2
    top = (new_height - target_height) // 2
    right = left + target_width
    bottom = top + target_height

    return img.crop((left, top, right, bottom))
