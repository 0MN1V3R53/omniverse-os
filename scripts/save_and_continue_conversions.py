#!/usr/bin/env python3
import sys
sys.path.append("scripts")
from get_page_content import run_js
import json
import time

def save_and_continue_conversions():
    code = """
    (() => {
        const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
        const saveBtn = btns.find(b => b.innerText && b.innerText.trim() === 'Save and continue');
        if (saveBtn) {
            saveBtn.click();
            return 'CLICKED_SAVE_AND_CONTINUE';
        }
        return 'SAVE_NOT_FOUND';
    })()
    """
    res = run_js(code)
    time.sleep(5)
    
    code_read = """
    (() => {
        return {
            title: document.title,
            url: window.location.href,
            textSample: document.body.innerText.substring(0, 3000)
        };
    })()
    """
    return {"save": res, "after": run_js(code_read)}

if __name__ == "__main__":
    print(json.dumps(save_and_continue_conversions(), indent=2))
