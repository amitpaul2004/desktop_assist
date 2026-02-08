from pynput import keyboard
import threading
import openwakeword
from openwakeword.model import Model

import openwakeword
from openwakeword.model import Model

class WakeWordListener(threading.Thread):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.daemon = True

    def run(self):
        # Force the model to use 'onnx' to avoid the tflite error
        model = Model(inference_framework="onnx")
        
class HotkeyListener(threading.Thread):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.daemon = True # Keeps it running in background

    def run(self):
        # Activation: Ctrl + Alt + A
        with keyboard.GlobalHotKeys({'<ctrl>+<alt>+a': self.callback}) as h:
            h.join()

class WakeWordListener(threading.Thread):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.daemon = True

    def run(self):
        # Using openWakeWord for efficient 24/7 listening
        model = Model() 
        while True:
            # Pseudo-code for mic stream; replace with PyAudio stream
            audio_frame = get_mic_audio() 
            prediction = model.predict(audio_frame)
            if any(prediction[mdl] > 0.5 for mdl in prediction):
                self.callback()