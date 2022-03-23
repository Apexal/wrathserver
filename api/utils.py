import base64
from PIL import Image


def b64_to_bytes(b64: str) -> bytes:
    return base64.standard_b64decode(b64)


def bytes_to_b64(b: bytes) -> str:
    return base64.standard_b64encode(b).decode("utf-8")


def b64_to_image(b64_png: str) -> Image.Image:
    return Image.open(b64_to_bytes(b64_png))