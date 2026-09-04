"""
Communicative De-Hallucination Dual-Agent Verification Loop.
Implements the ChatDev review pattern ensuring zero unresolved checklist defects.
"""

import uuid
import asyncio
from typing import Dict, List, Any, Optional, Callable, Tuple
from pydantic import BaseModel, Field

from core.bus.models import VerificationResult
from core.consensus.pairing import AgentPair, ENTERPRISE_PAIRS


class VerificationGateError(Exception):
    """Raised when an artifact fails dual-agent review after max rounds."""
    def __init__(self, message: str, unresolved_defects: List[str], rounds_conducted: int):
        self.unresolved_defects = unresolved_defects
        self.rounds_conducted = rounds_conducted
        super().__init__(f"Verification Gate Blocked: {message}. Unresolved defects: {unresolved_defects}")


class DeHallucinationLoop:
    """
    Executes iterative communicative de-hallucination loops between Producer & Reviewer agents.
    """

    def __init__(self, pair: AgentPair):
        self.pair = pair

    async def execute_review(
        self,
        target_ref_id: str,
        initial_artifact: Dict[str, Any],
        producer_revision_fn: Callable[[Dict[str, Any], List[str]], Any],
        reviewer_eval_fn: Callable[[Dict[str, Any], List[str]], Tuple[bool, Dict[str, bool], List[str], str]]
    ) -> Tuple[Dict[str, Any], VerificationResult]:
        """
        Execute iterative review loop.
        - `producer_revision_fn(artifact, defects) -> updated_artifact`
        - `reviewer_eval_fn(artifact, checklist) -> (passed, checklist_dict, defects_list, rationale)`
        """
        curr_artifact = initial_artifact
        checklist = self.pair.default_checklist

        for round_idx in range(1, self.pair.max_review_rounds + 1):
            # Step 1: Reviewer evaluates artifact
            if asyncio.iscoroutinefunction(reviewer_eval_fn):
                passed, check_dict, defects, rationale = await reviewer_eval_fn(curr_artifact, checklist)
            else:
                passed, check_dict, defects, rationale = reviewer_eval_fn(curr_artifact, checklist)

            # Step 2: Check zero-defect gate
            if passed and len(defects) == 0:
                signoff_token = f"SIGN-{uuid.uuid4().hex[:10].upper()}"
                result = VerificationResult(
                    target_ref_id=target_ref_id,
                    reviewer_agent_id=self.pair.reviewer_agent_id,
                    status="VERIFIED",
                    checklist_passed=check_dict,
                    unresolved_defects=[],
                    rationale=rationale or f"Verified with 0 defects in round {round_idx}.",
                    signoff_token=signoff_token
                )
                return curr_artifact, result

            # Step 3: If defects exist and more rounds remain, ask producer for revision
            if round_idx < self.pair.max_review_rounds:
                if asyncio.iscoroutinefunction(producer_revision_fn):
                    curr_artifact = await producer_revision_fn(curr_artifact, defects)
                else:
                    curr_artifact = producer_revision_fn(curr_artifact, defects)
            else:
                # Max rounds reached with unresolved defects
                raise VerificationGateError(
                    message=f"Review failed after {self.pair.max_review_rounds} rounds between {self.pair.producer_agent_id} and {self.pair.reviewer_agent_id}",
                    unresolved_defects=defects,
                    rounds_conducted=round_idx
                )

        raise VerificationGateError(
            message="Dual-agent verification exhausted without achieving consensus.",
            unresolved_defects=["Review timeout"],
            rounds_conducted=self.pair.max_review_rounds
        )
