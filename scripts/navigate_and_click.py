#!/usr/bin/env python3
import subprocess
import time
import json
import sys
sys.path.append("scripts")
from get_page_content import run_js

def navigate_and_click(url, click_text=None):
    script_nav = f'''tell application "Google Chrome"
    repeat with w in windows
        repeat with t in tabs of w
            if URL of t contains "ads.google.com" then
                set URL of t to "{url}"
                return "NAVIGATED"
            end if
        end repeat
    end repeat
end tell'''
    subprocess.run(["osascript", "-e", script_nav], capture_output=True, text=True)
    time.sleep(5)
    
    if click_text:
        code_click = f"""
        (() => {{
            const els = Array.from(document.querySelectorAll('a, button, [role="button"], [role="menuitem"], [role="treeitem"], div, span'));
            for (const el of els) {{
                if (el.innerText && el.innerText.trim() === '{click_text}') {{
                    el.click();
                    return 'CLICKED_' + '{click_text}';
                }}
            }}
            return 'NOT_FOUND';
        }})()
        """
        run_js(code_click)
        time.sleep(3)
        
    code_read = """
    (() => {
        return {
            title: document.title,
            url: window.location.href,
            textSample: document.body.innerText.substring(0, 3000)
        };
    })()
    """
    return run_js(code_read)

if __name__ == "__main__":
    res = navigate_and_click(
        "https://ads.google.com/aw/campaigns?ocid=8481561824&euid=6603286473&__u=3390480577&uscid=8481561824&__c=1290308576&authuser=0"
    )
    print(json.dumps(res, indent=2))
