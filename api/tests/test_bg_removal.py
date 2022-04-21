from api.removeBackground import remove_background_seg_mask
from api.tests.test_pose import IMAGE_DIR, IMAGE_OUT_DIR
from PIL import Image, ImageOps

from api.utils.posing import determine_pose_from_image


def test_bg_removal():
    # img = b64_to_bytes(b64_png)
    # removed_bg = remove_background(img)
    # with open("out.png", "wb") as f:
    #     f.write(removed_bg)
    pass


def test_bg_removal_seg_mask():
    input_image = IMAGE_DIR + "/ryan_punch.png"

    with Image.open(input_image) as img:
        img = ImageOps.exif_transpose(img)
        results = determine_pose_from_image(img)
        seg_mask = results.segmentation_mask

        img = remove_background_seg_mask(img, seg_mask)

        img.save(IMAGE_OUT_DIR + "/processed2.png", format="png")
