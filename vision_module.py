from google import genai
from google.genai import types
import pyautogui
import os
from dotenv import load_dotenv
from googlesearch import search

load_dotenv()

# Initialize Gemini Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
# Using the latest 2026 stable model
CURRENT_MODEL = 'gemini-2.5-flash-lite'

def get_screen_analysis(custom_prompt=None):
    """Captures screen and sends to Gemini for analysis"""
    screenshot_path = "temp_screen.png"
    pyautogui.screenshot(screenshot_path)
    
    with open(screenshot_path, "rb") as f:
        image_data = f.read()

    prompt = custom_prompt if custom_prompt else "Identify all questions on this screen and provide clear answers. Format them as a list."
    
    try:
        response = client.models.generate_content(
            model=CURRENT_MODEL,
            contents=[prompt, types.Part.from_bytes(data=image_data, mime_type='image/png')]
        )
        return response.text
    except Exception as e:
        return f"Vision Error: {str(e)}"

def get_chat_response(user_input):
    """Handles standard voice questions"""
    try:
        response = client.models.generate_content(
            model=CURRENT_MODEL,
            contents=user_input
        )
        return response.text
    except Exception as e:
        return f"Chat Error: {str(e)}"

def get_web_search(query):
    """Performs live web search and summarizes findings"""
    try:
        search_results = []
        # Get top 3 search results
        for res in search(query, num_results=3, advanced=True):
            search_results.append(f"Title: {res.title}\nSnippet: {res.description}\nSource: {res.url}")
        
        context = "\n\n".join(search_results)
        prompt = f"Using these 2026 search results, answer the question: '{query}'\n\nResults:\n{context}"
        
        return get_chat_response(prompt)
    except Exception as e:
        return f"Search Error: {str(e)}"