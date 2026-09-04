# RULE 08: TEST-TIME SIMULATION & TREE-SEARCH VERIFICATION

## 1. Test-Time Compute Simulation Protocol
1.1 Derived from frontier reasoning architectures (DeepSeek V4 Think-Max / Mythos 5 execution engine), agents must perform an internal virtual simulation of all code changes before invoking file-writing or terminal tools.
1.2 In high-complexity systems (cryptography, concurrency, database transactions, Web3 routing), linear thinking is strictly prohibited. The agent must evaluate multiple implementation branches in `<scratchpad_reasoning>`.

## 2. Tree-Search Branch Evaluation & Pruning
2.1 When designing a complex function or refactoring a module, the agent must evaluate candidate branches:
    - **Branch Alpha (Performance / Direct)**: Evaluated for speed, memory footprint, and simplicity.
    - **Branch Beta (Extensibility / Defensive)**: Evaluated for type safety, boundary guards, and async thread isolation.
2.2 The agent must document the branch trade-offs in `<Architectural_Decision_Matrix>` and explicitly justify why the selected branch satisfies all invariants.

## 3. Pre-Commit Counterfactual Stress-Testing
3.1 Before executing any file write, the agent must simulate the following adversarial scenarios:
    - **Zero / Empty / Null State**: What occurs if the Room DB returns an empty cursor, the WebSocket disconnects mid-handshake, or a wallet address is empty?
    - **Concurrent Race Conditions**: What occurs if two Kotlin coroutines simultaneously access the Double Ratchet state or attempt to write to the SQLCipher database?
    - **Cryptographic Zeroization**: Does every sensitive `ByteArray` (seed phrase, ephemeral private key, AEAD nonce) get securely wiped with `Arrays.fill(bytes, 0.toByte())` in a `finally` block?
3.2 Only when all virtual stress tests pass with zero exceptions may the agent emit the final production code.
