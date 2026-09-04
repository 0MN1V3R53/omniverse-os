#!/usr/bin/env python3
import sys
sys.path.append("scripts")
from get_page_content import run_js
import json

def get_signal_inputs():
    code = """
    (() => {
        const inputs = Array.from(document.querySelectorAll('input, [role="combobox"], [role="searchbox"], mat-select'))
            .map(i => ({
                tag: i.tagName,
                type: i.type || null,
                placeholder: i.placeholder || i.getAttribute('aria-label') || '',
                id: i.id || null,
                className: i.className
            }));
            
        return { inputs };
    })()
    """
    return run_js(code)

if __name__ == "__main__":
    print(json.dumps(get_signal_inputs(), indent=2))
