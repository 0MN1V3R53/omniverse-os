#!/usr/bin/env python3
import sys
sys.path.append("scripts")
from get_page_content import run_js
import json
import time

def save_signals():
    code = """
    (() => {
        const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
        const saveBtn = btns.find(b => b.innerText && b.innerText.trim() === 'Save');
        if (saveBtn) {
            saveBtn.click();
            return 'CLICKED_SAVE';
        }
        return 'SAVE_NOT_FOUND';
    })()
    """
    res = run_js(code)
    time.sleep(3)
    return {"status": res}

if __name__ == "__main__":
    print(json.dumps(save_signals(), indent=2))
