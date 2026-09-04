"""
Consensus Engine, Dual-Agent De-Hallucination, and Departmental Sign-Off Package.
"""

from .pairing import AgentPair, ENTERPRISE_PAIRS, get_agent_pair
from .verifier_loop import DeHallucinationLoop, VerificationGateError
from core.guards.consensus import ConsensusEngine, ConsensusVote, DepartmentSignoff

__all__ = [
    "AgentPair",
    "ENTERPRISE_PAIRS",
    "get_agent_pair",
    "DeHallucinationLoop",
    "VerificationGateError",
    "ConsensusEngine",
    "ConsensusVote",
    "DepartmentSignoff",
]
