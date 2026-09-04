"""
Pre-Flight Idempotency & Reusability Auditor.
Scans memory banks, logs, and codebase to avoid duplicate generation and link existing modules.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Any

from core.config import CONFIG
from core.dialectic.models import PreFlightAuditReport


class PreFlightAuditor:
    """
    Audits incoming task objectives against workspace memory and codebase state.
    """

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = workspace_root or CONFIG.workspace_root
        self.agents_dir = self.workspace_root / ".agents"
        self.context_dir = self.workspace_root / "context"

    def audit_objective(self, objective: str) -> PreFlightAuditReport:
        """
        Execute three-pillar pre-flight audit for a task objective.
        """
        keywords = [w.lower() for w in objective.replace("_", " ").split() if len(w) > 3]
        reusable_modules: List[str] = []
        existing_artifacts: List[str] = []
        recorded_pitfalls: List[str] = []

        # 1. Scan codebase for relevant existing modules
        core_dir = self.workspace_root / "core"
        if core_dir.exists():
            for py_file in core_dir.glob("**/*.py"):
                file_text = py_file.name.lower()
                if any(kw in file_text for kw in keywords):
                    reusable_modules.append(str(py_file.relative_to(self.workspace_root)))

        # 2. Scan .agents/context/ and research briefs
        briefs_dir = self.agents_dir / "context" / "research_briefs"
        if briefs_dir.exists():
            for md_file in briefs_dir.glob("*.md"):
                if any(kw in md_file.name.lower() for kw in keywords):
                    existing_artifacts.append(str(md_file.relative_to(self.workspace_root)))

        # 3. Scan tool learnings for pitfalls
        learnings_file = self.agents_dir / "logs" / "tool_learnings.md"
        if learnings_file.exists():
            content = learnings_file.read_text(encoding="utf-8")
            for line in content.splitlines():
                if line.startswith("- **Failed Command:**") or line.startswith("- **Observed Error:**"):
                    recorded_pitfalls.append(line.strip("- *").strip())
                    if len(recorded_pitfalls) >= 3:
                        break

        # Determine idempotency and recommendation
        is_idempotent = False
        recommendation = "PROCEED_WITH_DIALECTIC"
        readiness_score = 1.0

        if len(reusable_modules) >= 3 and len(existing_artifacts) >= 2:
            recommendation = "REUSE_EXISTING_AND_EXTEND"
            readiness_score = 0.95

        return PreFlightAuditReport(
            ticket_objective=objective,
            is_idempotent=is_idempotent,
            reusable_modules=reusable_modules[:5],
            existing_artifacts=existing_artifacts[:5],
            recorded_pitfalls=recorded_pitfalls,
            readiness_score=readiness_score,
            recommendation=recommendation
        )
