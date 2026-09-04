import urllib.request
import json
import re

states = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia",
    "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland",
    "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
    "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
    "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
]

# We will just do a simple search or use a known list if possible.
# Actually, since we want reliable photos without a complex script, let's just use Wikipedia's summary API which provides a thumbnail for each page!

res = []
for state in states:
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{state.replace(' ', '_')}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode('utf-8'))
        
        # We can use the 'originalimage' or 'thumbnail'
        if 'originalimage' in data:
            img_url = data['originalimage']['source']
            res.append(f'{{ state: "{state}", abbr: "{state[:2].upper()}", img: "{img_url}" }}')
        else:
            res.append(f'{{ state: "{state}", abbr: "{state[:2].upper()}", img: "" }}')
    except Exception as e:
        print(f"Failed for {state}: {e}")

with open("state_images.js", "w") as f:
    f.write("[\n" + ",\n".join(res) + "\n]")
print("Done")
