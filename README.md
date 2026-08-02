<div align="center">
  <img alt="SignBridge Logo" src="https://github.com/user-attachments/assets/dbdf71e8-a56b-4e63-9ced-ccd12c6e044a" width="60%">
</div>

SignBridge is an web application designed to bridge the communication gap for hearing and speech-impaired individuals. The system processes hand gestures from a live webcam stream or uploaded video files, detects 3D positional hand landmarks, and translates sign language gestures into textual output in real time.

## Inspiration

Traditional sign language translation systems often rely on heavy pre-trained classification models that are limited to static dictionaries. SignBridge utilizes a hybrid approach:
1. Spatial coordinate extraction using high-efficiency computer vision pipelines.
2. Large Language Model (LLM) processing to analyze spatial geometry and contextualize hand gestures into natural language sentences.

This approach provides higher accuracy, support for dynamic gestures, and lower processing overhead on client devices.

## Key Features

- **Dual Input Modes:** Supports live camera feed streaming and offline video file uploads.
- **Landmark Extraction:** Detects 21 3D hand coordinates (x, y, z) per detected hand in real time.
- **Real-Time Visual Overlay:** Draws keypoint skeletons on the user interface for visual feedback.
- **Contextual Translation:** Converts spatial hand configurations into concise text output using advanced AI inference.
- **Responsive Web Interface:** Accessible across modern browser environments with full-screen and control management options.

## System Architecture

The data pipeline follows a structured flow from input capture to inference rendering:

1. **Client Layer:** HTML5 media capture interfaces grab frames at a defined rate and transmit them as base64-encoded payloads via HTTP POST.
2. **Computer Vision Processing:** The backend decodes images into OpenCV frames and passes them to the hand-tracking engine to extract 21 keypoint landmarks per hand.
3. **AI Inference Layer:** Extracted spatial coordinates are structured into a prompt and evaluated by the LLM service to determine gesture meaning.
4. **Rendering:** Transformed frame overlays and generated translation strings are returned to the client and rendered dynamically.

<img alt="description" src="https://github.com/user-attachments/assets/a2b21971-0123-4c42-9069-9d7cfb660d0f" />

## Tech Stack

- **Backend:** Python, Flask
- **Frontend** HTML5, CSS3, Bootstrap, JavaScript
- **Computer Vision & AI:** OpenCV, MediaPipe, Numpy, Groq API (LLM)
- **Environment Management:** venv, python-dotenv

## Future Improvements

- **Multi-Hand Tracking & Recognition:** Expand the computer vision pipeline to support concurrent tracking of multiple hands for complex sign language gestures and phrases.
- **Text-to-Speech (TTS) Integration:** Implement client-side text-to-speech synthesis to convert translated text output into natural voice audio, enabling true two-way communication.
- **WebSocket Protocol Integration:** Replace HTTP polling mechanisms with persistent WebSockets to drastically reduce latency and optimize real-time frame streaming performance.
- **Expanded Vocabulary Database:** Train and integrate a more comprehensive lexicon of regional and international sign language dictionaries to improve translation accuracy.
- **Offline Edge Processing:** Explore lightweight on-device model quantization to minimize server dependency and enhance overall execution speed.