#!/usr/bin/env python3
"""
Integrates the official Sky Auto Services logo image uploaded by the user
into Header and Footer across all website templates and reports.
"""

import os
import shutil
import base64
from pathlib import Path

WORKSPACE = Path("/Users/silversurfer/Documents/Omniverse2")
UPLOADED_LOGO = Path("/Users/silversurfer/.gemini/antigravity-ide/brain/a1dbd49f-abea-4585-ad1b-8f9ebd061f8f/media__1784997437850.png")

# Target image locations
IMAGE_TARGETS = [
    WORKSPACE / "assets/images/logo.png",
    WORKSPACE / "public_html_local/assets/images/logo.png",
    WORKSPACE / "hostinger_site/public_html/assets/images/logo.png",
    WORKSPACE / "sky_next/public/assets/images/logo.png"
]

def deploy_logo_files():
    if not UPLOADED_LOGO.exists():
        print(f"Error: Uploaded logo file not found at {UPLOADED_LOGO}")
        return False
    
    for target in IMAGE_TARGETS:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(UPLOADED_LOGO, target)
        print(f"✓ Deployed official logo to: {target}")
    return True

if __name__ == "__main__":
    deploy_logo_files()
