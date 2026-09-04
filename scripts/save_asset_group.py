#!/usr/bin/env python3
import subprocess
import time
import json

def click_save():
    js_code = """
    (() => {
        const btns = Array.from(document.querySelectorAll('button, [role="button"], div, span'));
        const saveBtn = btns.find(b => b.innerText && b.innerText.trim() === 'Save');
        if (saveBtn) {
            saveBtn.click();
            return 'CLICKED_SAVE_BUTTON';
        }
        return 'SAVE_NOT_FOUND';
    })()
    """
    js_escaped = js_code.replace('"', '\\"').replace('\n', ' ')
    script = f'''tell application "Google Chrome"
    repeat with w in windows
        repeat with t in tabs of w
            if URL of t contains "ads.google.com" then
                return (execute t javascript "{js_escaped}")
            end if
        end repeat
    end repeat
end tell'''
    res = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    return res.stdout.strip()

if __name__ == "__main__":
    print("Action:", click_save())
    time.sleep(4)
    script_check = '''tell application "Google Chrome"
    repeat with w in windows
        repeat with t in tabs of w
            if URL of t contains "ads.google.com" then
                return (execute t javascript "window.location.href")
            end if
        end repeat
    end repeat
end tell'''
    res_check = subprocess.run(["osascript", "-e", script_check], capture_output=True, text=True)
    print("Current URL:", res_check.stdout.strip())
