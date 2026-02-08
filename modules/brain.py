# modules/brain.py
from google import genai
from config import GEMINI_API_KEY
import  time
from langdetect import detect

class AIProcessor:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        # 2.5 Flash-Lite is the current 'best' for free 24/7 assistants
        self.model_id = "gemini-2.5-flash-lite" 
        self.chat = self.client.chats.create(model=self.model_id)

    def get_response(self, prompt):
     try:
        response = self.chat.send_message(prompt)
        return response.text
     except Exception as e:
        if "429" in str(e):
            print("Rate limit reached. Sleeping for 15 seconds...")
            time.sleep(15) # Wait for the quota window to clear
            return "I'm a bit overwhelmed right now. Please wait a moment before asking again."
        return f"Error: {str(e)}"

    def run_pipeline(self):
        """Orchestrates the Listen -> Think -> Speak flow."""
        from modules.voice import VoiceEngine
        voice = VoiceEngine()
        
        # 1. Capture voice input
        user_text = voice.listen()
        
        if user_text:
            print(f"User: {user_text}")
            
            # 2. Get AI response from Gemini
            ai_reply = self.get_response(user_text)
            
            # 3. Speak the AI response
            voice.speak(ai_reply)

    def run_pipeline(self):
        from modules.voice import VoiceEngine
        voice = VoiceEngine()
        
        user_text = voice.listen()
        if user_text:
            # 1. Detect language (Hindi 'hi' or English 'en')
            try:
                detected_lang = detect(user_text)
            except:
                detected_lang = 'en'
            
            print(f"Detected Lang: {detected_lang} | User: {user_text}")
            
            # 2. Get AI response
            ai_reply = self.get_response(user_text)
            
            # 3. Speak back in the detected language
            voice.speak(ai_reply, lang=detected_lang)