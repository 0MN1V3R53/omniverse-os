#!/usr/bin/env python3
"""
Sync Next.js exported production build (montway_clone/out) to public_html_local
Preserving api/, data/, .htaccess, and IndexNow tokens
"""
import os
import shutil

SRC_DIR = "montway_clone/out"
DEST_DIR = "public_html_local"

print("[*] Copying Next.js build output to public_html_local...")

# Copy all files and folders from montway_clone/out to public_html_local
for item in os.listdir(SRC_DIR):
    s = os.path.join(SRC_DIR, item)
    d = os.path.join(DEST_DIR, item)
    if item in [".htaccess", "api", "data", "8f3b2a1c9e4d5f6a7b8c9d0e1f2a3b4c.txt"]:
        continue
    if os.path.isdir(s):
        if os.path.exists(d):
            shutil.rmtree(d)
        shutil.copytree(s, d)
    else:
        shutil.copy2(s, d)

print("[+] Successfully synchronized montway_clone/out to public_html_local!")
