import json
import requests
import random
import time

def search_wikimedia_images(query, limit=500):
    url = "https://commons.wikimedia.org/w/api.php"
    headers = {
        'User-Agent': 'SkyAutoServicesBot/1.0 (contact@skyautoservices.com)'
    }
    params = {
        "action": "query",
        "format": "json",
        "prop": "imageinfo",
        "generator": "search",
        "gsrsearch": f"filetype:bitmap {query}",
        "gsrnamespace": "6",
        "gsrlimit": limit,
        "iiprop": "url",
        "iiurlwidth": 1200
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        images = []
        if 'query' in data and 'pages' in data['query']:
            pages = data['query']['pages']
            for page_id in pages:
                page = pages[page_id]
                if 'imageinfo' in page:
                    info = page['imageinfo'][0]
                    # use thumburl, but strip the query params to ensure clean URLs
                    img_url = info.get('thumburl', info.get('url'))
                    if img_url:
                        # strip query params
                        clean_url = img_url.split('?')[0]
                        images.append(clean_url)
        return images
    except Exception as e:
        print(f"Error fetching {query}: {e}")
        return []

print("Fetching images from Wikimedia Commons...")
queries = ["car carrier truck", "semi truck highway", "interstate highway USA", "auto transport", "trucking highway", "transportation USA"]
all_images = set()

for q in queries:
    print(f"Querying: {q}")
    imgs = search_wikimedia_images(q, limit=200)
    all_images.update(imgs)
    time.sleep(1) # rate limiting

image_pool = list(all_images)
# shuffle to ensure nice distribution
random.seed(42)
random.shuffle(image_pool)

print(f"Total unique images collected: {len(image_pool)}")

if len(image_pool) == 0:
    print("Failed to fetch any images.")
    exit(1)

# Now apply to the JSON file
json_path = 'montway_clone/public/data/news_articles.json'
with open(json_path, 'r', encoding='utf-8') as f:
    articles = json.load(f)

for i, article in enumerate(articles):
    # Cycle through the image pool
    img = image_pool[i % len(image_pool)]
    article['backgroundImage'] = img

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(articles, f, indent=2)

print("Updated news_articles.json with real Wikimedia Commons images!")
