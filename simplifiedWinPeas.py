import os
import subprocess
import platform

# Function to execute and return output of shell commands
def run_command(command):
    try:
        result = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.DEVNULL)
        return result.strip()
    except subprocess.CalledProcessError:
        return None

# Enumerate System Information
def get_system_info():
    print("[*] Enumerating System Information...")
    print(f"OS Version: {platform.platform()}")
    print(f"Architecture: {platform.architecture()[0]}")
    print(f"Hostname: {platform.node()}")
    print(f"Username: {os.getenv('USERNAME')}")
    print(f"User Domain: {os.getenv('USERDOMAIN')}")
    print(f"Is Admin: {'Yes' if os.getenv('USERNAME') == 'Administrator' else 'No'}\n")

# Enumerate Services
def get_services():
    print("[*] Enumerating Running Services...")
    services = run_command("sc query state= all")
    if services:
        for line in services.split("\n"):
            if "SERVICE_NAME" in line:
                print(line.strip())
    else:
        print("No services found or access denied.\n")

# Check Environment Variables
def check_env_vars():
    print("[*] Checking Environment Variables...")
    for key, value in os.environ.items():
        print(f"{key}: {value}")
    print()

# Look for Sensitive Files
def find_sensitive_files():
    print("[*] Searching for Sensitive Files...")
    potential_files = [
        "unattend.xml", "web.config", "app.config", "credentials.xml",
        "id_rsa", "id_dsa", "passwords.txt"
    ]
    for root, dirs, files in os.walk("C:\\"):
        for file in files:
            if file in potential_files:
                print(f"Found: {os.path.join(root, file)}")
    print()

# Enumerate Installed Programs
def get_installed_programs():
    print("[*] Enumerating Installed Programs...")
    programs = run_command('wmic product get name,version')
    if programs:
        print(programs)
    else:
        print("No installed programs found or access denied.\n")

# Main Function
def main():
    print("=== Simplified WinPEAS Script ===\n")
    get_system_info()
    get_services()
    check_env_vars()
    find_sensitive_files()
    get_installed_programs()

if __name__ == "__main__":
    main()
