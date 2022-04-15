import math
from typing import Dict, List, Tuple

import numpy as np
from api.models import PoseLandmark
from mediapipe.python.solutions.pose import PoseLandmark as MPPoseLandmarks
from mediapipe.python.solutions.pose import Pose
from PIL import Image


def dist(a: PoseLandmark, b: PoseLandmark):
    return math.sqrt(((a.x - b.x) ** 2) + ((a.y - b.y) ** 2))


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
    img: Image.Image, normalized_pose_landmarks: List[PoseLandmark], buffer: int = 50
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
    y_min = y_max - pose_height(img, normalized_pose_landmarks)

    return (
        max(0, int((x_min * width) - buffer)),
        max(0, int((y_min * height) - buffer)),
        min(int((x_max * width) + buffer), width),
        min(int((y_max * height) + buffer), height),
    )


def pose_height(img: Image.Image, normalized_pose_landmarks: List[PoseLandmark]) -> int:
    """Given a pose in an image, calculate how tall the pose would be if standing up straight."""

    nose_y = normalized_pose_landmarks[MPPoseLandmarks.NOSE].y
    normalized_left_hip_y = normalized_pose_landmarks[MPPoseLandmarks.LEFT_HIP].y

    normalized_left_leg_height = dist(
        normalized_pose_landmarks[MPPoseLandmarks.LEFT_HEEL],
        normalized_pose_landmarks[MPPoseLandmarks.LEFT_KNEE],
    ) + dist(
        normalized_pose_landmarks[MPPoseLandmarks.LEFT_KNEE],
        normalized_pose_landmarks[MPPoseLandmarks.LEFT_HIP],
    )

    normalized_torso_height = normalized_left_hip_y - nose_y

    normalized_height = normalized_left_leg_height + normalized_torso_height
    actual_height = int((normalized_height) * img.size[1])

    return actual_height


def determine_pose_from_image(img: Image.Image):
    with Pose(
        static_image_mode=True,
        model_complexity=2,
        min_detection_confidence=0.5,
    ) as pose:
        results = pose.process(np.asarray(img))

        return results
