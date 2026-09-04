#!/usr/bin/env python3
import subprocess
import time
import urllib.request
import os

def is_port_active(port):
    try:
        req = urllib.request.urlopen(f"http://localhost:{port}/", timeout=1)
        return True
    except Exception:
        return False

print("🚀 Booting MASTER OMNIVERSE HUD Engine...")

# Check server on port 8080 (Master HUD Server)
if not is_port_active(8080):
    print("📡 Starting Master HUD HTTP server on port 8080...")
    subprocess.Popen(["python3", "launch_master_hud.py"], cwd="/Users/silversurfer/Documents/Omniverse2")
    time.sleep(2)
else:
    print("✅ Port 8080 HTTP server is active!")

# Open Google Chrome tabs using AppleScript for native iMac access
applescript = '''
tell application "Google Chrome"
    activate
    open location "http://localhost:8080/master_dashboard.html"
end tell
'''

print("🌐 Opening Google Chrome into the Master HUD SPA...")
res = subprocess.run(["osascript", "-e", applescript], capture_output=True, text=True)

if res.returncode == 0:
    print("✨ Successfully opened the MASTER HUD in Google Chrome!")
else:
    print(f"⚠️ AppleScript notice: {res.stderr}")
    # Fallback to system open command
    subprocess.run(["open", "http://localhost:8080/master_dashboard.html"])
    print("✨ Opened via default system browser!")
