with open("/Users/silversurfer/Documents/Omniverse2/omniverse_portal/generate_html.py", "r", encoding="utf-8") as f:
    code = f.read()

target = '<a href="neural_brain.html" class="nav-link"'
replacement = '<a href="grid_controller.html" class="nav-link" style="font-size: 0.82rem; color: #00f0ff; text-decoration: none; font-weight: 700;">⚡ 10G HyperGrid</a>\n      <a href="neural_brain.html" class="nav-link"'

if "grid_controller.html" not in code:
    code = code.replace(target, replacement, 1)

with open("/Users/silversurfer/Documents/Omniverse2/omniverse_portal/generate_html.py", "w", encoding="utf-8") as f:
    f.write(code)

print("SUCCESS: Updated generate_html.py cleanly!")
