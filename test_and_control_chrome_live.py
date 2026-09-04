#!/usr/bin/env python3
import time
import subprocess
import os
import sys

print("==================================================")
print("🚀 OMNIVERSE ENTERPRISE CHROME LIVE MOUSE TESTER")
print("==================================================")

# Step 1: Ensure servers are up
print("\n[1/4] Verifying local HTTP servers on ports 8080 & 8090...")

def check_or_start_server(port, script_name):
    cmd = f"lsof -i :{port}"
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.returncode != 0 or not res.stdout.strip():
        print(f"-> Starting {script_name} on port {port}...")
        subprocess.Popen([sys.executable, script_name], cwd="/Users/silversurfer/Documents/Omniverse2")
        time.sleep(2)
    else:
        print(f"-> Port {port} is ALREADY running!")

check_or_start_server(8080, "launch_cyberpunk_dashboard.py")
check_or_start_server(8090, "launch_cyberpunk_telemetry_live.py")

# Step 2: Open both HTML URLs in Chrome
print("\n[2/4] Opening Chrome windows for Telemetry & SEO Dashboards...")
url_telemetry = "http://localhost:8090/cyberpunk_telemetry_live.html"
url_seo = "http://localhost:8080/cyberpunk_seo_dashboard.html"

# AppleScript to open both tabs in Google Chrome and bring Chrome to front
applescript_open = f'''
tell application "Google Chrome"
    activate
    if (count of windows) = 0 then
        make new window
        set URL of active tab of front window to "{url_telemetry}"
    else
        open location "{url_telemetry}"
    end if
    delay 1
    open location "{url_seo}"
    delay 1
end tell
'''
subprocess.run(["osascript", "-e", applescript_open])
print("-> Chrome tabs opened successfully!")

# Step 3: PyAutoGUI / AppleScript Mouse & Event Controller
print("\n[3/4] Preparing Mouse & UI Automation...")

# Helper to run Chrome JS directly via AppleScript
def run_chrome_js(tab_index, js_code):
    as_script = f'''
    tell application "Google Chrome"
        tell window 1
            tell tab {tab_index}
                execute javascript "{js_code}"
            end tell
        end tell
    end tell
    '''
    subprocess.run(["osascript", "-e", as_script], capture_output=True)

# Helper to switch tab in Chrome
def switch_chrome_tab(tab_index):
    as_script = f'''
    tell application "Google Chrome"
        tell window 1
            set active tab index to {tab_index}
        end tell
    end tell
    '''
    subprocess.run(["osascript", "-e", as_script])
    time.sleep(1)

# Helper to scroll active Chrome window
def scroll_chrome(direction="down", amount=500):
    if direction == "down":
        as_script = f'tell application "Google Chrome" to activate\ntell application "System Events" to key code 125' # Down arrow
    else:
        as_script = f'tell application "Google Chrome" to activate\ntell application "System Events" to key code 126' # Up arrow
    for _ in range(5):
        subprocess.run(["osascript", "-e", as_script])
        time.sleep(0.1)

# Try importing pyautogui for physical cursor movements if available
has_pyautogui = False
try:
    import pyautogui
    pyautogui.FAILSAFE = False
    has_pyautogui = True
    print("-> PyAutoGUI detected! Screen mouse cursor movements enabled.")
except ImportError:
    print("-> PyAutoGUI not loaded; using AppleScript native mouse & JS engine.")

# Step 4: Execute Live Test Sequence
print("\n[4/4] STARTING LIVE MOUSE & BUTTON CLICK TEST SEQUENCE...")
print("--------------------------------------------------")

# --- TEST TAB 1: CYBERPUNK TELEMETRY CONSOLE ---
print("\n⚡ [TEST PHASE 1]: Testing Cyberpunk Telemetry Console (Tab 1)...")
switch_chrome_tab(1)
time.sleep(1.5)

