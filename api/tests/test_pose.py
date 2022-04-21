from PIL import Image, ImageDraw, ImageOps
from pytest import approx
from api.removeBackground import remove_background
from api.utils.images import (
    crop_to_pose,
    fully_process_img,
)
from api.utils.posing import (
    DESIRED_POSE_HEIGHT,
    determine_pose_from_image,
    pose_bounding_box,
    pose_standing_height,
)

IMAGE_DIR = "api/tests/images"
IMAGE_OUT_DIR = "api/tests/images/out"


def test_pose_bounding_box():
    input_image = IMAGE_DIR + "/ryan_punch.png"

    with Image.open(input_image) as img:
        img = ImageOps.exif_transpose(img)
        results = determine_pose_from_image(img)
        pose = results.pose_landmarks.landmark

        bb = pose_bounding_box(img, pose)
        draw = ImageDraw.Draw(img)
        draw.rectangle(bb, outline="Red", width=10)

        img.save(IMAGE_OUT_DIR + "/ryan_punch_pose_bb.png", format="png")

        assert bb == approx([1140, 1850, 2650, 4360], abs=50)


def test_pose_height():
    input_image = IMAGE_DIR + "/ryan_punch.png"

    with Image.open(input_image) as img:
        img = ImageOps.exif_transpose(img)

        results = determine_pose_from_image(img)
        pose = results.pose_landmarks.landmark

        standing_height = pose_standing_height(img, results.pose_landmarks.landmark)

        assert standing_height == approx(2400, abs=20)


def test_crop_to_pose():
    input_image = IMAGE_DIR + "/frank_standing.jpg"

    with Image.open(input_image) as img:
        img = ImageOps.exif_transpose(img)
        results = determine_pose_from_image(img)
        pose = results.pose_landmarks.landmark

        bb = pose_bounding_box(img, pose)
        img = crop_to_pose(img, pose)

        img.save(IMAGE_OUT_DIR + "/frank_cropped_scaled.png", format="png")


def test_full_image_process():
    input_image = IMAGE_DIR + "/frank_standing.jpg"

    with Image.open(input_image) as img:
        img = ImageOps.exif_transpose(img)
        results = determine_pose_from_image(img)
        pose = results.pose_landmarks.landmark

        img = fully_process_img(img, pose)

        img.save(IMAGE_OUT_DIR + "/processed.png", format="png")
