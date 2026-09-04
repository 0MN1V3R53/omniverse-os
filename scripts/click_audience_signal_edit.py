#!/usr/bin/env python3
import sys
sys.path.append("scripts")
from get_page_content import run_js
import json
import time

def click_audience_pencil():
    code = """
    (() => {
        // Find row for Asset Group 1
        const rows = Array.from(document.querySelectorAll('tr, [role="row"]'));
        const targetRow = rows.find(r => r.innerText && r.innerText.includes('Asset Group 1'));
        if (targetRow) {
            const editBtn = targetRow.querySelector('button[aria-label*="Audience"], button[aria-label*="signal"], [role="button"], i.material-icons, .edit-button, span.edit');
            // Or find any element with text 'edit' inside targetRow
            const editEl = Array.from(targetRow.querySelectorAll('*')).find(el => el.innerText && el.innerText.trim() === 'edit');
            if (editEl) {
                editEl.click();
                return { status: 'CLICKED_AUDIENCE_EDIT', tag: editEl.tagName };
            }
        }
        return { status: 'NOT_FOUND' };
    })()
    """
    res = run_js(code)
    time.sleep(4)
    
    code_read = """
    (() => {
        return {
            title: document.title,
            modals: Array.from(document.querySelectorAll('mat-dialog-container, .drawer, .dialog, [role="dialog"], form')).map(m => m.innerText.substring(0, 1500)),
            textSample: document.body.innerText.substring(0, 2000)
        };
    })()
    """
    return {"click": res, "after": run_js(code_read)}

if __name__ == "__main__":
    print(json.dumps(click_audience_pencil(), indent=2))
