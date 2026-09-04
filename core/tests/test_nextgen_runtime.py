"""
Unit and Integration Test Suite for Next-Gen Enterprise Runtime Architecture:
Declarative Scene-Graph Engine, Prompt Evolution Engine, Compute Tokenomics, and Closed-Loop Telemetry.
"""

import asyncio
import tempfile
import unittest
from pathlib import Path

from core.visual.models import SceneNode, SceneGraph, NodeType, LayoutConfig, StyleConfig
from core.visual.scene_graph import SceneGraphCompiler
from core.evolution.models import HeuristicRule, ReflexionReport
from core.evolution.engine import PromptEvolutionEngine
from core.economy.models import PodBudget, ComputeTransaction, BidProposal
from core.economy.ledger import CreditLedger, InsufficientCreditsError
from core.economy.auction import AuctionRouter
from core.telemetry_bus.models import TelemetryMetricEvent, IncidentTrigger
from core.telemetry_bus.monitor import ClosedLoopTelemetryMonitor
from core.bus.bus import MessageBus


class TestNextGenRuntime(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
        self.heuristics_dir = self.temp_path / "heuristics"
        self.ledger_path = self.temp_path / "compute_ledger.jsonl"
        self.bus = MessageBus()

        self.scene_compiler = SceneGraphCompiler()
        self.evolution_engine = PromptEvolutionEngine(self.heuristics_dir)
        self.credit_ledger = CreditLedger(self.ledger_path)
        self.telemetry_monitor = ClosedLoopTelemetryMonitor(self.bus)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_scene_graph_to_jsx_and_html(self):
        """Test compiling SceneGraph AST into React JSX and HTML5."""
        graph = SceneGraph(title="Test Corridor Banner")
        card = SceneNode(node_type=NodeType.CARD, name="MainCard")
        badge = SceneNode(node_type=NodeType.BADGE, content="$0 Deposit")
        btn = SceneNode(node_type=NodeType.BUTTON, content="Book Now")
        card.add_child(badge).add_child(btn)
        graph.root_node = card

        jsx = self.scene_compiler.to_jsx(graph, component_name="CorridorBanner")
        self.assertIn("export function CorridorBanner()", jsx)
        self.assertIn("$0 Deposit", jsx)
        self.assertIn("Book Now", jsx)
        self.assertIn("select-none", jsx)

        html = self.scene_compiler.to_html(graph)
        self.assertIn("scene-graph-root", html)

    def test_scene_graph_from_data_synthesis(self):
        """Test synthesizing a SceneGraph directly from raw marketing/analytics data."""
        data_payload = {
            "title": "Florida to New York Transport Rate",
            "badge_text": "GUARANTEED CARRIER",
            "metrics": {
                "transit_days": "2-3 Days",
                "open_carrier": "$850",
                "enclosed_carrier": "$1,250"
            },
            "cta_text": "Lock In Guaranteed Rate"
        }
        graph = self.scene_compiler.from_data("campaign", data_payload)
        self.assertEqual(graph.title, "Florida to New York Transport Rate")
        self.assertEqual(len(graph.root_node.children), 3)  # Header, MetricsGrid, CTA

        jsx = self.scene_compiler.to_jsx(graph, component_name="FloridaRouteView")
        self.assertIn("Florida to New York", jsx)
        self.assertIn("2-3 Days", jsx)
        self.assertIn("Lock In Guaranteed Rate", jsx)

    def test_prompt_evolution_and_reflexion_loop(self):
        """Test post-execution reflexion, rule generation, and prompt injection."""
        agent_id = "growth_meta_buyer"
        base_prompt = "You are a senior media buyer specializing in auto transport."

        # Simulate a defect detected on a ticket
        report = self.evolution_engine.evaluate_and_evolve(
            ticket_id="TICKET-DEFECT-1",
            agent_id=agent_id,
            execution_success=False,
            error_or_defect="State names were split mid-word across line breaks.",
            category="layout"
        )

        self.assertFalse(report.success)
        self.assertIsNotNone(report.proposed_rule)

        # Verify rule written to disk and injected into prompt
        injected = self.evolution_engine.inject_heuristics_into_prompt(agent_id, base_prompt)
        self.assertIn("Epigenetic Learned Invariants", injected)
        self.assertIn("State names were split mid-word", injected)

        # Verify version snapshot
        agent_dir = self.heuristics_dir / agent_id
        versions = list((agent_dir / "versions").glob("v*.json"))
        self.assertEqual(len(versions), 1)

    def test_compute_tokenomics_ledger(self):
        """Test credit ledger charges, balance deductions, and quota capping."""
        pod = "Web Frontend"
        initial_budget = self.credit_ledger.get_budget(pod)
        initial_available = initial_budget.available_credits

        # Charge 10,000 tokens (0.50 credits at rate 0.05 / 1k)
        tx = self.credit_ledger.charge_compute(
            agent_id="web_frontend_julian_thorne",
            pod_name=pod,
            ticket_id="TICKET-COMPUTE-1",
            tokens_consumed=10000
        )

        self.assertEqual(tx.credits_deducted, 0.50)
        self.assertEqual(self.credit_ledger.get_budget(pod).available_credits, round(initial_available - 0.50, 4))
        self.assertTrue(self.ledger_path.exists())

    def test_auction_bidding_router(self):
        """Test auction bidding router selecting the most token-efficient sub-agent."""
        bids = [
            BidProposal(agent_id="junior_dev", task_id="T-1", proposed_cost_credits=0.02, estimated_latency_ms=200.0, quality_score=0.85),
            BidProposal(agent_id="staff_dev", task_id="T-1", proposed_cost_credits=0.08, estimated_latency_ms=50.0, quality_score=0.98),
            BidProposal(agent_id="senior_dev", task_id="T-1", proposed_cost_credits=0.04, estimated_latency_ms=80.0, quality_score=0.95),
        ]
        best_bid = AuctionRouter.evaluate_bids(bids)
        self.assertIsNotNone(best_bid)
        # senior_dev balances high quality (0.95) and low cost/latency
        self.assertEqual(best_bid.agent_id, "senior_dev")

    async def test_closed_loop_telemetry_incident_dispatch(self):
        """Test automated emergency ticket dispatch when telemetry breaches threshold."""
        # 1. Subscribe Growth pod to incident topics on MessageBus
        growth_sub = self.bus.subscribe("growth_meta_buyer", topics=["incident.growth", "tasks.growth_meta_buyer"])

        # 2. Ingest a telemetry breach (conversion rate dropped to 1.8% vs threshold 3.5%)
        metric = TelemetryMetricEvent(
            subsystem="marketing_funnel",
            metric_name="funnel_conversion_rate",
            current_value=1.8,
            threshold=3.5,
            operator="<",
            severity="CRITICAL"
        )
        self.assertTrue(metric.is_breach)

        incident = await self.telemetry_monitor.ingest_metric(metric)
        self.assertIsNotNone(incident)
        self.assertEqual(incident.target_pod, "growth")
        self.assertEqual(incident.assigned_dri, "growth_meta_buyer")

        # 3. Pull emergency ticket from the agent's queue
        emergency_event = await self.bus.pull("growth_meta_buyer", timeout=1.0)
        self.assertIsNotNone(emergency_event)
        self.assertIn("incident", emergency_event.topic)


if __name__ == "__main__":
    unittest.main()
