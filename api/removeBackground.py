import base64
from io import BytesIO
from rembg import remove
from PIL import Image

from api.utils import b64_to_bytes, crop_to_content, resize, expand_img_to_square


def remove_background_bytes(img_bytes: bytes) -> bytes:
    output = remove(img_bytes)
    return output  # type: ignore


def remove_background_b64(img_b64: str) -> str:
    img_bytes = b64_to_bytes(img_b64)
    output_bytes = remove_background_bytes(img_bytes)
    return base64.standard_b64encode(output_bytes).decode("utf-8")


def remove_bg_and_resize_b64(img_b64: str) -> str:
    img = Image.open(BytesIO(base64.standard_b64decode(img_b64)))
    output = remove(img)
    final = expand_img_to_square(resize(crop_to_content(output)))  # type: ignore

    buffered = BytesIO()
    final.save(buffered, format="PNG")
    return base64.standard_b64encode(buffered.getvalue()).decode("utf-8")
