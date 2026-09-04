#!/usr/bin/env python3
import sys
sys.path.append("scripts")
from get_page_content import run_js
import json
import time

def click_add_url():
    code = """
    (() => {
        const btns = Array.from(document.querySelectorAll('button, [role="button"], a, span, div'));
        const addUrlBtn = btns.find(b => b.innerText && b.innerText.trim() === 'Add URL');
        if (addUrlBtn) {
            addUrlBtn.click();
            return 'CLICKED_ADD_URL';
        }
        return 'ADD_URL_NOT_FOUND';
    })()
    """
    res = run_js(code)
    time.sleep(3)
    code_read = """
    (() => {
        return {
            title: document.title,
            inputs: Array.from(document.querySelectorAll('input')).map(i => ({ type: i.type, placeholder: i.placeholder, value: i.value })),
            textSample: document.body.innerText.substring(0, 1500)
        };
    })()
    """
    return {"click": res, "after": run_js(code_read)}

if __name__ == "__main__":
    print(json.dumps(click_add_url(), indent=2))
