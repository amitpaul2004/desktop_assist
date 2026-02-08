import speech_recognition as sr
from gtts import gTTS
import pygame
import os
import time

class VoiceEngine:
    def __init__(self):
        pygame.mixer.init()
        # Use absolute path to avoid directory errors
        self.temp_file = os.path.join(os.getcwd(), "response.mp3")
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def speak(self, text, lang='en'):
        try:
            # Release file from mixer before saving new one
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            pygame.mixer.music.unload()

            # Save the new speech
            tts = gTTS(text=text, lang=lang)
            tts.save(self.temp_file)
            
            # Wait a tiny bit for the file to exist on disk
            while not os.path.exists(self.temp_file):
                time.sleep(0.1)

            pygame.mixer.music.load(self.temp_file)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
        except Exception as e:
            print(f"Voice Error: {e}")

    def listen(self):
        with self.microphone as source:
            print("Listening (Multi-language)...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                # We don't specify a language here so it picks up the dominant one
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                # Recognize using a list of likely languages
                query = self.recognizer.recognize_google(audio, language="hi-IN") 
                return query
            except Exception:
                return None