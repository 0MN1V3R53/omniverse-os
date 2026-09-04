#!/usr/bin/env python3
import subprocess
import time
import json

def check_banner():
    js_code = """
    (() => {
        const text = document.body.innerText;
        return {
            hasTermsAlert: text.includes('New Call and Messaging Ads Terms'),
            alertSnippet: text.substring(0, 1000)
        };
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
    print(check_banner())
