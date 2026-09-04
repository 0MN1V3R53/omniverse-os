#!/usr/bin/env python3
import sys
sys.path.append("scripts")
from get_page_content import run_js
import json
import time

def select_lead_category():
    code = """
    (() => {
        const btns = Array.from(document.querySelectorAll('button, [role="button"], a, span'));
        const seeAll = btns.find(b => b.innerText && b.innerText.trim() === 'See all');
        if (seeAll) {
            seeAll.click();
        }
        return { seeAllClicked: !!seeAll };
    })()
    """
    res = run_js(code)
    time.sleep(3)
    
    code_pick = """
    (() => {
        const cards = Array.from(document.querySelectorAll('.category-card, [role="button"], div, span, mat-card'));
        const leadCard = cards.find(c => c.innerText && (c.innerText.includes('Submit lead form') || c.innerText.includes('Request quote') || c.innerText.includes('Lead form')));
        if (leadCard) {
            leadCard.click();
            return { leadCardClicked: leadCard.innerText.trim() };
        }
        return { leadCardClicked: 'NOT_FOUND', allText: document.body.innerText.substring(0, 1500) };
    })()
    """
    res_pick = run_js(code_pick)
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
    return {"step1": res, "step2": res_pick, "save": res_save, "after": run_js(code_read)}

if __name__ == "__main__":
    print(json.dumps(select_lead_category(), indent=2))
