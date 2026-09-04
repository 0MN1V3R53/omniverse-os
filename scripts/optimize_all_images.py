#!/usr/bin/env python3
"""
Omniverse Tech - Production Image Optimization & Metadata Stripping Engine
Converts PNG/JPEG assets to next-gen WebP format, strips EXIF metadata,
and compresses images for optimal Core Web Vitals and LCP performance.
"""

import os
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TARGET_DIRS = [
    os.path.join(BASE_DIR, "montway_clone", "public"),
    os.path.join(BASE_DIR, "montway_clone", "public", "assets", "images"),
    os.path.join(BASE_DIR, "montway_clone", "public", "assets", "images", "news"),
    os.path.join(BASE_DIR, "public_html_local", "assets", "images"),
    os.path.join(BASE_DIR, "public_html_local", "assets", "images", "news"),
]

def optimize_image(filepath):
    filename = os.path.basename(filepath)
    ext = os.path.splitext(filename)[1].lower()
    
    if ext not in [".jpg", ".jpeg", ".png"]:
        return

    try:
        with Image.open(filepath) as img:
            # 1. Convert to RGB if RGBA/P
            if img.mode in ("RGBA", "LA") and ext != ".png":
                background = Image.new("RGB", img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background
            elif img.mode not in ("RGB", "RGBA"):
                img = img.convert("RGB")

            # 2. Generate Next-Gen WebP version
            webp_path = os.path.splitext(filepath)[0] + ".webp"
            
            # Save without EXIF or metadata
            img.save(webp_path, "WEBP", quality=82, method=6, optimize=True)
            
            original_size = os.path.getsize(filepath)
            webp_size = os.path.getsize(webp_path)
            savings = ((original_size - webp_size) / original_size) * 100 if original_size > 0 else 0
            
            print(f"✅ Converted: {filename} ({original_size/1024:.1f} KB) ➔ {os.path.basename(webp_path)} ({webp_size/1024:.1f} KB) [-{savings:.1f}%]")

            # 3. Strip metadata from the original image in place as well
            if ext in [".jpg", ".jpeg"]:
                img.save(filepath, "JPEG", quality=85, optimize=True)
            elif ext == ".png":
                img.save(filepath, "PNG", optimize=True)

    except Exception as e:
        print(f"❌ Failed to optimize {filepath}: {e}")

def main():
    print("🚀 Starting Omniverse Image Optimization & EXIF Stripping Pipeline...")
    total_processed = 0
    for target_dir in TARGET_DIRS:
        if not os.path.exists(target_dir):
            continue
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            if os.path.isfile(item_path):
                optimize_image(item_path)
                total_processed += 1
                
    print(f"\n🎉 Optimization complete! Processed {total_processed} files.")

if __name__ == "__main__":
    main()
