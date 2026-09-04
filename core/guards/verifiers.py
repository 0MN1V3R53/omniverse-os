"""
Deterministic Domain Verifier Nodes for Build, Security, and Code Quality Gates.
"""

import ast
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from core.config import CONFIG


class ASTSyntaxVerifier:
    """Verifies that generated or edited source code parses cleanly."""
    
    @staticmethod
    def verify_python(code_or_path: str) -> Dict[str, Any]:
        path = Path(code_or_path)
        if path.exists() and path.is_file():
            code = path.read_text(encoding="utf-8")
        else:
            code = code_or_path

        try:
            ast.parse(code)
            return {"passed": True, "error": None}
        except SyntaxError as err:
            return {"passed": False, "error": f"Python SyntaxError at line {err.lineno}: {err.msg}"}

    @staticmethod
    def verify_json(code_or_path: str) -> Dict[str, Any]:
        path = Path(code_or_path)
        if path.exists() and path.is_file():
            code = path.read_text(encoding="utf-8")
        else:
            code = code_or_path

        try:
            json.loads(code)
            return {"passed": True, "error": None}
        except json.JSONDecodeError as err:
            return {"passed": False, "error": f"JSONDecodeError at pos {err.pos}: {err.msg}"}


class ZeroDriftVerifier:
    """Enforces strict zero-drift & zero-mock directive across files."""
    
    MOCK_PATTERNS = [
        r"\blorem\s+ipsum\b",
        r"\bmock_data\b",
        r"\bdummy_profile\b",
        r"\bfake_ranking\b",
        r"\bsynthetic_traffic\b",
        r"test@example\.com"
    ]

    @classmethod
    def verify_file(cls, file_path: str) -> Dict[str, Any]:
        path = Path(file_path)
        if not path.is_absolute():
            path = CONFIG.workspace_root / path

        if not path.exists():
            return {"passed": False, "error": f"File '{file_path}' does not exist."}

        content = path.read_text(encoding="utf-8", errors="replace")
        found_violations = []

        for pat in cls.MOCK_PATTERNS:
            match = re.search(pat, content, re.IGNORECASE)
            if match:
                found_violations.append(match.group(0))

        if found_violations:
            return {
                "passed": False,
                "error": f"Zero-Drift violation detected: {found_violations} in {path.name}",
                "violations": found_violations
            }
        return {"passed": True, "error": None}


class ExitCodeVerifier:
    """Verifies that an execution exit code is strictly 0."""
    @staticmethod
    def verify(exit_code: int, command: str = "") -> Dict[str, Any]:
        return {
            "passed": exit_code == 0,
            "exit_code": exit_code,
            "error": f"Command '{command}' exited with non-zero status {exit_code}." if exit_code != 0 else None
        }


class HttpHeaderVerifier:
    """Verifies mandatory production security headers."""
    MANDATORY_HEADERS = [
        "strict-transport-security",
        "x-content-type-options",
        "x-frame-options",
        "x-xss-protection"
    ]

    @classmethod
    def verify_headers(cls, headers: Dict[str, str]) -> Dict[str, Any]:
        lowered = {k.lower(): v for k, v in headers.items()}
        missing = [h for h in cls.MANDATORY_HEADERS if h not in lowered]
        return {
            "passed": len(missing) == 0,
            "missing_headers": missing,
            "error": f"Missing mandatory security headers: {missing}" if missing else None
        }


class FileIntegrityVerifier:
    """Verifies non-empty file size and presence."""
    @staticmethod
    def verify(file_path: str, min_bytes: int = 1) -> Dict[str, Any]:
        path = Path(file_path)
        if not path.is_absolute():
            path = CONFIG.workspace_root / path

        if not path.exists():
            return {"passed": False, "error": f"File '{file_path}' missing."}

        size = path.stat().st_size
        return {
            "passed": size >= min_bytes,
            "size_bytes": size,
            "error": f"File '{file_path}' size ({size} bytes) below minimum {min_bytes} bytes." if size < min_bytes else None
        }
