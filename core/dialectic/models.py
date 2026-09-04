"""
Pydantic Data Models for Dialectical Task Force & Pre-Flight Audits.
"""

import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field


class PreFlightAuditReport(BaseModel):
    """Result of pre-flight workspace scan and idempotency audit."""
    audit_id: str = Field(default_factory=lambda: f"PFA-{uuid.uuid4().hex[:8].upper()}")
    ticket_objective: str
    is_idempotent: bool = False
    reusable_modules: List[str] = Field(default_factory=list)
    existing_artifacts: List[str] = Field(default_factory=list)
    recorded_pitfalls: List[str] = Field(default_factory=list)
    readiness_score: float = 1.0  # 0.0 - 1.0
    recommendation: str = "PROCEED_WITH_DIALECTIC"  # PROCEED_WITH_DIALECTIC, REUSE_EXISTING, ABORT_DUPLICATE
    scanned_at: datetime = Field(default_factory=datetime.utcnow)


class ArchitecturalOption(BaseModel):
    """A distinct architectural proposal generated during Stage 1 Divergence."""
    option_id: str = Field(default_factory=lambda: f"OPT-{uuid.uuid4().hex[:6].upper()}")
    title: str
    paradigm: str  # e.g., "Event-Driven Async", "Declarative Micro-Frontend", "Zero-Drift WebAssembly"
    novel_mechanisms: List[str] = Field(default_factory=list)
    advantages: List[str] = Field(default_factory=list)
    token_cost_estimate: str = "LOW"  # LOW, MEDIUM, HIGH
    complexity: str = "MODERATE"


class CritiqueReport(BaseModel):
    """Adversarial stress-test report generated during Stage 2 Critique."""
    critique_id: str = Field(default_factory=lambda: f"CRIT-{uuid.uuid4().hex[:6].upper()}")
    option_id: str
    vulnerabilities: List[str] = Field(default_factory=list)
    edge_cases: List[str] = Field(default_factory=list)
    token_overhead_risk: str
    security_risks: List[str] = Field(default_factory=list)
    counter_arguments: str
    passed_audit: bool = True


class SynthesizedPlan(BaseModel):
    """Unified, hardened implementation plan generated during Stage 3 Synthesis."""
    plan_id: str = Field(default_factory=lambda: f"SYNTH-{uuid.uuid4().hex[:8].upper()}")
    objective: str
    selected_paradigm: str
    hardened_mechanisms: List[str] = Field(default_factory=list)
    rejection_rationales: Dict[str, str] = Field(default_factory=dict)
    execution_steps: List[str] = Field(default_factory=list)
    safety_invariants: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
