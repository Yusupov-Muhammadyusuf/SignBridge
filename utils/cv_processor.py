import os
import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class HandTracker:
    def __init__(self):
        model_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "hand_landmarker.task"
        )

        base_options = python.BaseOptions(
            model_asset_path=model_path
        )

        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE,
            num_hands=2,
            min_hand_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            min_hand_presence_confidence=0.5
        )

        self.detector = vision.HandLandmarker.create_from_options(
            options
        )

        self.HAND_CONNECTIONS = [
            (0,1),(1,2),(2,3),(3,4),

            (0,5),(5,6),(6,7),(7,8),

            (5,9),(9,10),(10,11),(11,12),

            (9,13),(13,14),(14,15),(15,16),

            (13,17),(17,18),(18,19),(19,20),

            (0,17)
        ]

    def process_frame(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        result = self.detector.detect(mp_image)
        landmarks_data = []

        if not result.hand_landmarks:
            return frame, landmarks_data

        h, w, _ = frame.shape

        for hand_idx, hand in enumerate(result.hand_landmarks):
            hand_points = []
            pixel_points = []

            for lm in hand:
                x = int(lm.x * w)
                y = int(lm.y * h)

                pixel_points.append((x, y))
                hand_points.append({
                    "x": round(lm.x, 4),
                    "y": round(lm.y, 4),
                    "z": round(lm.z, 4)
                })

            for start, end in self.HAND_CONNECTIONS:
                cv2.line(
                    frame,
                    pixel_points[start],
                    pixel_points[end],
                    (0, 255, 0),
                    2
                )

            for point in pixel_points:
                cv2.circle(
                    frame,
                    point,
                    5,
                    (56, 189, 248),
                    -1
                )

            label = "Hand"

            if result.handedness:
                label = result.handedness[hand_idx][0].category_name

            landmarks_data.append({
                "label": label,
                "points": hand_points

            })

        return frame, landmarks_data