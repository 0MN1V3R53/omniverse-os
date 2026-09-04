"""
Neuro-Symbolic Invariant Verifier.
Evaluates code diffs against formal logical invariants and security boundaries before task completion.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

from core.config import CONFIG
from core.ast_engine.navigator import ASTNavigator



class InvariantViolation(BaseModel):
    """Specific invariant rule violation found in code."""
    invariant_id: str
    category: str
    severity: str
    description: str
    matched_pattern: str


class InvariantVerificationReport(BaseModel):
    """Complete invariant verification audit report."""
    target_file: str
    passed: bool = True
    total_invariants_checked: int = 0
    violations: List[InvariantViolation] = Field(default_factory=list)
    warnings: List[InvariantViolation] = Field(default_factory=list)
    ast_valid: bool = True
    has_blockers: bool = False



class InvariantVerifier:
    """
    Formal predicate verification engine ensuring code complies with workspace invariants.
    """

    def __init__(self, rules_path: Optional[Path] = None):
        self.rules_path = rules_path or (CONFIG.workspace_root / "rules" / "invariants.json")
        self.ast_navigator = ASTNavigator()
        self.rules_data = self._load_rules()

    def _load_rules(self) -> Dict[str, Any]:
        """Load invariant definitions from JSON."""
        if self.rules_path.exists():
            try:
                return json.loads(self.rules_path.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {"invariants": []}

    def validate_code(self, target_file: str, code_content: str) -> InvariantVerificationReport:
        """
        Validate source code against all formal invariant predicates.
        """
        invariants = self.rules_data.get("invariants", [])
        violations: List[InvariantViolation] = []
        warnings: List[InvariantViolation] = []

        # 1. Prohibited pattern scanning
        for inv in invariants:
            inv_id = inv.get("invariant_id", "INV-UNKNOWN")
            cat = inv.get("category", "general")
            sev = inv.get("severity", "BLOCKER")
            desc = inv.get("description", "")
            patterns = inv.get("prohibited_patterns", [])

            for pat in patterns:
                if pat.lower() in code_content.lower():
                    violation = InvariantViolation(
                        invariant_id=inv_id,
                        category=cat,
                        severity=sev,
                        description=desc,
                        matched_pattern=pat
                    )
                    if sev == "BLOCKER":
                        violations.append(violation)
                    else:
                        warnings.append(violation)
                    break


        # 2. AST Syntax Integrity (if Python)
        ast_valid = True
        if target_file.endswith(".py"):
            ast_rep = self.ast_navigator.verify_ast_integrity(code_content)
            ast_valid = ast_rep.is_valid_syntax
            if not ast_rep.is_valid_syntax:
                violations.append(InvariantViolation(
                    invariant_id="INV-AST-SYNTAX-VALIDITY",
                    category="code_correctness",
                    severity="BLOCKER",
                    description=f"Syntax Error: {ast_rep.error_message}",
                    matched_pattern="invalid_syntax"
                ))

        has_blockers = len(violations) > 0
        passed = not has_blockers

        return InvariantVerificationReport(
            target_file=target_file,
            passed=passed,
            total_invariants_checked=len(invariants),
            violations=violations,
            warnings=warnings,
            ast_valid=ast_valid,
            has_blockers=has_blockers
        )


    def reload_invariants(self) -> None:
        """Reload invariant rules from JSON file."""
        self.rules_data = self._load_rules()

    @property
    def invariants(self) -> List[Any]:
        """Return list of invariant definition objects/dicts."""
        from pydantic import BaseModel
        class InvariantRuleDef(BaseModel):
            invariant_id: str
            category: str
            description: str
            severity: str
            prohibited_patterns: List[str] = []

        return [
            InvariantRuleDef(
                invariant_id=i.get("invariant_id", "INV-UNKNOWN"),
                category=i.get("category", "general"),
                description=i.get("description", ""),
                severity=i.get("severity", "BLOCKER"),
                prohibited_patterns=i.get("prohibited_patterns", [])
            )
            for i in self.rules_data.get("invariants", [])
        ]

    def verify_code_invariants(self, code_content: str, target_file: str = "snippet.py") -> InvariantVerificationReport:
        """Helper alias for code validation."""
        return self.validate_code(target_file, code_content)


# Global Singleton Verifier
GLOBAL_INVARIANT_VERIFIER = InvariantVerifier()


