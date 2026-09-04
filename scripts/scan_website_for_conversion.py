#!/usr/bin/env python3
import sys
sys.path.append("scripts")
from get_page_content import run_js
import json
import time

def scan_website():
    code = """
    (() => {
        const urlInput = document.querySelector('input[type="url"], mat-dialog-container input');
        if (urlInput) {
            urlInput.value = 'https://www.skyautoservices.com/';
            urlInput.dispatchEvent(new Event('input', { bubbles: true }));
            urlInput.dispatchEvent(new Event('change', { bubbles: true }));
        }
        
        const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
        const scanBtn = btns.find(b => b.innerText && (b.innerText.trim() === 'Scan' || b.innerText.trim() === 'Save' || b.innerText.trim() === 'Add'));
        if (scanBtn) {
            scanBtn.click();
            return { status: 'CLICKED_SCAN', btn: scanBtn.innerText.trim() };
        }
        return { status: 'SCAN_BTN_NOT_FOUND', inputFound: !!urlInput };
    })()
    """
    res = run_js(code)
    time.sleep(6)
    
    code_read = """
    (() => {
        return {
            title: document.title,
            textSample: document.body.innerText.substring(0, 2500)
        };
    })()
    """
    return {"scan": res, "after": run_js(code_read)}

if __name__ == "__main__":
    print(json.dumps(scan_website(), indent=2))
