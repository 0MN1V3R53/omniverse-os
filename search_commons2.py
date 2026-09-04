import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch=Rolls-Royce_Phantom_VIII&srnamespace=6&utf8=&format=json"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
response = urllib.request.urlopen(req, context=ctx)
data = json.loads(response.read())
for item in data['query']['search']:
    title = item['title']
    print(title)
