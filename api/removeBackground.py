import base64
from rembg import remove

from api.utils import b64_to_bytes


def remove_background_bytes(img_bytes: bytes) -> bytes:
    output = remove(img_bytes)
    return output  # type: ignore


def remove_background_b64(img_b64: str) -> str:
    img_bytes = b64_to_bytes(img_b64)
    output_bytes = remove_background_bytes(img_bytes)
    return base64.standard_b64encode(output_bytes).decode("utf-8")
