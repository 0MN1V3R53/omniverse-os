"""
SOP Execution Pipeline connecting SOP State Machine to the Event MessageBus.
"""

from typing import Dict, Any, Optional
from core.bus.bus import MessageBus, GLOBAL_MESSAGE_BUS
from core.bus.models import (
    EventMessage,
    RequirementDoc,
    ArchitectureSpec,
    CodeDiff,
    VerificationResult,
    DeploymentManifest,
)
from core.sop.schemas import (
    SOPStage,
    GrowthPRD,
    EngineeringDesign,
    ImplementationBundle,
    QualityAuditSignoff,
    DeploymentReceipt,
)
from core.sop.state_machine import SOPEngine, SOPStateTransition


class SOPPipeline:
    """
    Coordinates end-to-end SOP execution while publishing events to the MessageBus.
    """

    def __init__(self, ticket_id: str, bus: Optional[MessageBus] = None):
        self.ticket_id = ticket_id
        self.engine = SOPEngine(ticket_id)
        self.bus = bus or GLOBAL_MESSAGE_BUS

    async def advance_prd(self, prd: GrowthPRD) -> SOPStateTransition:
        """Advance to PRD_SPEC stage and publish RequirementDoc event."""
        tr = self.engine.transition(SOPStage.PRD_SPEC, prd.author, prd)
        req_doc = RequirementDoc(
            prd_id=prd.prd_id,
            title=prd.feature_name,
            business_goal=prd.target_kpi,
            target_corridors=prd.target_corridors,
            user_stories=prd.user_pain_points,
            author_agent_id=prd.author
        )
        await self.bus.publish(EventMessage.create(
            topic="product.prd",
            sender_id=prd.author,
            payload_obj=req_doc,
            tags={"growth", "product", "planning"}
        ))
        return tr

    async def advance_design(self, design: EngineeringDesign) -> SOPStateTransition:
        """Advance to SYSTEM_DESIGN stage and publish ArchitectureSpec event."""
        tr = self.engine.transition(SOPStage.SYSTEM_DESIGN, design.lead_architect, design)
        spec = ArchitectureSpec(
            spec_id=design.design_id,
            prd_ref=design.prd_ref,
            system_name="Next.js Client Web & Transport Engine",
            components_affected=design.affected_files,
            data_flow=design.state_mutations,
            author_agent_id=design.lead_architect
        )
        await self.bus.publish(EventMessage.create(
            topic="engineering.spec",
            sender_id=design.lead_architect,
            payload_obj=spec,
            tags={"engineering", "architecture", "frontend"}
        ))
        return tr

    async def advance_implementation(self, bundle: ImplementationBundle) -> SOPStateTransition:
        """Advance to CODE_IMPLEMENTATION stage and publish CodeDiff event."""
        tr = self.engine.transition(SOPStage.CODE_IMPLEMENTATION, bundle.developer_agent, bundle)
        first_file = next(iter(bundle.files_modified.keys())) if bundle.files_modified else "unknown.js"
        diff = CodeDiff(
            diff_id=bundle.bundle_id,
            task_id=bundle.design_ref,
            file_path=first_file,
            code_content=str(bundle.files_modified),
            author_agent_id=bundle.developer_agent,
            commit_message=f"Implemented {len(bundle.files_modified)} files per design {bundle.design_ref}"
        )
        await self.bus.publish(EventMessage.create(
            topic="engineering.code",
            sender_id=bundle.developer_agent,
            payload_obj=diff,
            tags={"engineering", "code", "qa"}
        ))
        return tr

    async def advance_audit(self, audit: QualityAuditSignoff) -> SOPStateTransition:
        """Advance to PAIR_REVIEW stage and publish VerificationResult event."""
        tr = self.engine.transition(SOPStage.PAIR_REVIEW, audit.reviewer_agent, audit)
        ver_res = VerificationResult(
            audit_id=audit.audit_id,
            target_ref_id=audit.bundle_ref,
            reviewer_agent_id=audit.reviewer_agent,
            status="VERIFIED" if audit.quality_gate_passed else "REJECTED",
            checklist_passed=audit.checklist_passed,
            unresolved_defects=audit.unresolved_defects,
            signoff_token=audit.signoff_token
        )
        await self.bus.publish(EventMessage.create(
            topic="qa.verification",
            sender_id=audit.reviewer_agent,
            payload_obj=ver_res,
            tags={"qa", "verification", "devops"}
        ))
        return tr

    async def advance_deployment(self, receipt: DeploymentReceipt) -> SOPStateTransition:
        """Advance to PRODUCTION_DEPLOYMENT stage and publish DeploymentManifest event."""
        tr = self.engine.transition(SOPStage.PRODUCTION_DEPLOYMENT, receipt.devops_engineer, receipt)
        manifest = DeploymentManifest(
            manifest_id=receipt.receipt_id,
            build_version="2.8.06-STATIC-SECURE",
            environment="production",
            files_synced=[f"{receipt.synced_routes} routes synced"],
            cache_purged=receipt.cache_purged,
            domain=receipt.live_url,
            dri_agent_id=receipt.devops_engineer
        )
        await self.bus.publish(EventMessage.create(
            topic="devops.deploy",
            sender_id=receipt.devops_engineer,
            payload_obj=manifest,
            tags={"devops", "deployment", "production"}
        ))
        return tr
