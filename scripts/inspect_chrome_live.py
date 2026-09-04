#!/usr/bin/env python3
import subprocess
import json
import time

def inspect_all():
    # AppleScript to activate Google Chrome and extract info from all relevant tabs
    applescript_code = '''
tell application "Google Chrome"
    activate
    set output to ""
    repeat with w in windows
        repeat with t in tabs of w
            set tabUrl to (get URL of t)
            set tabTitle to (get title of t)
            
            if tabUrl contains "ads.google.com" then
                set jsAds to "document.title + ' [SPLIT] ' + window.location.href + ' [SPLIT] ' + document.body.innerText.substring(0, 3000)"
                set tabContent to (execute t javascript jsAds)
                set output to output & "### GOOGLE_ADS ###\\n" & tabContent & "\\n\\n"
            else if tabUrl contains "skyautoservices.com" and not (tabUrl contains "maintenance") then
                set jsWeb to "document.title + ' [SPLIT] ' + window.location.href + ' [SPLIT] ' + (typeof window.gtag) + ' [SPLIT] ' + (document.querySelector('h1') ? document.querySelector('h1').innerText : 'No H1') + ' [SPLIT] ' + (window.dataLayer ? window.dataLayer.length : 0)"
                set tabContent to (execute t javascript jsWeb)
                set output to output & "### WEBSITE ###\\n" & tabContent & "\\n\\n"
            else if tabUrl contains "search.google.com" then
                set jsGsc to "document.title + ' [SPLIT] ' + window.location.href"
                set tabContent to (execute t javascript jsGsc)
                set output to output & "### GSC ###\\n" & tabContent & "\\n\\n"
            end if
        end repeat
    end repeat
    return output
end tell
'''
    res = subprocess.run(["osascript", "-e", applescript_code], capture_output=True, text=True)
    if res.returncode != 0:
        return {"error": res.stderr.strip()}
    return {"raw_output": res.stdout.strip()}

if __name__ == "__main__":
    result = inspect_all()
    if "error" in result:
        print("ERROR:", result["error"])
    else:
        print(result["raw_output"])
