import base64
from io import BytesIO
from rembg import remove
from PIL import Image

from api.utils.converting import image_to_b64


def remove_background(img: Image.Image) -> Image.Image:
    output = remove(img)
    return output  # type: ignore
