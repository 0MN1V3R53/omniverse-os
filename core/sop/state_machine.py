"""
MetaGPT-Pattern SOP State Machine for Enterprise Multi-Agent Workflows.
"""

from datetime import datetime
from typing import Dict, List, Optional, Any, Type
from pydantic import BaseModel, Field

from core.sop.schemas import (
    SOPStage,
    GrowthPRD,
    EngineeringDesign,
    ImplementationBundle,
    QualityAuditSignoff,
    DeploymentReceipt,
)


class SOPStateTransition(BaseModel):
    """Immutable log of an SOP stage transition."""
    from_stage: SOPStage
    to_stage: SOPStage
    agent_id: str
    artifact_type: str
    artifact_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SOPEngine:
    """
    Deterministic SOP State Machine enforcing typed schemas and sequential stage handoffs.
    """

    # Schema validation requirements per stage
    STAGE_SCHEMAS: Dict[SOPStage, Type[BaseModel]] = {
        SOPStage.PRD_SPEC: GrowthPRD,
        SOPStage.SYSTEM_DESIGN: EngineeringDesign,
        SOPStage.CODE_IMPLEMENTATION: ImplementationBundle,
        SOPStage.PAIR_REVIEW: QualityAuditSignoff,
        SOPStage.PRODUCTION_DEPLOYMENT: DeploymentReceipt,
    }

    # Permitted stage transitions
    ALLOWED_TRANSITIONS: Dict[SOPStage, List[SOPStage]] = {
        SOPStage.INTAKE: [SOPStage.PRD_SPEC, SOPStage.FAILED],
        SOPStage.PRD_SPEC: [SOPStage.SYSTEM_DESIGN, SOPStage.FAILED],
        SOPStage.SYSTEM_DESIGN: [SOPStage.CODE_IMPLEMENTATION, SOPStage.FAILED],
        SOPStage.CODE_IMPLEMENTATION: [SOPStage.PAIR_REVIEW, SOPStage.FAILED],
        SOPStage.PAIR_REVIEW: [SOPStage.PRODUCTION_DEPLOYMENT, SOPStage.CODE_IMPLEMENTATION, SOPStage.FAILED],
        SOPStage.PRODUCTION_DEPLOYMENT: [SOPStage.COMPLETED, SOPStage.FAILED],
        SOPStage.COMPLETED: [],
        SOPStage.FAILED: [SOPStage.INTAKE],  # Can retry from intake
    }

    def __init__(self, ticket_id: str):
        self.ticket_id = ticket_id
        self.current_stage: SOPStage = SOPStage.INTAKE
        self.artifacts: Dict[SOPStage, BaseModel] = {}
        self.transitions: List[SOPStateTransition] = []

    def transition(
        self,
        to_stage: SOPStage,
        agent_id: str,
        artifact: BaseModel,
        metadata: Optional[Dict[str, Any]] = None
    ) -> SOPStateTransition:
        """
        Advance the SOP state machine to the next stage with typed artifact validation.
        """
        # 1. Verify transition is allowed
        allowed = self.ALLOWED_TRANSITIONS.get(self.current_stage, [])
        if to_stage not in allowed:
            raise ValueError(
                f"Invalid SOP transition from '{self.current_stage.value}' to '{to_stage.value}'. Allowed: {[s.value for s in allowed]}"
            )

        # 2. Verify artifact matches expected schema for target stage
        expected_schema = self.STAGE_SCHEMAS.get(to_stage)
        if expected_schema and not isinstance(artifact, expected_schema):
            raise TypeError(
                f"Stage '{to_stage.value}' requires artifact of type '{expected_schema.__name__}', got '{type(artifact).__name__}'."
            )

        # 3. Commit state transition
        artifact_id = getattr(artifact, "prd_id", getattr(artifact, "design_id", getattr(artifact, "bundle_id", getattr(artifact, "audit_id", getattr(artifact, "receipt_id", "artifact")))))
        transition_record = SOPStateTransition(
            from_stage=self.current_stage,
            to_stage=to_stage,
            agent_id=agent_id,
            artifact_type=type(artifact).__name__,
            artifact_id=str(artifact_id),
            metadata=metadata or {}
        )

        self.artifacts[to_stage] = artifact
        self.current_stage = to_stage
        self.transitions.append(transition_record)
        return transition_record

    def get_artifact(self, stage: SOPStage) -> Optional[BaseModel]:
        """Fetch artifact generated at a specific stage."""
        return self.artifacts.get(stage)
