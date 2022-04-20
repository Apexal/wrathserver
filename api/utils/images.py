from typing import List
from PIL import Image

from api.models import PoseLandmark
from api.removeBackground import remove_background
from api.utils.posing import (
    DESIRED_POSE_HEIGHT,
    pose_bounding_box,
    pose_standing_height,
)


def crop_to_content(img: Image.Image) -> Image.Image:
    bounding_box = img.getbbox()
    cropped = img.crop(bounding_box)
    return cropped


def crop_to_pose(
    img: Image.Image, normalized_pose_landmarks: List[PoseLandmark]
) -> Image.Image:
    """Crops image to the pose's bounding box with a buffer of pixels on each side."""

    bounding_box = pose_bounding_box(img, normalized_pose_landmarks)

    cropped = img.crop(
        (
            bounding_box[0] - 20,
            bounding_box[1] - 50,  # - height of top half of head
            bounding_box[2] + 20,
            bounding_box[3] + 20,
        )
    )
    return cropped


def resize(img: Image.Image) -> Image.Image:
    img.thumbnail((400, 400))
    return img


def expand_img_to_square(img: Image.Image, size: int = 400):
    background_color = (0, 0, 0, 0)

    width, height = img.size

    if height != 400:
        missing = 400 - height
        img = img.crop((0, -missing, width, height))

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
    print("scale_factor", scale_factor)
    return img.resize(tuple(int(scale_factor * s) for s in img.size))


def fully_process_img(
    img: Image.Image, normalized_pose_landmarks: List[PoseLandmark]
) -> Image.Image:
    """Scales, crops, removes background, and makes square an image with a pose."""
    standing_height = pose_standing_height(img, normalized_pose_landmarks)

    scale_factor = DESIRED_POSE_HEIGHT / standing_height

    img = scale_img(img, scale_factor)
    img = crop_to_pose(img, normalized_pose_landmarks)
    img = remove_background(img)
    img = expand_img_to_square(img, size=400)

    return img
