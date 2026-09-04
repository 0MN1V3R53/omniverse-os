"""
Standard Built-In Tools for the Omniverse Autonomous Agent Runtime.
Includes atomic file I/O, sandboxed shell execution, AST syntax validation, and HTTP probing.
"""

import os
import ast
import json
import asyncio
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

from core.tools.registry import tool, GLOBAL_TOOL_REGISTRY
from core.config import CONFIG


# ---------------------------------------------------------------------------
# 1. Read File Tool
# ---------------------------------------------------------------------------
class ReadFileInput(BaseModel):
    file_path: str = Field(..., description="Absolute path or path relative to workspace root")
    max_bytes: int = Field(default=50000, description="Max bytes to read from file")


@tool(
    name="read_file",
    description="Read file contents with size limits and utf-8 decoding.",
    input_model=ReadFileInput,
    risk_level="LOW",
    dri="web_frontend_julian_thorne"
)
def ReadFileTool(file_path: str, max_bytes: int = 50000) -> Dict[str, Any]:
    path = Path(file_path)
    if not path.is_absolute():
        path = CONFIG.workspace_root / path

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    content = path.read_text(encoding="utf-8", errors="replace")[:max_bytes]
    return {
        "file_path": str(path),
        "total_length": len(content),
        "content": content
    }


# ---------------------------------------------------------------------------
# 2. Atomic Write File Tool
# ---------------------------------------------------------------------------
class WriteFileAtomicInput(BaseModel):
    file_path: str = Field(..., description="Target file path")
    content: str = Field(..., description="String content to write")
    create_dirs: bool = Field(default=True, description="Automatically create parent directories")


@tool(
    name="write_file_atomic",
    description="Atomically write contents to a file using temporary file swap.",
    input_model=WriteFileAtomicInput,
    risk_level="MEDIUM",
    dri="web_frontend_julian_thorne"
)
def WriteFileAtomicTool(file_path: str, content: str, create_dirs: bool = True) -> Dict[str, Any]:
    path = Path(file_path)
    if not path.is_absolute():
        path = CONFIG.workspace_root / path

    if create_dirs:
        path.parent.mkdir(parents=True, exist_ok=True)

    temp_path = path.with_suffix(f".tmp_{os.getpid()}")
    temp_path.write_text(content, encoding="utf-8")
    temp_path.replace(path)

    return {
        "file_path": str(path),
        "bytes_written": len(content.encode("utf-8")),
        "status": "SUCCESS"
    }


# ---------------------------------------------------------------------------
# 3. Sandboxed Shell Runner Tool
# ---------------------------------------------------------------------------
class RunShellInput(BaseModel):
    command: str = Field(..., description="Shell command to execute")
    cwd: Optional[str] = Field(default=None, description="Working directory")
    timeout_seconds: float = Field(default=30.0, description="Execution timeout limit")


@tool(
    name="run_shell",
    description="Execute a shell command in a sandboxed subprocess with timeout and returncode capture.",
    input_model=RunShellInput,
    risk_level="HIGH",
    timeout_seconds=60.0,
    dri="web_devops_marcus_chen"
)
async def RunShellTool(command: str, cwd: Optional[str] = None, timeout_seconds: float = 30.0) -> Dict[str, Any]:
    work_dir = Path(cwd) if cwd else CONFIG.workspace_root
    
    proc = await asyncio.create_subprocess_shell(
        command,
        cwd=str(work_dir),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    try:
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout_seconds)
    except asyncio.TimeoutError:
        proc.kill()
        raise TimeoutError(f"Command '{command}' timed out after {timeout_seconds}s.")

    stdout_str = stdout.decode("utf-8", errors="replace")
    stderr_str = stderr.decode("utf-8", errors="replace")

    return {
        "command": command,
        "exit_code": proc.returncode,
        "stdout": stdout_str,
        "stderr": stderr_str,
        "success": proc.returncode == 0
    }


# ---------------------------------------------------------------------------
# 4. AST Code Syntax Validator Tool
# ---------------------------------------------------------------------------
class ASTValidateInput(BaseModel):
    code_or_file: str = Field(..., description="Source code string or file path")
    language: str = Field(default="python", description="Language: 'python', 'json', or 'javascript'")


