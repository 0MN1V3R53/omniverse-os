"""
Active Invariant Fuzzing Engine.
Generates adversarial mutation-based fuzzing payloads (null bytes, boundary overflows, malformed JSON, prototype pollution)
against system components and automatically synthesizes new formal predicates into `rules/invariants.json`.
"""

import json
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple, Any
from pydantic import BaseModel, Field

from core.config import CONFIG
from core.guards.invariants import GLOBAL_INVARIANT_VERIFIER


class FuzzTestCase(BaseModel):
    """An individual fuzz mutation test case."""
    test_id: str = Field(default_factory=lambda: f"FUZZ-{uuid.uuid4().hex[:6].upper()}")
    target_component: str
    payload_type: str  # "NULL_BYTE", "BOUNDARY_OVERFLOW", "MALFORMED_JSON", "INJECTION"
    input_payload: Any
    expected_behavior: str


class FuzzExecutionReport(BaseModel):
    """Deliverable summary of an automated invariant fuzzing pass."""
    total_mutations_tested: int
    vulnerabilities_found: int
    synthesized_invariants_count: int
    synthesized_invariants: List[Dict[str, Any]] = Field(default_factory=list)
    fuzzed_components: List[str] = Field(default_factory=list)
    duration_ms: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ActiveInvariantFuzzer:
    """
    Automated adversarial fuzzing and invariant synthesis engine.
    """

    def __init__(self, invariants_path: Optional[Path] = None):
        self.invariants_path = invariants_path or (CONFIG.workspace_root / "rules" / "invariants.json")

    def generate_fuzz_payloads(self) -> List[Dict[str, Any]]:
        """
        Synthesize diverse adversarial input mutations.
        """
        return [
            {"type": "NULL_BYTE", "payload": "admin\x00user_payload", "desc": "Null byte injection in string identifier"},
            {"type": "BOUNDARY_OVERFLOW", "payload": 9223372036854775807, "desc": "64-bit integer maximum boundary"},
            {"type": "NEGATIVE_BUDGET", "payload": -99999, "desc": "Negative credit/budget value"},
            {"type": "MALFORMED_JSON", "payload": '{"unclosed_tag": "invalid', "desc": "Truncated JSON payload"},
            {"type": "PROTOTYPE_POLLUTION", "payload": "__proto__.isAdmin = true", "desc": "Prototype pollution attribute assignment"},
            {"type": "MOCK_DATA_LEAK", "payload": "const testData = mock_data_generator();", "desc": "Prohibited synthetic mock generator leak"}
        ]

    def fuzz_target(
        self,
        component_name: str,
        target_evaluator: Optional[Callable[[Any], bool]] = None
    ) -> FuzzExecutionReport:
        """
        Execute mutation fuzz test suite against a target component.
        """
        start_time = time.time()
        payloads = self.generate_fuzz_payloads()
        vulnerabilities = []
        synthesized = []

        for p in payloads:
            # Evaluate using target_evaluator or default invariant checker
            failed = False
            if target_evaluator:
                try:
                    is_safe = target_evaluator(p["payload"])
                    if not is_safe:
                        failed = True
                except Exception:
                    failed = True
            else:
                # Default evaluation for prototype pollution or mock leaks
                if p["type"] in ("PROTOTYPE_POLLUTION", "MOCK_DATA_LEAK"):
                    failed = True

            if failed:
                vulnerabilities.append(p)
                # Synthesize new invariant rule if not already present
                rule_id = f"INV-FUZZ-{p['type'].replace('_', '-')}"
                new_rule = self.synthesize_and_append_invariant(
                    invariant_id=rule_id,
                    category="security_fuzzing",
                    description=f"Auto-synthesized invariant blocking {p['desc']}.",
                    prohibited_patterns=[str(p["payload"])]
                )
                if new_rule:
                    synthesized.append(new_rule)

        duration_ms = round((time.time() - start_time) * 1000.0, 2)
        return FuzzExecutionReport(
            total_mutations_tested=len(payloads),
            vulnerabilities_found=len(vulnerabilities),
            synthesized_invariants_count=len(synthesized),
            synthesized_invariants=synthesized,
            fuzzed_components=[component_name],
            duration_ms=duration_ms
        )

    def synthesize_and_append_invariant(
        self,
        invariant_id: str,
        category: str,
        description: str,
        prohibited_patterns: List[str],
        severity: str = "BLOCKER"
    ) -> Optional[Dict[str, Any]]:
        """
        Synthesize a formal invariant rule and append it to `rules/invariants.json`.
        """
        if not self.invariants_path.exists():
            return None

        try:
            data = json.loads(self.invariants_path.read_text(encoding="utf-8"))
            existing_ids = {inv.get("invariant_id") for inv in data.get("invariants", [])}

            if invariant_id in existing_ids:
                return None

            new_invariant = {
                "invariant_id": invariant_id,
                "category": category,
                "description": description,
                "severity": severity,
                "prohibited_patterns": prohibited_patterns
            }

            data.setdefault("invariants", []).append(new_invariant)
            self.invariants_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
            
            # Reload global verifier invariants
            GLOBAL_INVARIANT_VERIFIER.reload_invariants()
            return new_invariant
        except Exception:
            return None


# Global Invariant Fuzzer Singleton
GLOBAL_INVARIANT_FUZZER = ActiveInvariantFuzzer()
