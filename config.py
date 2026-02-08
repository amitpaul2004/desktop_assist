# ai_assistant/config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Replace the text inside the quotes with your actual key from Google AI Studio
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# You can also add other settings here
WAKE_WORD = "hey jarvis"
HOTKEY = "<ctrl>+<alt>+a"