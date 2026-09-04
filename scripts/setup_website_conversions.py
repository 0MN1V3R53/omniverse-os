#!/usr/bin/env python3
import sys
sys.path.append("scripts")
from get_page_content import run_js
import json
import time

def setup_website_conversions():
    code = """
    (() => {
        // Dismiss ad blocker modal
        Array.from(document.querySelectorAll('button, [role="button"], a'))
            .filter(b => b.innerText && (b.innerText.includes('Dismiss') || b.innerText.includes('Got it') || b.innerText.includes('Close') || b.innerText.includes('Show me later')))
            .forEach(b => b.click());

        // Find checkboxes for "Conversions on a website" and "Calls from website visits"
        const elements = Array.from(document.querySelectorAll('div, span, label, [role="checkbox"]'));
        const results = [];
        
        for (const el of elements) {
            const txt = el.innerText || '';
            if (txt.includes('Conversions on a website') && el.tagName === 'DIV' && el.querySelector('input, [role="checkbox"], mat-checkbox')) {
                const box = el.querySelector('input, [role="checkbox"], mat-checkbox, .mat-checkbox-inner-container');
                if (box) {
                    box.click();
                    results.push('CLICKED_WEBSITE_CHECKBOX');
                }
            }
            if (txt.includes('Calls from website visits') && el.tagName === 'DIV' && el.querySelector('input, [role="checkbox"], mat-checkbox')) {
                const box = el.querySelector('input, [role="checkbox"], mat-checkbox, .mat-checkbox-inner-container');
                if (box) {
                    box.click();
                    results.push('CLICKED_CALLS_WEBSITE_CHECKBOX');
                }
            }
        }
        
        // Also click on the parent card if not clicked
        const cards = Array.from(document.querySelectorAll('.card, [role="button"], mat-card, .data-source-card, div'));
        for (const c of cards) {
            if (c.innerText && c.innerText.includes('Conversions on a website') && c.innerText.length < 300) {
                c.click();
                results.push('CLICKED_WEBSITE_CARD');
                break;
            }
        }
        
        return results;
    })()
    """
    res = run_js(code)
    time.sleep(3)
    
    # Click Save and continue
    code_save = """
    (() => {
        const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
        const saveBtn = btns.find(b => b.innerText && b.innerText.trim() === 'Save and continue');
        if (saveBtn) {
            saveBtn.click();
            return 'CLICKED_SAVE_AND_CONTINUE';
        }
        return 'SAVE_BTN_NOT_FOUND';
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
    return {"checkboxes": res, "save": res_save, "nextPage": run_js(code_read)}

if __name__ == "__main__":
    print(json.dumps(setup_website_conversions(), indent=2))
