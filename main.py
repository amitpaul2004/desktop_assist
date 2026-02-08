import keyboard
import vision_module
import doc_module
import voice_module
import time
import os

def run_assistant():
    print("🚀 2026 Desktop AI Assistant is ONLINE")
    print("-" * 40)
    print("Commands:")
    print("[Ctrl+Shift+A] -> Read Screen & Create Word Doc")
    print("[V]             -> Voice Chat (General)")
    print("[G]             -> Web Search (Live Research)")
    print("[O]             -> Action Mode (Open Apps)")
    print("-" * 40)

    while True:
        # A. SCREEN READ & SAVE DOC
        if keyboard.is_pressed('ctrl+shift+a'):
            voice_module.speak("Capturing screen...")
            analysis = vision_module.get_screen_analysis()
            fname = doc_module.create_document(analysis)
            voice_module.speak(f"Analysis complete. Saved to {fname}.")
            print(analysis)
            time.sleep(1)

        # B. VOICE CHAT
        if keyboard.is_pressed('v'):
            voice_module.speak("I'm listening.")
            query = voice_module.listen()
            if query:
                response = vision_module.get_chat_response(query)
                voice_module.speak(response)

        # C. WEB RESEARCH (LIVE)
        if keyboard.is_pressed('g'):
            voice_module.speak("What should I search for?")
            query = voice_module.listen()
            if query:
                voice_module.speak(f"Searching Google for {query}...")
                response = vision_module.get_web_search(query)
                voice_module.speak(response)

        # D. ACTION MODE (APP OPENER)
        if keyboard.is_pressed('o'):
            voice_module.speak("Which app should I open?")
            app_name = voice_module.listen().lower()
            if "notepad" in app_name:
                os.system("notepad.exe")
            elif "chrome" in app_name:
                os.system("start chrome")
            elif "calculator" in app_name:
                os.system("calc.exe")
            else:
                voice_module.speak(f"I don't have a shortcut for {app_name} yet.")

        time.sleep(0.1)

if __name__ == "__main__":
    run_assistant()