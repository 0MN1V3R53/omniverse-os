"""
Organizational Morphogenesis Engine.
Enables dynamic agent lifecycle management: Just-In-Time Specialist Spawning, Inactivity Pruning, and Memory Consolidation.
"""

import shutil
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

from core.config import CONFIG


class DynamicAgentRecord(BaseModel):
    """Metadata tracking a dynamically spawned specialist agent."""
    agent_id: str
    role_title: str
    parent_pod: str
    spawn_reason: str
    cycles_active: int = 1
    is_active: bool = True
    persisted_path: str
    spawned_at: datetime = Field(default_factory=datetime.utcnow)


class MorphogenesisEngine:
    """
    Manages organizational morphing, dynamic specialist creation, and episodic consolidation.
    """

    def __init__(self, dynamic_dir: Optional[Path] = None):
        self.dynamic_dir = dynamic_dir or (CONFIG.agents_dir / "dynamic")
        self.archive_dir = self.dynamic_dir / "archive"
        self.dynamic_dir.mkdir(parents=True, exist_ok=True)
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        self.active_agents: Dict[str, DynamicAgentRecord] = {}

    def spawn_specialist_agent(
        self,
        specialist_name: str,
        role_title: str,
        parent_pod: str,
        spawn_reason: str
    ) -> DynamicAgentRecord:
        """
        Dynamically generates and registers a new specialist persona.
        """
        agent_id = f"dynamic_{specialist_name.lower().replace(' ', '_')}"
        agent_file = self.dynamic_dir / f"{agent_id}.md"

        persona_content = f"""# 🤖 Dynamic Specialist Persona: {role_title} (`{agent_id}`)
*Spawned dynamically by `{parent_pod}` on {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}*
*Reason: {spawn_reason}*

## Core Mandate & Competencies
- Dedicated specialist for: {spawn_reason}
- Direct reporting line: `{parent_pod} Lead`
- Strict compliance with `rules/agent_cognition_rules.md` and Zero-Drift Mandate.

## Active Tool Affordances
- `terminal_exec`
- `file_system_mcp`
- `scratchpad_virtualizer`
"""
        agent_file.write_text(persona_content, encoding="utf-8")

        record = DynamicAgentRecord(
            agent_id=agent_id,
            role_title=role_title,
            parent_pod=parent_pod,
            spawn_reason=spawn_reason,
            cycles_active=1,
            is_active=True,
            persisted_path=str(agent_file)
        )
        self.active_agents[agent_id] = record
        return record

    def prune_and_consolidate(self, max_idle_cycles: int = 3) -> List[str]:
        """
        Prunes idle dynamic agents, consolidates their memory, and archives personas.
        """
        pruned: List[str] = []
        for agent_id, record in list(self.active_agents.items()):
            if record.cycles_active >= max_idle_cycles:
                record.is_active = False
                source_file = Path(record.persisted_path)
                if source_file.exists():
                    # Consolidate knowledge into parent pod context
                    context_dir = CONFIG.agents_dir / "context"
                    context_dir.mkdir(parents=True, exist_ok=True)
                    cons_file = context_dir / "consolidated_dynamic_memory.md"
                    with open(cons_file, "a", encoding="utf-8") as f:
                        f.write(f"\n### 📦 Consolidated Memory: `{agent_id}` ({record.role_title})\n- Reason: {record.spawn_reason}\n- Archived: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")

                    # Move file to archive
                    dest_file = self.archive_dir / source_file.name
                    shutil.move(str(source_file), str(dest_file))
                    record.persisted_path = str(dest_file)

                pruned.append(agent_id)
                del self.active_agents[agent_id]

        return pruned
