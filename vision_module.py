from google import genai
from google.genai import types
import pyautogui
import os
from dotenv import load_dotenv
from googlesearch import search
import time

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
    
def get_personal_context():
    """Reads your personal info from the text file with UTF-8 encoding"""
    try:
        # Added encoding="utf-8" here to fix the charmap error
        with open("personal_info.txt", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "No personal info found."
    except UnicodeDecodeError:
        # Extra safety in case the file is still acting up
        return "Error reading personal_info.txt. Please ensure it is saved in UTF-8 format."
    
def get_chat_response(user_input):
    """Answers questions based on your personal info"""
    context = get_personal_context()
    # We combine your info with the user question
    full_prompt = f"User Info Context: {context}\n\nQuestion: {user_input}"
    
    response = client.models.generate_content(
        model=CURRENT_MODEL,
        contents=full_prompt
    )
    return response.text

def autofill_form_logic():
    """Reads the screen for form fields and provides the data to fill them"""
    context = get_personal_context()
    # 1. Capture the screen (the form)
    screenshot_path = "temp_form.png"
    pyautogui.screenshot(screenshot_path)
    
    with open(screenshot_path, "rb") as f:
        image_data = f.read()

    # 2. Ask Gemini to map your info to the form fields
    prompt = f"""
    I am looking at a form. Based on my personal info below, tell me exactly 
    what to type in each field visible on the screen.
    My Info: {context}
    """
    
    response = client.models.generate_content(
        model=CURRENT_MODEL,
        contents=[prompt, types.Part.from_bytes(data=image_data, mime_type='image/png')]
    )
    return response.text

def type_into_form(instructions):
    """Parses the AI text and types it into the browser"""
    # 1. Clean the text to find "Field: Value" pairs
    lines = instructions.split('\n')
    
    # 2. Give the user time to click the first input box
    print("⏳ Switching to 'Type Mode' in 5 seconds...")
    time.sleep(5) 
    
    for line in lines:
        if ":" in line:
            # Split "Name: Amit Paul" into "Amit Paul"
            parts = line.split(":", 1)
            if len(parts) == 2:
                value = parts[1].strip().replace("*", "")
                
                if value:
                    print(f"⌨️ Typing: {value}")
                    # Type the value slowly to avoid errors
                    pyautogui.write(value, interval=0.1) 
                    # Press Tab to move to the next field
                    pyautogui.press('tab') 
                    time.sleep(0.5) # Wait for page response