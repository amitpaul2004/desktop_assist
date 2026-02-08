from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc

def set_system_volume(level):
    """Sets system volume (level: 0 to 100)"""
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    
    # Pycaw uses decibels (dB). 0.0 is max, -65.25 is min (0%).
    # This formula converts 0-100 to the correct dB range.
    if level == 0:
        volume.SetMasterVolumeLevel(-65.25, None)
    else:
        # Interpolate 1-100 to dB range
        db = (level / 100) * 65.25 - 65.25
        volume.SetMasterVolumeLevel(db, None)
    print(f"Volume set to {level}%")

def set_system_brightness(level):
    """Sets screen brightness (level: 0 to 100)"""
    try:
        sbc.set_brightness(level)
        print(f"Brightness set to {level}%")
    except Exception as e:
        print(f"Brightness Error: {e}")