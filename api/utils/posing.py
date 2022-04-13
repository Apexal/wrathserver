import math
from typing import Dict, List, Tuple
from api.models import PoseLandmark
from mediapipe.python.solutions.pose import PoseLandmark as MPPoseLandmarks
from PIL import Image


def calculate_angle(a: PoseLandmark, b: PoseLandmark, c: PoseLandmark) -> float:
    print(a, b, c)
    angle = math.degrees(
        math.atan2(c.y - b.y, c.x - b.x) - math.atan2(a.y - b.y, a.x - b.x)
    )

    # Check if the angle is less than zero.
    if angle < 0:

        # Add 360 to the found angle.
        angle += 360

    # Return the calculated angle.
    return angle


def pose_bounding_box(
    img: Image.Image, normalized_pose_landmarks: List[PoseLandmark], buffer: int = 10
) -> Tuple[int, int, int, int]:
    """left, upper, right, and lower"""

    x_min = float("inf")
    x_max = float("-inf")
    y_min = float("inf")
    y_max = float("-inf")

    for landmark in normalized_pose_landmarks:
        if landmark.x < x_min:
            x_min = landmark.x
        if landmark.x > x_max:
            x_max = landmark.x
        if landmark.y < y_min:
            y_min = landmark.y
        if landmark.y > y_max:
            y_max = landmark.y

    width, height = img.size

    return (
        max(0, int((x_min * width) - buffer)),
        max(0, int((y_min * height) - buffer)),
        min(int((x_max * width) + buffer), width),
        min(int((y_max * height) + buffer), height),
    )
