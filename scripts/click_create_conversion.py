#!/usr/bin/env python3
import sys
sys.path.append("scripts")
from get_page_content import run_js
import json
import time

def click_create_conversion():
    code = """
    (() => {
        const btns = Array.from(document.querySelectorAll('button, [role="button"], a, div, span'));
        const btn = btns.find(b => b.innerText && b.innerText.trim().includes('Create conversion action'));
        if (btn) {
            btn.click();
            return 'CLICKED_CREATE_CONVERSION_ACTION';
        }
        return 'BTN_NOT_FOUND';
    })()
    """
    res = run_js(code)
    time.sleep(4)
    code_read = """
    (() => {
        return {
            title: document.title,
            url: window.location.href,
            textSample: document.body.innerText.substring(0, 2000)
        };
    })()
    """
    return {"click": res, "page": run_js(code_read)}

if __name__ == "__main__":
    print(json.dumps(click_create_conversion(), indent=2))
