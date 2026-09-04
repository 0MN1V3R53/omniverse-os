"""
End-to-End Integration Test for Omniverse Autonomous Agent Runtime.
Simulates a complete 4-tier ticket: Growth -> Frontend -> Quality Gate -> DevOps.
"""

import asyncio
import tempfile
import unittest
from pathlib import Path

from core.runtime.models import (
    ExecutionTicket,
    TaskNode,
    TaskStatus,
    TicketPriority,
)
from core.runtime.checkpointer import Checkpointer
from core.runtime.workflow import WorkflowOrchestrator
from core.guards.quality_gate import QualityGate
from core.guards.consensus import ConsensusEngine
from core.guards.verifiers import ASTSyntaxVerifier, ZeroDriftVerifier, ExitCodeVerifier
from core.telemetry.tracer import LocalTracer
from core.telemetry.circuit_breaker import DelegationCircuitBreaker, CircuitBreakerTrippedError


class TestRuntimeE2E(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "e2e_checkpoints.sqlite"
        self.trace_path = Path(self.temp_dir.name) / "e2e_traces.jsonl"
        self.checkpointer = Checkpointer(self.db_path)
        self.tracer = LocalTracer(self.trace_path)
        self.circuit_breaker = DelegationCircuitBreaker(max_depth=10)

    def tearDown(self):
        self.temp_dir.cleanup()

    async def test_full_ticket_lifecycle(self):
        ticket = ExecutionTicket(
            title="E2E Pipeline Test: Quick Quote Feature",
            description="End-to-end feature specification, development, quality check, and deploy.",
            priority=TicketPriority.HIGH,
            dri_agent_id="web_frontend_julian_thorne"
        )
        trace = self.tracer.start_trace(ticket.ticket_id, ticket.title)

        # 1. Growth Spec Handler
        async def growth_handler(inputs, ctx):
            self.circuit_breaker.record_hop("growth_meta_buyer", inputs)
            sp = self.tracer.start_span(trace.trace_id, "Spec Creation", "growth_meta_buyer")
            await asyncio.sleep(0.01)
            self.tracer.end_span(sp, status="OK")
            return {"spec": "Add $0 Deposit Badge in Hero", "target": "#hero"}

        # 2. Frontend Build Handler
        async def frontend_handler(inputs, ctx):
            self.circuit_breaker.record_hop("web_frontend_julian_thorne", inputs)
            sp = self.tracer.start_span(trace.trace_id, "Frontend Implementation", "web_frontend_julian_thorne")
            await asyncio.sleep(0.01)
            self.tracer.end_span(sp, status="OK")
            return {"component": "Badge.jsx", "code_valid": True}

        # 3. Quality Gate & Verifier Handler
        async def qa_handler(inputs, ctx):
            self.circuit_breaker.record_hop("qa_auto_script", inputs)
            sp = self.tracer.start_span(trace.trace_id, "Quality Gate", "qa_auto_script")
            
            gate = QualityGate("FrontendHandoffGate", dri="qa_auto_script")
            gate.add_check("Syntax Check", lambda c: ASTSyntaxVerifier.verify_python("x = 10")["passed"])
            gate.add_check("Exit Code 0", lambda c: ExitCodeVerifier.verify(0)["passed"])
            
            gate_res = await gate.evaluate()
            if not gate_res.passed:
                self.tracer.end_span(sp, status="ERROR", error="Gate Failed")
                raise RuntimeError("Quality Gate failed")
            
            self.tracer.end_span(sp, status="OK")
            return {"gate_passed": True, "passed_checks": gate_res.passed_checks}

        # 4. DevOps Deployment Handler
        async def devops_handler(inputs, ctx):
            self.circuit_breaker.record_hop("web_devops_marcus_chen", inputs)
            sp = self.tracer.start_span(trace.trace_id, "Production Deployment", "web_devops_marcus_chen")
            await asyncio.sleep(0.01)
            self.tracer.end_span(sp, status="OK")
            return {"deployed": True, "status_code": 200}

        orchestrator = WorkflowOrchestrator(self.checkpointer)
        workflow_state = orchestrator.create_linear_pipeline(
            ticket=ticket,
            steps=[
                {"id": "spec", "name": "Growth Spec", "agent_id": "growth_meta_buyer", "handler": growth_handler},
                {"id": "build", "name": "Frontend Build", "agent_id": "web_frontend_julian_thorne", "handler": frontend_handler},
                {"id": "verify", "name": "QA Quality Gate", "agent_id": "qa_auto_script", "handler": qa_handler},
                {"id": "deploy", "name": "DevOps Deploy", "agent_id": "web_devops_marcus_chen", "handler": devops_handler},
            ]
        )

        final_state = await orchestrator.run(
            ticket=ticket,
            nodes=workflow_state.nodes,
            edges=workflow_state.edges,
        )

        self.assertTrue(final_state.is_completed)
        self.assertEqual(len(final_state.completed_nodes), 4)

        # Verify Checkpointer state
        persisted_ticket = self.checkpointer.get_ticket(ticket.ticket_id)
        self.assertEqual(persisted_ticket.status, TaskStatus.SUCCESS)

        transitions = self.checkpointer.get_transitions(ticket.ticket_id)
        self.assertGreaterEqual(len(transitions), 8)  # 2 transitions per node (RUNNING, SUCCESS)

        # Verify Traces
        finished_trace = self.tracer.finish_trace(trace.trace_id)
        self.assertIsNotNone(finished_trace)
        self.assertEqual(len(finished_trace.spans), 4)
        self.assertTrue(self.trace_path.exists())

    def test_consensus_engine(self):
        engine = ConsensusEngine(ticket_id="TICKET-123")
        engine.require_department("Engineering", authorized_agents=["web_frontend_julian_thorne"], required_votes=1)
        engine.require_department("Security", authorized_agents=["security_ciso_michael_chang"], required_votes=1)

        # Cast Engineering vote
        engine.cast_vote("web_frontend_julian_thorne", "Engineering", approved=True, rationale="Code reviewed")
        reached, _ = engine.evaluate_consensus()
        self.assertFalse(reached)  # Security missing

        # Cast Security vote
        engine.cast_vote("security_ciso_michael_chang", "Security", approved=True, rationale="Zero-trust compliant")
        reached, summary = engine.evaluate_consensus()
        self.assertTrue(reached)
        self.assertTrue(summary["consensus_reached"])

    def test_circuit_breaker_loop_detection(self):
        cb = DelegationCircuitBreaker(max_depth=5, max_cyclic_repeats=2)
        cb.record_hop("agent_a", {"state": 1})
        cb.record_hop("agent_b", {"state": 2})

        # Repeating agent_a with exact same state a 2nd time should trip stagnant loop
        with self.assertRaises(CircuitBreakerTrippedError):
            cb.record_hop("agent_a", {"state": 1})



if __name__ == "__main__":
    unittest.main()
