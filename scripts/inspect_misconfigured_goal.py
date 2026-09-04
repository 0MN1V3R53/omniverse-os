#!/usr/bin/env python3
import sys
sys.path.append("scripts")
from get_page_content import run_js
import json
import time

def inspect_goal_details():
    code = """
    (() => {
        const text = document.body.innerText;
        const phoneIdx = text.indexOf('Phone call lead');
        return {
            snippet: phoneIdx !== -1 ? text.substring(phoneIdx, phoneIdx + 800) : 'NOT_FOUND'
        };
    })()
    """
    return run_js(code)

if __name__ == "__main__":
    res = inspect_goal_details()
    print(json.dumps(res, indent=2))
