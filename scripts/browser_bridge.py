#!/usr/bin/env python3
import subprocess
import json
import sys

def execute_js_in_tab(tab_url_match, js_code):
    script = f'''
    tell application "Google Chrome"
        repeat with w in windows
            repeat with t in tabs of w
                if URL of t contains "{tab_url_match}" then
                    return (execute t javascript "{js_code}")
                end if
            end repeat
        end repeat
        return "ERROR: Tab not found"
    end tell
    '''
    res = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    if res.returncode != 0:
        return {"error": res.stderr.strip()}
    return {"output": res.stdout.strip()}

def get_open_tabs():
    script = '''
    tell application "Google Chrome"
        set tabListInfo to ""
        repeat with w in windows
            repeat with t in tabs of w
                set tabListInfo to tabListInfo & (get title of t) & " <|||> " & (get URL of t) & "\\n"
            end repeat
        end repeat
        return tabListInfo
    end tell
    '''
    res = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    lines = res.stdout.strip().split("\n")
    tabs = []
    for l in lines:
        if "<|||>" in l:
            title, url = l.split("<|||>", 1)
            tabs.append({"title": title.strip(), "url": url.strip()})
    return tabs

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "tabs":
        print(json.dumps(get_open_tabs(), indent=2))
    elif len(sys.argv) > 2 and sys.argv[1] == "exec":
        print(json.dumps(execute_js_in_tab(sys.argv[2], sys.argv[3]), indent=2))
    else:
        print("Usage: python3 browser_bridge.py [tabs | exec <match> <js_code>]")
