import base64
from PIL import Image


def crop_to_content(img: Image.Image) -> Image.Image:
    bounding_box = img.getbbox()
    cropped = img.crop(bounding_box)
    return cropped


def resize(img: Image.Image) -> Image.Image:
    img.thumbnail((400, 400))
    return img


def b64_to_bytes(b64: str) -> bytes:
    return base64.standard_b64decode(b64)


def bytes_to_b64(b: bytes) -> str:
    return base64.standard_b64encode(b).decode("utf-8")


def b64_to_image(b64_png: str) -> Image.Image:
    return Image.open(b64_to_bytes(b64_png))


def expand_img_to_square(img: Image.Image):
    background_color = (0, 0, 0, 0)
    width, height = img.size
    if width == height:
        return img
    elif width > height:
        result = Image.new(img.mode, (width, width), background_color)
        result.paste(img, (0, (width - height) // 2))
        return result
    else:
        result = Image.new(img.mode, (height, height), background_color)
        result.paste(img, ((height - width) // 2, 0))
        return result
