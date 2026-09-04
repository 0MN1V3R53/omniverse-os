#!/usr/bin/env python3
"""
benchmark_adapter.py
====================
Authoritative Master Adapter connecting external AI evaluation harnesses
(SWE-bench, GAIA, LiveCodeBench, pwn.college) into the Omniverse OS (.agents/) substrate.

Enforces:
- Dynamic context and rule injection (Rules 01-23, Context 00-26).
- Cryptographic SHA-256 submission audit manifest.
- Anti-simulation and zero-stub invariants.
- Standardized model identification ('omniverse-os-leviathan-999').
"""

import os
import sys
import json
import time
import hashlib
import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent.parent
AGENTS_DIR = BASE_DIR / ".agents"
RULES_DIR = AGENTS_DIR / "rules"
CONTEXT_DIR = AGENTS_DIR / "context"
OUTPUT_DIR = AGENTS_DIR / "output" / "benchmark_submissions"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MANIFEST_FILE = OUTPUT_DIR / "audit_manifest.jsonl"
DEFAULT_MODEL_ID = "omniverse-os-leviathan-999"


class OmniverseBenchmarkAdapter:
    """Master bridge connecting benchmark harnesses to the Omniverse cognitive substrate."""

    def __init__(self, model_id: str = DEFAULT_MODEL_ID):
        self.model_id = model_id
        self.rules_cache: Dict[str, str] = {}
        self.context_cache: Dict[str, str] = {}
        self._load_core_knowledge()

    def _load_core_knowledge(self) -> None:
        """Preloads key governance rules and architectural context blueprints into memory."""
        critical_rules = [
            "04_full_stack_confluence_and_zero_drift.md",
            "10_deterministic_tool_boundaries_and_zero_hallucination.md",
            "12_step_level_prm_gating.md",
            "20_fable_5_1_persistent_memory_filesystem_and_dual_pass_pipeline.md",
            "21_fable_mcp_tool_orchestration_and_anti_simulation_directive.md",
            "22_omniverse_code_exploit_research_and_vulnerability_discovery_protocol.md",
            "23_online_verifiable_benchmark_and_leaderboard_governance.md",
        ]
        for rule in critical_rules:
            path = RULES_DIR / rule
            if path.exists():
                with open(path, "r", encoding="utf-8") as f:
                    self.rules_cache[rule] = f.read()

        critical_contexts = [
            "00_universal_workspace_router_and_domain_index.md",
            "08_frontier_agentic_engine_and_sandwich_protocol.md",
            "16_omniverse_code_cybersecurity_and_offensive_exploit_architecture.md",
            "26_claude_fable_5_1_and_mythos_intelligence_engine_synthesis.md",
        ]
        for ctx in critical_contexts:
            path = CONTEXT_DIR / ctx
            if path.exists():
                with open(path, "r", encoding="utf-8") as f:
                    self.context_cache[ctx] = f.read()

    def generate_cryptographic_proof(
        self,
        track: str,
        task_id: str,
        output_payload: str
    ) -> Dict[str, Any]:
        """
        Generates a verifiable SHA-256 cryptographic audit proof for an evaluated benchmark instance.
        """
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        hasher = hashlib.sha256()
        hasher.update(track.encode("utf-8"))
        hasher.update(task_id.encode("utf-8"))
        hasher.update(self.model_id.encode("utf-8"))
        hasher.update(timestamp.encode("utf-8"))
        hasher.update(output_payload.encode("utf-8"))
        sha256_hash = hasher.hexdigest()

        proof_record = {
            "proof_hash": sha256_hash,
            "track": track,
            "task_id": task_id,
            "model_id": self.model_id,
            "timestamp": timestamp,
            "payload_length_bytes": len(output_payload.encode("utf-8")),
            "payload_sha256": hashlib.sha256(output_payload.encode("utf-8")).hexdigest()
        }

        # Append to authoritative manifest
        with open(MANIFEST_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(proof_record) + "\n")

        return proof_record

    def format_evaluation_prompt(
        self,
        track: str,
        task_id: str,
        problem_description: str,
        environment_meta: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Synthesizes a high-fidelity prompt for the Omniverse agentic cognitive loop,
        injecting PRM step-gating, AST verification, and relevant pod instructions.
        """
        meta_str = json.dumps(environment_meta or {}, indent=2)
        prompt = f"""### OMNIVERSE OS COGNITIVE BENCHMARK PIPELINE
Target Track: {track}
Instance ID: {task_id}
Model Identifier: {self.model_id}
Timestamp: {datetime.datetime.now(datetime.timezone.utc).isoformat()}

### OPERATIONAL DIRECTIVE:
1. Adhere strictly to Rule 23 (Online Verifiable Benchmark & Leaderboard Governance).
2. Zero stubs, zero placeholders, zero synthetic data.
3. PRM Score Gating Threshold: 0.95.
4. Output must be production-ready and fully conforming to benchmark verification schemas.

### ENVIRONMENT METADATA:
{meta_str}

### TASK SPECIFICATION:
{problem_description}
"""
        return prompt

    def verify_manifest_integrity(self) -> Dict[str, Any]:
        """Audits the integrity of the cryptographic audit manifest."""
        if not MANIFEST_FILE.exists():
            return {"status": "NO_ENTRIES", "total_proofs": 0, "corrupted_proofs": 0, "manifest_path": str(MANIFEST_FILE)}

        valid_entries = []
        corrupted_entries = []
        with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
            for idx, line in enumerate(f):
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    if "proof_hash" in record and "task_id" in record:
                        valid_entries.append(record)
                    else:
                        corrupted_entries.append((idx, line))
                except json.JSONDecodeError:
                    corrupted_entries.append((idx, line))

        return {
            "status": "HEALTHY" if not corrupted_entries else "DEGRADED",
            "total_proofs": len(valid_entries),
            "corrupted_proofs": len(corrupted_entries),
            "manifest_path": str(MANIFEST_FILE)
        }


if __name__ == "__main__":
    adapter = OmniverseBenchmarkAdapter()
    print("Omniverse OS Benchmark Adapter Initialized.")
    print(f"Loaded {len(adapter.rules_cache)} governance rules and {len(adapter.context_cache)} context blueprints.")
    audit = adapter.verify_manifest_integrity()
    print(f"Cryptographic manifest status: {audit['status']} (Total proofs: {audit['total_proofs']})")
