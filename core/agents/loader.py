"""
Dynamic Agent Persona Loader and Omniverse Enterprise Roster.
Parses markdown memory files and reconstitutes autonomous agent specifications.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from pydantic import BaseModel, Field

from core.config import CONFIG


class OmniverseAgent(BaseModel):
    """Rich autonomous agent definition extracted from .agents/omniverse_memories/."""
    agent_id: str
    name: str
    role: str
    department: str
    level: str
    mbti: Optional[str] = None
    reports_to: str = "exec_ceo_alexander_vance"
    catchphrase: Optional[str] = None
    kpi: Optional[str] = None
    skills: Set[str] = Field(default_factory=set)
    tags: Set[str] = Field(default_factory=set)
    memory_path: str
    raw_memory: str = ""

    def get_system_prompt(self) -> str:
        """Construct full system prompt with persona, leveling, and memory context."""
        return (
            f"# AGENT PERSONA: {self.name} ({self.role})\n"
            f"- **Level / Hierarchy:** {self.level} | Reports To: {self.reports_to}\n"
            f"- **Department / Pod:** {self.department}\n"
            f"- **Core KPI:** {self.kpi or 'Zero-drift, enterprise-grade engineering excellence'}\n"
            f"- **Catchphrase:** {self.catchphrase or 'Executing with precision.'}\n\n"
            f"## ACTIVE CONTEXT & EPISODIC MEMORY:\n"
            f"{self.raw_memory[:3000]}\n"
        )


class AgentLoader:
    """
    Scans and manages the complete roster of 80+ Omniverse Tech agents.
    """

    def __init__(self, memories_dir: Optional[Path] = None):
        self.memories_dir = memories_dir or CONFIG.memories_dir
        self._cache: Dict[str, OmniverseAgent] = {}

    def load_agent(self, agent_id: str) -> Optional[OmniverseAgent]:
        """Load an individual agent persona from disk."""
        if agent_id in self._cache:
            return self._cache[agent_id]

        file_path = self.memories_dir / f"{agent_id}.md"
        if not file_path.exists():
            return None

        content = file_path.read_text(encoding="utf-8")
        
        name_m = re.search(r"\*\*(?:Full\s+)?Name:\*\*\s*(.+)", content)
        role_m = re.search(r"\*\*Role(?:\s*&\s*Title)?:\*\*\s*(.+)", content)
        dept_m = re.search(r"\*\*Department(?:\s*/\s*Division)?:\*\*\s*(.+)", content)
        level_m = re.search(r"\*\*(?:Silicon Valley\s+)?Level(?:ing)?:\*\*\s*(.+)", content)
        mbti_m = re.search(r"\*\*MBTI(?:\s*&\s*Cognitive Temperament)?:\*\*\s*\*{0,2}([A-Z]{4})\*{0,2}", content)
        rep_m = re.search(r"\*\*(?:(?:Direct Manager\s*/\s*)?Reporting Line|Reports To):\*\*\s*(.+)", content)
        phrase_m = re.search(r"\*\*(?:Signature Philosophy\s*/\s*)?(?:Personal\s+)?Catchphrase:\*\*\s*\"?([^\n\"]+)\"?", content)
        kpi_m = re.search(r"\*\*KPI(?:\s*/\s*Objectives)?:\*\*\s*(.+)", content)


        agent = OmniverseAgent(
            agent_id=agent_id,
            name=name_m.group(1).strip() if name_m else agent_id.replace("_", " ").title(),
            role=role_m.group(1).strip() if role_m else "Autonomous Specialist",
            department=dept_m.group(1).strip() if dept_m else "Omniverse Tech",
            level=level_m.group(1).strip() if level_m else "L5 / Senior Engineer",
            mbti=mbti_m.group(1).strip() if mbti_m else None,
            reports_to=rep_m.group(1).strip() if rep_m else "exec_ceo_alexander_vance",
            catchphrase=phrase_m.group(1).strip() if phrase_m else None,
            kpi=kpi_m.group(1).strip() if kpi_m else None,
            memory_path=str(file_path),
            raw_memory=content
        )
        self._cache[agent_id] = agent
        return agent

    def load_all_agents(self) -> Dict[str, OmniverseAgent]:
        """Load all agents in the memories directory."""
        if not self.memories_dir.exists():
            return {}

        for md_file in self.memories_dir.glob("*.md"):
            if md_file.name == "archive_summary.md":
                continue
            self.load_agent(md_file.stem)

        return self._cache
