import threading
import numpy as np
import pyaudio
from pynput import keyboard
import openwakeword
from openwakeword.model import Model

class HotkeyListener(threading.Thread):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.daemon = True

    def run(self):
        # Activation: Ctrl + Alt + A
        # Using a dictionary for better readability and scaling
        hotkeys = {
            '<ctrl>+<alt>+a': self.callback
        }
        with keyboard.GlobalHotKeys(hotkeys) as h:
            h.join()

class WakeWordListener(threading.Thread):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.daemon = True
        self.chunk_size = 1280  # Required chunk size for openWakeWord
        self.sample_rate = 16000 # Wake word models are trained at 16kHz

    def run(self):
        # FIX 1: Explicitly use ONNX to avoid TFLite errors on Windows
        # FIX 2: Ensure models are downloaded (see step below code)
        try:
            model = Model(
                wakeword_models=["hey_jarvis"], 
                inference_framework="onnx"
            )
        except Exception as e:
            print(f"Error loading Wake Word model: {e}")
            return

        # Initialize PyAudio
        audio_interface = pyaudio.PyAudio()
        mic_stream = audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )

        print("Wake Word Engine (ONNX) is active and listening...")

        while True:
            try:
                # Read raw bytes and convert to numpy array
                data = mic_stream.read(self.chunk_size, exception_on_overflow=False)
                audio_frame = np.frombuffer(data, dtype=np.int16)
                
                # Feed audio to the model
                prediction = model.predict(audio_frame)
                
                # Check prediction confidence
                for mdl in prediction:
                    # Threshold 0.6 balances accuracy and false triggers
                    if prediction[mdl] > 0.6:
                        print(f"Wake word detected: {mdl}")
                        self.callback()
            except Exception as e:
                print(f"Audio Stream Error: {e}")
                continue