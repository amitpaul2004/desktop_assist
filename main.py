import keyboard
import vision_module
import doc_module
import voice_module
import time
import os
from AppOpener import open as open_app, close as close_app

def run_assistant():
    print("🚀 2026 AI Assistant: FULLY INTEGRATED")
    print("-" * 45)
    print("COMMAND LIST:")
    print("[Ctrl+Shift+A] -> Read Screen & Create Word Doc")
    print("[V]             -> Personalized Voice Chat")
    print("[G]             -> Web Research (Live Google Search)")
    print("[O]             -> Action Mode (Open/Close Apps)")
    print("[F]             -> Autofill Form (Based on Personal Info)")
    print("[W]             -> WhatsApp Automation (CSV Contacts)")
    print("-" * 45)
    print("System is listening for hotkeys...")

    while True:
        try:
            # 1. READ SCREEN & SAVE DOCUMENT
            if keyboard.is_pressed('ctrl+shift+a'):
                voice_module.speak("Capturing screen and analyzing.")
                analysis = vision_module.get_screen_analysis()
                fname = doc_module.create_document(analysis)
                voice_module.speak(f"Finished. Answers saved in {fname}.")
                print(analysis)
                while keyboard.is_pressed('ctrl') or keyboard.is_pressed('a'): pass 

            # 2. PERSONALIZED VOICE CHAT (Who is Amit?)
            if keyboard.is_pressed('v'):
                voice_module.speak("I am listening.")
                query = voice_module.listen()
                if query:
                    response = vision_module.get_chat_response(query)
                    voice_module.speak(response)
                while keyboard.is_pressed('v'): pass 

            # 3. LIVE WEB RESEARCH
            if keyboard.is_pressed('g'):
                voice_module.speak("What should I search on the web?")
                query = voice_module.listen()
                if query:
                    voice_module.speak(f"Searching for {query}...")
                    response = vision_module.get_web_search(query)
                    voice_module.speak(response)
                while keyboard.is_pressed('g'): pass 

            # 4. ACTION MODE (OPEN & CLOSE APPS)
            if keyboard.is_pressed('o'):
                voice_module.speak("System command? Say Open or Close followed by the app name.")
                command = voice_module.listen().lower()
                if command:
                    if "close" in command:
                        target = command.replace("close", "").strip()
                        voice_module.speak(f"Closing {target}")
                        close_app(target, match_closest=True, output=False)
                    else:
                        target = command.replace("open", "").strip()
                        voice_module.speak(f"Opening {target}")
                        open_app(target, match_closest=True, output=False)
                while keyboard.is_pressed('o'): pass 

            # 5. AUTOFILL FORM (Typing mode)
            if keyboard.is_pressed('f'):
                voice_module.speak("Analyzing form fields. Prepare to click the first field.")
                instructions = vision_module.autofill_form_logic()
                print("\n--- FILLING INSTRUCTIONS ---")
                print(instructions)
                # This calls the function that actually types into the form
                vision_module.type_into_form(instructions)
                while keyboard.is_pressed('f'): pass 

            # 6. WHATSAPP AUTOMATION (CSV Based)
            if keyboard.is_pressed('w'):
                voice_module.speak("Who do you want to contact?")
                name = voice_module.listen() 
                if name:
                    voice_module.speak(f"Should I call or message {name}?")
                    choice = voice_module.listen().lower()
                    if "message" in choice or "text" in choice:
                        voice_module.speak("What is the message?")
                        msg = voice_module.listen()
                        if msg:
                            result = vision_module.whatsapp_action("text", name, msg)
                            voice_module.speak(result)
                    elif "call" in choice:
                        result = vision_module.whatsapp_action("call", name)
                        voice_module.speak(result)
                while keyboard.is_pressed('w'): pass 

        except Exception as e:
            print(f"Main Loop Error: {e}")
            time.sleep(1)

        time.sleep(0.05)

if __name__ == "__main__":
    run_assistant()