"""
Pydantic Models for Causal Graph and World Modeling Engine.
"""

import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field


class CausalLink(BaseModel):
    """Represents an observed action-outcome causal connection."""
    link_id: str = Field(default_factory=lambda: f"CLINK-{uuid.uuid4().hex[:8].upper()}")
    context_state: str        # e.g., "high_bounce_rate", "slow_lcp_mobile", "scraper_surge"
    action_taken: str         # e.g., "inject_select_none_tailwind", "transpile_scenegraph_banner"
    observed_impact: str      # e.g., "conversion_lift_18pct", "scraping_drop_99pct"
    success_rate: float = 1.0 # 0.0 to 1.0
    confidence_score: float = 0.85
    sample_count: int = 1
    last_verified: datetime = Field(default_factory=datetime.utcnow)


class CausalMatrix(BaseModel):
    """Complete persistent causal memory matrix for agents."""
    version: str = "1.0.0"
    links: List[CausalLink] = Field(default_factory=list)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
