"""
Unit and Integration Test Suite for Autonomous Evolution, Causal Cognition & Morphogenesis Engine.
"""

import tempfile
import unittest
from pathlib import Path

from core.cognition.models import CausalLink, CausalMatrix
from core.cognition.causal_graph import CausalGraphEngine
from core.evolution.heartbeat import HeartbeatDaemon, HeartbeatProposal, HeartbeatTickReport
from core.evolution.darwin import DarwinianOptimizer, PersonaVariant, DarwinianEvaluationResult
from core.evolution.rfc_governance import RFCEngine, PodVote, RFCGovernanceReport
from core.evolution.morphogenesis import MorphogenesisEngine, DynamicAgentRecord


class TestEvolutionMorphogenesis(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
        
        self.matrix_path = self.temp_path / "causal_matrix.json"
        self.proposals_dir = self.temp_path / "proposals"
        self.mutations_dir = self.temp_path / "mutations"
        self.dynamic_dir = self.temp_path / "dynamic"

        self.causal_engine = CausalGraphEngine(matrix_path=self.matrix_path)
        self.heartbeat = HeartbeatDaemon(proposals_dir=self.proposals_dir)
        self.darwin = DarwinianOptimizer(mutations_dir=self.mutations_dir)
        self.rfc_engine = RFCEngine()
        self.morphogenesis = MorphogenesisEngine(dynamic_dir=self.dynamic_dir)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_causal_graph_record_and_query(self):
        """Test recording causal observation and querying optimal strategy."""
        link = self.causal_engine.record_outcome(
            context_state="custom_conversion_anomaly",
            action_taken="deploy_instant_quote_badge",
            observed_impact="lift_14pct",
            success=True
        )
        self.assertEqual(link.context_state, "custom_conversion_anomaly")
        self.assertTrue(self.matrix_path.exists())

        # Query best action
        best = self.causal_engine.query_best_action("custom_conversion_anomaly")
        self.assertIsNotNone(best)
        self.assertEqual(best.action_taken, "deploy_instant_quote_badge")

    def test_heartbeat_daemon_initiatives(self):
        """Test autonomous heartbeat scans and RFC proposal drafting."""
        report = self.heartbeat.run_heartbeat_cycle()
        self.assertIsInstance(report, HeartbeatTickReport)
        self.assertGreater(report.detected_opportunities, 0)
        self.assertTrue(Path(report.proposals_generated[0].persisted_path).exists())

    def test_darwinian_mutation_and_selection(self):
        """Test spawning variant and merging winning traits."""
        variant = self.darwin.spawn_variant("growth_meta_buyer", "High-Velocity Converter")
        self.assertIn("Darwinian Mutation", variant.system_prompt_overlay)

        res = self.darwin.evaluate_and_select(
            base_agent_id="growth_meta_buyer",
            variant=variant,
            baseline_output="Basic headline without lock badge.",
            variant_output="Hardened headline with SVG lock and responsive typography."
        )
        self.assertTrue(res.variant_won)
        self.assertEqual(res.winning_variant_id, variant.variant_id)
        self.assertTrue(Path(res.mutation_log_path).exists())

    def test_rfc_governance_multi_pod_voting(self):
        """Test decentralized RFC voting and quorum verification."""
        proposal = HeartbeatProposal(
            origin_pod="Growth Squad",
            lead_agent_id="growth_meta_buyer",
            title="Deploy Instant Transport Rate Cards",
            problem_statement="Bounce rate on routes is high.",
            proposed_solution="Compile SceneGraph banners.",
            impacted_pods=["Growth Squad", "Web Engineering", "DevOps SRE"]
        )

        report = self.rfc_engine.conduct_voting_session(proposal)
        self.assertTrue(report.quorum_reached)
        self.assertEqual(report.final_status, "APPROVED")
        self.assertIsNotNone(report.execution_ticket_id)

    def test_morphogenesis_spawning_and_pruning(self):
        """Test dynamic specialist spawning and inactivity consolidation."""
        agent = self.morphogenesis.spawn_specialist_agent(
            specialist_name="WASM Route Renderer",
            role_title="WebAssembly Route Compilation Specialist",
            parent_pod="Web Engineering",
            spawn_reason="Accelerate sub-millisecond client price rendering."
        )
        self.assertEqual(agent.agent_id, "dynamic_wasm_route_renderer")
        self.assertTrue(Path(agent.persisted_path).exists())

        # Age agent to simulate idle cycles
        agent.cycles_active = 5
        pruned = self.morphogenesis.prune_and_consolidate(max_idle_cycles=3)
        self.assertIn("dynamic_wasm_route_renderer", pruned)
        self.assertFalse(agent.is_active)

    def test_end_to_end_evolutionary_simulation_cycle(self):
        """
        Simulate full decentralized lifecycle:
        1. Heartbeat detects opportunity & drafts RFC.
        2. Impacted pods vote and approve RFC.
        3. Causal graph queries best action and records execution outcome.
        4. Darwinian optimizer evolves persona heuristics.
        5. Morphogenesis manager registers dynamic specialist.
        """
        # 1. Heartbeat Tick
        tick = self.heartbeat.run_heartbeat_cycle()
        proposal = tick.proposals_generated[0]

        # 2. RFC Voting
        rfc_report = self.rfc_engine.conduct_voting_session(proposal)
        self.assertTrue(rfc_report.quorum_reached)

        # 3. Causal Graph Strategy Selection & Execution Record
        best_action = self.causal_engine.query_best_action("mobile_route")
        self.assertIsNotNone(best_action)
        self.causal_engine.record_outcome(
            context_state="east_to_west_mobile_route",
            action_taken=best_action.action_taken,
            observed_impact="conversion_rate_recovered_to_4.1pct",
            success=True
        )

        # 4. Darwinian Trait Evolution
        variant = self.darwin.spawn_variant("growth_meta_buyer")
        darwin_res = self.darwin.evaluate_and_select(
            base_agent_id="growth_meta_buyer",
            variant=variant,
            baseline_output="baseline",
            variant_output="optimized"
        )
        self.assertTrue(darwin_res.variant_won)

        # 5. Dynamic Specialist Spawning
        specialist = self.morphogenesis.spawn_specialist_agent(
            specialist_name="Corridor Latency Optimizer",
            role_title="East-to-West Route Optimization Specialist",
            parent_pod="Growth Squad",
            spawn_reason="Manage dynamic rate adjustments for East-to-West corridors."
        )
        self.assertTrue(specialist.is_active)


if __name__ == "__main__":
    unittest.main()
