#!/usr/bin/env python3
import sys
sys.path.append("scripts")
from get_page_content import run_js
import json
import time
import subprocess

def open_audience_signals():
    # Navigate to Asset Group edit
    url = "https://ads.google.com/aw/assetgroup/edit?campaignId=24189549598&ocid=8481561824&assetgroupId=6743221821&returnTo=%2Faw%2Fassetgroup%3Focid%3D8481561824%26assetGroupTableMode%3Dtrue&euid=6603286473&__u=3390480577&uscid=8481561824&__c=1290308576&authuser=0"
    nav_script = f'''tell application "Google Chrome"
    repeat with w in windows
        repeat with t in tabs of w
            if URL of t contains "ads.google.com" then
                set URL of t to "{url}"
                return "NAVIGATED"
            end if
        end repeat
    end repeat
end tell'''
    subprocess.run(["osascript", "-e", nav_script], capture_output=True, text=True)
    time.sleep(5)
    
    # Dismiss any popups and find Audience signals edit button
    code = """
    (() => {
        // Dismiss ad blocker modal
        Array.from(document.querySelectorAll('button, [role="button"], a'))
            .filter(b => b.innerText && (b.innerText.includes('Dismiss') || b.innerText.includes('Got it') || b.innerText.includes('Close')))
            .forEach(b => b.click());
            
        const text = document.body.innerText;
        const editBtns = Array.from(document.querySelectorAll('button, [role="button"], a, span, div'))
            .filter(el => el.innerText && (el.innerText.trim() === 'edit' || el.innerText.trim() === 'Edit' || el.innerText.trim().includes('signal') || el.innerText.trim().includes('Audience')));
            
        return {
            title: document.title,
            hasAudienceSection: text.includes('Audiences') || text.includes('Audience signal'),
            textSnippet: text.substring(0, 2000)
        };
    })()
    """
    return run_js(code)

if __name__ == "__main__":
    res = open_audience_signals()
    print(json.dumps(res, indent=2))
