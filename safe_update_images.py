#!/usr/bin/env python3
import os
import glob
import re
import random

TARGET_FILES = [
    'public_html_local/index.html',
    'public_html_local/privacy.html',
    'public_html_local/terms.html'
]
TARGET_FILES.extend(glob.glob('public_html_local/blog/*.html'))

# Must be american muscle and sports cars, no trucks.
IMAGE_CATEGORIES = [
    'american,muscle,car',
    'american,sports,car',
    'muscle,car',
    'sports,car'
]

def update_images(filepath):
    if not os.path.exists(filepath):
        print(f"Skipping {filepath} (not found)")
        return
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find <img ... src="something" ...>
    def replacer(match):
        category = random.choice(IMAGE_CATEGORIES)
        rand_id = random.randint(1, 10000)
        new_src = f"https://loremflickr.com/800/600/{category}?random={rand_id}"
        full_match = match.group(0)
        old_src = match.group(1)
        # only replace if it's not already a loremflickr url
        if "loremflickr" not in old_src:
            new_tag = full_match.replace(old_src, new_src)
            print(f"[{filepath}] Replaced {old_src} -> {new_src}")
            return new_tag
        return full_match

    new_content = re.sub(r'<img[^>]*?src="([^"]+)"[^>]*>', replacer, content, flags=re.IGNORECASE)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")
    else:
        print(f"No changes for {filepath}")

def main():
    print("Starting safe regex image replacement...")
    for filepath in TARGET_FILES:
        update_images(filepath)
    print("Done.")

if __name__ == '__main__':
    main()
