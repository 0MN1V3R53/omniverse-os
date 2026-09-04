"""
Unit and Integration Test Suite for Associative Neural Substrate & Dual-Process Routing.
Tests Spreading Activation, System 1/System 2 Dispatching, and Sleep Memory Consolidation.
"""

import tempfile
import unittest
from pathlib import Path

from core.cognition.spreading_activation import SpreadingActivationEngine
from core.orchestrator.dual_process import DualProcessDispatcher
from core.evolution.sleep_daemon import SleepConsolidationDaemon


class TestNeuralSubstrate(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

        self.topology_path = self.temp_path / "synaptic_weights.json"
        self.activation_engine = SpreadingActivationEngine(topology_path=self.topology_path)

        self.scratchpad_dir = self.temp_path / ".scratchpad"
        self.topology_doc = self.temp_path / "network_topology.md"
        self.sleep_daemon = SleepConsolidationDaemon(
            scratchpad_dir=self.scratchpad_dir,
            topology_doc=self.topology_doc
        )

        self.dispatcher = DualProcessDispatcher()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_spreading_activation_propagation_and_filtering(self):
        """Test energy propagation through synapses and active context set filtering."""
        # Inject energy into syntax refactor concept
        activations = self.activation_engine.propagate_activation({"concept:syntax_refactor": 1.0})
        self.assertGreater(activations.get("agent:web_frontend_julian_thorne", 0.0), 0.70)
        self.assertGreater(activations.get("tool:ast_navigator", 0.0), 0.50)

        # Context filtering (threshold >= 0.70)
        active_set = self.activation_engine.get_active_context_set(threshold=0.70)
        active_ids = [n.node_id for n in active_set]
        self.assertIn("concept:syntax_refactor", active_ids)
        self.assertIn("agent:web_frontend_julian_thorne", active_ids)

        # Unrelated nodes should remain sub-threshold
        self.assertNotIn("agent:growth_meta_buyer", active_ids)

    def test_hebbian_synaptic_reinforcement_and_decay(self):
        """Test strengthening co-active synapses and decaying unused pathways."""
        initial_weight = 0.5
        for edge in self.activation_engine.topology.edges:
            if edge.source_id == "concept:route_conversion" and edge.target_id == "agent:growth_meta_buyer":
                initial_weight = edge.weight
                break

        # Reinforce
        self.activation_engine.reinforce_synapse("concept:route_conversion", "agent:growth_meta_buyer", delta=0.05)
        for edge in self.activation_engine.topology.edges:
            if edge.source_id == "concept:route_conversion" and edge.target_id == "agent:growth_meta_buyer":
                self.assertGreater(edge.weight, initial_weight)
                break

        # Decay
        self.activation_engine.decay_all_synapses(decay_rate=0.95)
        for edge in self.activation_engine.topology.edges:
            if edge.source_id == "concept:route_conversion" and edge.target_id == "agent:growth_meta_buyer":
                self.assertLess(edge.weight, 1.0)
                break

    def test_dual_process_system_1_reflex_path(self):
        """Test fast reflex execution bypass (0 tokens) for verified high-confidence skill."""
        # Query matching registered skill or verified causal state
        res = self.dispatcher.route_and_execute(
            task_query="Cognitive AST Verifier",
            context_state="high_bounce_on_mobile_route"
        )
        self.assertEqual(res.decision.pathway, "SYSTEM_1_REFLEX")
        self.assertEqual(res.token_cost, 0)
        self.assertTrue(res.success)
        self.assertIn("[SYSTEM 1 FAST-PATH]", res.output_summary)

    def test_dual_process_system_2_cortical_path(self):
        """Test escalation to Dialectical Triad for novel unverified objectives."""
        res = self.dispatcher.route_and_execute(
            task_query="Design a novel zero-knowledge cryptographic state proof for corridor routes",
            context_state="unprecedented_cryptographic_zk_state"
        )
        self.assertEqual(res.decision.pathway, "SYSTEM_2_CORTICAL")
        self.assertGreater(res.token_cost, 0)
        self.assertTrue(res.success)
        self.assertIn("[SYSTEM 2 CORTICAL]", res.output_summary)

    def test_sleep_consolidation_daemon_replay_and_archive(self):
        """Test replaying scratchpad logs, distilling heuristics, and archiving stale buffers."""
        # Create test log in scratchpad
        test_log = self.scratchpad_dir / "test_error_log.log"
        test_log.write_text("Tool execution exception encountered in network buffer.", encoding="utf-8")

        report = self.sleep_daemon.run_sleep_consolidation_pass(max_logs_to_process=5)
        self.assertEqual(report.scratchpad_logs_replayed, 1)
        self.assertEqual(report.heuristics_distilled, 1)
        self.assertEqual(report.archived_buffer_count, 1)
        self.assertFalse(test_log.exists())
        self.assertTrue((self.sleep_daemon.archive_dir / "test_error_log.log").exists())
        self.assertTrue(self.topology_doc.exists())


if __name__ == "__main__":
    unittest.main()
