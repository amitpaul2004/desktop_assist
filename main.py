import keyboard
import vision_module
import doc_module
import voice_module
import time

def run_assistant():
    print("🚀 Assistant Active!")
    print("Ctrl+Shift+A: Read Screen | V: Ask Voice Question")

    while True:
        # Trigger 1: Screen Read
        if keyboard.is_pressed('ctrl+shift+a'):
            voice_module.speak("Analyzing your screen now.")
            analysis = vision_module.get_screen_analysis()
            
            # Save to doc
            doc_name = doc_module.create_document(analysis)
            
            # Speak the answer
            voice_module.speak(f"I've found the answers and saved them to {doc_name}. Here is the first part: {analysis[:150]}")
            time.sleep(1)

        # Trigger 2: Ask a question
        if keyboard.is_pressed('v'):
            voice_module.speak("I'm listening.")
            user_query = voice_module.listen()
            
            if user_query:
                response = vision_module.get_chat_response(user_query)
                voice_module.speak(response)
            else:
                voice_module.speak("I didn't catch that.")

        time.sleep(0.1)

if __name__ == "__main__":
    run_assistant()