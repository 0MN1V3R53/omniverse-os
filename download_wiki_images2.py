import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def search_wiki_image(query):
    url = f"https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req, context=ctx)
    data = json.loads(response.read())
    pages = data['query']['pages']
    for page_id in pages:
        if 'original' in pages[page_id]:
            return pages[page_id]['original']['source']
    return None

def download_image(url, filename):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req, context=ctx)
    with open(filename, 'wb') as f:
        f.write(response.read())

# Another try for mustang
mustang_url = search_wiki_image("Ford_Mustang_Shelby_GT500")
print("Mustang URL:", mustang_url)
if mustang_url:
    download_image(mustang_url, "public_html_local/assets/images/mustang_shelby.png")

rolls_url2 = search_wiki_image("Rolls-Royce_Phantom_VIII")
# Wait, let's look for Rolls-Royce Ghost or something to avoid the UK plate
rolls_url_ghost = search_wiki_image("Rolls-Royce_Ghost")
print("Ghost URL:", rolls_url_ghost)
if rolls_url_ghost:
    download_image(rolls_url_ghost, "public_html_local/assets/images/rolls_royce.png")
