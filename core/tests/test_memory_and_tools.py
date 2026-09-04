"""
Unit tests for Memory Compactor, Semantic Tagger, Context Decay, and Tool Harness.
"""

import tempfile
import unittest
from pathlib import Path
from pydantic import BaseModel, Field

from core.memory.compactor import MemoryCompactor
from core.memory.tagger import SemanticTagger
from core.memory.context_decay import ContextDecayEngine, MemoryItem
from core.tools.registry import ToolRegistry, tool
from core.tools.harness import GuardedToolHarness
from core.tools.builtin_tools import ASTValidateCodeTool, WriteFileAtomicTool, ReadFileTool


class TestMemoryAndTools(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_memory_compaction(self):
        mem_dir = self.temp_path / "memories"
        mem_dir.mkdir()
        archive_file = mem_dir / "archive_summary.md"

        # Create a large memory file
        sample_mem = (
            "# Agent: test_agent\n"
            "**Name:** Test Agent\n"
            "**Role:** Test Specialist\n\n"
            "## 📜 Chronological Action Log & Milestone Records\n"
            "### Update [2026-01-01] - Milestone 1\n"
            + ("- Log entry details for testing token compaction.\n" * 150)
            + "\n### Update [2026-02-01] - Milestone 2\n"
            + ("- Log entry details for testing token compaction.\n" * 150)
            + "\n### Update [2026-03-01] - Milestone 3\n"
            + ("- Log entry details for testing token compaction.\n" * 150)
            + "\n### Update [2026-04-01] - Milestone 4\n"
            + ("- Latest active log details.\n" * 20)
        )
        agent_file = mem_dir / "test_agent.md"
        agent_file.write_text(sample_mem, encoding="utf-8")

        compactor = MemoryCompactor(memories_dir=mem_dir, archive_path=archive_file, max_tokens=500)
        was_compacted, orig_tok, new_tok = compactor.compact_agent_memory(agent_file)

        self.assertTrue(was_compacted)
        self.assertGreater(orig_tok, new_tok)
        self.assertTrue(archive_file.exists())
        self.assertIn("Milestone 1", archive_file.read_text(encoding="utf-8"))

    def test_context_decay_relevance(self):
        engine = ContextDecayEngine(decay_rate=0.1)
        pinned = MemoryItem(id="pin1", content="Core Manifest", is_pinned=True)
        unpinned = MemoryItem(id="unpin1", content="Temporary scratchpad", is_pinned=False)

        self.assertEqual(engine.compute_relevance(pinned), 1.0)
        score = engine.compute_relevance(unpinned)
        self.assertGreater(score, 0.0)

    async def test_tool_harness_validation_and_execution(self):
        reg = ToolRegistry()

        class AddInput(BaseModel):
            a: int = Field(..., description="First number")
            b: int = Field(..., description="Second number")

        @tool(name="add_numbers", input_model=AddInput, registry=reg)
        def add(a: int, b: int) -> int:
            return a + b

        harness = GuardedToolHarness(reg)

        # Valid invocation
        res = await harness.execute_tool("add_numbers", {"a": 5, "b": 7})
        self.assertTrue(res.success)
        self.assertEqual(res.data, 12)

        # Invalid invocation (string instead of int)
        invalid_res = await harness.execute_tool("add_numbers", {"a": "not_an_int", "b": 7})
        self.assertFalse(invalid_res.success)
        self.assertIn("Invalid arguments", invalid_res.error)

    def test_builtin_ast_and_file_tools(self):
        test_file = self.temp_path / "sample.py"
        test_code = "def hello():\n    return 'world'\n"
        
        # Test atomic write
        WriteFileAtomicTool(file_path=str(test_file), content=test_code)
        self.assertTrue(test_file.exists())

        # Test read
        read_res = ReadFileTool(file_path=str(test_file))
        self.assertEqual(read_res["content"], test_code)

        # Test AST validate
        ast_res = ASTValidateCodeTool(code_or_file=str(test_file), language="python")
        self.assertTrue(ast_res["valid"])


if __name__ == "__main__":
    unittest.main()
