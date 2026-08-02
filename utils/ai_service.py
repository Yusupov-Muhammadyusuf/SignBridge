import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=api_key) if api_key else None
        
        self.system_prompt = (
            "You are an expert Sign Language Interpreter. "
            "You receive 3D coordinates (x, y, z) of 21 hand landmarks for hands detected in a video frame. "
            "Analyze the spatial arrangement of the landmarks and translate the sign gesture into a concise, natural, single line of text or phrase. "
            "Return ONLY the translated sentence/word. Do not include explanation, greetings, or formatting."
        )

    def translate_landmarks(self, landmarks_data):
        if not self.client or not landmarks_data:
            return "Ready to translate..."

        try:
            prompt_content = f"Hand landmarks data: {landmarks_data}"
            
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt_content}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.2,
                max_tokens=50
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"AI Service Error: {e}")
            return "Translating error..."