#!/usr/bin/env python3
import sys
sys.path.append("scripts")
from get_page_content import run_js
import json
import time

def check_misconfigured():
    code = """
    (() => {
        const el = Array.from(document.querySelectorAll('span, div, a')).find(e => e.innerText && e.innerText.trim() === 'Misconfigured');
        if (el) {
            el.click();
            return {
                clicked: true,
                title: el.getAttribute('title') || el.getAttribute('aria-label') || el.parentElement.innerText
            };
        }
        return { clicked: false };
    })()
    """
    res = run_js(code)
    time.sleep(2)
    code_read = """
    (() => {
        return {
            bodyText: document.body.innerText.substring(0, 2000)
        };
    })()
    """
    return {"status": res, "after": run_js(code_read)}

if __name__ == "__main__":
    print(json.dumps(check_misconfigured(), indent=2))
