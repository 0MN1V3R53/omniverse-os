#!/usr/bin/env python3
"""
Extract exact SVG path data from us-map.svg and format into a React/JS module
"""
import re
import json

with open("public_html_local/us-map.svg", "r", encoding="utf-8") as f:
    svg_text = f.read()

# Pattern to find <path class="xx" d="..."> <title>State Name</title> </path>
pattern = re.compile(r'<path\s+class="([a-z]{2})"\s+d="([^"]+)"[^>]*>.*?<title>([^<]+)</title>.*?</path>', re.DOTALL | re.IGNORECASE)

matches = pattern.findall(svg_text)
print(f"[+] Found {len(matches)} state paths in us-map.svg")

state_paths = {}
for cls, d, name in matches:
    cls = cls.upper()
    state_paths[cls] = {
        "abbr": cls,
        "name": name.strip(),
        "d": d.strip()
    }

# Also handle circle for DC if present
dc_circle = re.search(r'<circle\s+class="([a-z]{2})"\s+cx="([^"]+)"\s+cy="([^"]+)"\s+r="([^"]+)"', svg_text, re.IGNORECASE)
if dc_circle:
    cls, cx, cy, r = dc_circle.groups()
    state_paths["DC"] = {
        "abbr": "DC",
        "name": "District of Columbia",
        "circle": {"cx": float(cx), "cy": float(cy), "r": float(r)}
    }

print(f"[+] Total parsed states + DC: {len(state_paths)}")

output_js = f"""// AUTO-GENERATED 50 US STATES + DC HIGH-PRECISION SVG PATH DATA
// ZERO EXTERNAL CDN DEPENDENCY — 100% INLINE REACT/DOM COMPATIBLE

export const US_STATE_PATHS = {json.dumps(state_paths, indent=2)};
export default US_STATE_PATHS;
"""

with open("montway_clone/components/data/usStatePaths.js", "w", encoding="utf-8") as f:
    f.write(output_js)

print("[+] Wrote montway_clone/components/data/usStatePaths.js successfully!")
