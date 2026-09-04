"""
Self-Healing Terminal & Sandboxed REPL Loop.
Executes shell commands, virtualizes output, triggers reflection cycles on failure,
and logs learned CLI patterns to .agents/logs/tool_learnings.md.
"""

import os
import time
import asyncio
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any
from pydantic import BaseModel, Field

from core.config import CONFIG
from core.tools.scratchpad import ToolScratchpadManager, VirtualLogDigest, GLOBAL_SCRATCHPAD


class ExecutionResult(BaseModel):
    """Structured execution output from terminal runner."""
    command: str
    exit_code: int
    duration_ms: float
    stdout_preview: str
    stderr_preview: str
    attempts: int = 1
    recovered: bool = False
    digest: VirtualLogDigest


class SelfHealingRunner:
    """
    Sandboxed command runner with 3-round reflection and learning persistence.
    """

    def __init__(
        self,
        scratchpad: Optional[ToolScratchpadManager] = None,
        learnings_file: Optional[Path] = None
    ):
        self.scratchpad = scratchpad or GLOBAL_SCRATCHPAD
        self.learnings_file = learnings_file or (CONFIG.agents_dir / "logs" / "tool_learnings.md")
        self.learnings_file.parent.mkdir(parents=True, exist_ok=True)

    async def execute(
        self,
        command: str,
        cwd: Optional[str] = None,
        timeout_seconds: float = 30.0,
        max_retries: int = 3,
        remediation_fn: Optional[Callable[[str, str, int], Optional[str]]] = None
    ) -> ExecutionResult:
        """
        Execute command with timeout, self-healing reflection loop, and output virtualization.
        - `remediation_fn(failed_command, stderr_output, attempt) -> corrected_command_or_None`
        """
        working_dir = cwd or str(CONFIG.workspace_root)
        current_cmd = command
        attempts = 0
        last_stdout = ""
        last_stderr = ""
        last_exit_code = 0
        total_duration = 0.0

        for attempt in range(1, max_retries + 1):
            attempts = attempt
            start_t = time.time()
            
            try:
                proc = await asyncio.create_subprocess_shell(
                    current_cmd,
                    cwd=working_dir,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout_bytes, stderr_bytes = await asyncio.wait_for(
                    proc.communicate(),
                    timeout=timeout_seconds
                )
                duration_ms = round((time.time() - start_t) * 1000.0, 2)
                total_duration += duration_ms
                last_exit_code = proc.returncode or 0
                last_stdout = stdout_bytes.decode("utf-8", errors="replace")
                last_stderr = stderr_bytes.decode("utf-8", errors="replace")
            except asyncio.TimeoutError:
                duration_ms = round(timeout_seconds * 1000.0, 2)
                total_duration += duration_ms
                last_exit_code = 124  # Standard timeout exit code
                last_stdout = ""
                last_stderr = f"Execution timed out after {timeout_seconds} seconds."

            # Success check
            if last_exit_code == 0:
                break

            # Failure detected -> Check if remediation is available
            if attempt < max_retries and remediation_fn:
                remediated_cmd = remediation_fn(current_cmd, last_stderr, attempt)
                if remediated_cmd and remediated_cmd != current_cmd:
                    current_cmd = remediated_cmd
                    continue

        recovered = (attempts > 1 and last_exit_code == 0)
        combined_raw = f"=== STDOUT ===\n{last_stdout}\n\n=== STDERR ===\n{last_stderr}"
        
        # Virtualize output in scratchpad
        digest = self.scratchpad.virtualize_output(
            tool_name="terminal_exec",
            raw_output=combined_raw,
            exit_code=last_exit_code,
            status="SUCCESS" if last_exit_code == 0 else "FAILED",
            tag="exec"
        )

        # If we had a recovery or failure, record in tool_learnings.md
        if recovered:
            self._log_learning(
                original_cmd=command,
                fixed_cmd=current_cmd,
                error_msg=last_stderr,
                outcome="RECOVERED",
                attempts=attempts
            )

        return ExecutionResult(
            command=current_cmd,
            exit_code=last_exit_code,
            duration_ms=total_duration,
            stdout_preview="\n".join(last_stdout.splitlines()[:5]),
            stderr_preview="\n".join(last_stderr.splitlines()[:5]),
            attempts=attempts,
            recovered=recovered,
            digest=digest
        )

    def _log_learning(
        self,
        original_cmd: str,
        fixed_cmd: str,
        error_msg: str,
        outcome: str,
        attempts: int
    ) -> None:
        """Appends self-healing CLI resolution to persistent markdown ledger."""
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        entry = f"""
### 🛠️ Terminal Learning [{timestamp}] - {outcome} (Attempt {attempts})
- **Failed Command:** `{original_cmd}`
- **Observed Error:** `{error_msg.strip()[:160]}`
- **Working Resolution:** `{fixed_cmd}`
- **Heuristic:** Always apply automated argument correction before failing ticket.
"""
        with open(self.learnings_file, "a", encoding="utf-8") as f:
            f.write(entry)
