#!/usr/bin/env python3
"""
Fetch or assemble exact 50-state SVG paths for zero-dependency local rendering
"""
import urllib.request
import json
import os

# We can fetch the standard public domain US SVG Map paths from Wikimedia / OpenStreetMap
url = "https://raw.githubusercontent.com/martinjc/UK-GeoJSON/master/json/administrative/gb/topo_lad.json" # test
# Let's fetch a clean US Map SVG from a public source or construct the 50-state paths
us_map_url = "https://commons.wikimedia.org/wiki/Special:FilePath/Blank_US_Map_(states_only).svg"

print("[*] Fetching SVG map data...")
try:
    req = urllib.request.Request(us_map_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as resp:
        svg_content = resp.read().decode('utf-8')
        with open("/Users/silversurfer/Documents/Omniverse2/public_html_local/us-map.svg", "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"[+] Downloaded full US Map SVG: {len(svg_content)} bytes")
except Exception as e:
    print(f"[-] Error fetching: {e}")
