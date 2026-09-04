#!/usr/bin/env python3
import sys
sys.path.append("scripts")
from get_page_content import run_js
import json
import time
import subprocess

def test_live_site():
    # Navigate to live site in Chrome
    url = "https://www.skyautoservices.com"
    nav_script = f'''tell application "Google Chrome"
    repeat with w in windows
        repeat with t in tabs of w
            if URL of t contains "skyautoservices.com" or URL of t contains "about:blank" then
                set URL of t to "{url}"
                return "NAVIGATED"
            end if
        end repeat
    end repeat
    -- If no tab, open in first tab of first window
    tell first window
        set URL of active tab to "{url}"
        return "NAVIGATED_ACTIVE"
    end tell
end tell'''
    subprocess.run(["osascript", "-e", nav_script], capture_output=True, text=True)
    time.sleep(5)
    
    code = """
    (() => {
        // Test calculator inputs and buttons
        const originInput = document.querySelector('input[name="origin"]');
        const destInput = document.querySelector('input[name="destination"]');
        const nextBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Next Step'));
        
        let calcTest = {
            hasOriginInput: !!originInput,
            hasDestInput: !!destInput,
            hasNextBtn: !!nextBtn
        };
        
        if (originInput && destInput && nextBtn) {
            originInput.value = "Los Angeles, CA";
            originInput.dispatchEvent(new Event('input', { bubbles: true }));
            originInput.dispatchEvent(new Event('change', { bubbles: true }));
            
            destInput.value = "New York, NY";
            destInput.dispatchEvent(new Event('input', { bubbles: true }));
            destInput.dispatchEvent(new Event('change', { bubbles: true }));
            
            // Try clicking nextBtn
            nextBtn.click();
        }
        
        return {
            title: document.title,
            url: window.location.href,
            calcTest,
            htmlStateSample: document.querySelector('#quote-calculator-top') ? document.querySelector('#quote-calculator-top').innerText : 'NO_CALC_FOUND',
            mapSection: Array.from(document.querySelectorAll('section')).map(s => s.innerText.substring(0, 100))
        };
    })()
    """
    
    time.sleep(2)
    res = run_js(code)
    time.sleep(3)
    
    # Check if step 2 appeared
    code2 = """
    (() => {
        return {
            currentCalcText: document.querySelector('#quote-calculator-top') ? document.querySelector('#quote-calculator-top').innerText : null,
            buttons: Array.from(document.querySelectorAll('button')).map(b => b.innerText.trim()).filter(t => t.length > 0)
        };
    })()
    """
    return {"step1": res, "step2": run_js(code2)}

if __name__ == "__main__":
    print(json.dumps(test_live_site(), indent=2))
