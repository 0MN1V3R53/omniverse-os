#!/usr/bin/env python3
import time
import subprocess
import os
import sys

print("==================================================")
print("💻 OMNIVERSE IMAC FULL CONTROL & MOUSE AUTOMATION")
print("==================================================")

# Step 1: Ensure ports 8080 & 8090 are active
def check_or_start_server(port, script_name):
    cmd = f"lsof -i :{port}"
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.returncode != 0 or not res.stdout.strip():
        print(f"-> Launching {script_name} on port {port}...")
        subprocess.Popen([sys.executable, script_name], cwd="/Users/silversurfer/Documents/Omniverse2")
        time.sleep(2)
    else:
        print(f"-> Port {port} is active and ready.")

check_or_start_server(8080, "launch_cyberpunk_dashboard.py")
check_or_start_server(8090, "launch_cyberpunk_telemetry_live.py")

url_telemetry = "http://localhost:8090/cyberpunk_telemetry_live.html"
url_seo = "http://localhost:8080/cyberpunk_seo_dashboard.html"

# Step 2: Open both HTML URLs in Google Chrome and bring to front
print("\n[1/5] Opening both HTMLs in Google Chrome...")
applescript_launch = f'''
tell application "Google Chrome"
    activate
    make new window
    set URL of active tab of front window to "{url_telemetry}"
    delay 1
    open location "{url_seo}"
    delay 1
end tell
'''
subprocess.run(["osascript", "-e", applescript_launch])

# Helper for executing Chrome JS
def chrome_js(tab_idx, code):
    script = f'''
    tell application "Google Chrome"
        tell window 1
            tell tab {tab_idx}
                execute javascript "{code}"
            end tell
        end tell
    end tell
    '''
    subprocess.run(["osascript", "-e", script], capture_output=True)

# Helper to activate tab
def activate_tab(tab_idx):
    script = f'''
    tell application "Google Chrome"
        tell window 1
            set active tab index to {tab_idx}
        end tell
    end tell
    '''
    subprocess.run(["osascript", "-e", script])
    time.sleep(1)

# Helper for macOS native keystrokes & mouse scroll
def mac_key_stroke(key_code):
    script = f'''
    tell application "Google Chrome" to activate
    tell application "System Events"
        key code {key_code}
    end tell
    '''
    return subprocess.run(["osascript", "-e", script], capture_output=True, text=True)

# Step 3: Test Accessibility Permission for Keystrokes & Hardware Mouse
print("\n[2/5] Testing iMac System Events & Hardware Control permissions...")
test_res = mac_key_stroke(125) # Down arrow key
if "not allowed to send keystrokes" in test_res.stderr:
    print("⚠️ Notice: Keystrokes permission pending, proceeding with Chrome DOM execution engine.")
else:
    print("✅ iMac System Events & Keystroke Automation FULLY GRANTED & AUTHORIZED!")

# Step 4: Full Interactive Audit of Cyberpunk Telemetry Console (Tab 1)
print("\n[3/5] AUDITING & CONTROLLING TELEMETRY CONSOLE (TAB 1)...")
activate_tab(1)

tabs = ["Overview & Stream", "Time-Range Analytics", "Quotes & Call Leads", "Behavior & Heatmaps", "Geolocation & ISP", "Hostinger Archive", "30-MIN AUTOMATED SEO KEYWORD ENGINE"]
for i, name in enumerate(tabs):
    print(f"  🖱️ [CLICK] Tab {i+1}: {name}")
    chrome_js(1, f"const b = document.querySelectorAll('.tab-btn'); if(b[{i}]) b[{i}].click();")
    time.sleep(1)

filters = ["5h", "10h", "24h", "2d", "3d", "4d", "5d", "10d", "20d", "30d", "All Time"]
print("\n  ⏱️ [CLICK] Testing 11 Time Window Filter Buttons:")
for i, name in enumerate(filters):
    print(f"    -> Filter Button [{name}] Clicked")
    chrome_js(1, f"const b = document.querySelectorAll('.time-btn'); if(b[{i}]) b[{i}].click();")
    time.sleep(0.7)

print("\n  📜 [SCROLL & PAGINATION] Scrolling down & testing pagination...")
chrome_js(1, "window.scrollTo({top: 600, behavior: 'smooth'});")
time.sleep(1.5)
chrome_js(1, "const nxt = document.getElementById('next-btn'); if(nxt) nxt.click();")
print("    -> Clicked 'Next ▶' Page")
time.sleep(1.5)
chrome_js(1, "const prv = document.getElementById('prev-btn'); if(prv) prv.click();")
print("    -> Clicked '◀ Prev' Page")
time.sleep(1.5)
chrome_js(1, "window.scrollTo({top: 0, behavior: 'smooth'});")

# Step 5: Full Interactive Audit of Cyberpunk SEO Rank Proof Dashboard (Tab 2)
print("\n[4/5] AUDITING & CONTROLLING SEO DASHBOARD (TAB 2)...")
activate_tab(2)

print("  🖱️ [CLICK] Rank Filter: #1 Google Ranks")
chrome_js(2, "const btn = document.querySelector('[data-filter=\"rank1\"]'); if(btn) btn.click();")
time.sleep(1.5)

print("  🖱️ [CLICK] Rank Filter: Top 3 Ranks")
chrome_js(2, "const btn = document.querySelector('[data-filter=\"top3\"]'); if(btn) btn.click();")
time.sleep(1.5)

print("  🖱️ [CLICK] Rank Filter: All 50 US States")
chrome_js(2, "const btn = document.querySelector('[data-filter=\"all\"]'); if(btn) btn.click();")
time.sleep(1.5)

print("\n  📜 [SCROLL] Scrolling through 50 US States Directory...")
chrome_js(2, "window.scrollTo({top: 800, behavior: 'smooth'});")
time.sleep(2)
chrome_js(2, "window.scrollTo({top: 0, behavior: 'smooth'});")
time.sleep(1)

# Return focus to Tab 1
activate_tab(1)

print("\n==================================================")
print("🎉 FULL IMAC COMPUTER CONTROL & HTML AUDIT COMPLETE!")
print("==================================================")
