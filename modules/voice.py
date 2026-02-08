import speech_recognition as sr
from gtts import gTTS
import pygame
import os
import time

class VoiceEngine:
    def __init__(self):
        """Initializes the audio mixer and speech recognizer."""
        pygame.mixer.init()
        # Ensure we use an absolute path for the audio file
        self.temp_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "response.mp3")
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def speak(self, text, lang='en'):
        """
        Converts text to speech using gTTS and plays it via Pygame.
        Supported langs: 'en' (English), 'hi' (Hindi), 'bn' (Bengali)
        """
        try:
            # 1. Stop and unload the mixer to release the file handle
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            pygame.mixer.music.unload()

            # 2. Delete the old file if it exists to start fresh
            if os.path.exists(self.temp_file):
                try:
                    os.remove(self.temp_file)
                except OSError:
                    pass # Skip if file is still locked by system

            # 3. Generate new speech and save
            tts = gTTS(text=text, lang=lang)
            tts.save(self.temp_file)
            
            # 4. Wait for file to be ready, then play
            time.sleep(0.2) 
            pygame.mixer.music.load(self.temp_file)
            pygame.mixer.music.play()

            # 5. Keep the thread alive until the AI finishes speaking
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
                
        except Exception as e:
            print(f"Voice Output Error: {e}")

    def listen(self, lang="en-IN"):
        """
        Listens to the microphone and converts speech to text.
        Returns the string or None if it fails.
        """
        with self.microphone as source:
            print(f"Listening ({lang})...")
            # Adjust for background noise in your room
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                # Capture audio with a 5s wait time and 10s max recording
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                print("Processing speech...")
                
                # Convert to text using Google's API
                query = self.recognizer.recognize_google(audio, language=lang)
                print(f"Captured: {query}")
                return query
            except sr.UnknownValueError:
                print("Could not understand the audio.")
                return None
            except sr.RequestError:
                print("Speech API service is down.")
                return None
            except Exception as e:
                print(f"Microphone Error: {e}")
                return None