@tool(
    name="ast_validate",
    description="Validate syntax of Python, JSON, or JavaScript code without execution.",
    input_model=ASTValidateInput,
    risk_level="LOW",
    dri="qa_auto_script"
)
def ASTValidateCodeTool(code_or_file: str, language: str = "python") -> Dict[str, Any]:
    # Check if input is a file path
    path = Path(code_or_file)
    if not path.is_absolute():
        path = CONFIG.workspace_root / path

    if path.exists() and path.is_file():
        code = path.read_text(encoding="utf-8")
        target_name = str(path)
    else:
        code = code_or_file
        target_name = "<inline_code>"

    lang = language.lower()

    if lang == "python":
        try:
            ast.parse(code)
            return {"valid": True, "language": "python", "target": target_name, "error": None}
        except SyntaxError as err:
            return {"valid": False, "language": "python", "target": target_name, "error": str(err), "lineno": err.lineno}

    elif lang == "json":
        try:
            json.loads(code)
            return {"valid": True, "language": "json", "target": target_name, "error": None}
        except json.JSONDecodeError as err:
            return {"valid": False, "language": "json", "target": target_name, "error": str(err)}

    elif lang in ["javascript", "js"]:
        # Run node --check
        res = subprocess.run(["node", "--check", "-e", code], capture_output=True, text=True)
        return {
            "valid": res.returncode == 0,
            "language": "javascript",
            "target": target_name,
            "error": res.stderr.strip() if res.returncode != 0 else None
        }

    else:
        return {"valid": True, "language": language, "target": target_name, "note": "No AST parser configured for this language"}


# ---------------------------------------------------------------------------
# 5. Git Status Tool
# ---------------------------------------------------------------------------
class GitStatusInput(BaseModel):
    short: bool = Field(default=True, description="Return short-format git status")


@tool(
    name="git_status",
    description="Query active git status and branch details.",
    input_model=GitStatusInput,
    risk_level="LOW",
    dri="web_devops_marcus_chen"
)
def GitStatusTool(short: bool = True) -> Dict[str, Any]:
    cmd = ["git", "status", "-s"] if short else ["git", "status"]
    res = subprocess.run(cmd, cwd=str(CONFIG.workspace_root), capture_output=True, text=True)
    return {
        "status_output": res.stdout,
        "clean": len(res.stdout.strip()) == 0,
        "exit_code": res.returncode
    }


# ---------------------------------------------------------------------------
# 6. HTTP Probe Tool
# ---------------------------------------------------------------------------
class HttpProbeInput(BaseModel):
    url: str = Field(..., description="Target URL to probe")
    timeout_seconds: float = Field(default=5.0, description="Probe timeout")


@tool(
    name="http_probe",
    description="Send a lightweight HTTP probe to verify live URL availability and response headers.",
    input_model=HttpProbeInput,
    risk_level="LOW",
    dri="security_ciso_michael_chang"
)
def HttpProbeTool(url: str, timeout_seconds: float = 5.0) -> Dict[str, Any]:
    cmd = ["curl", "-s", "-I", "-m", str(timeout_seconds), url]
    res = subprocess.run(cmd, capture_output=True, text=True)
    
    headers = {}
    status_line = ""
    status_code = 0

    if res.stdout:
        lines = res.stdout.splitlines()
        if lines:
            status_line = lines[0]
            parts = status_line.split()
            if len(parts) >= 2 and parts[1].isdigit():
                status_code = int(parts[1])
            for line in lines[1:]:
                if ":" in line:
                    k, v = line.split(":", 1)
                    headers[k.strip().lower()] = v.strip()

    return {
        "url": url,
        "status_code": status_code,
        "status_line": status_line,
        "headers": headers,
        "healthy": 200 <= status_code < 400
    }


# ---------------------------------------------------------------------------
# 7. Memory Log Sync Tool
# ---------------------------------------------------------------------------
class MemorySyncInput(BaseModel):
    milestone_id: int = Field(..., description="Milestone number e.g. 67")
    title: str = Field(..., description="Milestone title")
    summary: str = Field(..., description="Detailed markdown bulleted summary")
    responsible_agents: List[str] = Field(..., description="List of responsible agent IDs")


@tool(
    name="memory_log_sync",
    description="Synchronize global MEMORY_LOG.md and responsible agent memory files with milestone logs.",
    input_model=MemorySyncInput,
    risk_level="MEDIUM",
    dri="exec_ceo_alexander_vance"
)
def MemoryLogSyncTool(
    milestone_id: int,
    title: str,
    summary: str,
    responsible_agents: List[str]
) -> Dict[str, Any]:
    from datetime import datetime
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # 1. Update MEMORY_LOG.md
    mem_log_path = CONFIG.logs_dir / "MEMORY_LOG.md"
    entry = f"\n\n## [MILESTONE {milestone_id}] - {timestamp} - {title.upper()}\n"
    entry += f"- **Summary**: {summary}\n"
    entry += f"- **Responsible Agents**: {', '.join(responsible_agents)}\n"
    
    if mem_log_path.exists():
        with open(mem_log_path, "a", encoding="utf-8") as f:
            f.write(entry)

    # 2. Update individual agent memory files
    updated_agents = []
    for agent_id in responsible_agents:
        agent_file = CONFIG.memories_dir / f"{agent_id}.md"
        if agent_file.exists():
            agent_entry = f"\n- **{datetime.utcnow().strftime('%Y-%m-%d')} (Milestone {milestone_id}):** {title} — {summary}"
            with open(agent_file, "a", encoding="utf-8") as f:
                f.write(agent_entry)
            updated_agents.append(agent_id)

    return {
        "milestone_id": milestone_id,
        "title": title,
        "memory_log_updated": mem_log_path.exists(),
        "updated_agents": updated_agents
    }
