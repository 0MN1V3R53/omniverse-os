"""
Standardized Sandboxed Tool Interfaces.
Exposes containerized terminal execution and high-speed symbol lookups to all 81 enterprise agents.
"""

from typing import Dict, List, Optional, Any
from pathlib import Path

from core.sandbox.container_runner import GLOBAL_SANDBOX_RUNNER, ContainerConfig
from core.ast_engine.fast_indexer import GLOBAL_FAST_INDEXER
from core.ast_engine.navigator import GLOBAL_AST_NAVIGATOR


def sandboxed_terminal_exec(
    command: str,
    timeout_sec: int = 60,
    network: bool = False,
    cwd: Optional[str] = None
) -> Dict[str, Any]:
    """
    Execute a shell command inside an ephemeral containerized sandbox with CoW tmpfs,
    cgroup memory/CPU limits, and automatic subprocess fallback.
    """
    cfg = ContainerConfig(
        network_mode="bridge" if network else "none",
        timeout_sec=timeout_sec,
        workdir=cwd or "/workspace"
    )
    result = GLOBAL_SANDBOX_RUNNER.run_sandboxed(command, config=cfg)
    return {
        "command": result.command,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "exit_code": result.exit_code,
        "duration_ms": result.duration_ms,
        "is_containerized": result.is_containerized,
        "container_id": result.container_id
    }


def fast_symbol_lookup(
    symbol_name: str,
    symbol_type: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Query the persistent SQLite WAL symbol index for instantaneous sub-10ms symbol resolution.
    """
    # Ensure index is updated incrementally
    records = GLOBAL_FAST_INDEXER.lookup_symbol(symbol_name, symbol_type)
    if not records:
        # If cache miss, run quick incremental sync and retry
        GLOBAL_FAST_INDEXER.sync_incremental()
        records = GLOBAL_FAST_INDEXER.lookup_symbol(symbol_name, symbol_type)

    return [r.model_dump() for r in records]


def find_all_references(symbol_name: str) -> Dict[str, Any]:
    """
    Find all AST definitions and symbol usages across the enterprise codebase.
    """
    rep = GLOBAL_AST_NAVIGATOR.get_symbol_references(symbol_name)
    return rep.model_dump()
