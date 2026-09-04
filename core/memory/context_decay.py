"""
Context Decay and Memory Relevance Scoring Engine.
Applies time-weighted and access-frequency decay while preserving invariant core directives.
"""

import math
from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class MemoryItem(BaseModel):
    """An individual unit of memory or context."""
    id: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_accessed_at: datetime = Field(default_factory=datetime.utcnow)
    access_count: int = 1
    is_pinned: bool = False  # Core directives and baseline rules are pinned (no decay)
    tags: List[str] = Field(default_factory=list)


class ContextDecayEngine:
    """
    Computes context relevance and exponential memory decay scores.
    Formula: R(t) = is_pinned ? 1.0 : e^(-lambda * delta_hours) * (1 + alpha * log(access_count + 1))
    """

    def __init__(self, decay_rate: float = 0.05, access_boost: float = 0.2):
        self.decay_rate = decay_rate  # Half-life approximately 14 hours
        self.access_boost = access_boost

    def compute_relevance(self, item: MemoryItem, current_time: Optional[datetime] = None) -> float:
        """Compute relevance score in range [0.0, 1.0+]. Pinned items always return 1.0."""
        if item.is_pinned:
            return 1.0

        now = current_time or datetime.utcnow()
        delta_hours = max(0.0, (now - item.last_accessed_at).total_seconds() / 3600.0)
        
        time_decay = math.exp(-self.decay_rate * delta_hours)
        frequency_multiplier = 1.0 + self.access_boost * math.log(item.access_count + 1)
        
        return round(time_decay * frequency_multiplier, 4)

    def filter_active_context(
        self,
        items: List[MemoryItem],
        min_relevance_threshold: float = 0.3,
        max_total_items: int = 10
    ) -> List[MemoryItem]:
        """
        Sort memory items by relevance score and return the top active items exceeding threshold.
        """
        scored = [(item, self.compute_relevance(item)) for item in items]
        # Filter items above threshold or pinned
        filtered = [item for item, score in scored if score >= min_relevance_threshold or item.is_pinned]
        
        # Sort by relevance descending (pinned always at top)
        sorted_items = sorted(
            filtered,
            key=lambda it: (it.is_pinned, self.compute_relevance(it)),
            reverse=True
        )
        return sorted_items[:max_total_items]
