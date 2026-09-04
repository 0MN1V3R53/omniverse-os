import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://en.wikipedia.org/w/api.php?action=query&prop=imageinfo&iiprop=url&format=json&titles=File:Rolls-Royce_Phantom_VIII_Black_(5).jpg"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
response = urllib.request.urlopen(req, context=ctx)
data = json.loads(response.read())
pages = data['query']['pages']
for page_id in pages:
    if 'imageinfo' in pages[page_id]:
        image_url = pages[page_id]['imageinfo'][0]['url']
        print("URL:", image_url)
        req2 = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
        res2 = urllib.request.urlopen(req2, context=ctx)
        with open("public_html_local/assets/images/rolls_royce.png", 'wb') as f:
            f.write(res2.read())
