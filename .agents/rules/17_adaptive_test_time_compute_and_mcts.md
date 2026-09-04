# RULE 17: ADAPTIVE TEST-TIME COMPUTE & DYNAMIC MCTS THOUGHT-SPACE ENGINE

## 🚨 MANDATORY TEST-TIME COMPUTE PROTOCOL
Autonomous agents in the Omniverse OS must not rely solely on single-pass autoregressive generation for non-trivial tasks. Every complex software engineering, refactoring, cryptographic, or architectural initiative must dynamically allocate Test-Time Compute (TTC) using Monte Carlo Tree Search (MCTS) inside the structured `<mythos_scratchpad>`.

---

## 1. Dynamic Depth Allocation Formula
Compute depth ($\text{Depth}(T)$) is calculated dynamically based on problem entropy and blast radius:
$$\text{Depth}(T) = \alpha \cdot \mathcal{H}(\text{Task Complexity}) + \beta \cdot \text{Risk}(\text{AST Blast Radius})$$

- **Tier 1 (Direct Execution, $\text{Depth} = 1$)**: Simple formatting, mechanical syntax edits, documentation updates.
- **Tier 2 (Parallel-Distill-Refine, $\text{Depth} = 2–3$)**: Single-module functional changes, route updates, database schema migrations. Evaluates 2–3 candidate branches before writing.
- **Tier 3 (Deep MCTS Tree Search, $\text{Depth} \ge 4$)**: Multi-file refactors, cryptographic state machines, kernel-level optimizations, and cross-pod architecture shifts. Simulates 4–8 candidate rollout paths in `<mythos_scratchpad>`.

---

## 2. In-Scratchpad MCTS Tree-Search Mechanics
When operating in Tier 2 or Tier 3 mode, the agent MUST explicitly format its reasoning tree inside `<mythos_scratchpad>`:

```xml
<mythos_scratchpad>
MCTS_SIMULATION_SPACE:
  BRANCH_A:
    - Hypothesis: [Implementation Strategy A]
    - Failure Modes Evaluated: [Boundary cases, memory leaks, contract breaches]
    - PRM Score: [0.0 - 1.0]
  BRANCH_B:
    - Hypothesis: [Implementation Strategy B]
    - Failure Modes Evaluated: [Alternative boundary collisions]
    - PRM Score: [0.0 - 1.0]
  SELECTION_SYNTHESIS:
    - Winning Branch: [Branch A / Branch B]
    - Mathematical / Architectural Justification: [Reason for selection]
</mythos_scratchpad>
```

---

## 3. Step-Level Process Reward Model (GenPRM Gating)
Every intermediate step must pass the Process Reward Model gating rubric:
$$\text{Score}_{PRM} = 0.35(S_{AST}) + 0.30(S_{Contract}) + 0.20(S_{Safety}) + 0.15(S_{Diff}) \ge 0.95$$

- If any proposed step yields $\text{Score}_{PRM} < 0.95$, the branch MUST be pruned immediately and an alternative hypothesis evaluated before touching the file system.
- Zero-Stub Invariant: Any branch proposing placeholders (`// TODO`, `pass`, `/* later */`) is automatically assigned $S_{AST} = 0.0$ and disqualified.
