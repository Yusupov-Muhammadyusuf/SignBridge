import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=api_key) if api_key else None
        self.system_prompt = """
        You are an AI Sign Language Interpreter.
        You will receive JSON containing 3D hand landmarks detected by MediaPipe Hand Landmarker.
        Rules:
        - Return ONLY the translated word or short sentence.
        - If the gesture is unclear, return: Unknown gesture
        - Never explain your answer.
        - Never output markdown.
        - Never describe landmarks.
        - Maximum 8 words.
        """

    def translate_landmarks(self, landmarks_data):
        if self.client is None:
            return "Groq API not configured"

        if not landmarks_data:
            return "Waiting for hand..."

        try:
            prompt = json.dumps(landmarks_data)

            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                temperature=0,
                max_tokens=20,
                messages=[
                    {
                        "role": "system",
                        "content": self.system_prompt
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            text = response.choices[0].message.content.strip()

            if not text:
                return "Unknown gesture"

            return text

        except Exception as e:
            print("GROQ ERROR:", str(e))
            return "Translation unavailable"