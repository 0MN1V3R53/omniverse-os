#!/usr/bin/env python3
import subprocess
import time

def click_fix_it():
    js_code = """
    (() => {
        const btns = Array.from(document.querySelectorAll('button, [role="button"], a, span, div'));
        const fixBtn = btns.find(b => b.innerText && b.innerText.trim() === 'Fix it');
        if (fixBtn) {
            fixBtn.click();
            return 'CLICKED_FIX_IT';
        }
        return 'FIX_IT_NOT_FOUND';
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
    print("Result:", click_fix_it())
    time.sleep(3)
    # Check dialog content
    script2 = '''tell application "Google Chrome"
    repeat with w in windows
        repeat with t in tabs of w
            if URL of t contains "ads.google.com" then
                return (execute t javascript "document.body.innerText.substring(0, 1500)")
            end if
        end repeat
    end repeat
end tell'''
    res2 = subprocess.run(["osascript", "-e", script2], capture_output=True, text=True)
    print("Screen after Fix it:", res2.stdout.strip())
