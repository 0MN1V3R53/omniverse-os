#!/usr/bin/env python3
import subprocess
import json
import time

def click_edit_asset_group():
    js_code = """
    (() => {
        const links = Array.from(document.querySelectorAll('a, button, [role="button"], span, div'));
        for (const el of links) {
            if (el.innerText && el.innerText.trim() === 'Edit asset group') {
                el.click();
                return 'CLICKED_EDIT_ASSET_GROUP';
            }
        }
        return 'NOT_FOUND';
    })()
    """
    js_escaped = js_code.replace('"', '\\"')
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
    print("Result:", click_edit_asset_group())
    time.sleep(5)
    script2 = '''tell application "Google Chrome"
    repeat with w in windows
        repeat with t in tabs of w
            if URL of t contains "ads.google.com" then
                return (execute t javascript "JSON.stringify({url: window.location.href, text: document.body.innerText.substring(0, 2000)})")
            end if
        end repeat
    end repeat
end tell'''
    res2 = subprocess.run(["osascript", "-e", script2], capture_output=True, text=True)
    try:
        print(json.dumps(json.loads(res2.stdout.strip()), indent=2))
    except Exception:
        print(res2.stdout.strip())
