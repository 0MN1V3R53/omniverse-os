#!/usr/bin/env python3
import subprocess
import json

def get_ads_summary():
    js_code = "JSON.stringify({title: document.title, url: window.location.href, text: document.body.innerText.substring(0, 1500)});"
    script = f'''tell application "Google Chrome"
    repeat with w in windows
        repeat with t in tabs of w
            if URL of t contains "ads.google.com" then
                return (execute t javascript "{js_code}")
            end if
        end repeat
    end repeat
end tell'''
    
    res = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    if res.returncode == 0 and res.stdout.strip():
        try:
            return json.loads(res.stdout.strip())
        except Exception:
            return {"raw": res.stdout.strip()}
    return {"error": res.stderr.strip()}

if __name__ == "__main__":
    data = get_ads_summary()
    print(json.dumps(data, indent=2))
