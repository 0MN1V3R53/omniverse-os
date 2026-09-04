import os
import json
import random

ROUTES_JSON = "public_html_local/assets/data/state_routes.json"
INDEX_HTML = "public_html_local/index.html"

def inject_pagerank_hubs():
    if not os.path.exists(ROUTES_JSON) or not os.path.exists(INDEX_HTML):
        print("Missing required files.")
        return

    with open(ROUTES_JSON, 'r', encoding='utf-8') as f:
        routes_data = json.load(f)

    # Top high volume states for auto transport
    top_states = ["California", "Florida", "New York", "Texas", "Illinois", "New Jersey", "Pennsylvania", "Georgia", "Washington", "Arizona"]
    
    hub_links = []
    
    # Generate cross links between top states
    for origin in top_states:
        if origin in routes_data:
            for route in routes_data[origin]:
                dest = route["destination"]
                if dest in top_states and dest != origin:
                    slug = route["slug"]
                    hub_links.append(f'<a href="/routes/{slug}" class="text-gray-400 hover:text-emerald-400 transition">{origin} to {dest}</a>')

    if not hub_links:
        print("No hub links generated.")
        return

    # Create the HTML block
    links_html = "".join(hub_links)
    
    hub_block = f'''<div class="max-w-7xl mx-auto px-4 py-8 border-t border-white/10"><h4 class="text-emerald-400 font-bold mb-4 text-sm uppercase">Popular Transport Corridors</h4><div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-y-2 gap-x-4 text-xs">{links_html}</div></div>'''

    with open(INDEX_HTML, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Find where to inject - right before the <footer> tag
    target_tag = "<footer class="
    if target_tag in html_content and "Popular Transport Corridors" not in html_content:
        new_html = html_content.replace(target_tag, hub_block + target_tag)
        with open(INDEX_HTML, 'w', encoding='utf-8') as f:
            f.write(new_html)
        print(f"[SUCCESS] Injected {len(hub_links)} deep Hub-and-Spoke PR links into index.html")
    else:
        print("[SKIP] Hubs already exist or target tag not found.")

if __name__ == "__main__":
    inject_pagerank_hubs()
