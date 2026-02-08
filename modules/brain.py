# modules/brain.py
from google import genai
from config import GEMINI_API_KEY
from modules.actions import set_system_volume, set_system_brightness # Import actions here
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class AIProcessor:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model_id = "gemini-2.0-flash-lite" 
        self.chat = self.client.chats.create(model=self.model_id)

    def get_response(self, prompt):
        try:
            response = self.chat.send_message(prompt)
            return response.text
        except Exception as e:
            return f"Error: {e}"

    def run_pipeline(self):
        from modules.voice import VoiceEngine
        voice = VoiceEngine()
        
        # This is where user_text is defined!
        user_text = voice.listen()
        
        if user_text:
            user_text_lower = user_text.lower()
            print(f"User: {user_text}")

            # --- HARDWARE CONTROL LOGIC MOVED HERE ---
            if "volume to" in user_text_lower:
                level = [int(s) for s in user_text.split() if s.isdigit()][0]
                set_system_volume(level)
                voice.speak(f"Setting volume to {level} percent")
                return # Stop here so it doesn't ask Gemini as well

            elif "brightness to" in user_text_lower:
                level = [int(s) for s in user_text.split() if s.isdigit()][0]
                set_system_brightness(level)
                voice.speak(f"Setting brightness to {level} percent")
                return
            
            # --- NORMAL AI RESPONSE ---
            ai_reply = self.get_response(user_text)
            voice.speak(ai_reply)