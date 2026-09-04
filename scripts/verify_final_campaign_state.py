#!/usr/bin/env python3
import subprocess
import time
import json
import sys
sys.path.append("scripts")
from get_page_content import run_js

def verify_all():
    nav_script = '''tell application "Google Chrome"
    repeat with w in windows
        repeat with t in tabs of w
            if URL of t contains "ads.google.com" then
                set URL of t to "https://ads.google.com/aw/campaigns?ocid=8481561824&euid=6603286473&__u=3390480577&uscid=8481561824&__c=1290308576&authuser=0"
                return "NAVIGATED_TO_CAMPAIGNS"
            end if
        end repeat
    end repeat
end tell'''
    subprocess.run(["osascript", "-e", nav_script], capture_output=True, text=True)
    time.sleep(5)
    
    code = """
    (() => {
        // Dismiss ad blocker modal if present
        Array.from(document.querySelectorAll('button, [role="button"], a'))
            .filter(b => b.innerText && (b.innerText.includes('Dismiss') || b.innerText.includes('Got it') || b.innerText.includes('Close')))
            .forEach(b => b.click());
            
        const text = document.body.innerText;
        return {
            title: document.title,
            url: window.location.href,
            campaignPresent: text.includes('Campaign #1'),
            budgetPresent: text.includes('$28.50/day'),
            statusEligible: text.includes('Eligible') || text.includes('Enabled'),
            sample: text.substring(0, 2000)
        };
    })()
    """
    return run_js(code)

if __name__ == "__main__":
    res = verify_all()
    print(json.dumps(res, indent=2))
