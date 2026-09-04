#!/usr/bin/env python3
import sys
sys.path.append("scripts")
from get_page_content import run_js
import json

def get_clickable_conversion_elements():
    code = """
    (() => {
        return Array.from(document.querySelectorAll('a, button, [role="button"], span, div'))
            .map(el => ({
                text: el.innerText ? el.innerText.trim() : '',
                tag: el.tagName,
                href: el.href || null
            }))
            .filter(item => item.text.includes('Call from Ads') || item.text.includes('Misconfigured') || item.text.includes('Create conversion action'));
    })()
    """
    return run_js(code)

if __name__ == "__main__":
    print(json.dumps(get_clickable_conversion_elements(), indent=2))
