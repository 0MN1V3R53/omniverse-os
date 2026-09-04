# CONTEXT 10: IN-CONTEXT PROCESS REWARD RUBRIC (PRM)

## 1. Process Reward Model (PRM) Specification
Following 2026 Process Reward Model paradigms (*SWE-Shepherd*, *SWE-TRACE*), every agent must evaluate intermediate candidate actions against four discrete evaluation vectors before executing tool operations.

---

## 2. The Four Scoring Vectors

### Dimension 1: Abstract Syntax Tree & Type Safety ($S_{AST}$)
- **1.0 (Pass)**: Clean AST structure. All bracket pairs match. No duplicate imports or unresolved class references. Valid Kotlin 2.0+ / Compose / TypeScript syntax.
- **0.5 (Warning)**: Minor non-breaking lint warning (e.g. unused import).
- **0.0 (Fail)**: Unclosed braces, invalid variable references, broken type signatures, or truncated stub code.

### Dimension 2: Cryptographic Invariants & Memory Zeroization ($S_{Crypto}$)
- **1.0 (Pass)**: Sensitive keys (`ByteArray`, `CharArray`) are explicitly wiped with `.fill(0)` inside `finally` blocks. SQLCipher passphrases never pass through immutable `String`. Libsodium secure memory functions used for secret keys.
- **0.5 (Warning)**: Secure memory used but zeroization relies solely on GC finalization.
- **0.0 (Fail)**: Plaintext secrets logged, hardcoded private keys, mock randomness, or unencrypted keystores.

### Dimension 3: Thread Concurrency & State Safety ($S_{Thread}$)
- **1.0 (Pass)**: Coroutine dispatchers correctly bound (`Dispatchers.IO` for DB/Network, `Dispatchers.Main` for UI). Room DAO operations flow-reactive or `suspend`. Mutex locks protecting Double Ratchet session state.
- **0.5 (Warning)**: Potential thread-hop delay or unconfined flow collection.
- **0.0 (Fail)**: Blocking calls on `Dispatchers.Main`, race conditions in cryptographic ratcheting, or unhandled coroutine cancellations.

### Dimension 4: Token Efficiency & Surgical Diff Precision ($S_{Diff}$)
- **1.0 (Pass)**: Edits use minimal, exact line targeting. No whole-file overwrites for trivial changes. Zero redundant prompt bloat.
- **0.5 (Warning)**: Multi-line chunk replace where a single line edit would suffice.
- **0.0 (Fail)**: Full-file overwrite wiping existing documentation, accidental deletion of invariant rules.

---

## 3. Invariant Evaluation Formula
The composite Process Reward Score ($PRM_{Score}$) is calculated as:

$$PRM_{Score} = 0.35 \times S_{AST} + 0.35 \times S_{Crypto} + 0.20 \times S_{Thread} + 0.10 \times S_{Diff}$$

> [!CRITICAL]
> **Execution Gate Rule**: If $PRM_{Score} < 0.95$, the candidate action is REJECTED. The agent must loop back, pivot, and regenerate the candidate patch until $PRM_{Score} \ge 0.95$.
