#!/usr/bin/env python3
import subprocess
import time

def dismiss_overlay():
    script = '''tell application "Google Chrome"
    repeat with w in windows
        repeat with t in tabs of w
            if URL of t contains "ads.google.com" then
                execute t javascript "Array.from(document.querySelectorAll(\"button, [role=\\\"button\\\"], a\")).filter(b => b.innerText && (b.innerText.includes(\"Dismiss\") || b.innerText.includes(\"Got it\") || b.innerText.includes(\"Close\") || b.innerText.includes(\"OK\"))).forEach(b => b.click());"
                return "OVERLAY_DISMISSED"
            end if
        end repeat
    end repeat
end tell'''
    res = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    return res.stdout.strip()

if __name__ == "__main__":
    print(dismiss_overlay())
