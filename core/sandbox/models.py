"""
Pydantic Data Models for Speculative Multiverse Sandbox Engine.
"""

import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field


class BenchmarkScore(BaseModel):
    """Execution and quality benchmark scores for a candidate branch."""
    test_pass_rate: float = 1.0       # 0.0 - 1.0
    execution_duration_ms: float = 10.0
    code_complexity_score: float = 0.90 # 0.0 - 1.0 (higher = cleaner/simpler)
    ast_integrity_passed: bool = True
    composite_score: float = 0.95     # Weighted overall score


class CandidateBranch(BaseModel):
    """An ephemeral speculative implementation branch."""
    branch_id: str = Field(default_factory=lambda: f"BRANCH-{uuid.uuid4().hex[:6].upper()}")
    paradigm_label: str  # e.g., "PerformanceOptimized", "SimplicityFirst", "ExtensiblePlugin"
    target_file: str
    staged_code: str
    benchmark: Optional[BenchmarkScore] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class MultiverseEvaluationResult(BaseModel):
    """Result of racing multiple speculative implementation branches."""
    evaluation_id: str = Field(default_factory=lambda: f"MULTI-{uuid.uuid4().hex[:8].upper()}")
    target_file: str
    total_candidates: int
    winning_branch_id: str
    winning_paradigm: str
    applied_diff_summary: str
    benchmark_comparison: Dict[str, float] = Field(default_factory=dict)
    committed: bool = False
    timestamp: datetime = Field(default_factory=datetime.utcnow)
