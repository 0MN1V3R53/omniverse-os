#!/usr/bin/env python3
import subprocess
import json
import base64

def run_js(js_code):
    b64_code = base64.b64encode(js_code.encode("utf-8")).decode("utf-8")
    script = f'''
    tell application "Google Chrome"
        repeat with w in windows
            repeat with t in tabs of w
                if URL of t contains "ads.google.com" then
                    set jsToRun to "btoa(unescape(encodeURIComponent((function(){{ return JSON.stringify(eval(decodeURIComponent(escape(atob('{b64_code}'))))) }})())))"
                    return (execute t javascript jsToRun)
                end if
            end repeat
        end repeat
    end tell
    '''
    res = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    if res.returncode == 0 and res.stdout.strip():
        try:
            raw_out = res.stdout.strip()
            decoded = base64.b64decode(raw_out).decode("utf-8")
            return json.loads(decoded)
        except Exception as e:
            return {"raw": res.stdout.strip(), "error": str(e)}
    return {"error": res.stderr.strip()}

if __name__ == "__main__":
    test_code = """
    (() => {
        return {
            title: document.title,
            url: window.location.href,
            textLength: document.body.innerText.length,
            textSample: document.body.innerText.substring(0, 3000)
        };
    })()
    """
    res = run_js(test_code)
    print(json.dumps(res, indent=2))
