"""
Standard Operating Procedure (SOP) State Machine Package.
Converts departmental Markdown rules into deterministic, executable state machines.
"""

from .schemas import (
    SOPStage,
    GrowthPRD,
    EngineeringDesign,
    ImplementationBundle,
    QualityAuditSignoff,
    DeploymentReceipt,
)
from .state_machine import SOPEngine, SOPStateTransition
from .pipeline import SOPPipeline

__all__ = [
    "SOPStage",
    "GrowthPRD",
    "EngineeringDesign",
    "ImplementationBundle",
    "QualityAuditSignoff",
    "DeploymentReceipt",
    "SOPEngine",
    "SOPStateTransition",
    "SOPPipeline",
]
