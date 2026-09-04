#!/usr/bin/env python3
import sys
sys.path.append("scripts")
from get_page_content import run_js
import json
import time

def enter_url_and_scan():
    code = """
    (() => {
        // Find URL input
        const inputs = Array.from(document.querySelectorAll('input[type="text"], input[type="url"], input:not([type="checkbox"])'));
        let filled = false;
        for (const input of inputs) {
            input.value = 'https://www.skyautoservices.com/';
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
            filled = true;
        }
        
        // Find Scan / Add URL button
        const btns = Array.from(document.querySelectorAll('button, [role="button"], a, span'));
        const scanBtn = btns.find(b => b.innerText && (b.innerText.trim() === 'Scan' || b.innerText.trim() === 'Add URL' || b.innerText.trim() === 'Add' || b.innerText.trim() === 'Apply'));
        if (scanBtn) {
            scanBtn.click();
            return { filled, scanClicked: scanBtn.innerText.trim() };
        }
        return { filled, scanClicked: 'NOT_FOUND' };
    })()
    """
    res = run_js(code)
    time.sleep(5)
    
    # Click Save and continue if enabled
    code_save = """
    (() => {
        const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
        const saveBtn = btns.find(b => b.innerText && b.innerText.trim() === 'Save and continue');
        if (saveBtn && !saveBtn.disabled) {
            saveBtn.click();
            return 'CLICKED_SAVE_AND_CONTINUE';
        }
        return saveBtn ? ('DISABLED: ' + saveBtn.innerText) : 'SAVE_NOT_FOUND';
    })()
    """
    res_save = run_js(code_save)
    time.sleep(5)
    
    code_read = """
    (() => {
        return {
            title: document.title,
            url: window.location.href,
            textSample: document.body.innerText.substring(0, 2500)
        };
    })()
    """
    return {"step1": res, "save": res_save, "page": run_js(code_read)}

if __name__ == "__main__":
    print(json.dumps(enter_url_and_scan(), indent=2))
