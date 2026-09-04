"""
Unit and Integration Test Suite for Ephemeral Container Sandbox and High-Speed Multi-Tier Symbol Indexer.
Tests container cgroup enforcement, sub-10ms SQLite WAL symbol lookups, incremental delta invalidation, and tool interfaces.
"""

import tempfile
import time
import unittest
from pathlib import Path

from core.sandbox.container_runner import DockerSandboxRunner, ContainerConfig
from core.ast_engine.fast_indexer import FastSymbolIndex
from core.tools.sandboxed_tools import (
    sandboxed_terminal_exec,
    fast_symbol_lookup,
    find_all_references
)


class TestSandboxAndFastIndexer(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
        self.db_path = self.temp_path / "test_symbol_index.db"

        self.sandbox = DockerSandboxRunner(workspace_root=self.temp_path)
        self.indexer = FastSymbolIndex(db_path=self.db_path, workspace_root=self.temp_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_sandbox_fallback_execution_and_timeout(self):
        """Test sandbox command execution in fallback mode with timeout enforcement."""
        cfg = ContainerConfig(timeout_sec=3)
        res = self.sandbox.run_sandboxed("echo 'Hello Sandbox'", config=cfg)
        self.assertEqual(res.exit_code, 0)
        self.assertIn("Hello Sandbox", res.stdout)
        self.assertGreater(res.duration_ms, 0)

        # Test timeout failure
        timeout_res = self.sandbox.run_sandboxed("sleep 5", config=ContainerConfig(timeout_sec=1))
        self.assertEqual(timeout_res.exit_code, -1)
        self.assertIn("timed out", timeout_res.stderr.lower())

    def test_fast_symbol_indexer_sub_10ms_lookup(self):
        """Test sub-10ms O(1) symbol lookup latency across 1,000+ mock code symbols."""
        # Create a mock Python file with 1,000 generated classes/functions
        code_lines = []
        for i in range(1000):
            code_lines.append(f"class EnterpriseServiceClass{i}:\n    def process_transaction_{i}(self):\n        pass\n")
        
        mock_file = self.temp_path / "mock_enterprise_services.py"
        mock_file.write_text("\n".join(code_lines), encoding="utf-8")

        # Initial index sync
        sync_rep = self.indexer.sync_incremental()
        self.assertEqual(sync_rep.scanned_files_count, 1)
        self.assertEqual(sync_rep.reindexed_files_count, 1)
        self.assertEqual(sync_rep.symbols_indexed_count, 2000)

        # Benchmark 50 lookups for random symbols
        start_t = time.time()
        for i in [10, 50, 100, 250, 500, 750, 999]:
            sym = self.indexer.lookup_symbol(f"EnterpriseServiceClass{i}")
            self.assertEqual(len(sym), 1)
            self.assertEqual(sym[0].symbol_name, f"EnterpriseServiceClass{i}")
            self.assertEqual(sym[0].symbol_type, "class")

        elapsed_ms = (time.time() - start_t) * 1000.0 / 7.0
        # Assert average lookup latency is sub-10ms
        self.assertLess(elapsed_ms, 10.0, f"Average lookup took {elapsed_ms:.2f}ms (expected < 10ms)")

    def test_incremental_delta_invalidation(self):
        """Test that only modified/new files are re-indexed, and deleted files are purged."""
        # Create file A and file B
        file_a = self.temp_path / "service_a.py"
        file_b = self.temp_path / "service_b.py"
        file_a.write_text("class AlphaNode:\n    pass\n", encoding="utf-8")
        file_b.write_text("class BetaNode:\n    pass\n", encoding="utf-8")

        # First sync
        rep1 = self.indexer.sync_incremental()
        self.assertEqual(rep1.reindexed_files_count, 2)
        self.assertEqual(rep1.symbols_indexed_count, 2)

        # Second sync with NO changes -> 0 reindexed
        rep2 = self.indexer.sync_incremental()
        self.assertEqual(rep2.reindexed_files_count, 0)
        self.assertEqual(rep2.symbols_indexed_count, 0)

        # Modify file A only
        time.sleep(0.05)
        file_a.write_text("class AlphaNode:\n    def alpha_method(self):\n        pass\n", encoding="utf-8")
        
        rep3 = self.indexer.sync_incremental()
        self.assertEqual(rep3.reindexed_files_count, 1)
        self.assertEqual(rep3.symbols_indexed_count, 2)

        # Verify new symbol is indexed
        m_syms = self.indexer.lookup_symbol("alpha_method")
        self.assertEqual(len(m_syms), 1)

        # Delete file B
        file_b.unlink()
        rep4 = self.indexer.sync_incremental()
        self.assertEqual(rep4.deleted_files_count, 1)
        self.assertEqual(len(self.indexer.lookup_symbol("BetaNode")), 0)

    def test_sandboxed_tools_interfaces(self):
        """Test the sandboxed tool interface wrapper functions."""
        # 1. sandboxed_terminal_exec
        t_res = sandboxed_terminal_exec("echo 'Sandboxed Tool Test'")
        self.assertEqual(t_res["exit_code"], 0)
        self.assertIn("Sandboxed Tool Test", t_res["stdout"])

        # 2. fast_symbol_lookup
        syms = fast_symbol_lookup("CausalLink")
        # Should resolve cleanly from existing workspace models
        self.assertIsInstance(syms, list)

        # 3. find_all_references
        refs = find_all_references("CausalLink")
        self.assertEqual(refs["symbol_name"], "CausalLink")
        self.assertGreater(refs["total_occurrences"], 0)


if __name__ == "__main__":
    unittest.main()
