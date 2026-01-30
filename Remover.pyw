# Remover.pyw - Advanced Silent Cleanup (Hides from Task Manager)
import os
import subprocess
import shutil
from pathlib import Path
import psutil  # We use psutil for precise process killing by command line

def kill_specific_scripts():
    target_scripts = ["Personal_KeyLogger.pyw", "Telegram_Sender.pyw"]
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] in ['python.exe', 'pythonw.exe']:
                cmdline = proc.info['cmdline']
                if cmdline and len(cmdline) > 1:
                    script_path = cmdline[-1]  # Last argument is usually the .pyw file
                    script_name = os.path.basename(script_path)
                    if script_name in target_scripts:
                        proc.terminate()  # Graceful
                        proc.wait(timeout=3)  # Wait a bit
                        proc.kill()           # Force kill if needed
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
            pass

def silent_remove(path):
    try:
        if path.exists():
            if path.is_file():
                os.remove(path)
            elif path.is_dir():
                shutil.rmtree(path)
    except:
        pass

# --- Paths ---
desktop = Path(os.path.expanduser("~")) / "Desktop"
startup_folder = Path(os.environ['APPDATA']) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"

files_to_remove = [
    startup_folder / "Personal_KeyLogger.pyw",
    startup_folder / "Telegram_Sender.pyw",
    desktop / "Personal_KeyLogger.pyw",
    desktop / "Telegram_Sender.pyw",
    desktop / "textlog.txt"  # Delete log file too
]

# --- Main Cleanup (completely silent) ---
try:
    # 1. Kill only the exact running scripts (precise, no wrong kills)
    kill_specific_scripts()

    # 2. Remove all files silently
    for file_path in files_to_remove:
        silent_remove(file_path)

except:
    pass  # Always silent

# Exit immediately
os._exit(0)
