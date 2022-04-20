import cv2
import numpy as np
from PIL import Image


def remove_background_seg_mask(img: Image.Image, segmentation_mask) -> Image.Image:
    """Given a segmentation mask, apply it on the given image so only the person remains and the bg is transparent."""

    # Convert to opencv image that numpy works with
    opencv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGBA2BGRA)

    # 4 channel data since BGRA, no idea what axis means, 0.5 is cutoff
    condition = np.stack((segmentation_mask,) * 4, axis=-1) > 0.5

    background = np.zeros(opencv_img.shape, dtype=np.uint8)
    background[:] = (0, 0, 0, 0)  # transparent
    foreground = opencv_img.copy()

    opencv_img = np.where(condition, foreground, background)

    return Image.fromarray(cv2.cvtColor(opencv_img, cv2.COLOR_BGRA2RGBA))
