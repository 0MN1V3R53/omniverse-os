"""
Unit and Integration Test Suite for Apex Systems Architecture Upgrade.
Tests AST Navigation, Multiverse Sandbox, Invariant Guards, JIT Skill Vault, and Panopticon Server.
"""

import tempfile
import unittest
import urllib.request
import json
from pathlib import Path

from core.ast_engine.navigator import ASTNavigator

from core.sandbox.multiverse import MultiverseSandboxEngine
from core.guards.invariants import InvariantVerifier
from core.skills.vault import SkillVaultEngine
from core.ui.panopticon_server import PanopticonServer


class TestApexEngineering(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
        
        self.ast_nav = ASTNavigator(workspace_root=self.temp_path)
        self.sandbox = MultiverseSandboxEngine(sandbox_root=self.temp_path / ".sandbox")
        
        # Invariants setup
        self.rules_file = self.temp_path / "invariants.json"
        self.rules_file.write_text(json.dumps({
            "invariants": [
                {
                    "invariant_id": "INV-NO-MOCK-DATA",
                    "category": "data_integrity",
                    "severity": "BLOCKER",
                    "description": "No mock data allowed",
                    "prohibited_patterns": ["mock_data", "fake_user"]
                }
            ]
        }), encoding="utf-8")
        self.verifier = InvariantVerifier(rules_path=self.rules_file)
        self.vault = SkillVaultEngine(skills_dir=self.temp_path / "skills")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_ast_navigator_integrity_and_symbols(self):
        """Test AST syntax validation and symbol tracking."""
        valid_code = "class TransportQuote:\n    def calculate_total(self):\n        return 1500\n"
        rep = self.ast_nav.verify_ast_integrity(valid_code)
        self.assertTrue(rep.is_valid_syntax)
        self.assertIn("TransportQuote", rep.defined_classes)
        self.assertIn("calculate_total", rep.defined_functions)

        invalid_code = "class Broken(:\n    pass\n"
        rep_inv = self.ast_nav.verify_ast_integrity(invalid_code)
        self.assertFalse(rep_inv.is_valid_syntax)

    def test_multiverse_sandbox_racing(self):
        """Test staging parallel candidate branches and selecting the winning diff."""
        code_v1 = "class CorridorQuote:\n    # High Performance\n    rate = 1450\n"
        code_v2 = "class CorridorQuote:\n    # Simple\n    rate = 1450\n"

        b1 = self.sandbox.stage_candidate_branch("models/quote.py", code_v1, "PerformanceOptimized")
        b2 = self.sandbox.stage_candidate_branch("models/quote.py", code_v2, "SimplicityFirst")

        result = self.sandbox.race_and_select_winner([b1, b2], auto_commit=False)
        self.assertEqual(result.winning_branch_id, b1.branch_id)
        self.assertEqual(result.winning_paradigm, "PerformanceOptimized")

    def test_neuro_symbolic_invariant_verifier(self):
        """Test blocking violations and passing clean code."""
        clean_code = "class LiveCarrier:\n    carrier_id = 'US-DOT-9921'\n"
        rep_clean = self.verifier.validate_code("carrier.py", clean_code)
        self.assertTrue(rep_clean.passed)
        self.assertEqual(len(rep_clean.violations), 0)

        dirty_code = "class MockCarrier:\n    carrier_id = mock_data.fake_user()\n"
        rep_dirty = self.verifier.validate_code("carrier.py", dirty_code)
        self.assertFalse(rep_dirty.passed)
        self.assertEqual(len(rep_dirty.violations), 1)
        self.assertEqual(rep_dirty.violations[0].invariant_id, "INV-NO-MOCK-DATA")

    def test_jit_skill_vault_compilation_and_discovery(self):
        """Test self-compiling an executable Python CLI tool into the Skill Vault."""
        script_code = """import sys
if __name__ == '__main__':
    origin = sys.argv[1] if len(sys.argv) > 1 else 'Miami'
    print(f"CALCULATED_ROUTE_RATE:{origin}->Los Angeles:$1650")
"""
        skill = self.vault.compile_and_register_skill(
            name="Route Rate Estimator",
            domain="seo",
            description="Computes transport corridor estimates for route pages.",
            author_agent_id="growth_meta_buyer",
            python_code=script_code,
            input_parameters={"origin": "Origin city name"},
            output_schema={"rate": "Formatted route quote"}
        )
        self.assertEqual(skill.name, "Route Rate Estimator")
        self.assertTrue(Path(self.vault.skills_dir / "manifest.json").exists())

        # Discover skill
        found = self.vault.discover_skills("Rate Estimator")
        self.assertEqual(len(found), 1)

        # Execute skill
        output = self.vault.execute_skill(skill.skill_id, ["Orlando"])
        self.assertIn("CALCULATED_ROUTE_RATE:Orlando->Los Angeles:$1650", output)

    def test_panopticon_server_telemetry_endpoint(self):
        """Test Panopticon server background launch and REST telemetry response."""
        server = PanopticonServer(port=8991)
        server.start_background()
        try:
            with urllib.request.urlopen("http://localhost:8991/api/telemetry") as response:
                self.assertEqual(response.status, 200)
                data = json.loads(response.read().decode("utf-8"))
                self.assertIn("active_agents", data)
                self.assertIn("causal_links_count", data)

            with urllib.request.urlopen("http://localhost:8991/panopticon") as response:
                self.assertEqual(response.status, 200)
                html = response.read().decode("utf-8")
                self.assertIn("PANOPTICON", html)
        finally:
            server.stop()

    def test_integrated_apex_refactor_pipeline(self):
        """
        Integrated task:
        1. Verify AST integrity of base model.
        2. Race 2 speculative candidate branches in Sandbox.
        3. Verify invariants on winning branch.
        4. Compile winning pattern into JIT Skill Vault.
        """
        base_code = "class CorridorModel:\n    corridor_id: str = 'FL-CA'\n"
        ast_rep = self.ast_nav.verify_ast_integrity(base_code)
        self.assertTrue(ast_rep.is_valid_syntax)

        cand1 = self.sandbox.stage_candidate_branch("corridor.py", base_code, "PerformanceOptimized")
        cand2 = self.sandbox.stage_candidate_branch("corridor.py", base_code + "    # Extra comments\n", "SimplicityFirst")
        race_res = self.sandbox.race_and_select_winner([cand1, cand2], auto_commit=False)
        self.assertEqual(race_res.winning_branch_id, cand1.branch_id)

        inv_rep = self.verifier.validate_code("corridor.py", cand1.staged_code)
        self.assertTrue(inv_rep.passed)

        skill_code = "import sys\nprint('REFAC_SKILL_SUCCESS')\n"
        skill = self.vault.compile_and_register_skill(
            name="Corridor AST Validator",
            domain="tooling",
            description="Validates corridor ASTs",
            author_agent_id="web_frontend_julian_thorne",
            python_code=skill_code
        )
        self.assertIsNotNone(skill.skill_id)


if __name__ == "__main__":
    unittest.main()
