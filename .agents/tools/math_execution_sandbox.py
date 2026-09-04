#!/usr/bin/env python3
"""
.agents/tools/math_execution_sandbox.py
========================================
Tool-Integrated Reasoning (TIR) Execution Sandbox for Competition Mathematics.
Equips Leviathan 999 and Omniverse OS with an isolated, real-time Python REPL
capable of executing algebraic verification, modular arithmetic, combinatorics,
and numerical computations.

Eliminates LLM arithmetic drift and hallucinated calculation errors.
"""

import os
import sys
import re
import subprocess
import time
from typing import Dict, Any, List, Optional, Tuple

class MathExecutionSandbox:
    """
    Executes Python calculation scripts generated during chain-of-thought reasoning,
    captures outputs, and extracts verified numerical answers.
    """

    def __init__(self, timeout_seconds: float = 5.0):
        self.timeout_seconds = timeout_seconds

    def execute_code(self, code_snippet: str) -> Dict[str, Any]:
        """
        Executes a Python code snippet in a clean subprocess and returns stdout, stderr,
        execution time, and return code.
        """
        t0 = time.time()
        # Security sanitization: prevent filesystem/network damage
        forbidden_patterns = ["rm -rf", "os.system", "shutil.rmtree", "subprocess", "socket"]
        for p in forbidden_patterns:
            if p in code_snippet:
                return {
                    "stdout": "",
                    "stderr": f"Security violation: '{p}' is forbidden in Math Execution Sandbox.",
                    "exit_code": -1,
                    "elapsed_seconds": 0.0,
                    "success": False
                }

        # Wrap in safe harness that imports standard math libraries
        harness = f"""
import math
import itertools
from fractions import Fraction

{code_snippet}
"""
        try:
            res = subprocess.run(
                [sys.executable, "-c", harness],
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds
            )
            elapsed = time.time() - t0
            return {
                "stdout": res.stdout.strip(),
                "stderr": res.stderr.strip(),
                "exit_code": res.returncode,
                "elapsed_seconds": round(elapsed, 4),
                "success": (res.returncode == 0)
            }
        except subprocess.TimeoutExpired:
            return {
                "stdout": "",
                "stderr": f"Execution timed out after {self.timeout_seconds}s",
                "exit_code": -2,
                "elapsed_seconds": self.timeout_seconds,
                "success": False
            }
        except Exception as e:
            return {
                "stdout": "",
                "stderr": str(e),
                "exit_code": -3,
                "elapsed_seconds": round(time.time() - t0, 4),
                "success": False
            }

    def process_and_verify(self, text_with_code: str) -> Dict[str, Any]:
        """
        Scans chain-of-thought text for embedded ```python or ```python-exec blocks,
        executes them sequentially, and extracts computed values.
        """
        code_blocks = re.findall(r"```(?:python|python-exec|py)?\s*(.*?)\s*```", text_with_code, re.DOTALL)
        if not code_blocks:
            return {"has_code": False, "verified": False, "outputs": []}

        execution_outputs = []
        last_computed_number = None

        for idx, block in enumerate(code_blocks):
            # Skip blocks that look like raw text or comments only
            if not any(kw in block for kw in ["=", "print", "for ", "def ", "return", "+", "-", "*"]):
                continue

            exec_res = self.execute_code(block)
            execution_outputs.append({
                "block_index": idx,
                "code": block,
                "result": exec_res
            })

            # Check stdout for printed integers
            if exec_res["success"] and exec_res["stdout"]:
                # Look for numbers in stdout
                nums = re.findall(r"\b([0-9]+)\b", exec_res["stdout"])
                if nums:
                    last_computed_number = int(nums[-1])

        return {
            "has_code": True,
            "verified": bool(last_computed_number is not None),
            "last_computed_number": last_computed_number,
            "outputs": execution_outputs
        }

    def build_tir_math_prompt(self, problem_statement: str) -> str:
        """
        Wraps a competition math problem in the authoritative Tool-Integrated Reasoning (TIR)
        cognitive scaffolding prompt.
        """
        return f"""You are an elite Olympiad mathematician equipped with an automated Python verification environment.
Solve the following competition math problem.

MANDATORY TOOL USAGE DIRECTIVE:
To guarantee 100% arithmetic accuracy and eliminate calculation drift:
1. Formulate your mathematical derivation clearly.
2. Write a short Python script inside ```python ... ``` that computes or verifies the exact numerical answer (e.g. loops, combinations, modular arithmetic, polynomial evaluation).
3. The script must print the final numerical result using print(answer).
4. Conclude your response with:
Final Answer: [integer]

Problem:
{problem_statement}"""
