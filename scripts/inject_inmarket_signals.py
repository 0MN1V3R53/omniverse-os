#!/usr/bin/env python3
import sys
sys.path.append("scripts")
from get_page_content import run_js
import json
import time

def expand_additional_signals():
    code = """
    (() => {
        // Dismiss ad blocker modal
        Array.from(document.querySelectorAll('button, [role="button"], a'))
            .filter(b => b.innerText && (b.innerText.includes('Dismiss') || b.innerText.includes('Got it') || b.innerText.includes('Close')))
            .forEach(b => b.click());

        const btns = Array.from(document.querySelectorAll('div, span, button, [role="button"]'));
        const addSignals = btns.find(b => b.innerText && b.innerText.trim().includes('Additional signals'));
        if (addSignals) {
            addSignals.click();
            return { clicked: 'Additional signals' };
        }
        return { clicked: 'NOT_FOUND' };
    })()
    """
    res = run_js(code)
    time.sleep(3)
    
    code_read = """
    (() => {
        return {
            title: document.title,
            inputs: Array.from(document.querySelectorAll('input')).map(i => ({ placeholder: i.placeholder, value: i.value })),
            textSample: document.body.innerText.substring(0, 2000)
        };
    })()
    """
    return {"step1": res, "after": run_js(code_read)}

if __name__ == "__main__":
    print(json.dumps(expand_additional_signals(), indent=2))
