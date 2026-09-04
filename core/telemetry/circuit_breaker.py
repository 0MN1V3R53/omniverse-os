"""
Circuit Breakers and Loop Detection Engine for Multi-Agent Workflows.
Prevents infinite recursion, cyclic delegation ping-pong, and stalled workflows.
"""

import hashlib
import json
from typing import List, Dict, Tuple, Any, Optional
from core.config import CONFIG


class CircuitBreakerTrippedError(Exception):
    """Raised when delegation depth or cyclic repetition thresholds are breached."""
    def __init__(self, reason: str, delegation_path: List[str], details: Optional[Dict[str, Any]] = None):
        self.reason = reason
        self.delegation_path = delegation_path
        self.details = details or {}
        super().__init__(f"Circuit Breaker Tripped: {reason}. Path: {' -> '.join(delegation_path)}")


class DelegationCircuitBreaker:
    """
    Stateful circuit breaker tracking agent hops and state mutations.
    """

    def __init__(
        self,
        max_depth: Optional[int] = None,
        max_cyclic_repeats: Optional[int] = None
    ):
        self.max_depth = max_depth or CONFIG.max_delegation_depth
        self.max_cyclic_repeats = max_cyclic_repeats or CONFIG.max_cyclic_repeats
        self.hop_history: List[Tuple[str, str]] = []  # List of (agent_id, state_hash)

    def _hash_state(self, state_payload: Any) -> str:
        """Generate deterministic MD5 hash of state payload."""
        try:
            serialized = json.dumps(state_payload, sort_keys=True, default=str)
        except Exception:
            serialized = str(state_payload)
        return hashlib.md5(serialized.encode("utf-8")).hexdigest()[:12]

    def record_hop(self, agent_id: str, state_payload: Any = None) -> None:
        """
        Record an agent delegation hop and evaluate circuit breaker invariants.
        Raises CircuitBreakerTrippedError if an anomaly or infinite loop is detected.
        """
        state_hash = self._hash_state(state_payload)
        self.hop_history.append((agent_id, state_hash))
        agent_path = [h[0] for h in self.hop_history]

        # 1. Check Max Delegation Depth
        if len(self.hop_history) > self.max_depth:
            raise CircuitBreakerTrippedError(
                reason=f"Exceeded maximum delegation depth of {self.max_depth} hops",
                delegation_path=agent_path,
                details={"total_hops": len(self.hop_history), "max_depth": self.max_depth}
            )

        # 2. Check Stagnant Agent Loops (same agent invoked repeatedly with identical state)
        identical_state_visits = sum(
            1 for a, h in self.hop_history if a == agent_id and h == state_hash
        )
        if identical_state_visits >= self.max_cyclic_repeats:
            raise CircuitBreakerTrippedError(
                reason=f"Agent '{agent_id}' invoked {identical_state_visits} times with zero state mutation (stagnant loop)",
                delegation_path=agent_path,
                details={"agent_id": agent_id, "state_hash": state_hash, "repeats": identical_state_visits}
            )

        # 3. Check Cyclic Patterns (e.g. A -> B -> A -> B -> A -> B)
        if len(agent_path) >= 6:
            # Check 2-hop cycles (A, B, A, B, A, B)
            if agent_path[-1] == agent_path[-3] == agent_path[-5] and agent_path[-2] == agent_path[-4] == agent_path[-6]:
                raise CircuitBreakerTrippedError(
                    reason=f"Detected oscillating 2-agent loop between '{agent_path[-1]}' and '{agent_path[-2]}'",
                    delegation_path=agent_path,
                    details={"cycle": [agent_path[-2], agent_path[-1]]}
                )

    def reset(self) -> None:
        """Clear hop history for a fresh ticket execution."""
        self.hop_history.clear()
