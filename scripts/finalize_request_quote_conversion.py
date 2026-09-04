#!/usr/bin/env python3
import sys
sys.path.append("scripts")
from get_page_content import run_js
import json
import time

def finalize_quote_conversion():
    code = """
    (() => {
        const btns = Array.from(document.querySelectorAll('button, [role="button"], a, span'));
        const createBtn = btns.find(b => b.innerText && b.innerText.trim().includes('Create conversion'));
        if (createBtn) {
            createBtn.click();
            return { clicked: 'Create conversion' };
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
            inputs: Array.from(document.querySelectorAll('input, select')).map(i => ({ type: i.type, name: i.name, placeholder: i.placeholder, value: i.value })),
            textSample: document.body.innerText.substring(0, 2000)
        };
    })()
    """
    return {"step1": res, "page": run_js(code_read)}

if __name__ == "__main__":
    print(json.dumps(finalize_quote_conversion(), indent=2))
