import os
import base64
import cv2
import numpy as np

from flask import Flask, render_template, request, jsonify

from utils.cv_processor import HandTracker
from utils.ai_service import AIService

app = Flask(__name__)

tracker = None
ai_service = AIService()


def get_tracker():
    global tracker

    if tracker is None:
        tracker = HandTracker()

    return tracker


@app.route("/")
def index():
    return render_template("main.html")


@app.route("/health")
def health():
    return "OK", 200


@app.route("/process_frame", methods=["POST"])
def process_frame():
    try:

        data = request.json

        image_data = data.get("image", "")

        if image_data == "":
            return jsonify({"error": "No image"}), 400

        encoded = image_data.split(",")[1] if "," in image_data else image_data

        frame = cv2.imdecode(
            np.frombuffer(base64.b64decode(encoded), np.uint8),
            cv2.IMREAD_COLOR
        )

        if frame is None:
            return jsonify({"error": "Invalid image"}), 400

        tracker = get_tracker()

        processed_frame, landmarks = tracker.process_frame(frame)

        _, buffer = cv2.imencode(".jpg", processed_frame)

        translated = "Ready to translate..."

        if landmarks:
            translated = ai_service.translate_landmarks(landmarks)

        return jsonify({

            "image":
            "data:image/jpeg;base64," +
            base64.b64encode(buffer).decode(),

            "text": translated

        })

    except Exception as e:
        print(e)

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)