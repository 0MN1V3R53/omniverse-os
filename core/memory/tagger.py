"""
Semantic Tagging Parser and Inverted Index for Agent Lookup.
Parses agent memory files, extracts capabilities, and builds inverted index.
"""

import re
from pathlib import Path
from typing import Dict, List, Set, Optional, Any
from pydantic import BaseModel, Field
from core.config import CONFIG


class AgentProfile(BaseModel):
    """Structured persona profile extracted from markdown memory."""
    agent_id: str
    name: str
    role: str
    department: str
    level: str
    mbti: Optional[str] = None
    reports_to: Optional[str] = None
    skills: Set[str] = Field(default_factory=set)
    tags: Set[str] = Field(default_factory=set)
    file_path: str


class SemanticTagger:
    """
    Parses Markdown headers, frontmatter, and semantic indicators across
    agent memory folders to build a high-speed inverted lookup index.
    """

    # Keyword mappings to canonical semantic tags
    TAG_PATTERNS = {
        "frontend": [r"\bfrontend\b", r"\bnext\.?js\b", r"\breact\b", r"\bcss\b", r"\btailwind\b", r"\bui\b", r"\bux\b", r"\ba11y\b", r"\baccessibility\b"],
        "devops": [r"\bdevops\b", r"\bsre\b", r"\bcloud\b", r"\bhostinger\b", r"\bssh\b", r"\brsync\b", r"\bnginx\b", r"\bapache\b", r"\bhtacces\b", r"\bdocker\b"],
        "seo": [r"\bseo\b", r"\brank\b", r"\bserp\b", r"\bschema\b", r"\bgooglebot\b", r"\bkeywords?\b", r"\bcitations?\b", r"\bgsc\b"],
        "security": [r"\bsecurity\b", r"\bciso\b", r"\bauth\b", r"\bcrypto\b", r"\bpenetration\b", r"\bzero-trust\b", r"\bfirewall\b", r"\banti-theft\b"],
        "3d_graphics": [r"\b3d\b", r"\bwebgl\b", r"\bthree\.?js\b", r"\bshaders?\b", r"\bdraco\b", r"\bblender\b", r"\bcanvas\b"],
        "web3": [r"\bweb3\b", r"\bsolidity\b", r"\bsmart contract\b", r"\brpc\b", r"\bledger\b", r"\bblockchain\b", r"\bwallet\b"],
        "mobile_android": [r"\bandroid\b", r"\bkotlin\b", r"\bcompose\b", r"\bgradle\b", r"\bndk\b", r"\bapk\b"],
        "qa_testing": [r"\bqa\b", r"\btest(?:ing|s)?\b", r"\bverifier\b", r"\bquality\b", r"\bvalidation\b", r"\bautomation\b"],
        "data_science": [r"\bdata\b", r"\btelemetry\b", r"\banalytics\b", r"\battribution\b", r"\bforensic\b", r"\bgeoip\b"],
        "growth_marketing": [r"\bgrowth\b", r"\bmeta\b", r"\bcopywrit(?:er|ing)\b", r"\bcro\b", r"\bconversion\b", r"\bretention\b"],
        "executive": [r"\bceo\b", r"\bcpo\b", r"\bchro\b", r"\bexecutive\b", r"\borchestrat(?:or|ion)\b", r"\bdirector\b"]
    }

    def __init__(self, memories_dir: Optional[Path] = None):
        self.memories_dir = memories_dir or CONFIG.memories_dir
        self.profiles: Dict[str, AgentProfile] = {}
        self.tag_index: Dict[str, Set[str]] = {}
        self.build_index()

    def build_index(self) -> None:
        """Scan memories directory and build inverted index."""
        if not self.memories_dir.exists():
            return

        self.profiles.clear()
        self.tag_index.clear()

        for md_file in self.memories_dir.glob("*.md"):
            if md_file.name == "archive_summary.md":
                continue
            profile = self._parse_memory_file(md_file)
            if profile:
                self.profiles[profile.agent_id] = profile
                for tag in profile.tags:
                    if tag not in self.tag_index:
                        self.tag_index[tag] = set()
                    self.tag_index[tag].add(profile.agent_id)

    def _parse_memory_file(self, file_path: Path) -> Optional[AgentProfile]:
        """Extract profile information from Markdown text."""
        agent_id = file_path.stem
        content = file_path.read_text(encoding="utf-8")

        # Extract name & role
        name_match = re.search(r"\*\*(?:Full\s+)?Name:\*\*\s*(.+)", content)
        role_match = re.search(r"\*\*Role(?:\s*&\s*Title)?:\*\*\s*(.+)", content)
        dept_match = re.search(r"\*\*Department(?:\s*/\s*Division)?:\*\*\s*(.+)", content)
        level_match = re.search(r"\*\*(?:Silicon Valley\s+)?Level(?:ing)?:\*\*\s*(.+)", content)
        mbti_match = re.search(r"\*\*MBTI(?:\s*&\s*Cognitive Temperament)?:\*\*\s*\*{0,2}([A-Z]{4})\*{0,2}", content)
        reports_match = re.search(r"\*\*(?:(?:Direct Manager\s*/\s*)?Reporting Line|Reports To):\*\*\s*(.+)", content)


        name = name_match.group(1).strip() if name_match else agent_id.replace("_", " ").title()
        role = role_match.group(1).strip() if role_match else "Autonomous Specialist"
        dept = dept_match.group(1).strip() if dept_match else "Engineering"
        level = level_match.group(1).strip() if level_match else "L5 / Senior Specialist"
        mbti = mbti_match.group(1).strip() if mbti_match else None
        reports = reports_match.group(1).strip() if reports_match else "exec_ceo_alexander_vance"

        # Detect semantic tags
        tags = set()
        lower_content = content.lower()
        for tag, patterns in self.TAG_PATTERNS.items():
            for pat in patterns:
                if re.search(pat, lower_content):
                    tags.add(tag)
                    break

        return AgentProfile(
            agent_id=agent_id,
            name=name,
            role=role,
            department=dept,
            level=level,
            mbti=mbti,
            reports_to=reports,
            skills=tags,
            tags=tags,
            file_path=str(file_path)
        )

    def find_agents_by_tag(self, tag: str) -> List[AgentProfile]:
        """Return list of agent profiles tagged with a specific tag."""
        agent_ids = self.tag_index.get(tag, set())
        return [self.profiles[aid] for aid in agent_ids if aid in self.profiles]

    def find_agent_by_id(self, agent_id: str) -> Optional[AgentProfile]:
        """Fetch a specific agent profile."""
        return self.profiles.get(agent_id)

    def route_task_to_agent(self, task_description: str) -> Optional[AgentProfile]:
        """
        Heuristic semantic router matching a task description to the most qualified agent.
        """
        task_lower = task_description.lower()
        scored_agents: Dict[str, int] = {}

        for tag, patterns in self.TAG_PATTERNS.items():
            match_count = 0
            for pat in patterns:
                if re.search(pat, task_lower):
                    match_count += 1
            if match_count > 0:
                for aid in self.tag_index.get(tag, set()):
                    scored_agents[aid] = scored_agents.get(aid, 0) + match_count

        if not scored_agents:
            return self.profiles.get("exec_ceo_alexander_vance")

        # Pick highest scoring agent (breaking ties by level L8 > L7 > L6 > L5)
        def level_rank(p: AgentProfile) -> int:
            if "L8" in p.level: return 8
            if "L7" in p.level: return 7
            if "L6" in p.level: return 6
            if "L5" in p.level: return 5
            return 4

        sorted_agents = sorted(
            scored_agents.keys(),
            key=lambda aid: (scored_agents[aid], level_rank(self.profiles[aid])),
            reverse=True
        )
        return self.profiles.get(sorted_agents[0])
