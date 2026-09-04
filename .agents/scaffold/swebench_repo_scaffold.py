#!/usr/bin/env python3
"""
.agents/scaffold/swebench_repo_scaffold.py
===========================================
Hierarchical Repository Localization & Patch Synthesis Scaffold for SWE-bench.
Synchronizes leading open-source architectural patterns from Moatless Tools
and Agentless into the Omniverse OS (Pod 16 / Omniverse Code) substrate:

1. Hierarchical Fault Localization via Ripgrep & AST symbol graph visitor.
2. Targeted Context Slicing (100–250 lines) to prevent context saturation.
3. AST-preserving unified git diff generation.
4. In-memory patch syntax & AST regression verification.
"""

import os
import sys
import re
import ast
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

class SWEBenchRepoScaffold:
    """
    Orchestrates repository inspection, fault localization, context slicing,
    and unified diff synthesis for SWE-bench tasks.
    """

    def __init__(self, repo_root: Optional[Path] = None):
        self.repo_root = repo_root or Path.cwd()

    def extract_issue_keywords(self, problem_statement: str) -> List[str]:
        """
        Extracts high-priority search tokens (class names, function names, file paths, exceptions)
        from a raw GitHub issue description.
        """
        # Find snake_case or CamelCase identifiers
        identifiers = re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_]{3,}\b", problem_statement)
        # Filter out common English stop words
        stopwords = {
            "this", "that", "there", "then", "when", "where", "which", "with",
            "from", "have", "issue", "error", "problem", "expected", "actual",
            "reproduce", "steps", "using", "should", "would", "could", "about"
        }
        filtered = [ident for ident in identifiers if ident.lower() not in stopwords]
        # Frequency count
        counts: Dict[str, int] = {}
        for token in filtered:
            counts[token] = counts.get(token, 0) + 1
        sorted_tokens = sorted(counts.keys(), key=lambda k: counts[k], reverse=True)
        return sorted_tokens[:15]

    def localize_candidate_files(self, keywords: List[str], max_files: int = 5) -> List[Dict[str, Any]]:
        """
        Uses ripgrep or directory traversal to identify candidate source files
        containing the highest density of issue keywords.
        """
        candidate_scores: Dict[str, int] = {}
        
        for kw in keywords[:8]:
            try:
                cmd = ["rg", "--files-with-matches", "-t", "py", kw, str(self.repo_root)]
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                if res.returncode == 0 and res.stdout:
                    for line in res.stdout.strip().split("\n"):
                        path_str = line.strip()
                        # Ignore tests, venvs, and build dirs in localization phase
                        if any(ex in path_str for ex in ["/venv/", "/.venv/", "/tests/", "/test_", "/docs/"]):
                            continue
                        candidate_scores[path_str] = candidate_scores.get(path_str, 0) + 1
            except Exception:
                continue

        sorted_files = sorted(candidate_scores.items(), key=lambda x: x[1], reverse=True)
        return [{"file_path": f[0], "match_score": f[1]} for f in sorted_files[:max_files]]

    def extract_symbol_context_slice(
        self,
        file_path: Path,
        target_symbol: Optional[str] = None,
        max_lines: int = 200
    ) -> Dict[str, Any]:
        """
        Parses a target file with Python AST to isolate the specific function or class
        responsible for the bug, returning a numbered line slice.
        """
        if not file_path.exists():
            return {"status": "FILE_NOT_FOUND", "slice": ""}

        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()

        content = "".join(lines)
        try:
            tree = ast.parse(content)
        except SyntaxError:
            # Fallback to head of file if syntax invalid
            slice_lines = lines[:max_lines]
            return {
                "status": "FALLBACK_HEAD",
                "start_line": 1,
                "end_line": len(slice_lines),
                "slice": "".join([f"{i+1:04d}: {l}" for i, l in enumerate(slice_lines)])
            }

        # Locate symbol in AST
        target_node = None
        if target_symbol:
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    if node.name == target_symbol:
                        target_node = node
                        break

        if target_node and hasattr(target_node, "lineno"):
            start = max(1, target_node.lineno - 5)
            end = min(len(lines), getattr(target_node, "end_lineno", target_node.lineno + 50) + 5)
        else:
            # Default to first 150 lines
            start = 1
            end = min(len(lines), max_lines)

        numbered_slice = "".join([f"{i+1:04d}: {lines[i]}" for i in range(start - 1, end)])
        return {
            "status": "AST_ISOLATED",
            "file": str(file_path),
            "start_line": start,
            "end_line": end,
            "slice": numbered_slice
        }

    def validate_patch_syntax(self, patch_str: str) -> Dict[str, Any]:
        """
        Audits candidate patch against unified diff syntax rules and zero-stub invariants.
        """
        if not patch_str.strip():
            return {"valid": False, "error": "Empty patch payload"}

        has_header = bool(re.search(r"^diff --git|^--- |^\+\+\+ |^@@ ", patch_str, re.MULTILINE))
        if not has_header:
            return {"valid": False, "error": "Missing unified diff headers (diff --git or --- / +++)"}

        # Rule 04: Zero-stub check
        stubs = re.findall(r"(\bTODO\b|\bFIXME\b|pass\s*$|/\*\s*implement\s*later\s*\*/)", patch_str, re.IGNORECASE | re.MULTILINE)
        if stubs:
            return {"valid": False, "error": f"Patch contains forbidden stubs/placeholders: {stubs}"}

        return {"valid": True, "error": None}
