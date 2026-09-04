#!/usr/bin/env python3
import sys
sys.path.append("scripts")
from get_page_content import run_js
import json
import time
import subprocess

def audit_campaign_settings():
    # Navigate to Campaign Settings
    nav_script = '''tell application "Google Chrome"
    repeat with w in windows
        repeat with t in tabs of w
            if URL of t contains "ads.google.com" then
                set URL of t to "https://ads.google.com/aw/campaigns/settings?campaignId=24189549598&ocid=8481561824&euid=6603286473&__u=3390480577&uscid=8481561824&__c=1290308576&authuser=0"
                return "NAVIGATED_TO_SETTINGS"
            end if
        end repeat
    end repeat
end tell'''
    subprocess.run(["osascript", "-e", nav_script], capture_output=True, text=True)
    time.sleep(5)
    
    code = """
    (() => {
        return {
            title: document.title,
            url: window.location.href,
            textSample: document.body.innerText.substring(0, 3000)
        };
    })()
    """
    return run_js(code)

if __name__ == "__main__":
    res = audit_campaign_settings()
    print(json.dumps(res, indent=2))
