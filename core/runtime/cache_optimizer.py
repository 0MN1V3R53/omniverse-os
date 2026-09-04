"""
Gemini KV-Cache Prefix Optimizer & Context Compaction Engine.
Structures prompts into strictly static immutable prefixes ([SYSTEM ID] -> [RULES] -> [TOOLS])
and append-only dynamic tails to maximize prompt caching hit rates and eliminate repetitive token costs.
"""

import hashlib
from typing import Dict, List, Optional, Tuple
from pydantic import BaseModel, Field

from core.config import CONFIG
from core.guards.invariants import GLOBAL_INVARIANT_VERIFIER


class CacheIntegrityReport(BaseModel):
    """Validation report verifying strict prefix byte-invariance across prompt executions."""
    agent_id: str
    is_prefix_valid: bool
    prefix_sha256: str
    static_prefix_tokens_estimate: int
    dynamic_tail_tokens_estimate: int
    integrity_status: str


class KVCachePrefixOptimizer:
    """
    Compiler enforcing static prefix boundaries for optimal KV-cache pinning.
    """

    def __init__(self):
        self.invariant_verifier = GLOBAL_INVARIANT_VERIFIER
        self._prefix_cache: Dict[str, str] = {}

    def generate_static_prefix(self, agent_id: str) -> str:
        """
        Build the immutable static anchor block for an agent.
        Format: [SYSTEM IDENTIFIER] -> [CORE RULES & INVARIANTS] -> [STATIC TOOL SCHEMAS]
        """
        if agent_id in self._prefix_cache:
            return self._prefix_cache[agent_id]

        # 1. System Identifier
        part_sys = f"<!-- SYSTEM_IDENTIFIER_ANCHOR: {agent_id.upper()} -->\n"
        part_sys += f"You are agent `{agent_id}` in the Omniverse multi-agent enterprise runtime.\n"

        # 2. Core Invariants & Cognitive Rules
        part_rules = "\n<!-- CORE_RULES_AND_INVARIANTS_ANCHOR -->\n"
        part_rules += "MANDATORY INVARIANTS:\n"
        for inv in self.invariant_verifier.invariants:
            part_rules += f"- [{inv.invariant_id}] {inv.description} (Severity: {inv.severity})\n"
        part_rules += "- Zero Drift: Strictly prohibit mock datasets, synthetic profiles, and unverified data props.\n"

        # 3. Static Tool Affordance Schemas
        part_tools = "\n<!-- STATIC_TOOL_SCHEMAS_ANCHOR -->\n"
        part_tools += "AVAILABLE TOOL OPERATORS:\n"
        part_tools += "- `sandboxed_terminal_exec(command, timeout_sec=60, network=False)`\n"
        part_tools += "- `fast_symbol_lookup(symbol_name, symbol_type=None)`\n"
        part_tools += "- `find_all_references(symbol_name)`\n"
        part_tools += "- `web_researcher(query, target_url=None)`\n"
        part_tools += "- `youtube_intel(query_or_url)`\n"
        part_tools += "<!-- END_STATIC_PREFIX_ANCHOR -->\n"

        prefix = part_sys + part_rules + part_tools
        self._prefix_cache[agent_id] = prefix
        return prefix

    def assemble_prompt(self, agent_id: str, dynamic_context: str) -> str:
        """
        Assemble the full prompt by appending volatile dynamic buffers strictly to the tail.
        """
        static_prefix = self.generate_static_prefix(agent_id)
        dynamic_tail = f"\n<!-- DYNAMIC_EXECUTION_BUFFER_START -->\n{dynamic_context.strip()}\n<!-- DYNAMIC_EXECUTION_BUFFER_END -->"
        return static_prefix + dynamic_tail

    def validate_cache_integrity(
        self,
        prompt_a: str,
        prompt_b: str,
        agent_id: str
    ) -> CacheIntegrityReport:
        """
        Validate that the static prefix bytes remain 100% byte-invariant across two distinct prompts.
        """
        delimiter = "<!-- END_STATIC_PREFIX_ANCHOR -->\n"
        
        prefix_a = prompt_a.split(delimiter)[0] + delimiter if delimiter in prompt_a else prompt_a
        prefix_b = prompt_b.split(delimiter)[0] + delimiter if delimiter in prompt_b else prompt_b

        hash_a = hashlib.sha256(prefix_a.encode("utf-8")).hexdigest()
        hash_b = hashlib.sha256(prefix_b.encode("utf-8")).hexdigest()

        is_valid = (hash_a == hash_b)
        status = "PASSED: 100% Byte-Invariant KV-Cache Prefix Pinning" if is_valid else "FAILED: Prefix byte drift detected"

        prefix_tokens = len(prefix_a.split())
        tail_tokens = len(prompt_a.replace(prefix_a, "").split())

        return CacheIntegrityReport(
            agent_id=agent_id,
            is_prefix_valid=is_valid,
            prefix_sha256=hash_a,
            static_prefix_tokens_estimate=prefix_tokens,
            dynamic_tail_tokens_estimate=tail_tokens,
            integrity_status=status
        )


# Global KV-Cache Prefix Optimizer Singleton
GLOBAL_CACHE_OPTIMIZER = KVCachePrefixOptimizer()
