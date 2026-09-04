#!/usr/bin/env python3
"""
Omniverse Live Screen Watcher & Visual HTML Testing Audit Tool
Maintains active screen captures and opens HTML entrypoints for real-time user testing.
"""

import os
import time
import subprocess
import webbrowser
import json

BASE_DIR = "/Users/silversurfer/Documents/Omniverse2"
CAPTURE_PATH = os.path.join(BASE_DIR, "live_screen_capture.png")
LOG_PATH = os.path.join(BASE_DIR, "live_screen_audit_log.json")

# 1. HTML Entrypoint URLs
URLS = [
    "http://localhost:8080/index.html",
    "http://localhost:8080/public_html_local/index.html",
    "http://localhost:8080/cyberpunk_telemetry_live.html"
]

def open_html_pages():
    print("[+] Opening HTML entrypoints in Google Chrome / default browser...")
    for url in URLS:
        try:
            # Use mac open command to launch Chrome tab
            subprocess.run(["open", url], check=True)
            print(f"    ✓ Opened: {url}")
            time.sleep(0.5)
        except Exception as e:
            print(f"    [!] Error opening {url}: {e}")

def capture_screen():
    try:
        # screencapture -x disables sound
        subprocess.run(["screencapture", "-x", CAPTURE_PATH], check=True)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_data = {
            "last_capture_time": timestamp,
            "image_path": CAPTURE_PATH,
            "status": "ACTIVE_CAPTURING"
        }
        with open(LOG_PATH, "w", encoding="utf-8") as f:
            json.dump(log_data, f, indent=2)
        return True
    except Exception as e:
        print(f"[!] Screen capture error: {e}")
        return False

def run_watcher(interval_seconds=3, duration_seconds=120):
    print(f"[*] Starting Live Screen Watcher (capturing every {interval_seconds}s for {duration_seconds}s)...")
    start_time = time.time()
    count = 0
    while time.time() - start_time < duration_seconds:
        if capture_screen():
            count += 1
            print(f"    [Frame #{count}] Screen captured to {CAPTURE_PATH}")
        time.sleep(interval_seconds)
    print("[*] Screen Watcher session finished.")

if __name__ == "__main__":
    open_html_pages()
    capture_screen()
    print("\n[✓] Screen Watcher initialized and single-frame captured.")
    print("Run `python3 live_screen_watcher.py --loop` for continuous background monitoring.")
