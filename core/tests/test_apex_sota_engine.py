"""
Omniverse Apex SOTA Engine Test Suite
=====================================
Validates Dimension 5 (Apex Theorem & Code Synthesizer),
Dimension 6 (Graph-RAG Virtual Context Paging Engine),
and Dimension 7 (Zero-Copy Multimodal Sensory Bridge).
"""

import unittest
from core.cognition.apex_theorem_solver import ApexTheoremSolver, DialecticCodeSynthesizer
from core.cognition.graph_rag_virtualizer import VirtualContextPagingEngine
from core.visual.zero_copy_sensory_bridge import ZeroCopySensoryBridge

class TestApexSotaEngine(unittest.TestCase):

    def setUp(self):
        self.theorem_solver = ApexTheoremSolver()
        self.code_synthesizer = DialecticCodeSynthesizer()
        self.context_pager = VirtualContextPagingEngine(dimension=16)
        self.sensory_bridge = ZeroCopySensoryBridge()

    # --- Dimension 5 Tests ---
    def test_dimension_5_symbolic_math_solver(self):
        # Exact arithmetic and transcendental functions
        expr = "sin(pi / 2) + sqrt(16) * 2 + factorial(5)"
        sol = self.theorem_solver.solve_symbolic_expression(expr)
        self.assertTrue(sol.is_formally_verified)
        self.assertEqual(sol.final_result, 1.0 + 8.0 + 120)  # 129.0
        self.assertLess(sol.execution_time_ms, 50.0)

    def test_dimension_5_polynomial_roots(self):
        # x^2 - 5x + 6 = 0 -> roots 3 and 2
        r1, r2 = self.theorem_solver.solve_polynomial_roots(1, -5, 6)
        self.assertEqual(r1.real, 3.0)
        self.assertEqual(r2.real, 2.0)

    def test_dimension_5_dialectic_code_synthesizer(self):
        code = """
def calculate_corridor_multiplier(base_rate, distance_miles):
    if distance_miles > 1000:
        return base_rate * 1.25
    return base_rate * 1.10
"""
        test_specs = [
            {"function": "calculate_corridor_multiplier", "inputs": [100.0, 500], "expected": 110.0},
            {"function": "calculate_corridor_multiplier", "inputs": [100.0, 1500], "expected": 125.0}
        ]
        res = self.code_synthesizer.synthesize_and_verify(code, test_specs)
        self.assertTrue(res.ast_valid)
        self.assertTrue(res.is_production_ready)
        self.assertEqual(res.unit_tests_passed, 2)
        self.assertEqual(len(res.invariant_violations), 0)

    # --- Dimension 6 Tests ---
    def test_dimension_6_graph_rag_virtualizer(self):
        # Register nodes and dependencies
        n1 = self.context_pager.register_node(
            "pricing_engine", "Dynamic corridor pricing specialist algorithm with fuel surcharge.", "AST_FUNCTION", ["pricing", "corridor"]
        )
        n2 = self.context_pager.register_node(
            "fuel_index", "Real-time EIA diesel fuel price indexer and regional adjuster.", "HEURISTIC_RULE", ["fuel", "pricing"]
        )
        n3 = self.context_pager.register_node(
            "route_mesh", "50-state geographical shortest-path graph router.", "SCHEMA", ["route", "geo"]
        )

        self.context_pager.link_nodes("pricing_engine", "fuel_index")
        self.context_pager.link_nodes("pricing_engine", "route_mesh")

        # Query with HyDE expansion
        result = self.context_pager.query_with_hyde_expansion("Calculate dynamic freight corridor pricing", top_k=2)
        self.assertGreater(len(result.primary_nodes), 0)
        self.assertGreater(len(result.expanded_subgraph), 0)
        self.assertLess(result.retrieval_latency_ms, 25.0)

    # --- Dimension 7 Tests ---
    def test_dimension_7_zero_copy_sensory_bridge(self):
        raw_elements = [
            {"id": "btn_quote", "tag": "button", "x": 10, "y": 20, "width": 120, "height": 40, "color": "#00f0ff"},
            {"id": "hero_canvas", "tag": "canvas", "x": 0, "y": 0, "width": 1920, "height": 1080, "color": "#04060a"}
        ]
        raw_audio_fft = [0.1, 0.2, 0.8, 0.95, 0.4, 0.2, 0.05]

        # Initial frame (both elements dirty)
        pkt1 = self.sensory_bridge.stream_telemetry_packet(raw_elements, raw_audio_fft)
        self.assertEqual(len(pkt1.active_visual_deltas), 2)
        self.assertTrue(pkt1.is_realtime_capable)

        # Second frame with no visual changes (differential delta = 0)
        pkt2 = self.sensory_bridge.stream_telemetry_packet(raw_elements, raw_audio_fft)
        self.assertEqual(len(pkt2.active_visual_deltas), 0)
        self.assertAlmostEqual(pkt2.bandwidth_saved_ratio, 1.0)

if __name__ == '__main__':
    unittest.main()
