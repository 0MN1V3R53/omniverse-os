#!/usr/bin/env python3
import subprocess
import json

def inspect_asset_group_table():
    js_code = """
    (() => {
        const rows = Array.from(document.querySelectorAll('tr, [role="row"]'))
            .map(r => r.innerText.trim())
            .filter(t => t.includes('Asset Group 1') || t.includes('Campaign #1') || t.includes('Ad Strength'));
        
        return JSON.stringify({
            rowCount: rows.length,
            rows: rows
        });
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
    try:
        return json.loads(res.stdout.strip())
    except Exception:
        return {"raw": res.stdout.strip()}

if __name__ == "__main__":
    print(json.dumps(inspect_asset_group_table(), indent=2))
