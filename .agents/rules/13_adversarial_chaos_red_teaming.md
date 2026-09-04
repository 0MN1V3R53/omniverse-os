# RULE 13: ADVERSARIAL CHAOS & RED-TEAMING SIMULATION

## 1. Zero-Trust Verification Mandate
Aegis is an uncompromised sovereign privacy and Web3 terminal. All critical code changes must survive simulated adversarial attacks before integration.

---

## 2. Mandatory Chaos Attack Vectors
Prior to code emission, the agent must internally stress-test candidate implementations against the following vectors:

1. **Cryptographic Malformation Attack**:
   - Inject corrupted or truncated ciphertexts into `ratchetDecrypt()`.
   - Verify that invalid MAC / auth tag failures trigger safe zeroization and clean exception bubbles without leaking raw keys or crashing the app.

2. **Web3 Financial Race Condition & Boundary Fuzzing**:
   - Simulate zero-value `$send` inputs, negative amounts, integer overflows, and double-spend race conditions on Solana/EVM transactions.
   - Verify that the 0.5% developer protocol routing fee cannot be bypassed or front-run.

3. **Network Partition & Asynchronous Drop Simulation**:
   - Simulate sudden socket disconnection during WebRTC DTLS-SRTP handshake or Double Ratchet DH key exchange.
   - Verify that the offline queue stores pending actions securely in encrypted SQLCipher storage with zero plaintext cache.

---

## 3. Red-Team Audit Report
Any security-critical pull request or file modification must document its adversarial survival in the `<Architectural_Decision_Matrix>` section.
