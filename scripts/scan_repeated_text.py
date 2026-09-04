import os
import glob
import re
from collections import Counter

def clean_html(html):
    # Remove script, style, svg, noscript
    html = re.sub(r"<(script|style|svg|noscript)[^>]*>.*?</\1>", "", html, flags=re.DOTALL|re.IGNORECASE)
    return html

def extract_text_blocks(html):
    # Match tags: p, h1-h6, li, blockquote, dt, dd, span, div, a
    blocks = re.findall(r"<(p|h[1-6]|li|blockquote|dt|dd|span|div)(?:\s+[^>]*)?>(.*?)</\1>", html, flags=re.DOTALL|re.IGNORECASE)
    cleaned_blocks = []
    # Ignore global header/footer navigation items that naturally appear in both mobile and desktop menus
    global_nav_ignore = {
        "Door-to-Door", "Instant Quote", "Get an Instant Quote", "Get Free Quote", "Get Instant Quote",
        "Terms of Service", "Privacy Policy", "Sky Auto Services", "All Rights Reserved",
        "USDOT: 4504932", "MC: 1782670", "3216 N Salk Rd", "Arlington Heights, IL 60004",
        "(224) 449-0397", "sales@skyservicesllc.com", "Open Auto Transport", "Enclosed Auto Transport",
        "State-to-State Routes", "Auto Transport News", "About Us", "Contact Us", "Route Directory",
        "Popular State Routes", "Top Metro Locations", "Services", "About", "Contact", "Terms", "Privacy"
    }
    for tag, content in blocks:
        # Strip internal tags
        txt = re.sub(r"<[^>]+>", " ", content)
        txt = re.sub(r"\s+", " ", txt).strip()
        # Filter for sentences longer than 18 characters
        if len(txt) > 18 and txt not in global_nav_ignore:
            cleaned_blocks.append(txt)
    return cleaned_blocks


def main():
    files = glob.glob("public_html_local/**/*.html", recursive=True)
    print(f"Scanning {len(files)} HTML files for repeating text on the same page...")
    
    duplicate_reports = {}
    
    for path in files:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            raw_html = f.read()
        
        cleaned = clean_html(raw_html)
        blocks = extract_text_blocks(cleaned)
        counts = Counter(blocks)
        
        # Look for duplicate paragraphs / sentences
        dupes = {text: count for text, count in counts.items() if count > 1}
        
        # Check if the duplicate is just a standard global footer or header item that appears in both
        if dupes:
            duplicate_reports[path] = dupes

    print(f"\n=======================================================")
    print(f"TOTAL HTML FILES WITH DUPLICATE TEXT: {len(duplicate_reports)}")
    print(f"=======================================================\n")
    
    # Categorize by template pattern
    for path, dupes in list(duplicate_reports.items())[:20]:
        print(f"FILE: {path}")
        for txt, c in dupes.items():
            print(f"  [{c}x]: {txt[:120]}...")
        print()

if __name__ == "__main__":
    main()
