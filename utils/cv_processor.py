import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class HandTracker:
    def __init__(self, model_path='hand_landmarker.task', max_hands=2, min_detection_confidence=0.5):
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE,
            num_hands=max_hands,
            min_hand_detection_confidence=min_detection_confidence
        )
        self.detector = vision.HandLandmarker.create_from_options(options)

    def process_frame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        detection_result = self.detector.detect(mp_image)

        landmarks_data = []

        if detection_result.hand_landmarks:
            h, w, _ = frame.shape

            for hand_idx, hand_landmarks in enumerate(detection_result.hand_landmarks):
                hand_label = "Hand"
                if detection_result.handedness and len(detection_result.handedness) > hand_idx:
                    hand_label = detection_result.handedness[hand_idx][0].category_name

                hand_points = []
                
                for lm in hand_landmarks:
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cv2.circle(frame, (cx, cy), 5, (56, 189, 248), -1)

                    hand_points.append({
                        'x': round(lm.x, 4),
                        'y': round(lm.y, 4),
                        'z': round(lm.z, 4)
                    })

                landmarks_data.append({
                    'label': hand_label,
                    'points': hand_points
                })

        return frame, landmarks_data