# RULE 19: SIMULATION SANDBOXES, SPECULATIVE AST & HARDWARE UPSCALING

## 🚨 MANDATORY IN-MEMORY SIMULATION PROTOCOL
Before committing structural architectural changes or executing high-blast-radius operations, Omniverse agents must pre-validate constraints within virtual simulation sandboxes.

---

## 1. Simulated Silicon & Hardware Up-scaling
When designing algorithms, database queries, or compute-heavy pipelines:
1. **Virtual Micro-Architecture Modeling**: Simulate register allocation, memory bandwidth throughput, and CPU cache-line alignment in-memory.
2. **Computational Complexity Verification**: Verify asymptotic bounds $\mathcal{O}(N)$ before generating concrete implementation scripts.
3. **Speculative AST Execution**: Evaluate competing file diffs inside isolated in-memory AST buffers without touching physical disk I/O.

---

## 2. Wet-Lab / Dry-Lab Algorithmic Testing
- Complex mathematical transformations, state machines, and cryptographic protocols must be tested against synthetic state-space vectors in a sandbox script prior to integration into production modules.
- Verification mandates that synthetic vectors test boundary extremes (e.g. empty payloads, maximum buffer sizes, Unicode normalization, malformed headers).

---

## 3. Zero Disk Contamination Invariant
- Speculative rollouts and temporary simulation scratch files must remain isolated to in-memory buffers or designated temporary test harnesses.
- Physical project files must never contain temporary debug statements or unverified experiment artifacts.
