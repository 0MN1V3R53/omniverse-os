import os
import glob
import re

def strip_fluff():
    memories_dir = "/Users/silversurfer/Documents/Omniverse2/omniverse_memories"
    files = glob.glob(os.path.join(memories_dir, "*.md"))
    
    technical_invariants = """
## 🛠️ TECHNICAL INVARIANTS

- **Frameworks/Stack:** Must strictly adhere to repository framework versions (e.g., Next.js 14, React 19).
- **Architecture Rules:** Strict component isolation. Ensure zero-drift routing and data parity.
- **Prohibited Practices:** No mock data, no synthetic profiles, no nested ternary operators, no placeholders.
- **Error Handling:** Explicit exception handling. Fail fast and escalate rather than guessing.
"""
    
    count = 0
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            
        original_content = content
        
        # Regex to strip these sections up to the next ## or end of file
        content = re.sub(r"## 🎭 LLM Personality.*?((?=## )|\Z)", "", content, flags=re.DOTALL)
        content = re.sub(r"## 🎓 Academic Grounding.*?((?=## )|\Z)", "", content, flags=re.DOTALL)
        content = re.sub(r"## 📺 YouTube Research Channels.*?((?=## )|\Z)", "", content, flags=re.DOTALL)
        content = re.sub(r"## 💼 Industry Experience.*?((?=## )|\Z)", "", content, flags=re.DOTALL)

        # Remove extra blank lines and separator lines ---
        content = re.sub(r"\n---\n\s*\n---", "\n---", content)
        
        # If it doesn't already have TECHNICAL INVARIANTS, inject it after the frontmatter / role description
        if "TECHNICAL INVARIANTS" not in content and "Master Memory System" in content:
            content = content.replace("## 📌 Master Memory System", technical_invariants + "\n## 📌 Master Memory System")
            
        if content != original_content:
            with open(file, "w", encoding="utf-8") as f:
                f.write(content)
            count += 1
            
    print(f"Stripped fluff and added Technical Invariants to {count} agent files.")

if __name__ == "__main__":
    strip_fluff()
