import os
import glob
import re

POD_LEAD_TEMPLATE = """# POD LEAD PROTOCOL: {domain}

## [1] ROLE & SCOPE
You are the {domain} Pod Lead. You report directly to Dr. Vance. You receive domain-level objectives from Dr. Vance, break them down into granular technical tasks, and delegate execution to your domain sub-agents.

## [2] SUB-AGENT ORCHESTRATION
When Dr. Vance assigns you a task:
1. **Scope the Domain:** Determine which specialized sub-agents under your pod are needed.
2. **Delegate Tactical Tasks:** Assign specific, non-overlapping tasks to your sub-agents with strict technical invariants.
3. **Code Quality Control:** Review the raw code returned by your sub-agents against domain best practices (performance, accessibility, security).
4. **Package for Executive Review:** Combine your sub-agents' work into a single, cohesive domain deliverable and pass it back to Dr. Vance.

## [3] DOMAIN INVARIANTS
- Ensure all code produced by your sub-agents contains ZERO placeholders (`// TODO`, `pass`, `...`).
- Verify that sub-agents strictly adhere to the project's global tech stack choices before returning work to Dr. Vance.
"""

SUB_AGENT_TEMPLATE = """# SUB-AGENT PROTOCOL: {specialty}

## [1] ROLE & SCOPE
You are a tactical execution sub-agent specializing in {specialty}. You report directly to your Pod Lead. You do not communicate with Dr. Vance or other Pod Leads.

## [2] EXECUTION DIRECTIVES
- **Pure Implementation:** Execute the exact coding or analytical assignment provided by your Pod Lead.
- **Zero Drift / Zero Placeholders:** Write 100% complete, fully implemented, production-ready code. Never leave stubbed functions or placeholder comments.
- **Halt on Missing Context:** If required API endpoints, schemas, or variables are missing from your task assignment, immediately inform your Pod Lead instead of inventing mock data.
"""

def process_agents():
    memories_dir = "/Users/silversurfer/Documents/Omniverse2/omniverse_memories"
    files = glob.glob(os.path.join(memories_dir, "*.md"))
    
    lead_count = 0
    sub_count = 0
    
    for file in files:
        if "exec_ceo" in file:
            continue
            
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Extract Role and Department to figure out their domain/specialty
        role_match = re.search(r"\*\*Role:\*\*\s*(.+)", content)
        dept_match = re.search(r"\*\*Department / Pod:\*\*\s*(.+)", content)
        
        role = role_match.group(1).strip() if role_match else "Specialist"
        dept = dept_match.group(1).strip() if dept_match else "Division"
        
        # Determine if Pod Lead
        is_lead = False
        if any(keyword in role.lower() for keyword in ["lead", "director", "chief", "head", "manager"]):
            is_lead = True
        if "lead" in file.lower():
            is_lead = True
            
        # Remove existing TECHNICAL INVARIANTS section to replace with the new templates
        content = re.sub(r"## 🛠️ TECHNICAL INVARIANTS.*?(?=## |\Z)", "", content, flags=re.DOTALL)
        content = re.sub(r"## 📌 Master Memory System", "", content) # Remove old section header if left behind
        
        if is_lead:
            domain = dept.upper() + " - " + role.upper()
            template = POD_LEAD_TEMPLATE.format(domain=domain)
            lead_count += 1
        else:
            specialty = role.upper()
            template = SUB_AGENT_TEMPLATE.format(specialty=specialty)
            sub_count += 1
            
        # Append the template to the end of the frontmatter/memory area
        # To avoid duplicating, we'll just append it to the end of the file
        
        # Check if the protocol is already there
        if "ROLE & SCOPE" not in content:
            new_content = content.strip() + "\n\n" + template
            with open(file, "w", encoding="utf-8") as f:
                f.write(new_content)
                
    print(f"Applied Pod Lead Protocol to {lead_count} supervisors.")
    print(f"Applied Sub-Agent Protocol to {sub_count} workers.")

if __name__ == "__main__":
    process_agents()
