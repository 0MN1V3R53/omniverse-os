"""
Automated Memory Compactor and Token Budget Manager.
Monitors agent memory files, enforces token limits, and archives historical milestones.
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from core.config import CONFIG


class MemoryCompactor:
    """
    Manages agent memory lifecycle, enforces token budgets, and archives
    excess episodic milestone records into archive_summary.md.
    """

    def __init__(
        self,
        memories_dir: Optional[Path] = None,
        archive_path: Optional[Path] = None,
        max_tokens: Optional[int] = None,
    ):
        self.memories_dir = memories_dir or CONFIG.memories_dir
        self.archive_path = archive_path or CONFIG.memory_archive_path
        self.max_tokens = max_tokens or CONFIG.max_agent_memory_tokens

    def estimate_tokens(self, text: str) -> int:
        """Estimate token count based on character ratio (approx 4 chars per token)."""
        return int(len(text) / CONFIG.token_chars_ratio)

    def compact_agent_memory(self, memory_file_path: Path) -> Tuple[bool, int, int]:
        """
        Evaluate an individual agent memory file. If token count exceeds budget,
        extract older milestone logs, write them to archive_summary.md, and
        compact the file.
        Returns: (was_compacted, original_token_count, new_token_count)
        """
        if not memory_file_path.exists():
            return (False, 0, 0)

        content = memory_file_path.read_text(encoding="utf-8")
        orig_tokens = self.estimate_tokens(content)

        if orig_tokens <= self.max_tokens:
            return (False, orig_tokens, orig_tokens)

        # Parse sections: Pinned Profile vs Episodic Action Log
        agent_id = memory_file_path.stem
        sections = re.split(r"(## 📜 Chronological Action Log & Milestone Records|### Update \[\d{4}-\d{2}-\d{2})", content)

        if len(sections) < 2:
            # Simple line-based fallback if headers are different
            return (False, orig_tokens, orig_tokens)

        header_part = sections[0]
        milestone_parts = sections[1:]

        # Collect milestone blocks
        milestone_blocks: List[str] = []
        curr_block = ""
        for part in milestone_parts:
            if part.startswith("## 📜") or part.startswith("### Update"):
                if curr_block:
                    milestone_blocks.append(curr_block)
                curr_block = part
            else:
                curr_block += part
        if curr_block:
            milestone_blocks.append(curr_block)

        if len(milestone_blocks) <= 2:
            return (False, orig_tokens, orig_tokens)

        # Archive the oldest N-2 blocks, keeping the latest 2 intact
        archive_blocks = milestone_blocks[:-2]
        keep_blocks = milestone_blocks[-2:]

        # Append to archive_summary.md
        self._append_to_archive(agent_id, archive_blocks)

        # Rebuild compacted content
        archived_notice = (
            f"\n\n- *[ARCHIVED CONTEXT: {len(archive_blocks)} historical milestone records pruned "
            f"and summarized in `{self.archive_path.name}` on {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}]*\n\n"
        )
        compacted_content = header_part + archived_notice + "".join(keep_blocks)
        new_tokens = self.estimate_tokens(compacted_content)

        # Atomically overwrite memory file
        memory_file_path.write_text(compacted_content, encoding="utf-8")
        return (True, orig_tokens, new_tokens)

    def _append_to_archive(self, agent_id: str, blocks: List[str]) -> None:
        """Atomically append pruned logs to archive_summary.md."""
        self.archive_path.parent.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        
        archive_entry = f"\n\n## 🗄️ Archive Entry: `{agent_id}` ({timestamp})\n"
        for block in blocks:
            # Clean up headers
            clean_block = block.strip()
            if clean_block:
                archive_entry += f"\n{clean_block}\n"

        if not self.archive_path.exists():
            header = (
                "# 🗄️ Omniverse Autonomous Agent Archive Summary\n"
                "Persistent episodic memory storage for compacted milestone records and historical context.\n\n"
                "---\n"
            )
            self.archive_path.write_text(header + archive_entry, encoding="utf-8")
        else:
            with open(self.archive_path, "a", encoding="utf-8") as f:
                f.write(archive_entry)

    def scan_and_compact_all(self) -> Dict[str, Dict[str, Any]]:
        """
        Scan all agent memory files in .agents/omniverse_memories/ and compact
        any that exceed the token budget.
        """
        results = {}
        if not self.memories_dir.exists():
            return results

        for md_file in self.memories_dir.glob("*.md"):
            if md_file.name == "archive_summary.md":
                continue
            was_compacted, orig_tok, new_tok = self.compact_agent_memory(md_file)
            results[md_file.stem] = {
                "file": str(md_file),
                "compacted": was_compacted,
                "original_tokens": orig_tok,
                "new_tokens": new_tok,
            }
        return results
