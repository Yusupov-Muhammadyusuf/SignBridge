import base64
import cv2
import numpy as np
from flask import Flask, render_template, request, jsonify
from utils.cv_processor import HandTracker
from utils.ai_service import AIService

app = Flask(__name__)

tracker = HandTracker()
ai_service = AIService()

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/process_frame', methods=['POST'])
def process_frame():
    try:
        data = request.json
        image_data = data.get('image', '')

        if not image_data:
            return jsonify({'error': 'No image provided'}), 400

        encoded_data = image_data.split(',')[1] if ',' in image_data else image_data
        nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if frame is None:
            return jsonify({'error': 'Invalid image format'}), 400

        processed_frame, landmarks_data = tracker.process_frame(frame)

        _, buffer = cv2.imencode('.jpg', processed_frame)
        processed_image_base64 = base64.b64encode(buffer).decode('utf-8')

        translated_text = "Ready to translate..."
        if landmarks_data:
            translated_text = ai_service.translate_landmarks(landmarks_data)

        return jsonify({
            'image': f"data:image/jpeg;base64,{processed_image_base64}",
            'text': translated_text
        })

    except Exception as e:
        print(f"Error processing frame: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)