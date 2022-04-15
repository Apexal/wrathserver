from typing import List
from PIL import Image

from api.models import PoseLandmark
from api.utils.posing import pose_bounding_box


def crop_to_content(img: Image.Image) -> Image.Image:
    bounding_box = img.getbbox()
    cropped = img.crop(bounding_box)
    return cropped


def crop_to_pose(
    img: Image.Image, normalized_pose_landmarks: List[PoseLandmark]
) -> Image.Image:
    bounding_box = pose_bounding_box(img, normalized_pose_landmarks, buffer=75)
    cropped = img.crop(bounding_box)
    return cropped


def resize(img: Image.Image) -> Image.Image:
    img.thumbnail((400, 400))
    return img


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


def scale_img(img: Image.Image, scale_factor: float) -> Image.Image:
    return img.resize(tuple(int(scale_factor * s) for s in img.size))
