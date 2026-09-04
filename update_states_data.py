import re

states_data_file = "montway_clone/components/data/statesData.js"

with open(states_data_file, 'r') as f:
    content = f.read()

def replace_line(match):
    prefix = match.group(1)
    state = match.group(2)
    suffix = match.group(3)
    state_slug = state.lower().replace(' ', '-')
    return f'{prefix}state: "{state}",{suffix}img: "/images/states/{state_slug}.webp" }}'

new_content = re.sub(r'(.*?\{\s*)state:\s*"([^"]+)",(.*?)\bimg:\s*"[^"]+"\s*\}', replace_line, content)

with open(states_data_file, 'w') as f:
    f.write(new_content)

print(f"Updated {states_data_file}")
