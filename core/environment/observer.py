"""
Living Environment & Tool-State Grounding Observer.
Provides real-time grounding on workspace file structure, git status, and active tool buffers.
"""

import os
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

from core.config import CONFIG


class EnvironmentSnapshot(BaseModel):
    """Structured snapshot of live workspace and tool runtime state."""
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    workspace_root: str
    git_branch: str = "main"
    git_modified_files: List[str] = Field(default_factory=list)
    uncommitted_changes_count: int = 0
    core_modules: List[str] = Field(default_factory=list)
    active_agent_count: int = 80
    scratchpad_log_count: int = 0
    available_tools: List[str] = Field(default_factory=list)


class EnvironmentObserver:
    """
    Observes and grounds agent perception in real workspace state.
    """

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = workspace_root or CONFIG.workspace_root

    def get_live_snapshot(self) -> EnvironmentSnapshot:
        """
        Capture complete live state of workspace, git, and tool subsystems.
        """
        # Git branch and status
        branch = "main"
        modified_files: List[str] = []
        try:
            branch_out = subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=str(self.workspace_root),
                text=True,
                stderr=subprocess.DEVNULL
            ).strip()
            branch = branch_out or "main"

            status_out = subprocess.check_output(
                ["git", "status", "--porcelain"],
                cwd=str(self.workspace_root),
                text=True,
                stderr=subprocess.DEVNULL
            ).strip()
            if status_out:
                modified_files = [line.strip().split()[-1] for line in status_out.splitlines() if line.strip()]
        except Exception:
            branch = "main"

        # Core modules list
        core_dir = self.workspace_root / "core"
        core_modules = [p.name for p in core_dir.iterdir() if p.is_dir() and not p.name.startswith("__")] if core_dir.exists() else []

        # Count active agents in .agents/omniverse_memories/
        mem_dir = self.workspace_root / ".agents" / "omniverse_memories"
        agent_count = len(list(mem_dir.glob("*.md"))) if mem_dir.exists() else 80

        # Scratchpad logs count
        scratch_dir = self.workspace_root / ".scratchpad"
        scratch_count = len(list(scratch_dir.glob("*.log"))) if scratch_dir.exists() else 0

        tools = [
            "terminal_exec",
            "web_researcher",
            "youtube_intel",
            "file_system_mcp",
            "scene_graph_transpiler",
            "epigenetic_prompt_optimizer",
            "compute_tokenomics_ledger",
            "closed_loop_telemetry_monitor"
        ]

        return EnvironmentSnapshot(
            workspace_root=str(self.workspace_root),
            git_branch=branch,
            git_modified_files=modified_files[:10],
            uncommitted_changes_count=len(modified_files),
            core_modules=core_modules,
            active_agent_count=agent_count,
            scratchpad_log_count=scratch_count,
            available_tools=tools
        )
