"""
Unit and Integration Test Suite for Autonomous Dialectic, Pre-Flight Audit & Reflexion Upgrades.
"""

import unittest
from pathlib import Path

from core.dialectic.models import PreFlightAuditReport, ArchitecturalOption, CritiqueReport, SynthesizedPlan
from core.dialectic.preflight import PreFlightAuditor
from core.dialectic.engine import DialecticEngine
from core.reflexion.models import SelfCritiqueRubric, ReflexionResult
from core.reflexion.evaluator import AutonomousReflexionLoop
from core.environment.observer import EnvironmentObserver, EnvironmentSnapshot


class TestDialecticCognition(unittest.TestCase):

    def setUp(self):
        self.preflight = PreFlightAuditor()
        self.dialectic = DialecticEngine()
        self.reflexion = AutonomousReflexionLoop()
        self.observer = EnvironmentObserver()

    def test_preflight_auditor_scan(self):
        """Test preflight auditor scans workspace and emits readiness report."""
        report = self.preflight.audit_objective("campaign optimization telemetry")
        self.assertIsInstance(report, PreFlightAuditReport)
        self.assertGreaterEqual(report.readiness_score, 0.5)
        self.assertIn("PROCEED", report.recommendation)

    def test_dialectic_three_stage_deliberation(self):
        """Test Stage 1 Divergence, Stage 2 Critique, Stage 3 Synthesis."""
        objective = "Architect an autonomous campaign optimization feature"
        options, critiques, plan = self.dialectic.run_full_deliberation(
            objective=objective,
            lead_agent_id="growth_meta_buyer",
            auditor_agent_id="security_ciso_michael_chang",
            synthesizer_agent_id="exec_ceo_alexander_vance"
        )

        # Divergence: 3 distinct options
        self.assertEqual(len(options), 3)
        self.assertNotEqual(options[0].paradigm, options[1].paradigm)

        # Critique: 3 critiques stress-testing each option
        self.assertEqual(len(critiques), 3)
        for c in critiques:
            self.assertTrue(len(c.vulnerabilities) > 0 or len(c.edge_cases) > 0)

        # Synthesis: Hardened plan combines strongest elements
        self.assertIsInstance(plan, SynthesizedPlan)
        self.assertGreaterEqual(len(plan.hardened_mechanisms), 3)
        self.assertGreaterEqual(len(plan.execution_steps), 3)

    def test_reflexion_evaluator_clean_pass(self):
        """Test rubric passes clean non-baseline code with error handling."""
        clean_code = """
def calculate_optimal_bid(conversion_rate: float, cpa_target: float) -> float:
    try:
        if conversion_rate <= 0:
            return 0.0
        return round(conversion_rate * cpa_target, 2)
    except Exception as e:
        raise ValueError(f"Calculation failed: {e}")
"""
        rubric = self.reflexion.evaluate_draft(clean_code)
        self.assertTrue(rubric.is_novel_and_robust)
        self.assertTrue(rubric.zero_mock_or_hallucinations)
        self.assertTrue(rubric.zero_unhandled_exceptions)
        self.assertGreaterEqual(rubric.overall_quality_score, 0.85)

    def test_reflexion_evaluator_defect_detection_and_refinement(self):
        """Test rubric detects defects (TODO, mock data, no try/except) and refines."""
        defective_code = "def get_traffic():\n    # TODO: implement\n    return mock_data_generator()"
        rubric = self.reflexion.evaluate_draft(defective_code)
        self.assertFalse(rubric.is_novel_and_robust)
        self.assertFalse(rubric.zero_mock_or_hallucinations)
        self.assertLess(rubric.overall_quality_score, 0.85)

        # Execute self-refinement
        res = self.reflexion.execute_self_refinement(
            agent_id="growth_meta_buyer",
            ticket_id="TICKET-REFINE-1",
            initial_draft=defective_code
        )
        self.assertTrue(res.passed)
        self.assertGreaterEqual(res.final_rubric.overall_quality_score, 0.85)

    def test_environment_observer_snapshot(self):
        """Test living environment observer captures live state."""
        snap = self.observer.get_live_snapshot()
        self.assertIsInstance(snap, EnvironmentSnapshot)
        self.assertGreater(len(snap.core_modules), 0)
        self.assertGreaterEqual(snap.active_agent_count, 50)
        self.assertGreaterEqual(len(snap.available_tools), 5)


if __name__ == "__main__":
    unittest.main()
