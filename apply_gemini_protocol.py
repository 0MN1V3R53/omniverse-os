import os
import glob

HEADER = """> [!IMPORTANT]
> **BASELINE PROTOCOL:** You must operate under the `Gemini.md` protocol.
> **ROUTING AUTHORITY:** Tasks are delegated exclusively by Dr. Alexander Vance (CEO). You are receiving this task because it matches your specific agent profile.
> **STRICT DIRECTIVE:** Absolutely no drift, no hallucination, no mock data, and no simulated mock data.

"""

def update_agent_files():
    memories_dir = "/Users/silversurfer/Documents/Omniverse2/omniverse_memories"
    files = glob.glob(os.path.join(memories_dir, "*.md"))
    
    count = 0
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            
        if "> **BASELINE PROTOCOL:**" not in content:
            with open(file, "w", encoding="utf-8") as f:
                f.write(HEADER + content)
            count += 1
            
    print(f"Updated {count} agent files in omniverse_memories/")

if __name__ == "__main__":
    update_agent_files()
