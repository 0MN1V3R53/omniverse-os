# HEURISTIC: MCTS THOUGHT-SPACE TREE SEARCH & PRM GATING

**Heuristic ID**: `HE-MCTS-001`  
**Category**: Procedural Reasoning / Test-Time Compute  
**PRM Threshold**: $\ge 0.95$

---

## Key Tactical Invariants
1. **Branch Pruning**: Immediately discard any rollout branch that introduces a new external dependency without explicit justification.
2. **Blast Radius Minimization**: Prefer atomic AST edits that modify only the targeted function or block over whole-file regenerations.
3. **Dual-Critic Balance**: Ensure syntactic compliance ($S_{AST} = 1.0$) does not violate interface contracts ($S_{Contract} = 1.0$).
4. **Counterfactual Validation**: When diagnosing a failing test or bug, construct at least 2 distinct failure hypotheses before applying a code change.
