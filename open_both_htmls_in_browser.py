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

print("🚀 Checking local telemetry & SEO HTTP servers...")

# Check server on port 8090 (Telemetry & Main Site)
if not is_port_active(8090):
    print("📡 Starting Telemetry HTTP server on port 8090...")
    subprocess.Popen(["python3", "launch_cyberpunk_telemetry_live.py"], cwd="/Users/silversurfer/Documents/Omniverse2")
    time.sleep(1.5)
else:
    print("✅ Port 8090 HTTP server is active!")

# Check server on port 8080 (SEO Dashboard)
if not is_port_active(8080):
    print("📡 Starting SEO Dashboard HTTP server on port 8080...")
    subprocess.Popen(["python3", "launch_cyberpunk_dashboard.py"], cwd="/Users/silversurfer/Documents/Omniverse2")
    time.sleep(1.5)
else:
    print("✅ Port 8080 HTTP server is active!")

# Open Google Chrome tabs using AppleScript for native iMac access
applescript = '''
tell application "Google Chrome"
    activate
    open location "http://localhost:8090/cyberpunk_telemetry_live.html"
    delay 0.5
    open location "http://localhost:8080/cyberpunk_seo_dashboard.html"
    delay 0.5
    open location "http://localhost:8090/index.html"
    delay 0.5
    open location "http://localhost:8080/client_seo_audit_report.html"
end tell
'''

print("🌐 Opening Google Chrome with all active HTML dashboards & website...")
res = subprocess.run(["osascript", "-e", applescript], capture_output=True, text=True)

if res.returncode == 0:
    print("✨ Successfully opened all HTML dashboards in Google Chrome!")
else:
    print(f"⚠️ AppleScript notice: {res.stderr}")
    # Fallback to system open command
    subprocess.run(["open", "http://localhost:8090/cyberpunk_telemetry_live.html"])
    subprocess.run(["open", "http://localhost:8080/cyberpunk_seo_dashboard.html"])
    subprocess.run(["open", "http://localhost:8090/index.html"])
    subprocess.run(["open", "http://localhost:8080/client_seo_audit_report.html"])
    print("✨ Opened via default system browser!")
