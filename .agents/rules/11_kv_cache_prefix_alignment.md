# RULE 11: KV-CACHE PREFIX ALIGNMENT & WORM MEMORY

## 1. Principle of Static Prefix Optimization
Modern frontier LLMs (specifically Gemini 3.7 Flash High) utilize massive Key-Value (KV) prompt caching. Dynamic or randomly ordered prompt structures invalidate cached attention matrices, causing high time-to-first-token (TTFT) and wasted compute.

---

## 2. Invariant Token Layout Rules
Every system instruction, agent initialization, and memory injection MUST follow the deterministic Write-Once-Read-Many (WORM) sequence:

1. **System Identity & Master Governance** (Static Top Prefix):
   - `.agents/rules/` (Rules 01–14 in exact numerical sequence)
2. **Authoritative Domain Context Vault** (Immutable Reference Block):
   - `.agents/context/` (Blueprints 01–11 in exact numerical sequence)
3. **Persistent Role Memory** (Semi-Static Block):
   - `.agents/omniverse_memories/<agent_id>.md`
4. **Dynamic Workspace State** (Volatile Tail):
   - Active user query, task metadata, and AST target diff.

---

## 3. Prohibited Modifications
- **NEVER** re-order rule or context inclusions dynamically.
- **NEVER** inject volatile timestamps or random noise into the static prefix headers.
- **ALWAYS** keep the immutable context headers pinned at the absolute beginning of the cognitive context window.
