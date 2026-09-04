import os
import glob
import json
import re

def extract_field(content, pattern):
    match = re.search(pattern, content, re.IGNORECASE)
    return match.group(1).strip() if match else ""

def parse_md(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    agent_id = extract_field(content, r'\*\*Agent ID:\*\*\s*`([^`]+)`')
    if not agent_id:
        return None
        
    full_name = extract_field(content, r'\*\*Full Name:\*\*\s*(.*)')
    role = extract_field(content, r'\*\*Role:\*\*\s*(.*)')
    department = extract_field(content, r'\*\*Department / Pod:\*\*\s*(.*)')
    manager = extract_field(content, r'\*\*Manager / Reporting Line:\*\*\s*(.*)')
    
    mbti = extract_field(content, r'-\s*\*\*MBTI & Temperament:\*\*\s*\*\*(.*?)\*\*')
    if not mbti:
        mbti = extract_field(content, r'-\s*\*\*MBTI & Temperament:\*\*\s*(.*)')
        
    personality = extract_field(content, r'-\s*\*\*Personality Description:\*\*\s*(.*)')
    coffee = extract_field(content, r'-\s*\*\*Coffee & Break Preference:\*\*\s*(.*)')
    slack = extract_field(content, r'-\s*\*\*Slack Communication Style:\*\*\s*(.*)')
    happy_hour = extract_field(content, r'-\s*\*\*Friday `#happy-hour` Choice:\*\*\s*(.*)')
    
    # Extract Academic Grounding block
    academic_match = re.search(r'## 🎓 Academic Grounding[^\n]*\n\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
    academic = academic_match.group(1).strip() if academic_match else ""
    
    # Extract YouTube Channels
    youtube_channels = []
    youtube_match = re.search(r'- \*\*Curated YouTube Research Channels:\*\*\s*\n(.*?)(?=\n- |\n## |\Z)', content, re.DOTALL)
    if youtube_match:
        lines = youtube_match.group(1).strip().split('\n')
        for line in lines:
            # - [DesignCourse (Gary Simon)](https://...)
            link_match = re.search(r'\[([^\]]+)\]\(([^)]+)\)', line)
            if link_match:
                youtube_channels.append({
                    "name": link_match.group(1),
                    "url": link_match.group(2)
                })

    return {
        "id": agent_id,
        "name": full_name,
        "role": role,
        "department": department,
        "manager": manager,
        "mbti": mbti,
        "personality": personality,
        "coffee": coffee,
        "slack": slack,
        "happy_hour": happy_hour,
        "academic": academic,
        "youtube": youtube_channels
    }

def main():
    directory = "/Users/silversurfer/Documents/Omniverse2/omniverse_memories/"
    output_dir = "/Users/silversurfer/Documents/Omniverse2/public_html_local/assets/data/"
    os.makedirs(output_dir, exist_ok=True)
    
    md_files = glob.glob(os.path.join(directory, "*.md"))
    staff = []
    for md in md_files:
        profile = parse_md(md)
        if profile:
            staff.append(profile)
            
    with open(os.path.join(output_dir, "omniverse_staff.json"), "w", encoding="utf-8") as out:
        json.dump(staff, out, indent=4)
        
    print(f"Extracted {len(staff)} agent profiles.")

if __name__ == "__main__":
    main()
