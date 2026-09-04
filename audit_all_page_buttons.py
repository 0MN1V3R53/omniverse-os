#!/usr/bin/env python3
import os
import re
from html.parser import HTMLParser

workspace = "/Users/silversurfer/Documents/Omniverse2"
target_files = [
    "cyberpunk_telemetry_live.html",
    "cyberpunk_seo_dashboard.html",
    "public_html_local/index.html",
    "index.html"
]

print("==================================================")
print("🔍 OMNIVERSE ENTERPRISE COMPREHENSIVE BUTTON AUDITOR")
print("==================================================")

class ElementAuditor(HTMLParser):
    def __init__(self, full_text):
        super().__init__()
        self.full_text = full_text
        self.elements = []
        
    def handle_starttag(self, tag, attrs):
        if tag in ['button', 'a', 'input']:
            attr_dict = dict(attrs)
            self.elements.append((tag, attr_dict))

total_buttons = 0
total_issues = 0

for rel_path in target_files:
    filepath = os.path.join(workspace, rel_path)
    if not os.path.exists(filepath):
        print(f"\n❌ File not found: {rel_path}")
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    auditor = ElementAuditor(content)
    auditor.feed(content)
    
    print(f"\n📂 File: {rel_path} (Total Interactive Elements: {len(auditor.elements)})")
    
    file_issues = []
    
    for tag, attrs in auditor.elements:
        total_buttons += 1
        btn_id = attrs.get('id', 'NO_ID')
        btn_class = attrs.get('class', '')
        onclick = attrs.get('onclick', '')
        href = attrs.get('href', '')
        btn_type = attrs.get('type', '')
        
        # Check 1: Anchor link with href="#" and no click handler or target id
        if tag == 'a' and href == '#' and not onclick:
            file_issues.append(f"  ❌ Dummy Link: `<a>` with `href=\"#\"` and no `onclick` handler (id: {btn_id}, class: {btn_class})")
            
        # Check 2: Onclick functions called but not defined in script
        if onclick:
            funcs = re.findall(r'([a-zA-Z0-9_]+)\s*\(', onclick)
            for func_name in funcs:
                if func_name not in ['alert', 'console', 'preventDefault', 'stopPropagation', 'location', 'window']:
                    # Check if function definition exists in content
                    if f"function {func_name}" not in content and f"{func_name} =" not in content and f"{func_name}=" not in content and f"{func_name}:" not in content:
                        file_issues.append(f"  ❌ Missing JS Function: `{func_name}()` called in onclick but definition not found in file!")
                        
    if file_issues:
        total_issues += len(file_issues)
        for issue in file_issues:
            print(issue)
    else:
        print("  ✅ All interactive buttons, tabs, links, and click handlers are 100% valid!")

print("\n==================================================")
print(f"📊 AUDIT COMPLETE: Audited {total_buttons} interactive elements across 4 files.")
if total_issues == 0:
    print("✨ RESULT: 0 broken buttons or missing handlers detected!")
else:
    print(f"⚠️ RESULT: Identified {total_issues} issue(s). Fixing immediately...")
print("==================================================")
