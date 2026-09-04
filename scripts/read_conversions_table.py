#!/usr/bin/env python3
import sys
sys.path.append("scripts")
from get_page_content import run_js
import json
import time

def read_conversions_table():
    code = """
    (() => {
        // Dismiss any ad blocker modal
        Array.from(document.querySelectorAll('button, [role="button"], a'))
            .filter(b => b.innerText && (b.innerText.includes('Dismiss') || b.innerText.includes('Got it') || b.innerText.includes('Close')))
            .forEach(b => b.click());
            
        const rows = Array.from(document.querySelectorAll('tr, [role="row"], .conversion-action-row, .conversion-action-name'))
            .map(el => el.innerText.trim())
            .filter(t => t.length > 2);
            
        return {
            title: document.title,
            rows: rows.slice(0, 20),
            fullText: document.body.innerText.substring(0, 2000)
        };
    })()
    """
    return run_js(code)

if __name__ == "__main__":
    time.sleep(3)
    res = read_conversions_table()
    print(json.dumps(res, indent=2))
