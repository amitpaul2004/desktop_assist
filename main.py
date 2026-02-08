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
    print("[V]             -> Voice Chat (General Knowledge)")
    print("[G]             -> Web Research (Live Google Search)")
    print("[O]             -> Action Mode (Open/Close Apps)")
    print("-" * 45)
    print("System is listening for hotkeys...")

    while True:
        try:
            # 1. READ SCREEN & SAVE DOCUMENT
            if keyboard.is_pressed('ctrl+shift+a'):
                voice_module.speak("Capturing screen and analyzing.")
                # Uses the vision module to read questions/text
                analysis = vision_module.get_screen_analysis()
                # Saves the result into a Word Document
                fname = doc_module.create_document(analysis)
                voice_module.speak(f"Finished. Answers are saved in {fname}.")
                time.sleep(1)

            # 2. GENERAL VOICE CHAT
            if keyboard.is_pressed('v'):
                voice_module.speak("I am listening.")
                query = voice_module.listen()
                if query:
                    response = vision_module.get_chat_response(query)
                    voice_module.speak(response)

            # 3. LIVE WEB RESEARCH
            if keyboard.is_pressed('g'):
                voice_module.speak("What should I search on the web?")
                query = voice_module.listen()
                if query:
                    voice_module.speak(f"Searching for {query}...")
                    response = vision_module.get_web_search(query)
                    voice_module.speak(response)

            # 4. ACTION MODE (OPEN & CLOSE APPS)
            if keyboard.is_pressed('o'):
                voice_module.speak("System command? Say 'Open' or 'Close' followed by the app name.")
                command = voice_module.listen().lower()
                
                if command:
                    # Logic for CLOSING an app
                    if "close" in command:
                        target = command.replace("close", "").strip()
                        voice_module.speak(f"Closing {target}")
                        close_app(target, match_closest=True, output=False)
                    
                    # Logic for OPENING an app
                    else:
                        target = command.replace("open", "").strip()
                        voice_module.speak(f"Opening {target}")
                        open_app(target, match_closest=True, output=False)

        except Exception as e:
            print(f"Main Loop Error: {e}")
            time.sleep(1) # Small pause to prevent rapid-fire errors

        time.sleep(0.05) # Keeps CPU usage low

if __name__ == "__main__":
    run_assistant()