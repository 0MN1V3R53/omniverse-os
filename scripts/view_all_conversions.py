#!/usr/bin/env python3
import sys
sys.path.append("scripts")
from get_page_content import run_js
import json
import time

def view_all_conversions():
    code = """
    (() => {
        const links = Array.from(document.querySelectorAll('a, button, [role="button"], span'));
        const btn = links.find(el => el.innerText && el.innerText.trim() === 'View all conversion actions');
        if (btn) {
            btn.click();
            return 'CLICKED_VIEW_ALL';
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
            textSample: document.body.innerText.substring(0, 3000)
        };
    })()
    """
    return {"click": res, "page": run_js(code_read)}

if __name__ == "__main__":
    print(json.dumps(view_all_conversions(), indent=2))
