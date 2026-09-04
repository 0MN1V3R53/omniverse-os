# HEURISTIC: STATIC WORM PREFIX CACHING & CONTEXT FRUSTUM CULLING

**Heuristic ID**: `HE-CACHE-002`  
**Category**: Context Optimization & KV-Cache Management  
**Cache Target**: $>95\%$ Hit Rate

---

## Key Tactical Invariants
1. **WORM Prefix Integrity**: Never prepend dynamic, per-turn data (timestamps, transient counters) before static rule definitions. Dynamic context must always follow the static prefix boundary.
2. **Level-of-Detail (LOD) Culling**:
   - Target File: Full AST symbol tree and function definitions.
   - Immediate Dependencies: Exported type interfaces and method signatures only.
   - Distant Modules: 1-line topological file path and high-level role summary.
3. **Sub-Vector Graph Assembly**: Fetch only high-relevance heuristics ($H_{vec}$) dynamically to keep context sandwiches dense and fast ($<5\text{ms}$).
