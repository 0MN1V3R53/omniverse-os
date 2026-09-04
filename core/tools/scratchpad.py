"""
Tool Output Virtualization and Scratchpad Engine.
Prevents LLM context bloat by writing heavy raw tool outputs to temporary .scratchpad/ buffers
and returning concise Pydantic digests with slice & grep affordances.
"""

import os
import uuid
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

from core.config import CONFIG


class VirtualLogDigest(BaseModel):
    """Concise summary of virtualized tool execution output returned to LLM."""
    digest_id: str = Field(default_factory=lambda: f"DIGEST-{uuid.uuid4().hex[:8].upper()}")
    tool_name: str
    status: str = "SUCCESS"  # SUCCESS, FAILED, TIMEOUT
    exit_code: int = 0
    total_lines: int = 0
    total_bytes: int = 0
    head_preview: List[str] = Field(default_factory=list)
    tail_preview: List[str] = Field(default_factory=list)
    log_reference_path: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ToolScratchpadManager:
    """
    Manages virtualization and disk buffering of heavy tool payloads.
    """

    def __init__(self, scratchpad_dir: Optional[Path] = None):
        self.scratchpad_dir = scratchpad_dir or (CONFIG.workspace_root / ".scratchpad")
        self.scratchpad_dir.mkdir(parents=True, exist_ok=True)

    def virtualize_output(
        self,
        tool_name: str,
        raw_output: str,
        exit_code: int = 0,
        status: str = "SUCCESS",
        tag: str = "output",
        preview_lines: int = 4
    ) -> VirtualLogDigest:
        """
        Dumps raw output to .scratchpad/ and generates a lightweight VirtualLogDigest.
        """
        timestamp_str = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        log_filename = f"{timestamp_str}_{tool_name}_{tag}_{uuid.uuid4().hex[:6]}.log"
        log_path = self.scratchpad_dir / log_filename

        log_path.write_text(raw_output, encoding="utf-8")

        lines = raw_output.splitlines()
        total_lines = len(lines)
        total_bytes = len(raw_output.encode("utf-8"))

        head_preview = lines[:preview_lines]
        tail_preview = lines[-preview_lines:] if total_lines > preview_lines else []

        return VirtualLogDigest(
            tool_name=tool_name,
            status=status,
            exit_code=exit_code,
            total_lines=total_lines,
            total_bytes=total_bytes,
            head_preview=head_preview,
            tail_preview=tail_preview,
            log_reference_path=str(log_path)
        )

    def grep_scratchpad(
        self,
        log_reference_path: str,
        pattern: str,
        max_matches: int = 20,
        case_insensitive: bool = True
    ) -> Dict[str, Any]:
        """
        Targeted pattern search inside a virtualized scratchpad log file.
        """
        path = Path(log_reference_path)
        if not path.exists():
            return {"error": f"Log file not found: {log_reference_path}", "matches": []}

        flags = re.IGNORECASE if case_insensitive else 0
        compiled_re = re.compile(pattern, flags)
        matches: List[Dict[str, Any]] = []

        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line_idx, line in enumerate(f, 1):
                if compiled_re.search(line):
                    matches.append({"line_number": line_idx, "content": line.rstrip("\r\n")})
                    if len(matches) >= max_matches:
                        break

        return {
            "log_path": str(path),
            "pattern": pattern,
            "match_count": len(matches),
            "matches": matches
        }

    def read_slice(
        self,
        log_reference_path: str,
        start_line: int = 1,
        end_line: int = 50
    ) -> Dict[str, Any]:
        """
        Read a specific slice of lines from a virtualized log file.
        """
        path = Path(log_reference_path)
        if not path.exists():
            return {"error": f"Log file not found: {log_reference_path}", "lines": []}

        lines_out = []
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line_idx, line in enumerate(f, 1):
                if start_line <= line_idx <= end_line:
                    lines_out.append({"line_number": line_idx, "content": line.rstrip("\r\n")})
                elif line_idx > end_line:
                    break

        return {
            "log_path": str(path),
            "start_line": start_line,
            "end_line": end_line,
            "lines": lines_out
        }


# Global Scratchpad Singleton
GLOBAL_SCRATCHPAD = ToolScratchpadManager()
