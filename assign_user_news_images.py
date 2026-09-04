import os
import shutil
import json
import re

source_dir = "/Users/silversurfer/Documents/Omniverse2/images for news/images"
dest_dir_next = "/Users/silversurfer/Documents/Omniverse2/montway_clone/public/assets/images/news"
dest_dir_local = "/Users/silversurfer/Documents/Omniverse2/public_html_local/assets/images/news"

os.makedirs(dest_dir_next, exist_ok=True)
os.makedirs(dest_dir_local, exist_ok=True)

valid_extensions = ('.jpg', '.jpeg', '.png', '.webp')
all_files = sorted(os.listdir(source_dir))

image_files = [f for f in all_files if f.lower().endswith(valid_extensions)]

print(f"Found {len(image_files)} valid image files in {source_dir}:")
for idx, f in enumerate(image_files):
    print(f"  [{idx+1}] {f} ({os.path.getsize(os.path.join(source_dir, f))} bytes)")

# Copy and standardize filenames
copied_images = []
for idx, f in enumerate(image_files):
    ext = os.path.splitext(f)[1].lower()
    # Clean filename or numbered slug
    safe_name = f"news_image_{idx+1}{ext}"
    src_path = os.path.join(source_dir, f)
    dst_path_next = os.path.join(dest_dir_next, safe_name)
    dst_path_local = os.path.join(dest_dir_local, safe_name)
    
    shutil.copy2(src_path, dst_path_next)
    shutil.copy2(src_path, dst_path_local)
    
    web_path = f"/assets/images/news/{safe_name}"
    copied_images.append({
        "original": f,
        "clean_name": safe_name,
        "web_path": web_path
    })

print(f"\nSuccessfully copied {len(copied_images)} images to public assets directories.")

# Now update news_articles.json
json_path = "/Users/silversurfer/Documents/Omniverse2/montway_clone/public/data/news_articles.json"
json_path_local = "/Users/silversurfer/Documents/Omniverse2/public_html_local/data/news_articles.json"

with open(json_path, 'r', encoding='utf-8') as f:
    articles = json.load(f)

print(f"Total articles in JSON: {len(articles)}")
print(f"Total images provided: {len(copied_images)}")

# Assign each article a bespoke image from the copied images
for i, article in enumerate(articles):
    img_info = copied_images[i % len(copied_images)]
    article['backgroundImage'] = img_info['web_path']
    print(f"Article {i+1}: '{article['title']}' -> {img_info['web_path']} (from {img_info['original']})")

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(articles, f, indent=2)

with open(json_path_local, 'w', encoding='utf-8') as f:
    json.dump(articles, f, indent=2)

print("\nUpdated news_articles.json in both next and local locations.")
