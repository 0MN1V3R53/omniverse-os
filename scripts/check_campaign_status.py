#!/usr/bin/env python3
import subprocess
import time
import json

def check_campaign_status():
    script_nav = '''tell application "Google Chrome"
    repeat with w in windows
        repeat with t in tabs of w
            if URL of t contains "ads.google.com" then
                set URL of t to "https://ads.google.com/aw/campaigns?ocid=8481561824&euid=6603286473&__u=3390480577&uscid=8481561824&__c=1290308576&authuser=0"
                return "NAVIGATED_TO_CAMPAIGNS"
            end if
        end repeat
    end repeat
end tell'''
    res_nav = subprocess.run(["osascript", "-e", script_nav], capture_output=True, text=True)
    time.sleep(4)
    
    script_read = '''tell application "Google Chrome"
    repeat with w in windows
        repeat with t in tabs of w
            if URL of t contains "ads.google.com" then
                return (execute t javascript "document.body.innerText.substring(0, 2500)")
            end if
        end repeat
    end repeat
end tell'''
    res_read = subprocess.run(["osascript", "-e", script_read], capture_output=True, text=True)
    return res_read.stdout.strip()

if __name__ == "__main__":
    print(check_campaign_status())
