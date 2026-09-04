import requests
import json

def search_wikimedia_images(query, limit=50):
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
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    images = []
    
    if 'query' in data and 'pages' in data['query']:
        pages = data['query']['pages']
        for page_id in pages:
            page = pages[page_id]
            if 'imageinfo' in page:
                info = page['imageinfo'][0]
                if 'thumburl' in info:
                    images.append(info['thumburl'])
                elif 'url' in info:
                    images.append(info['url'])
    return images

images = search_wikimedia_images("highway US", 5)
for img in images:
    print(img)
