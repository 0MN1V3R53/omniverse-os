#!/usr/bin/env python3
import sys
sys.path.append("scripts")
from get_page_content import run_js
import json
import time

def read_wizard_options():
    code = """
    (() => {
        // Dismiss ad blocker modal if present
        Array.from(document.querySelectorAll('button, [role="button"], a'))
            .filter(b => b.innerText && (b.innerText.includes('Dismiss') || b.innerText.includes('Got it') || b.innerText.includes('Close')))
            .forEach(b => b.click());
            
        return {
            title: document.title,
            textSample: document.body.innerText.substring(0, 2500),
            cards: Array.from(document.querySelectorAll('.card, [role="radio"], [role="button"], h2, h3, div.header'))
                .map(el => el.innerText ? el.innerText.trim() : '')
                .filter(t => t.length > 2 && t.length < 100)
                .slice(0, 15)
        };
    })()
    """
    return run_js(code)

if __name__ == "__main__":
    time.sleep(3)
    res = read_wizard_options()
    print(json.dumps(res, indent=2))
