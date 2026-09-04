#!/usr/bin/env python3
import sys
sys.path.append("scripts")
from get_page_content import run_js
import json
import time

def select_request_quote():
    code = """
    (() => {
        const els = Array.from(document.querySelectorAll('div, span, [role="button"], mat-card, .category-card'));
        const reqQuote = els.find(e => e.innerText && e.innerText.trim() === 'Request quote');
        if (reqQuote) {
            reqQuote.click();
            return { clicked: 'Request quote' };
        }
        const submitLead = els.find(e => e.innerText && e.innerText.trim() === 'Submit lead form');
        if (submitLead) {
            submitLead.click();
            return { clicked: 'Submit lead form' };
        }
        return { clicked: 'NONE' };
    })()
    """
    res = run_js(code)
    time.sleep(2)
    
    code_save = """
    (() => {
        const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
        const saveBtn = btns.find(b => b.innerText && b.innerText.trim() === 'Save and continue');
        if (saveBtn) {
            saveBtn.click();
            return 'CLICKED_SAVE';
        }
        return 'SAVE_NOT_FOUND';
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
    print(json.dumps(select_request_quote(), indent=2))
