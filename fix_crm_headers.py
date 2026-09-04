#!/usr/bin/env python3
import subprocess
import time

url = "https://docs.google.com/spreadsheets/d/1wKV8oJCdYzz9C6fuRH78diTPrNoSsip7QOFqUkjCaq4/edit?pli=1&gid=0#gid=0"

headers = [
    "Quote ID", "Received At", "Full Name", "Email", "Phone", 
    "Origin", "Destination", "Miles", "Vehicle", "Type", 
    "Condition", "Transport", "Date", "Price", "Range", "ETA",
    "Lead Stage", "Call Status", "Answer Status", "Availability", "Next Follow-Up", "Notes"
]

print("Activating Chrome...")
applescript_focus = f'''
tell application "Google Chrome"
    activate
    open location "{url}"
end tell
'''
subprocess.run(["osascript", "-e", applescript_focus])
time.sleep(4)

print("Clearing row 1...")
as_clear = '''
tell application "System Events"
    key code 126 using {command down}
    delay 0.5
    key code 123 using {command down}
    delay 0.5
    key code 49 using {shift down}
    delay 0.5
    key code 51
    delay 0.5
    key code 123 using {command down}
    delay 0.5
end tell
'''
subprocess.run(["osascript", "-e", as_clear])

print("Typing headers properly with robust delays...")
for h in headers:
    safe_val = h.replace('"', '\\"')
    script = f'''
    set the clipboard to "{safe_val}"
    tell application "System Events"
        keystroke "v" using command down
        delay 0.4
        keystroke tab
        delay 0.4
    end tell
    '''
    subprocess.run(["osascript", "-e", script])

print("Bolding headers...")
as_bold = '''
tell application "System Events"
    key code 123 using {command down}
    delay 0.5
    key code 49 using {shift down}
    delay 0.5
    keystroke "b" using {command down}
    delay 0.5
end tell
'''
subprocess.run(["osascript", "-e", as_bold])

print("Freezing row 1...")
as_freeze = '''
tell application "System Events"
    key code 44 using {option down}
    delay 1.5
    keystroke "Freeze 1 row"
    delay 1
    key code 36
    delay 1
end tell
'''
subprocess.run(["osascript", "-e", as_freeze])

print("Adding message to row 2...")
as_msg_nav = '''
tell application "System Events"
    key code 125
    delay 0.5
    key code 123 using {command down}
    delay 0.5
end tell
'''
subprocess.run(["osascript", "-e", as_msg_nav])

msg = "⚠️ Python Bot: Headers fixed! To instantly add the CRM colored dropdown menus and perfect column widths, click Extensions -> Apps Script, paste the macro code I provided, and hit Run!"
script = f'''
set the clipboard to "{msg}"
tell application "System Events"
    keystroke "v" using command down
    delay 0.5
    key code 36
end tell
'''
subprocess.run(["osascript", "-e", script])

print("Fix completed.")
