"""
Epigenetic Prompt Optimizer & Reflexion Engine.
Analyzes ticket execution traces and mutates agent system prompts with learned constraints.
"""

import json
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

from core.config import CONFIG
from core.evolution.models import HeuristicRule, ReflexionReport, PromptVersion


class PromptEvolutionEngine:
    """
    Automated system prompt optimizer managed by the HR / Quality Pod.
    """

    def __init__(self, base_heuristics_dir: Optional[Path] = None):
        self.heuristics_dir = base_heuristics_dir or (CONFIG.agents_dir / "heuristics")
        self.heuristics_dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def _get_agent_dir(self, agent_id: str) -> Path:
        agent_dir = self.heuristics_dir / agent_id
        agent_dir.mkdir(parents=True, exist_ok=True)
        (agent_dir / "versions").mkdir(parents=True, exist_ok=True)
        return agent_dir

    def get_active_rules(self, agent_id: str) -> List[HeuristicRule]:
        """Fetch all active heuristic rules for an agent."""
        agent_dir = self._get_agent_dir(agent_id)
        rules_file = agent_dir / "heuristics.json"
        if not rules_file.exists():
            return []

        try:
            data = json.loads(rules_file.read_text(encoding="utf-8"))
            return [HeuristicRule(**r) for r in data if r.get("is_active", True)]
        except Exception:
            return []

    def add_heuristic_rule(self, agent_id: str, rule: HeuristicRule) -> None:
        """Directly append and persist a new heuristic rule for an agent."""
        agent_dir = self._get_agent_dir(agent_id)
        with self._lock:
            active_rules = self.get_active_rules(agent_id)
            active_rules.append(rule)

            # Save heuristics.json
            rules_file = agent_dir / "heuristics.json"
            rules_file.write_text(
                json.dumps([r.model_dump() for r in active_rules], default=str, indent=2),
                encoding="utf-8"
            )

            # Save heuristics.md
            md_file = agent_dir / "heuristics.md"
            md_content = f"# 🧬 Evolved Prompt Heuristics for `{agent_id}`\n"
            md_content += f"*Last Updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}*\n\n"
            md_content += "## 📜 Active Learned Invariants & Constraints\n"
            for r in active_rules:
                md_content += f"- **[{r.category.upper()}]** `{r.rule_text}` *(Derived from {r.source_ticket_id})*\n"
            md_file.write_text(md_content, encoding="utf-8")


    def evaluate_and_evolve(
        self,
        ticket_id: str,
        agent_id: str,
        execution_success: bool,
        error_or_defect: Optional[str] = None,
        category: str = "general"
    ) -> ReflexionReport:
        """
        Reflexion analysis: Derive a new hardened heuristic constraint if a defect occurred.
        """
        agent_dir = self._get_agent_dir(agent_id)

        if execution_success and not error_or_defect:
            report = ReflexionReport(
                ticket_id=ticket_id,
                agent_id=agent_id,
                success=True,
                critique="Execution completed cleanly with zero unresolved defects.",
                proposed_rule=None
            )
            return report

        # Failure mode detected -> generate reflective rule
        failure_msg = error_or_defect or "Sub-optimal execution or verifier rejection."
        rule_text = f"Enforce invariant validation: {failure_msg} must be verified before handoff."
        
        new_rule = HeuristicRule(
            category=category,
            rule_text=rule_text,
            rationale=f"Derived from post-execution critique on ticket {ticket_id}.",
            source_ticket_id=ticket_id,
            severity="MUST",
            is_active=True
        )

        with self._lock:
            # 1. Load existing rules
            active_rules = self.get_active_rules(agent_id)
            active_rules.append(new_rule)

            # 2. Save heuristics.json
            rules_file = agent_dir / "heuristics.json"
            rules_file.write_text(
                json.dumps([r.model_dump() for r in active_rules], default=str, indent=2),
                encoding="utf-8"
            )

            # 3. Write Markdown summary to heuristics.md
            md_file = agent_dir / "heuristics.md"
            md_content = f"# 🧬 Evolved Prompt Heuristics for `{agent_id}`\n"
            md_content += f"*Last Updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}*\n\n"
            md_content += "## 📜 Active Learned Invariants & Constraints\n"
            for r in active_rules:
                md_content += f"- **[{r.category.upper()}]** `{r.rule_text}` *(Derived from {r.source_ticket_id})*\n"
            md_file.write_text(md_content, encoding="utf-8")

            # 4. Save version snapshot
            v_num = len(list((agent_dir / "versions").glob("v*.json"))) + 1
            version_snapshot = PromptVersion(
                agent_id=agent_id,
                version_number=v_num,
                active_rules=active_rules
            )
            v_file = agent_dir / "versions" / f"v{v_num}.json"
            v_file.write_text(version_snapshot.model_dump_json(indent=2), encoding="utf-8")

        report = ReflexionReport(
            ticket_id=ticket_id,
            agent_id=agent_id,
            success=False,
            identified_failure_mode=failure_msg,
            critique=f"Defect analyzed on ticket {ticket_id}. Generated hardened rule {new_rule.rule_id}.",
            proposed_rule=new_rule
        )
        return report

    def inject_heuristics_into_prompt(self, agent_id: str, base_prompt: str) -> str:
        """Dynamically appends active learned heuristics to an agent's base system prompt."""
        active_rules = self.get_active_rules(agent_id)
        if not active_rules:
            return base_prompt

        heuristics_section = "\n\n## 🧬 Epigenetic Learned Invariants (Auto-Evolved)\n"
        heuristics_section += "The following rules were evolved from real-world execution audits and MUST be obeyed:\n"
        for r in active_rules:
            heuristics_section += f"- **[{r.category.upper()}]** {r.rule_text}\n"

        return base_prompt + heuristics_section

    def rollback_heuristics(self, agent_id: str, target_version: int) -> PromptVersion:
        """Rollback an agent's heuristics to an earlier version snapshot."""
        agent_dir = self._get_agent_dir(agent_id)
        v_file = agent_dir / "versions" / f"v{target_version}.json"
        if not v_file.exists():
            raise ValueError(f"Version snapshot v{target_version} does not exist for agent '{agent_id}'.")

        data = json.loads(v_file.read_text(encoding="utf-8"))
        restored = PromptVersion(**data)

        with self._lock:
            rules_file = agent_dir / "heuristics.json"
            rules_file.write_text(
                json.dumps([r.model_dump() for r in restored.active_rules], default=str, indent=2),
                encoding="utf-8"
            )

        return restored
