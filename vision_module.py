import os
# This MUST come before 'import cv2' or 'from deepface import DeepFace'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'


from google import genai
from google.genai import types
import pyautogui

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
    try:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if not ret: return "Camera Error", False
        
        face_img = "current_face.png"
        cv2.imwrite(face_img, frame)
        cap.release()

        analysis = DeepFace.analyze(img_path=face_img, actions=['emotion'], enforce_detection=False)
        dominant_emotion = analysis[0]['dominant_emotion']
        
        # Logic for fatigue tracking
        # We consider 'neutral', 'sad' (often looks like tired), or 'fear' (stress)
        if dominant_emotion in ['neutral', 'sad']:
            tired_counter += 1
        else:
            tired_counter = 0 # Reset if you look happy or active
            
        # Trigger break if detected 3 times in a row
        should_break = False
        if tired_counter >= 3:
            should_break = True
            tired_counter = 0 # Reset after suggesting
            
        return dominant_emotion, should_break

    except Exception as e:
        print(f"Emotion Error: {e}")
        return "error", False
    
# YouTube link for relaxation music
RELAX_URL = "https://www.youtube.com/watch?v=5qap5aO4i9A" # Lofi / Relaxing music

def open_relaxation_music():
    """Opens a YouTube video for a study break"""
    print("🎵 Opening relaxation music...")
    webbrowser.open(RELAX_URL)

def fatigue_monitor_loop(voice_module):
    """Background loop that runs every 5 minutes"""
    while True:
        # Wait for 5 minutes (300 seconds)
        time.sleep(10)
        
        print("🕒 5-Minute Check: Analyzing fatigue...")
        emotion, suggest_break = detect_emotion_and_check_fatigue()
        
        if suggest_break:
            voice_module.speak("Amit, you've been working hard at JIS University for a while. It's time for a break.")
            open_relaxation_music()
        elif emotion in ['neutral', 'sad']:
            print(f"System noticed you look {emotion}. Fatigue counter: {tired_counter}")