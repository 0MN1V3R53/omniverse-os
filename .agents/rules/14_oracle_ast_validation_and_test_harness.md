# RULE 14: ORACLE AST VALIDATION & TEST HARNESS

## 1. Concrete AST Pre-Validation Mandate
Code generation without syntax and type verification leads to broken builds and execution halts. Agents must act as their own internal compiler and test oracle prior to committing code.

---

## 2. In-Memory Compiler Verification Checklist
Every code snippet or diff must pass this 5-point verification checklist:

1. **Syntax & Bracket Confluence**: All braces `{`, brackets `[`, and parentheses `(` are strictly closed and balanced.
2. **Type Signatures & Return Types**: Function arguments, generics, and return signatures match caller expectations exactly.
3. **Import Completeness**: Every referenced class, extension function, and annotation has an explicit `import` statement.
4. **Scope & Mutability**: Variables are declared `val` by default; mutable state uses thread-safe primitives (`AtomicReference`, `StateFlow`, `Mutex`).
5. **Exception Handling**: All throwing calls (cryptographic decryption, JSON RPC, file I/O) are wrapped in `runCatching`, `try/finally`, or custom `Result<T>` monads.

---

## 3. Test-Driven Verification Oracle
When writing or refactoring business logic, agents must write corresponding unit tests or simulate the exact test oracle execution steps demonstrating test pass/fail conditions.
