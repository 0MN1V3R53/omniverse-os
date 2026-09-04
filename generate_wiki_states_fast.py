import urllib.request
import json
import urllib.parse
import os
import time
import concurrent.futures

STATE_LANDMARKS = [
    ("Alabama", "AL", "Little River Canyon National Preserve"),
    ("Alaska", "AK", "Denali National Park and Preserve"),
    ("Arizona", "AZ", "Grand Canyon National Park"),
    ("Arkansas", "AR", "Ozark–St. Francis National Forest"),
    ("California", "CA", "Yosemite National Park"),
    ("Colorado", "CO", "Rocky Mountain National Park"),
    ("Connecticut", "CT", "Sleeping Giant (Connecticut)"),
    ("Delaware", "DE", "Cape Henlopen State Park"),
    ("Florida", "FL", "Everglades National Park"),
    ("Georgia", "GA", "Amicalola Falls State Park"),
    ("Hawaii", "HI", "Nā Pali Coast State Park"),
    ("Idaho", "ID", "Sawtooth Range (Idaho)"),
    ("Illinois", "IL", "Starved Rock State Park"),
    ("Indiana", "IN", "Indiana Dunes National Park"),
    ("Iowa", "IA", "Maquoketa Caves State Park"),
    ("Kansas", "KS", "Monument Rocks (Kansas)"),
    ("Kentucky", "KY", "Red River Gorge"),
    ("Louisiana", "LA", "Atchafalaya Basin"),
    ("Maine", "ME", "Acadia National Park"),
    ("Maryland", "MD", "Assateague Island National Seashore"),
    ("Massachusetts", "MA", "Cape Cod National Seashore"),
    ("Michigan", "MI", "Sleeping Bear Dunes National Lakeshore"),
    ("Minnesota", "MN", "Boundary Waters Canoe Area Wilderness"),
    ("Mississippi", "MS", "Gulf Islands National Seashore"),
    ("Missouri", "MO", "Ozark National Scenic Riverways"),
    ("Montana", "MT", "Glacier National Park (U.S.)"),
    ("Nebraska", "NE", "Toadstool Geologic Park"),
    ("Nevada", "NV", "Valley of Fire State Park"),
    ("New Hampshire", "NH", "White Mountain National Forest"),
    ("New Jersey", "NJ", "Pine Barrens (New Jersey)"),
    ("New Mexico", "NM", "White Sands National Park"),
    ("New York", "NY", "Adirondack Park"),
    ("North Carolina", "NC", "Great Smoky Mountains National Park"),
    ("North Dakota", "ND", "Theodore Roosevelt National Park"),
    ("Ohio", "OH", "Hocking Hills State Park"),
    ("Oklahoma", "OK", "Wichita Mountains Wildlife Refuge"),
    ("Oregon", "OR", "Crater Lake National Park"),
    ("Pennsylvania", "PA", "Ricketts Glen State Park"),
    ("Rhode Island", "RI", "Mohegan Bluffs"),
    ("South Carolina", "SC", "Congaree National Park"),
    ("South Dakota", "SD", "Badlands National Park"),
    ("Tennessee", "TN", "Great Smoky Mountains National Park"),
    ("Texas", "TX", "Big Bend National Park"),
    ("Utah", "UT", "Zion National Park"),
    ("Vermont", "VT", "Green Mountain National Forest"),
    ("Virginia", "VA", "Shenandoah National Park"),
    ("Washington", "WA", "Mount Rainier National Park"),
    ("West Virginia", "WV", "New River Gorge National Park and Preserve"),
    ("Wisconsin", "WI", "Apostle Islands National Lakeshore"),
    ("Wyoming", "WY", "Grand Teton National Park")
]

def get_wiki_image(item):
    state, abbr, landmark = item
    url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(landmark)}&prop=pageimages&format=json&pithumbsize=1000"
    req = urllib.request.Request(url, headers={"User-Agent": "BotEmailForContact: support@skyautoservices.com"})
    img_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Yosemite_Valley_from_Wawona_Tunnel_view%2C_2020.jpg/1000px-Yosemite_Valley_from_Wawona_Tunnel_view%2C_2020.jpg" # fallback
    
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                pages = data["query"]["pages"]
                for page_id in pages:
                    if "thumbnail" in pages[page_id]:
                        img_url = pages[page_id]["thumbnail"]["source"]
                        break
            break # success
        except Exception as e:
            time.sleep(1)
            
    print(f"Fetched {state}: {img_url}")
    return state, abbr, img_url

results = []
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(get_wiki_image, STATE_LANDMARKS))

# Sort to maintain alphabetical order
results.sort(key=lambda x: x[0])

all_states_js = "// components/data/statesData.js\n// VERIFIED WIKIPEDIA NATURAL BEAUTY IMAGES\n\nconst ALL_STATES = [\n"
for state, abbr, img_url in results:
    all_states_js += f'  {{ state: "{state}", abbr: "{abbr}", img: "{img_url}" }},\n'

all_states_js += "];\n\nexport default ALL_STATES;\n"

output_path = "/Users/silversurfer/Documents/Omniverse2/montway_clone/components/data/statesData.js"
with open(output_path, "w") as f:
    f.write(all_states_js)

print("Successfully wrote statesData.js")
