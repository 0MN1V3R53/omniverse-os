#!/usr/bin/env python3
import subprocess
import json
import time

def click_element_by_text(text):
    js_code = f"""
    (() => {{
        const elements = Array.from(document.querySelectorAll('a, button, [role="button"], [role="treeitem"], [role="menuitem"], div, span'));
        for (const el of elements) {{
            if (el.innerText && el.innerText.trim() === '{text}') {{
                el.click();
                return 'CLICKED: ' + el.innerText.trim();
            }}
        }}
        return 'NOT_FOUND';
    }})()
    """
    # Escape for AppleScript
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
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "Asset groups"
    print("Action:", click_element_by_text(target))
    time.sleep(3)
    # Check new URL & title
    script2 = '''tell application "Google Chrome"
    repeat with w in windows
        repeat with t in tabs of w
            if URL of t contains "ads.google.com" then
                return (execute t javascript "JSON.stringify({url: window.location.href, text: document.body.innerText.substring(0, 1500)})")
            end if
        end repeat
    end repeat
end tell'''
    res2 = subprocess.run(["osascript", "-e", script2], capture_output=True, text=True)
    try:
        print(json.dumps(json.loads(res2.stdout.strip()), indent=2))
    except Exception:
        print(res2.stdout.strip())
