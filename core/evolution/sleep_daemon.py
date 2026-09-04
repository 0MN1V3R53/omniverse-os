"""
Memory Replay and Sleep Consolidation Daemon.
Periodically replays scratchpad execution logs during idle cycles, distills lessons into agent heuristics,
applies Hebbian synaptic weight adjustments, and safely archives stale buffers.
"""

import shutil
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

from core.config import CONFIG
from core.evolution.models import HeuristicRule
from core.evolution.engine import PromptEvolutionEngine
from core.cognition.spreading_activation import GLOBAL_SPREADING_ACTIVATION


class SleepConsolidationReport(BaseModel):
    """Execution summary of an idle-cycle memory consolidation and sleep pass."""
    sleep_pass_id: str = Field(default_factory=lambda: f"SLEEP-{uuid.uuid4().hex[:8].upper()}")
    scratchpad_logs_replayed: int = 0
    heuristics_distilled: int = 0
    synapses_decayed: int = 0
    synapses_reinforced: int = 0
    archived_buffer_count: int = 0
    topology_doc_path: str = ""
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class SleepConsolidationDaemon:
    """
    Background idle-cycle daemon managing memory consolidation and synaptic plasticity.
    """

    def __init__(
        self,
        scratchpad_dir: Optional[Path] = None,
        topology_doc: Optional[Path] = None
    ):
        self.scratchpad_dir = scratchpad_dir or (CONFIG.workspace_root / ".scratchpad")
        self.archive_dir = self.scratchpad_dir / "archive"
        self.topology_doc = topology_doc or (CONFIG.workspace_root / "rules" / "network_topology.md")
        self.scratchpad_dir.mkdir(parents=True, exist_ok=True)
        self.archive_dir.mkdir(parents=True, exist_ok=True)

        self.evolution_engine = PromptEvolutionEngine()
        self.activation_engine = GLOBAL_SPREADING_ACTIVATION

    def run_sleep_consolidation_pass(self, max_logs_to_process: int = 10) -> SleepConsolidationReport:
        """
        Execute one sleep consolidation pass over idle workspace memories.
        """
        logs = list(self.scratchpad_dir.glob("*.log"))
        processed_count = 0
        distilled_count = 0
        archived_count = 0

        # 1. Process recent scratchpad logs
        for log_file in logs[:max_logs_to_process]:
            processed_count += 1
            content = log_file.read_text(encoding="utf-8", errors="replace")

            # Check if log contains a tool error or pattern
            if "error" in content.lower() or "exception" in content.lower():
                rule = HeuristicRule(
                    rule_text=f"Verify tool input preconditions for {log_file.name[:25]} to avoid buffer failures.",
                    rationale=f"Distilled during sleep replay from scratchpad log {log_file.name}.",
                    category="tooling",
                    severity="MUST",
                    source_ticket_id=f"SLEEP-REPLAY-{log_file.name[:15]}"
                )
                self.evolution_engine.add_heuristic_rule("ops_sweeper_web", rule)
                distilled_count += 1

            # 2. Archive log file
            dest_file = self.archive_dir / log_file.name
            shutil.move(str(log_file), str(dest_file))
            archived_count += 1

        # 3. Hebbian Synaptic Weight Adjustment
        # Decay all unused synapses
        self.activation_engine.decay_all_synapses(decay_rate=0.98)
        
        # Reinforce winning core pathways
        self.activation_engine.reinforce_synapse("concept:route_conversion", "agent:growth_meta_buyer", delta=0.04)
        self.activation_engine.reinforce_synapse("agent:web_frontend_julian_thorne", "tool:ast_navigator", delta=0.05)
        self.activation_engine.reinforce_synapse("agent:security_ciso_michael_chang", "tool:invariant_verifier", delta=0.05)

        syn_count = len(self.activation_engine.topology.edges)

        # 4. Write Markdown Network Topology Report
        md_content = f"""# 🧠 Omniverse Neural Synaptic Network Topology
*Last Consolidated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}*
*Active Synaptic Edges: {syn_count} | Node Count: {len(self.activation_engine.topology.nodes)}*

---

## Active High-Salience Associative Pathways
"""
        for edge in self.activation_engine.topology.edges:
            src = self.activation_engine.topology.nodes.get(edge.source_id)
            tgt = self.activation_engine.topology.nodes.get(edge.target_id)
            src_lbl = src.label if src else edge.source_id
            tgt_lbl = tgt.label if tgt else edge.target_id
            md_content += f"- `{src_lbl}` ───[{edge.weight:.3f}]───▶ `{tgt_lbl}` *(Updated: {edge.last_reinforced.strftime('%H:%M:%S')})*\n"

        self.topology_doc.write_text(md_content, encoding="utf-8")

        return SleepConsolidationReport(
            scratchpad_logs_replayed=processed_count,
            heuristics_distilled=distilled_count,
            synapses_decayed=syn_count,
            synapses_reinforced=3,
            archived_buffer_count=archived_count,
            topology_doc_path=str(self.topology_doc)
        )


# Global Singleton Sleep Daemon
GLOBAL_SLEEP_DAEMON = SleepConsolidationDaemon()
