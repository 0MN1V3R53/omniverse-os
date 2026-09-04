"""
Unit and Integration Test Suite for Enterprise Multi-Agent Runtime:
Pub-Sub Message Pool, De-Hallucination Pairs, SOP Engine, and Resilient Orchestrator.
"""

import asyncio
import tempfile
import unittest
from pathlib import Path

from core.bus.bus import MessageBus
from core.bus.models import EventMessage, RequirementDoc, CodeDiff, VerificationResult
from core.consensus.pairing import AgentPair, ENTERPRISE_PAIRS
from core.consensus.verifier_loop import DeHallucinationLoop, VerificationGateError
from core.sop.schemas import (
    SOPStage,
    GrowthPRD,
    EngineeringDesign,
    ImplementationBundle,
    QualityAuditSignoff,
    DeploymentReceipt,
)
from core.sop.state_machine import SOPEngine
from core.sop.pipeline import SOPPipeline
from core.orchestrator.state_logger import StateLogger
from core.orchestrator.router import DynamicRouter
from core.orchestrator.orchestrator import EnterpriseOrchestrator
from core.telemetry.tracer import LocalTracer


class TestEnterpriseRuntime(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
        self.log_path = self.temp_path / "state.jsonl"
        self.trace_path = self.temp_path / "traces.jsonl"
        self.bus = MessageBus()
        self.state_logger = StateLogger(self.log_path)
        self.tracer = LocalTracer(self.trace_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    async def test_message_bus_pub_sub_filtering(self):
        """Test tag and topic filtering in MessageBus."""
        # 1. Register subscriptions
        devops_sub = self.bus.subscribe("web_devops_marcus_chen", topics=["devops.*"], tags={"deployment"})
        frontend_sub = self.bus.subscribe("web_frontend_julian_thorne", topics=["engineering.*"], tags={"frontend"})

        # 2. Publish Engineering event (matches frontend_sub only)
        diff = CodeDiff(
            task_id="TASK-1",
            file_path="components/Hero.jsx",
            code_content="export default function Hero() {}",
            commit_message="Add Hero"
        )
        msg_eng = EventMessage.create(
            topic="engineering.code",
            sender_id="frontend_component_dev",
            payload_obj=diff,
            tags={"frontend", "engineering"}
        )
        delivered = await self.bus.publish(msg_eng)
        self.assertEqual(delivered, 1)

        pulled_eng = await self.bus.pull("web_frontend_julian_thorne", timeout=1.0)
        self.assertIsNotNone(pulled_eng)
        self.assertEqual(pulled_eng.topic, "engineering.code")

        # DevOps should receive nothing
        pulled_devops = await self.bus.pull("web_devops_marcus_chen", timeout=0.1)
        self.assertIsNone(pulled_devops)

    async def test_de_hallucination_loop_success_and_revisions(self):
        """Test ChatDev iterative review loop with revisions."""
        pair = AgentPair(
            pair_id="test_pair",
            domain="Testing",
            producer_agent_id="producer_a",
            reviewer_agent_id="reviewer_b",
            default_checklist=["Syntax valid", "Security tokens included"],
            max_review_rounds=3
        )
        loop = DeHallucinationLoop(pair)

        # Producer starts with missing token
        initial_data = {"code": "function run() {}", "tokens": []}

        def reviewer_eval(artifact, checklist):
            has_tokens = len(artifact.get("tokens", [])) > 0
            check_dict = {"Syntax valid": True, "Security tokens included": has_tokens}
            defects = [] if has_tokens else ["Missing security tokens"]
            return has_tokens, check_dict, defects, "Security token check"

        def producer_revise(artifact, defects):
            artifact["tokens"].append("HSTS_HEADER")
            return artifact

        final_artifact, signoff = await loop.execute_review(
            target_ref_id="REF-123",
            initial_artifact=initial_data,
            producer_revision_fn=producer_revise,
            reviewer_eval_fn=reviewer_eval
        )

        self.assertEqual(signoff.status, "VERIFIED")
        self.assertEqual(len(signoff.unresolved_defects), 0)
        self.assertIn("HSTS_HEADER", final_artifact["tokens"])
        self.assertIsNotNone(signoff.signoff_token)

    async def test_de_hallucination_loop_rejection(self):
        """Test that unresolved defects raise VerificationGateError after max rounds."""
        pair = AgentPair(
            pair_id="strict_pair",
            domain="Strict Check",
            producer_agent_id="producer_a",
            reviewer_agent_id="reviewer_b",
            default_checklist=["Zero bugs"],
            max_review_rounds=2
        )
        loop = DeHallucinationLoop(pair)

        def failing_reviewer(artifact, checklist):
            return False, {"Zero bugs": False}, ["Persistent memory leak"], "Rejected"

        def failing_producer(artifact, defects):
            return artifact  # Fails to fix defect

        with self.assertRaises(VerificationGateError):
            await loop.execute_review(
                target_ref_id="FAIL-123",
                initial_artifact={"state": "buggy"},
                producer_revision_fn=failing_producer,
                reviewer_eval_fn=failing_reviewer
            )

    def test_sop_state_machine_transitions(self):
        """Test MetaGPT-pattern SOP stage validation and sequencing."""
        sop = SOPEngine("TICKET-SOP-1")
        self.assertEqual(sop.current_stage, SOPStage.INTAKE)

        # 1. Intake -> PRD_SPEC
        prd = GrowthPRD(feature_name="Quick Quote", target_kpi="+20% leads")
        tr1 = sop.transition(SOPStage.PRD_SPEC, "growth_meta_buyer", prd)
        self.assertEqual(sop.current_stage, SOPStage.PRD_SPEC)

        # 2. PRD_SPEC -> SYSTEM_DESIGN
        design = EngineeringDesign(prd_ref=prd.prd_id, affected_files=["app/page.js"])
        tr2 = sop.transition(SOPStage.SYSTEM_DESIGN, "web_frontend_julian_thorne", design)
        self.assertEqual(sop.current_stage, SOPStage.SYSTEM_DESIGN)

        # 3. Invalid transition test (cannot jump directly to PRODUCTION_DEPLOYMENT)
        receipt = DeploymentReceipt(audit_ref="AUD-1")
        with self.assertRaises(ValueError):
            sop.transition(SOPStage.PRODUCTION_DEPLOYMENT, "web_devops_marcus_chen", receipt)

    def test_state_logger_persistence_and_rollback(self):
        """Test JSONL state logger persistence, history retrieval, and rollback."""
        self.state_logger.log_state("T-1", "PRD", "growth_meta_buyer", {"kpi": 10}, "COMPLETED")
        rec2 = self.state_logger.log_state("T-1", "DESIGN", "web_frontend_julian_thorne", {"files": ["a.js"]}, "COMPLETED")
        self.state_logger.log_state("T-1", "CODE", "frontend_component_dev", {"diff": "+1"}, "COMPLETED")

        history = self.state_logger.get_ticket_history("T-1")
        self.assertEqual(len(history), 3)

        # Rollback to rec2 (DESIGN stage)
        rolled = self.state_logger.rollback("T-1", rec2.record_id)
        self.assertEqual(rolled.status, "ROLLED_BACK")
        self.assertEqual(rolled.state_payload["rolled_back_to"], rec2.record_id)

    async def test_full_campaign_simulation(self):
        """Test master enterprise orchestrator simulating complete campaign."""
        orchestrator = EnterpriseOrchestrator(
            bus=self.bus,
            state_logger=self.state_logger,
            tracer=self.tracer
        )

        res = await orchestrator.run_campaign_workflow(
            title="Launch Auto-Transport 50-State Quick Quote Campaign",
            target_corridors=["CA to TX", "FL to NY", "IL to GA"],
            target_kpi="+22.5% Conversion Lift"
        )

        self.assertEqual(res["status"], "COMPLETED")
        self.assertEqual(len(res["stages_completed"]), 5)
        self.assertIn("growth", res["signoffs"])
        self.assertIn("frontend_ui", res["signoffs"])
        self.assertIn("security", res["signoffs"])

        # Check JSONL state log
        history = self.state_logger.get_ticket_history(res["ticket_id"])
        self.assertEqual(len(history), 5)


if __name__ == "__main__":
    unittest.main()
