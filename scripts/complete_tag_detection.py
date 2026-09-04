#!/usr/bin/env python3
import sys
sys.path.append("scripts")
from get_page_content import run_js
import json
import time

def click_done_and_save():
    code = """
    (() => {
        const dialog = document.querySelector('mat-dialog-container') || document;
        const box = dialog.querySelector('input[type="checkbox"], [role="checkbox"], mat-checkbox, .mat-checkbox-inner-container');
        if (box) {
            box.click();
        }
        
        const btns = Array.from(dialog.querySelectorAll('button, [role="button"]'));
        const doneBtn = btns.find(b => b.innerText && b.innerText.trim() === 'Done');
        if (doneBtn) {
            doneBtn.click();
            return { boxClicked: !!box, doneClicked: true };
        }
        return { boxClicked: !!box, doneClicked: false };
    })()
    """
    res = run_js(code)
    time.sleep(3)
    
    code_save = """
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
    return {"step1": res, "save": res_save, "after": run_js(code_read)}

if __name__ == "__main__":
    print(json.dumps(click_done_and_save(), indent=2))
