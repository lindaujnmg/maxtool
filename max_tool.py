import ctypes
from ctypes import wintypes
import sys
import time

# Constants
APP_NAME = "MaxTool"
VOLUME_INCREMENT = 5  # Percentage to increase/decrease volume

# Windows API constants
DEVICE_STATE_ACTIVE = 0x00000001
STGM_READ = 0x00000000

# Audio Endpoint Role
eConsole = 0
eMultimedia = 1
eCommunications = 2

# Initialize COM library
ctypes.windll.ole32.CoInitialize(None)

# Define Windows interfaces
class IAudioEndpointVolume(ctypes.IUnknown):
    _iid_ = ctypes.GUID("{5CDF2C82-841E-4546-9722-0CF74078229A}")

    _methods_ = [
        ctypes.COMMETHOD([], ctypes.HRESULT, "RegisterControlChangeNotify"),
        ctypes.COMMETHOD([], ctypes.HRESULT, "UnregisterControlChangeNotify"),
        ctypes.COMMETHOD([], ctypes.HRESULT, "GetChannelCount"),
        ctypes.COMMETHOD([], ctypes.HRESULT, "SetMasterVolumeLevel"),
        ctypes.COMMETHOD([], ctypes.HRESULT, "SetMasterVolumeLevelScalar", 
            (['in'], ctypes.c_float, 'fLevel'), 
            (['in'], ctypes.POINTER(ctypes.GUID), 'pguidEventContext')),
        ctypes.COMMETHOD([], ctypes.HRESULT, "GetMasterVolumeLevelScalar", 
            (['out'], ctypes.POINTER(ctypes.c_float), 'pfLevel')),
        ctypes.COMMETHOD([], ctypes.HRESULT, "SetMute"),
        ctypes.COMMETHOD([], ctypes.HRESULT, "GetMute"),
        ctypes.COMMETHOD([], ctypes.HRESULT, "GetVolumeStepInfo"),
        ctypes.COMMETHOD([], ctypes.HRESULT, "VolumeStepUp"),
        ctypes.COMMETHOD([], ctypes.HRESULT, "VolumeStepDown"),
        ctypes.COMMETHOD([], ctypes.HRESULT, "QueryHardwareSupport"),
        ctypes.COMMETHOD([], ctypes.HRESULT, "GetVolumeRange"),
    ]

def get_audio_endpoint_volume():
    # Load necessary Windows DLLs
    ole32 = ctypes.windll.ole32
    ole32.CoInitialize(None)

    # Get the default audio endpoint
    MMDeviceEnumerator = ctypes.windll.LoadLibrary("Mmdevapi.dll")
    IMMDeviceEnumerator = ctypes.GUID("{A95664D2-9614-4F35-A746-DE8DB63617E6}")
    IAudioEndpointVolume = ctypes.GUID("{5CDF2C82-841E-4546-9722-0CF74078229A}")

    pEnumerator = ctypes.POINTER(IMMDeviceEnumerator)()
    MMDeviceEnumerator.CoCreateInstance(ctypes.byref(IMMDeviceEnumerator), None, ctypes.CLSCTX_INPROC_SERVER, ctypes.byref(pEnumerator))

    pDevice = ctypes.POINTER(IMMDeviceEnumerator)()
    pEnumerator.GetDefaultAudioEndpoint(0, eConsole, ctypes.byref(pDevice))

    pVolume = ctypes.POINTER(IAudioEndpointVolume)()
    pDevice.Activate(ctypes.byref(IAudioEndpointVolume), ctypes.CLSCTX_INPROC_SERVER, None, ctypes.byref(pVolume))

    return pVolume

def set_volume(volume_level):
    pVolume = get_audio_endpoint_volume()
    volume_level = min(1.0, max(0.0, volume_level))
    pVolume.SetMasterVolumeLevelScalar(volume_level, None)

def get_volume():
    pVolume = get_audio_endpoint_volume()
    level = ctypes.c_float()
    pVolume.GetMasterVolumeLevelScalar(ctypes.byref(level))
    return level.value

def increase_volume():
    current_volume = get_volume()
    new_volume = current_volume + (VOLUME_INCREMENT / 100.0)
    set_volume(new_volume)

def decrease_volume():
    current_volume = get_volume()
    new_volume = current_volume - (VOLUME_INCREMENT / 100.0)
    set_volume(new_volume)

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {APP_NAME} [up|down]")
        sys.exit(1)

    command = sys.argv[1].lower()
    if command == "up":
        increase_volume()
    elif command == "down":
        decrease_volume()
    else:
        print(f"Invalid command. Use 'up' or 'down'.")
        sys.exit(1)

    print(f"Volume set to {get_volume() * 100:.0f}%")

if __name__ == "__main__":
    main()