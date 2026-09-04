import re
import os
import json

base_dir = "/Users/silversurfer/Documents/Omniverse2"

files_to_check = [
    "cyberpunk_telemetry_live.html",
    "cyberpunk_seo_dashboard.html",
    "index.html",
    "public_html_local/index.html"
]

print("🔍 RUNNING OMNIVERSE TEAM FULL BUTTON & AUDIT CHECK...")

for rel_path in files_to_check:
    full_path = os.path.join(base_dir, rel_path)
    if not os.path.exists(full_path):
        continue
    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find all button and onclick elements
    onclicks = re.findall(r'onclick=["\'](.*?)["\']', content)
    buttons = re.findall(r'<button.*?>', content)
    
    print(f"\n📄 Auditing {rel_path}:")
    print(f"   - Found {len(buttons)} <button> tags.")
    print(f"   - Found {len(onclicks)} inline onclick handlers.")

    # Check for missing JS functions referenced in onclick
    js_functions = re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', content)
    print(f"   - Defined JS functions: {len(js_functions)}")

    missing = []
    for handler in onclicks:
        func_match = re.match(r'([a-zA-Z0-9_]+)\s*\(', handler.strip())
        if func_match:
            func_name = func_match.group(1)
            if func_name not in js_functions and func_name not in ["event", "window", "document", "alert", "console"]:
                missing.append((func_name, handler))

    if missing:
        print(f"   ⚠️ WARNING: Referenced onclick functions not defined locally: {missing}")
    else:
        print("   ✓ All onclick handlers resolve cleanly to defined JS functions!")

print("\n✓ Full Omniverse Team Button Audit Completed.")
