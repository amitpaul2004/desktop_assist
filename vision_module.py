from google import genai
from google.genai import types
import pyautogui
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Use the latest available stable model
# Options in 2026: 'gemini-2.5-flash' or 'gemini-2.0-flash'
CURRENT_MODEL = 'gemini-2.5-flash-lite' 

def get_screen_analysis():
    screenshot_path = "temp_screen.png"
    pyautogui.screenshot(screenshot_path)
    
    with open(screenshot_path, "rb") as f:
        image_data = f.read()

    prompt = "Read the questions on this screen and provide clear, concise answers."
    
    try:
        response = client.models.generate_content(
            model=CURRENT_MODEL,
            contents=[prompt, types.Part.from_bytes(data=image_data, mime_type='image/png')]
        )
        return response.text
    except Exception as e:
        return f"Vision Error: {str(e)}"

def get_chat_response(user_input):
    try:
        response = client.models.generate_content(
            model=CURRENT_MODEL,
            contents=user_input
        )
        return response.text
    except Exception as e:
        return f"Chat Error: {str(e)}"