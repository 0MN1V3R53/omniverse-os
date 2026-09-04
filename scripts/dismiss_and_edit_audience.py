#!/usr/bin/env python3
import sys
sys.path.append("scripts")
from get_page_content import run_js
import json
import time

def dismiss_and_inspect():
    code = """
    (() => {
        // Dismiss ad blocker modal
        const closeBtns = Array.from(document.querySelectorAll('button, [role="button"], a, span, div.close-button, material-button'))
            .filter(b => b.innerText && (b.innerText.includes('Dismiss') || b.innerText.includes('Got it') || b.innerText.includes('Close') || b.innerText.includes('close')));
        closeBtns.forEach(b => b.click());
        
        return {
            closed: closeBtns.length
        };
    })()
    """
    res = run_js(code)
    time.sleep(2)
    
    code_read = """
    (() => {
        return {
            title: document.title,
            url: window.location.href,
            textSample: document.body.innerText.substring(0, 2000)
        };
    })()
    """
    return {"dismiss": res, "page": run_js(code_read)}

if __name__ == "__main__":
    print(json.dumps(dismiss_and_inspect(), indent=2))
