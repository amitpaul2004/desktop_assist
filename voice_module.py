import pyttsx3
import speech_recognition as sr

# Initialize the 'Mouth' (Text-to-Speech)
def init_engine():
    try:
        # sapi5 is the standard voice driver for Windows
        engine = pyttsx3.init('sapi5')
    except Exception:
        engine = pyttsx3.init()
    
    engine.setProperty('rate', 180)
    engine.setProperty('volume', 1.0)
    return engine

engine = init_engine()

def speak(text):
    """Makes the AI speak"""
    print(f"🎙️ AI: {text}")
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Voice Error: {e}")

def listen():
    """Listens for the user's voice and returns text"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        # Adjust for background noise
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            query = r.recognize_google(audio)
            print(f"👤 You: {query}")
            return query
        except sr.WaitTimeoutError:
            print("No speech detected.")
            return ""
        except Exception as e:
            print(f"Listening Error: {e}")
            return ""