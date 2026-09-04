"""
Compute Tokenomics Data Models.
Structured models for virtual compute credit allocations, transaction logs, and bidding proposals.
"""

import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class ComputeTransaction(BaseModel):
    """Immutable ledger record of compute token expenditure."""
    tx_id: str = Field(default_factory=lambda: f"TX-{uuid.uuid4().hex[:10].upper()}")
    agent_id: str
    pod_name: str
    ticket_id: str
    tokens_consumed: int
    credits_deducted: float
    rate_per_k_token: float = 0.05
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class PodBudget(BaseModel):
    """Compute credit budget allocation for a departmental pod."""
    pod_name: str
    allocated_credits: float = 1000.0
    spent_credits: float = 0.0
    
    @property
    def available_credits(self) -> float:
        return max(0.0, round(self.allocated_credits - self.spent_credits, 4))


class BidProposal(BaseModel):
    """Sub-agent auction bid for task dispatch."""
    bid_id: str = Field(default_factory=lambda: f"BID-{uuid.uuid4().hex[:8].upper()}")
    agent_id: str
    task_id: str
    proposed_cost_credits: float
    estimated_latency_ms: float
    quality_score: float = 0.95
    token_budget: int = 1500
