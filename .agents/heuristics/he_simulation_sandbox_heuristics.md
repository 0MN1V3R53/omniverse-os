# HEURISTIC: IN-MEMORY SIMULATION SANDBOXES & SPECULATIVE DIFFS

**Heuristic ID**: `HE-SIM-003`  
**Category**: In-Memory Verification / Hardware Upscaling  
**Zero-Disk-Leak Target**: 100%

---

## Key Tactical Invariants
1. **Speculative In-Memory Compilation**: Always compile and parse proposed AST modifications in-memory before invoking file modification tools.
2. **Boundary Stress Testing**: Run in-memory simulation against empty collections, max-value integers, null parameters, and malformed strings.
3. **Hardware Constraint Modeling**: When profiling algorithms, evaluate memory footprint, cache-line friendliness, and concurrency locks prior to emitting production logic.
