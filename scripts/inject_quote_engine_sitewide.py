#!/usr/bin/env python3
"""
OMNIVERSE ENTERPRISE SITEWIDE QUOTE CALCULATOR & MAP ENGINE INJECTOR
Pod 4 (Full-Stack Web) & Pod 5 (Technical SEO)
Ensures every HTML page has active quote calculation and lead capture scripts
"""

import os
import glob

BASE_DIR = "/Users/silversurfer/Documents/Omniverse2/public_html_local"

html_files = []
for root, _, files in os.walk(BASE_DIR):
    for f in files:
        if f.endswith(".html") and not f.startswith("."):
            html_files.append(os.path.join(root, f))

print(f"[*] Found {len(html_files)} HTML pages to verify.")

injected_count = 0
for path in html_files:
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        changed = False
        # Ensure quote calculator engine is referenced
        if "quote_calculator_engine.js" not in content and "</body>" in content:
            content = content.replace("</body>", '<script src="/assets/js/quote_calculator_engine.js"></script>\n</body>')
            changed = True

        if changed:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            injected_count += 1
    except Exception as e:
        print(f"[-] Error processing {path}: {e}")

print(f"[+] Sitewide audit complete! Injected quote engine into {injected_count} HTML pages.")
