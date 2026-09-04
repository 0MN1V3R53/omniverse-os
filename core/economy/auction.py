"""
Token-Efficiency Auction Router.
Allows multi-agent task dispatch via cost, latency, and quality bidding.
"""

from typing import Dict, List, Optional, Any
from core.economy.models import BidProposal



class AuctionRouter:
    """
    Auction engine for optimal sub-agent path selection.
    """

    @classmethod
    def evaluate_bids(cls, bids: List[BidProposal]) -> Optional[BidProposal]:
        """
        Rank bids and select the most token-efficient agent with optimal quality-to-cost ratio.
        """
        if not bids:
            return None

        def score_bid(b: BidProposal) -> float:
            cost_weight = max(0.001, b.proposed_cost_credits)
            latency_sec = max(0.01, b.estimated_latency_ms / 1000.0)
            # Higher quality and lower cost/latency yield higher score
            return (b.quality_score * 100.0) / ((cost_weight * 0.6) + (latency_sec * 0.4))

        sorted_bids = sorted(bids, key=score_bid, reverse=True)
        return sorted_bids[0]

    @classmethod
    def create_candidate_bids(cls, task_id: str, candidates: List[Dict[str, Any]]) -> List[BidProposal]:
        """
        Convenience generator for candidate agent bids.
        """
        bids = []
        for c in candidates:
            bids.append(BidProposal(
                agent_id=c["agent_id"],
                task_id=task_id,
                proposed_cost_credits=c.get("cost_credits", 0.05),
                estimated_latency_ms=c.get("latency_ms", 50.0),
                quality_score=c.get("quality_score", 0.95),
                token_budget=c.get("token_budget", 1500)
            ))
        return bids
