"""
Configuration settings for the Omniverse Autonomous Agent Runtime.
"""

from pathlib import Path
from typing import Dict, Any
from pydantic import BaseModel, Field


class RuntimeConfig(BaseModel):
    """Global runtime configuration with default paths and enterprise limits."""
    
    # Filesystem Paths
    workspace_root: Path = Field(
        default_factory=lambda: Path("/Users/silversurfer/Documents/Omniverse2")
    )
    agents_dir: Path = Field(
        default_factory=lambda: Path("/Users/silversurfer/Documents/Omniverse2/.agents")
    )
    memories_dir: Path = Field(
        default_factory=lambda: Path("/Users/silversurfer/Documents/Omniverse2/.agents/omniverse_memories")
    )
    rules_dir: Path = Field(
        default_factory=lambda: Path("/Users/silversurfer/Documents/Omniverse2/.agents/rules")
    )
    logs_dir: Path = Field(
        default_factory=lambda: Path("/Users/silversurfer/Documents/Omniverse2/.agents/logs")
    )
    checkpoint_db_path: Path = Field(
        default_factory=lambda: Path("/Users/silversurfer/Documents/Omniverse2/.agents/logs/runtime_checkpoints.sqlite")
    )
    traces_log_path: Path = Field(
        default_factory=lambda: Path("/Users/silversurfer/Documents/Omniverse2/.agents/logs/runtime_traces.jsonl")
    )
    memory_archive_path: Path = Field(
        default_factory=lambda: Path("/Users/silversurfer/Documents/Omniverse2/.agents/omniverse_memories/archive_summary.md")
    )

    # Memory & Compaction Thresholds
    max_agent_memory_tokens: int = 4000
    token_chars_ratio: float = 4.0  # Approx 4 characters per token
    archive_batch_size: int = 5

    # Telemetry & Safety
    max_delegation_depth: int = 15
    max_cyclic_repeats: int = 3
    circuit_breaker_enabled: bool = True
    
    # Tool Execution Sandboxing
    default_tool_timeout_seconds: float = 30.0
    strict_sandbox_mode: bool = True
    
    # Quality Gates & Verification
    strict_quality_gates: bool = True
    require_consensus_signoff: bool = True

    class Config:
        arbitrary_types_allowed = True


# Global Singleton Config Instance
CONFIG = RuntimeConfig()
