import os
import time
import base64
import cv2
import numpy as np

from flask import Flask, render_template, request, jsonify
from utils.cv_processor import HandTracker
from utils.ai_service import AIService

app = Flask(__name__)

tracker = HandTracker()
ai_service = AIService()

last_translation = "Ready to translate..."
last_ai_time = 0

@app.route("/")
def index():
    return render_template("main.html")

@app.route("/health")
def health():
    return "OK", 200

@app.route("/process_frame", methods=["POST"])
def process_frame():
    global last_translation
    global last_ai_time

    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON data"}), 400

        image_data = data.get("image")

        if not image_data:
            return jsonify({"error": "No image"}), 400

        if "," in image_data:
            encoded = image_data.split(",")[1]
        else:
            encoded = image_data

        frame = cv2.imdecode(
            np.frombuffer(base64.b64decode(encoded), np.uint8),
            cv2.IMREAD_COLOR
        )

        if frame is None:
            return jsonify({"error": "Invalid frame"}), 400

        processed_frame, landmarks = tracker.process_frame(frame)

        if landmarks and (time.time() - last_ai_time) >= 2:
            last_translation = ai_service.translate_landmarks(landmarks)
            last_ai_time = time.time()

        success, buffer = cv2.imencode(".jpg", processed_frame)
        if not success:
            return jsonify({"error": "Image encoding failed"}), 500

        processed_image = base64.b64encode(buffer).decode("utf-8")

        return jsonify({
            "image": f"data:image/jpeg;base64,{processed_image}",
            "text": last_translation
        })

    except Exception as e:
        print("PROCESS FRAME ERROR:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )