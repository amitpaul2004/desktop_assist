import keyboard
import vision_module
import doc_module
import voice_module
import time
import os
import threading
from AppOpener import open as open_app, close as close_app

def run_assistant():
    # Ensure the threading environment sees the imported module
    global voice_module 

    print("🚀 2026 AI Assistant: FULLY INTEGRATED (Amit Paul Edition)")
    print("-" * 50)
    print("ACTIVE HOTKEYS:")
    print("[Ctrl+Shift+A] -> Capture & Analyze Screen")
    print("[V]             -> Chat with AI Assistant")
    print("[G]             -> Web Search (DuckDuckGo)")
    print("[O]             -> App Control (Open/Close)")
    print("[F]             -> Smart Autofill Form")
    print("[W]             -> WhatsApp (Call/Message)")
    print("[E]             -> Manual Mood Check")
    print("[R]             -> Reset System State")
    print("-" * 50)
    print("🕒 Background Fatigue Monitor: ACTIVE (Every 5 Mins)")

    # --- START BACKGROUND THREAD ---
    # The comma in args=(voice_module,) is CRITICAL for Python Tuples
    try:
        monitor_thread = threading.Thread(
            target=vision_module.fatigue_monitor_loop, 
            args=(voice_module,), 
            daemon=True
        )
        monitor_thread.start()
    except Exception as e:
        print(f"Failed to start Fatigue Monitor: {e}")

    while True:
        try:
            # 1. WEB RESEARCH (G KEY)
            if keyboard.is_pressed('g'):
                voice_module.speak("What should I search on the web?")
                query = voice_module.listen()
                if query:
                    voice_module.speak(f"Searching for {query}...")
                    response = vision_module.get_web_search(query)
                    voice_module.speak(response)
                while keyboard.is_pressed('g'): pass 

            # 2. VOICE CHAT (V KEY)
            if keyboard.is_pressed('v'):
                voice_module.speak("I am listening.")
                query = voice_module.listen()
                if query:
                    response = vision_module.get_chat_response(query)
                    voice_module.speak(response)
                while keyboard.is_pressed('v'): pass 

            # 3. MANUAL EMOTION CHECK (E KEY)
            if keyboard.is_pressed('e'):
                voice_module.speak("Analyzing your mood.")
                emotion, suggest_break = vision_module.detect_emotion_and_check_fatigue()
                if suggest_break:
                    voice_module.speak("Amit, you look exhausted. Opening relaxation music.")
                    vision_module.open_relaxation_music()
                else:
                    voice_module.speak(f"You seem to be feeling {emotion}.")
                while keyboard.is_pressed('e'): pass

            # 4. RESET SYSTEM (R KEY)
            if keyboard.is_pressed('r'):
                voice_module.speak("Clearing memory and resetting fatigue counters.")
                vision_module.reset_assistant_state()
                voice_module.speak("System reset complete.")
                while keyboard.is_pressed('r'): pass

            # 5. ACTION MODE (O KEY)
            if keyboard.is_pressed('o'):
                voice_module.speak("Say Open or Close followed by the app name.")
                command = voice_module.listen()
                if command:
                    command = command.lower()
                    if "close" in command:
                        target = command.replace("close", "").strip()
                        close_app(target, match_closest=True, output=False)
                    else:
                        target = command.replace("open", "").strip()
                        open_app(target, match_closest=True, output=False)
                while keyboard.is_pressed('o'): pass

                # 5. SMART AUTOFILL (Based on Personal Info)
            if keyboard.is_pressed('f'):
                voice_module.speak("I am analyzing the form. You have 3 seconds to click into the first input field.")
                
                # Capture and analyze form
                instructions = vision_module.smart_autofill() 
                
                # CRITICAL: Wait for you to focus the browser
                time.sleep(3) 
                
                # Now type the data
                vision_module.type_into_form(instructions)
                
                voice_module.speak("Form filling complete, Amit.")
                while keyboard.is_pressed('f'): pass

        except Exception as e:
            print(f"Main Loop Error: {e}")
            time.sleep(1)

        time.sleep(0.05) # Prevent CPU spikes

if __name__ == "__main__":
    run_assistant()