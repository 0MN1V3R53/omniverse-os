import re

with open("public_html_local/index.html", "r", encoding="utf-8") as f:
    content = f.read()

buttons = re.findall(r'<button[^>]*>.*?</button>', content, re.IGNORECASE | re.DOTALL)
links_as_buttons = re.findall(r'<a[^>]*class="[^"]*button[^"]*"[^>]*>.*?</a>', content, re.IGNORECASE | re.DOTALL)
links = re.findall(r'<a[^>]*>.*?</a>', content, re.IGNORECASE | re.DOTALL)

print(f"Found {len(buttons)} <button> tags.")
for b in buttons:
    print(f"Button: {b[:100]}...")

print(f"\nFound {len(links_as_buttons)} links styled as buttons.")
for l in links_as_buttons:
    print(f"Link Button: {l[:100]}...")
