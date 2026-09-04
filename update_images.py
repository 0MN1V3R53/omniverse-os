#!/usr/bin/env python3
import os
import glob
import random
from bs4 import BeautifulSoup

TARGET_FILES = [
    'public_html_local/index.html',
    'public_html_local/privacy.html',
    'public_html_local/terms.html'
]
TARGET_FILES.extend(glob.glob('public_html_local/blog/*.html'))

IMAGE_CATEGORIES = [
    'american,muscle,car',
    'german,sports,car',
    'classic,sports,car',
    'snowmobile',
    'modified,tuner,car'
]

def update_images(filepath):
    if not os.path.exists(filepath):
        print(f"Skipping {filepath} (file not found)")
        return
    
    with open(filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'lxml')
        
    img_tags = soup.find_all('img')
    if not img_tags:
        print(f"No images found in {filepath}")
        return

    updated = False
    for i, img in enumerate(img_tags):
        category = random.choice(IMAGE_CATEGORIES)
        # Using a reliable placeholder image service with keywords
        new_src = f"https://loremflickr.com/800/600/{category}?random={i}"
        
        # Optionally, preserve existing width/height if available, otherwise just set src
        if 'src' in img.attrs:
            old_src = img['src']
            img['src'] = new_src
            print(f"  Replaced {old_src} -> {new_src}")
            updated = True
            
    if updated:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"Updated images in {filepath}")

def main():
    print("Starting image replacement on front-facing HTML files...")
    for filepath in TARGET_FILES:
        update_images(filepath)
    print("Done.")

if __name__ == '__main__':
    main()
