import os
# This MUST come before 'import cv2' or 'from deepface import DeepFace'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from duckduckgo_search import DDGS
from google import genai
from google.genai import types
import pyautogui
from googlesearch import search as google_query
from dotenv import load_dotenv
from googlesearch import search
import time
import csv
import pywhatkit as kit
import cv2
from deepface import DeepFace
import webbrowser
import threading
import time
import pyautogui





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
    """
    Performs a live web search using the latest DDGS syntax.
    """
    try:
        print(f"🔍 Searching the web for: {query}...")
        
        results = []
        # In the newest versions, DDGS() works as a context manager
        with DDGS() as ddgs:
            # We use list comprehension to capture the generator output
            ddgs_gen = ddgs.text(query, max_results=5)
            for r in ddgs_gen:
                results.append(r)

        if not results:
            return "I searched the web but couldn't find any relevant information."

        # Format the data for Gemini
        search_context = ""
        for i, r in enumerate(results, 1):
            search_context += f"Source {i}: {r['title']}\nSnippet: {r['body']}\n\n"

        # Strict Prompt to keep it focused on the web, not your resume
        prompt = f"Answer this question based ONLY on these web results:\n\n{search_context}\n\nQuestion: {query}"

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        print(f"Web Search Error: {e}")
        return "Sorry Amit, I'm having trouble connecting to the search service."
    
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


import csv

def get_number_by_name(name):
    """Searches the Google Contacts CSV format for a name"""
    try:
        # Using utf-8-sig to handle hidden Windows characters
        with open('contacts.csv', mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Use 'First Name' instead of 'Name'
                contact_name = row.get('First Name', '')
                # Use 'Phone 1 - Value' instead of 'Number'
                contact_number = row.get('Phone 1 - Value', '')
                
                if contact_name.lower() == name.lower():
                    # Strip any spaces from the number to avoid errors
                    return contact_number.replace(" ", "")
        return None
    except Exception as e:
        print(f"❌ CSV Error: {e}")
        return None

def whatsapp_action(action_type, name, message=None):
    """Handles WhatsApp messaging and calls using CSV lookup"""
    number = get_number_by_name(name)
    
    if not number:
        return f"Contact '{name}' not found in your CSV."

    try:
        if action_type == "text" and message:
            print(f"💬 Texting {name} ({number}): {message}")
            kit.sendwhatmsg_instantly(number, message, wait_time=25, tab_close=True)
            return f"Message sent to {name}."
            
        elif action_type == "call":
            print(f"📞 Calling {name} ({number})...")
            # This opens the chat; you click the call button in the Desktop App
            call_url = f"whatsapp://send?phone={number}" 
            os.startfile(call_url)
            return f"WhatsApp opened for {name}."
            
    except Exception as e:
        return f"WhatsApp Error: {str(e)}"
    
def smart_autofill():
    """Captures form, checks personal info, searches web for unknowns, then types"""
    # 1. Get your personal data
    personal_context = get_personal_context()
    
    # 2. Capture the form
    screenshot_path = "temp_form.png"
    pyautogui.screenshot(screenshot_path)
    
    with open(screenshot_path, "rb") as f:
        image_data = f.read()

    # 3. Ask Gemini to identify fields and flag "Unknowns"
    prompt = f"""
    Analyze this form. For each field:
    1. If the answer is in my info: {personal_context}, use it.
    2. If the answer is a general knowledge question NOT in my info, 
       respond with 'SEARCH: [the question]'.
    Format as 'Field Name: Value'.
    """
    
    initial_analysis = client.models.generate_content(
        model=CURRENT_MODEL,
        contents=[prompt, types.Part.from_bytes(data=image_data, mime_type='image/png')]
    ).text

    # 4. Process "SEARCH" flags
    final_instructions = []
    lines = initial_analysis.split('\n')
    
    for line in lines:
        if "SEARCH:" in line:
            # Extract the search query
            query = line.split("SEARCH:")[1].strip()
            voice_module.speak(f"Searching web for {query}")
            # Use your existing web search function
            web_answer = get_web_search(query)
            # Clean the answer to be short for the form
            final_instructions.append(f"{line.split(':')[0]}: {web_answer}")
        else:
            final_instructions.append(line)

    return "\n".join(final_instructions)

# At the top of vision_module.py
tired_counter = 0 

def detect_emotion_and_check_fatigue():
    global tired_counter
    # 1. INITIALIZE AT THE VERY TOP
    dominant_emotion = "unknown"
    suggest_break = False 
    
    try:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        
        if not ret:
            print("❌ Camera access failed.")
            cap.release()
            return dominant_emotion, suggest_break # Returns (unknown, False)
        
        face_img = "current_face.png"
        cv2.imwrite(face_img, frame)
        cap.release()

        # Perform DeepFace analysis
        analysis = DeepFace.analyze(img_path=face_img, actions=['emotion'], enforce_detection=False)
        dominant_emotion = analysis[0]['dominant_emotion']
        
        # 2. LOGIC UPDATES
        if dominant_emotion in ['neutral', 'sad']:
            tired_counter += 1
        else:
            tired_counter = 0 
            
        if tired_counter >= 3:
            suggest_break = True
            tired_counter = 0 
            
        return dominant_emotion, suggest_break

    except Exception as e:
        # 3. FALLBACK
        print(f"Emotion Logic Error: {e}")
        return dominant_emotion, suggest_break
    
# YouTube link for relaxation music
RELAX_URL = "https://www.youtube.com/watch?v=jfKfPfyJRdk" # Lofi / Relaxing music

def open_relaxation_music():
    """Opens a YouTube video for a study break"""
    print("🎵 Opening relaxation music...")
    webbrowser.open(RELAX_URL)

def fatigue_monitor_loop(voice_module):
    """Background loop that runs every 5 minutes with Emotional Speech"""
    while True:
        # Wait for 5 minutes (300 seconds)
        time.sleep(300) 
        
        print("🕒 5-Minute Check: Analyzing fatigue...")
        emotion, suggest_break = detect_emotion_and_check_fatigue()
        
        # 1. HANDLE STUDY BREAKS FIRST
        if suggest_break:
            voice_module.speak("Amit, you've been working hard at JIS University for a while. It's time for a break.")
            open_relaxation_music()
        
        # 2. EMOTIONAL SPEECH (If no break is needed yet)
        elif emotion == "happy":
            voice_module.speak("I noticed you're looking happy, Amit! Did you solve a tough bug in your MERN project?")
        elif emotion == "angry":
            voice_module.speak("You look a bit frustrated. Take a deep breath; we will fix the code together.")
        elif emotion == "sad":
            voice_module.speak("You seem a bit down. Remember, you're a great developer. Keep going!")
        elif emotion == "neutral":
            # Only print neutral to avoid being too annoying, but speak if counter is high
            print(f"System noticed you look neutral. Fatigue counter: {tired_counter}")
        
        # Log the status for debugging
        if emotion == "unknown":
            print("🕒 Check complete: No face detected.")


def type_into_form(data_list):
    # data_list should be a list of strings like ["Amit Paul", "Ichapur", "MERN Developer"]
    for info in data_list:
        # Type the info with a slight human-like delay
        pyautogui.write(info, interval=0.1) 
        
        # Press Tab to move to the next field
        pyautogui.press('tab')
        
        # Short pause between fields to let the website keep up
        time.sleep(0.5)