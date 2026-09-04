import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

states = [
    ("Alabama", "AL"), ("Alaska", "AK"), ("Arizona", "AZ"), ("Arkansas", "AR"), ("California", "CA"),
    ("Colorado", "CO"), ("Connecticut", "CT"), ("Delaware", "DE"), ("Florida", "FL"), ("Georgia", "GA"),
    ("Hawaii", "HI"), ("Idaho", "ID"), ("Illinois", "IL"), ("Indiana", "IN"), ("Iowa", "IA"),
    ("Kansas", "KS"), ("Kentucky", "KY"), ("Louisiana", "LA"), ("Maine", "ME"), ("Maryland", "MD"),
    ("Massachusetts", "MA"), ("Michigan", "MI"), ("Minnesota", "MN"), ("Mississippi", "MS"), ("Missouri", "MO"),
    ("Montana", "MT"), ("Nebraska", "NE"), ("Nevada", "NV"), ("New Hampshire", "NH"), ("New Jersey", "NJ"),
    ("New Mexico", "NM"), ("New York", "NY"), ("North Carolina", "NC"), ("North Dakota", "ND"), ("Ohio", "OH"),
    ("Oklahoma", "OK"), ("Oregon", "OR"), ("Pennsylvania", "PA"), ("Rhode Island", "RI"), ("South Carolina", "SC"),
    ("South Dakota", "SD"), ("Tennessee", "TN"), ("Texas", "TX"), ("Utah", "UT"), ("Vermont", "VT"),
    ("Virginia", "VA"), ("Washington", "WA"), ("West Virginia", "WV"), ("Wisconsin", "WI"), ("Wyoming", "WY")
]

res = []
for state, abbr in states:
    try:
        query = urllib.parse.quote(f"{state} skyline")
        url = f"https://commons.wikimedia.org/w/index.php?search={query}&title=Special:MediaSearch&go=Go&type=image"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read()
        soup = BeautifulSoup(html, 'html.parser')
        
        # The images in media search usually have class 'sdms-image-result'
        img = soup.find('img')
        img_url = ""
        if img and img.get('src'):
            img_url = img.get('src')
        
        # fallback
        if not img_url or "wikimedia-logo" in img_url:
            img_url = f"https://picsum.photos/seed/{state.replace(' ', '')}/400/300"
            
        res.append(f'    {{ state: "{state}", abbr: "{abbr}", img: "{img_url}" }}')
    except Exception as e:
        res.append(f'    {{ state: "{state}", abbr: "{abbr}", img: "https://picsum.photos/seed/{state.replace(" ", "")}/400/300" }}')

with open("state_images_final.js", "w") as f:
    f.write("export const ALL_STATES = [\n" + ",\n".join(res) + "\n];")
print("Done")
