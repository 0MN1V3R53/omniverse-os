"""
Pydantic Data Models for Autonomous Self-Critique and Re-Prompting Engine.
"""

import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field


class SelfCritiqueRubric(BaseModel):
    """Evaluation rubric for drafted agent deliverables."""
    rubric_id: str = Field(default_factory=lambda: f"RUBRIC-{uuid.uuid4().hex[:6].upper()}")
    is_novel_and_robust: bool = True       # Beyond generic baseline
    respects_workspace_rules: bool = True  # Strict file boundaries & schemas
    zero_unhandled_exceptions: bool = True # Complete error handling
    zero_mock_or_hallucinations: bool = True # Zero fake telemetry/data
    critique_points: List[str] = Field(default_factory=list)
    overall_quality_score: float = 1.0     # 0.0 - 1.0


class ReflexionResult(BaseModel):
    """Result of an autonomous self-critique and re-prompting cycle."""
    reflexion_id: str = Field(default_factory=lambda: f"REFLX-{uuid.uuid4().hex[:8].upper()}")
    agent_id: str
    ticket_id: str
    iterations: int = 1
    passed: bool = True
    initial_rubric: SelfCritiqueRubric
    final_rubric: SelfCritiqueRubric
    refined_output_summary: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
