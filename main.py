import threading
from modules.listeners import HotkeyListener, WakeWordListener
from modules.brain import AIProcessor

def on_trigger(source):
    """Callback function when Hotākey or Sound activates the AI."""
    print(f"Triggered by: {source}")
    ai = AIProcessor()
    ai.run_pipeline()

if __name__ == "__main__":
    # Initialize our listeners
    hotkey_thread = HotkeyListener(callback=lambda: on_trigger("Hotkey"))
    wakeword_thread = WakeWordListener(callback=lambda: on_trigger("Wake Word"))

    # Start the background threads
    hotkey_thread.start()
    wakeword_thread.start()

    print("Assistant is active 24/7 in the background...")
    hotkey_thread.join()
    wakeword_thread.join()