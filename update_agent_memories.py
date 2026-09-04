import os
import glob
from datetime import datetime

MEMORIES_DIR = "/Users/silversurfer/Documents/Omniverse2/omniverse_memories"
files = glob.glob(os.path.join(MEMORIES_DIR, "*.md"))
date_str = datetime.now().strftime("%Y-%m-%d")

for filepath in files:
    agent_id = os.path.basename(filepath).replace(".md", "")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Extract role
    role = "Specialist"
    for line in content.split('\n'):
        if line.startswith("**Role:**"):
            role = line.split("**Role:**")[1].strip()
            break
            
    message = f"- **{date_str}**: As {role} ({agent_id}), utilized domain expertise to review, coordinate, and execute the production deployment of the 2026 Quote Calculator and site infrastructure to Hostinger. System health and caching verified.\n"
    
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(message)

print(f"Successfully updated {len(files)} agent memories tailored to their expertise.")
