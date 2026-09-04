#!/usr/bin/env python3
import sys
sys.path.append("scripts")
from get_page_content import run_js
import json
import time

def click_create_conversion_modal():
    code = """
    (() => {
        const btn = document.querySelector('button[aria-label*="Create conversion"], button.create-conversion-button, button.add-conversion-button') ||
                    Array.from(document.querySelectorAll('button, [role="button"]')).find(b => b.innerText && b.innerText.includes('Create conversion'));
        if (btn) {
            btn.click();
            return { clicked: true, text: btn.innerText.trim() };
        }
        return { clicked: false };
    })()
    """
    res = run_js(code)
    time.sleep(4)
    code_read = """
    (() => {
        return {
            title: document.title,
            modals: Array.from(document.querySelectorAll('mat-dialog-container, .dialog, .modal, form')).map(m => m.innerText.substring(0, 1500)),
            textSample: document.body.innerText.substring(0, 2000)
        };
    })()
    """
    return {"btn": res, "after": run_js(code_read)}

if __name__ == "__main__":
    print(json.dumps(click_create_conversion_modal(), indent=2))
