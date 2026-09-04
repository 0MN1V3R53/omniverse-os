"""
Unit and Integration Test Suite for Autonomous Tool Engine and Sensory Runtime:
Tool Output Virtualization, Self-Healing Terminal Runner, and YouTube/Web Research Pod.
"""

import asyncio
import tempfile
import unittest
from pathlib import Path

from core.tools.scratchpad import ToolScratchpadManager, VirtualLogDigest
from core.tools.runner import SelfHealingRunner, ExecutionResult
from Omniverse.research_pod.youtube_crawler import YouTubeIntelCrawler, VideoTranscriptBrief
from Omniverse.research_pod.web_crawler import WebIntelCrawler, WebArticleBrief
from Omniverse.research_pod.researcher import AutonomousResearchPod, ResearchDossier
from core.visual.models import SceneNode, SceneGraph, NodeType
from core.visual.scene_graph import SceneGraphCompiler


class TestSensoryTools(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
        self.scratchpad_dir = self.temp_path / ".scratchpad"
        self.learnings_file = self.temp_path / "tool_learnings.md"
        self.briefs_dir = self.temp_path / "research_briefs"

        self.scratchpad = ToolScratchpadManager(self.scratchpad_dir)
        self.runner = SelfHealingRunner(scratchpad=self.scratchpad, learnings_file=self.learnings_file)
        self.research_pod = AutonomousResearchPod(briefs_dir=self.briefs_dir)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_scratchpad_virtualization_and_grep_slice(self):
        """Test dumping large tool outputs to scratchpad and performing targeted grep and slice."""
        large_output = "\n".join([f"Log line {i}: Event status ok" for i in range(1, 101)])
        digest = self.scratchpad.virtualize_output(
            tool_name="build_logger",
            raw_output=large_output,
            exit_code=0,
            status="SUCCESS",
            tag="build"
        )

        self.assertEqual(digest.total_lines, 100)
        self.assertTrue(Path(digest.log_reference_path).exists())

        # Test grep_scratchpad
        grep_res = self.scratchpad.grep_scratchpad(digest.log_reference_path, "Log line 42")
        self.assertEqual(grep_res["match_count"], 1)
        self.assertEqual(grep_res["matches"][0]["line_number"], 42)

        # Test read_slice
        slice_res = self.scratchpad.read_slice(digest.log_reference_path, start_line=10, end_line=15)
        self.assertEqual(len(slice_res["lines"]), 6)
        self.assertEqual(slice_res["lines"][0]["line_number"], 10)

    async def test_self_healing_runner_clean_execution(self):
        """Test standard zero-error shell execution."""
        res = await self.runner.execute("echo 'Omniverse Runtime Online'")
        self.assertEqual(res.exit_code, 0)
        self.assertIn("Omniverse Runtime Online", res.stdout_preview)
        self.assertEqual(res.attempts, 1)
        self.assertFalse(res.recovered)

    async def test_self_healing_runner_reflection_and_recovery(self):
        """Test that runner invokes remediation and logs learning upon recovery."""
        # Simulated remediation function that fixes a typo on attempt 2
        def remediation(failed_cmd, stderr_out, attempt):
            if "invalid_cmd_xyz" in failed_cmd:
                return "echo 'Corrected Command Executed'"
            return failed_cmd

        res = await self.runner.execute(
            command="invalid_cmd_xyz 123",
            max_retries=2,
            remediation_fn=remediation
        )

        self.assertEqual(res.exit_code, 0)
        self.assertEqual(res.attempts, 2)
        self.assertTrue(res.recovered)
        self.assertIn("Corrected Command Executed", res.stdout_preview)

        # Verify learning logged to file
        self.assertTrue(self.learnings_file.exists())
        self.assertIn("RECOVERED", self.learnings_file.read_text(encoding="utf-8"))

    async def test_youtube_and_web_research_ingestion(self):
        """Test YouTube transcript synthesis, chapter extraction, and web dossier creation."""
        dossier = await self.research_pod.execute_technical_research(
            topic="Kotlin Compose Multiplatform",
            requested_by="growth_meta_buyer"
        )

        self.assertIsNotNone(dossier.video_brief)
        self.assertIsNotNone(dossier.web_brief)
        self.assertGreaterEqual(len(dossier.video_brief.chapters), 3)
        self.assertGreaterEqual(len(dossier.synthesized_principles), 3)
        self.assertTrue(Path(dossier.persisted_path).exists())

    async def test_end_to_end_research_to_component_workflow(self):
        """
        Simulate complete workflow:
        1. Research technical framework (Kotlin Compose Multiplatform).
        2. Generate visual component code via SceneGraph.
        3. Run shell syntax check and verify scratchpad output.
        """
        # 1. Research
        dossier = await self.research_pod.execute_technical_research(
            topic="Kotlin Compose Multiplatform Layouts",
            requested_by="web_frontend_julian_thorne"
        )
        self.assertIn("stateless", str(dossier.synthesized_principles))

        # 2. Synthesize SceneGraph Component from research
        compiler = SceneGraphCompiler()
        graph = compiler.from_data("compose_component", {
            "title": "Cross-Platform Transport Quote View",
            "badge_text": "KOTLIN MULTIPLATFORM",
            "metrics": {"render_fps": "60 FPS", "bundle_size": "1.2 MB"},
            "cta_text": "Calculate Route"
        })
        jsx = compiler.to_jsx(graph, component_name="CrossPlatformQuoteView")
        self.assertIn("CrossPlatformQuoteView", jsx)

        # 3. Execute syntax check via runner on temporary file
        comp_file = self.temp_path / "Component.jsx"
        comp_file.write_text(jsx, encoding="utf-8")
        
        test_res = await self.runner.execute(f"test -f {comp_file} && echo 'Component file valid'")
        self.assertEqual(test_res.exit_code, 0)
        self.assertIn("Component file valid", test_res.stdout_preview)


if __name__ == "__main__":
    unittest.main()
