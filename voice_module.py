import pyttsx3
import speech_recognition as sr
import threading

# Create a lock to prevent simultaneous speech overlapping
speech_lock = threading.Lock()

def speak(text):
    """Thread-safe speech function to prevent 'run loop' errors."""
    def _run_speech():
        with speech_lock:
            try:
                # Initialize engine locally inside the thread for stability
                engine = pyttsx3.init()
                
                # Optional: Adjust speed for a more natural feel
                engine.setProperty('rate', 180) 
                
                print(f"🎙️ AI: {text}")
                engine.say(text)
                engine.runAndWait()
                engine.stop() # Cleanly stop the engine
            except Exception as e:
                print(f"Voice Output Error: {e}")

    # Run speech in a temporary thread so it doesn't freeze the main app
    t = threading.Thread(target=_run_speech)
    t.start()

def listen():
    """Listens for user voice input and returns text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        return query
    except Exception as e:
        print("Could not understand audio.")
        return None