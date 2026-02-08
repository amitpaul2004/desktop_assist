# modules/brain.py
from google import genai
from config import GEMINI_API_KEY

class AIProcessor:
    def __init__(self):
        # New syntax for the unified SDK
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model_id = "gemini-1.5-flash"
        # Chat session initialization
        self.chat = self.client.chats.create(model=self.model_id)

    def get_response(self, prompt):
        try:
            # New method name is 'send_message' on the chat object
            response = self.chat.send_message(prompt)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"

    def run_pipeline(self):
        # Your voice logic stays mostly the same
        from modules.voice import VoiceEngine
        voice = VoiceEngine()
        user_text = voice.listen()

        if user_text:
            print(f"You: {user_text}")
            reply = self.get_response(user_text)
            print(f"AI: {reply}")
            voice.speak(reply)