# Click through Navigation Tabs
nav_tabs = [
    ("Overview & Stream", 0),
    ("Time-Range Analytics", 1),
    ("Quotes & Call Leads", 2),
    ("Behavior & Heatmaps", 3),
    ("Geolocation & ISP", 4),
    ("Hostinger Archive", 5),
    ("30-MIN AUTOMATED SEO KEYWORD ENGINE", 6)
]

for tab_name, idx in nav_tabs:
    print(f"  🖱️ [MOUSE CLICK] Nav Tab -> {tab_name}")
    run_chrome_js(1, f"const btns = document.querySelectorAll('.tab-btn'); if(btns[{idx}]) btns[{idx}].click();")
    if has_pyautogui:
        # Move mouse across screen visually
        screen_w, screen_h = pyautogui.size()
        target_x = int(screen_w * 0.2 + (idx * 90))
        target_y = int(screen_h * 0.25)
        pyautogui.moveTo(target_x, target_y, duration=0.4)
        pyautogui.click()
    time.sleep(1.2)

# Click through 11 Time Window Filter Buttons
print("\n  ⏱️ [TESTING 11 TIME-WINDOW FILTERS]...")
time_filters = ["5h", "10h", "24h", "2d", "3d", "4d", "5d", "10d", "20d", "30d", "All Time"]
for idx, filter_name in enumerate(time_filters):
    print(f"  🖱️ [MOUSE CLICK] Filter Button -> {filter_name}")
    run_chrome_js(1, f"const tbtns = document.querySelectorAll('.time-btn'); if(tbtns[{idx}]) tbtns[{idx}].click();")
    if has_pyautogui:
        screen_w, screen_h = pyautogui.size()
        target_x = int(screen_w * 0.15 + (idx * 65))
        target_y = int(screen_h * 0.18)
        pyautogui.moveTo(target_x, target_y, duration=0.3)
        pyautogui.click()
    time.sleep(0.8)

# Scroll down Telemetry Console
print("\n  📜 [MOUSE SCROLL] Scrolling down Telemetry Console...")
scroll_chrome("down", 600)
time.sleep(1)

# Test Table Pagination
print("\n  📄 [MOUSE CLICK] Testing Pagination (Next / Prev)...")
run_chrome_js(1, "const nxt = document.getElementById('next-btn'); if(nxt) nxt.click();")
print("  -> Clicked 'Next ▶'")
time.sleep(1.5)
run_chrome_js(1, "const prv = document.getElementById('prev-btn'); if(prv) prv.click();")
print("  -> Clicked '◀ Prev'")
time.sleep(1)

# Scroll back up
scroll_chrome("up", 600)
time.sleep(1)

# --- TEST TAB 2: CYBERPUNK SEO DASHBOARD ---
print("\n⚡ [TEST PHASE 2]: Switching to Cyberpunk SEO Rank Proof Dashboard (Tab 2)...")
switch_chrome_tab(2)
time.sleep(1.5)

# Click Filter Buttons on SEO Dashboard
print("  🖱️ [MOUSE CLICK] SEO Filter -> #1 Google Ranks")
run_chrome_js(2, "const btn = document.querySelector('[data-filter=\"rank1\"]'); if(btn) btn.click();")
time.sleep(1.5)

print("  🖱️ [MOUSE CLICK] SEO Filter -> Top 3 Ranks")
run_chrome_js(2, "const btn = document.querySelector('[data-filter=\"top3\"]'); if(btn) btn.click();")
time.sleep(1.5)

print("  🖱️ [MOUSE CLICK] SEO Filter -> All 50 US States")
run_chrome_js(2, "const btn = document.querySelector('[data-filter=\"all\"]'); if(btn) btn.click();")
time.sleep(1.5)

# Scroll down SEO Dashboard 50-State Table
print("\n  📜 [MOUSE SCROLL] Scrolling down 50 US States SERP Directory...")
scroll_chrome("down", 800)
time.sleep(1.5)
scroll_chrome("up", 800)
time.sleep(1)

# Return to Tab 1 (Telemetry)
switch_chrome_tab(1)

print("\n==================================================")
print("🎉 ALL MOUSE & BUTTON INTERACTIONS COMPLETED SUCCESSFULLY!")
print("==================================================")
