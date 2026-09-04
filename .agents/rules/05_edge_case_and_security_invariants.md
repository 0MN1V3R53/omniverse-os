# RULE 05: EDGE-CASE RESILIENCE & SECURITY INVARIANTS

## 1. Cryptographic Invariants & Key Lifecycle
1.1 **Zero-Memory Residue**: Sensitive byte arrays (private keys, ephemeral seeds, master passphrase bytes) must be explicitly overwritten with zeros (`java.util.Arrays.fill(bytes, 0.toByte())`) immediately after cryptographic operations.
1.2 **Ratchet Skipped-Key Recovery**: The Double Ratchet engine must maintain a bounded cache of skipped message keys (maximum 2000 keys per session) with deterministic key destruction upon decryption or session expiry (24h timeout).
1.3 **Keystore Invalidation Handling**: If the Android Keystore key is permanently invalidated (e.g., biometrics re-enrolled or device lock removed), the application must securely lock database sessions, notify the user, and require passphrase re-authentication without corrupting the encrypted SQLCipher database file.

## 2. Network, Concurrency & Battery Lifecycle Edge Cases
2.1 **Abrupt Socket Disconnects**: `SignalingClient` and `FirebaseMessageSyncRepository` must handle abrupt connection drops using exponential backoff retry algorithms (base: 1000ms, max: 30000ms, jitter: 20%) without dropping in-flight outbox messages.
2.2 **Local Outbox Queueing**: If a user transmits a message or crypto tip while offline, the payload must be encrypted, committed to `Room` database with `PENDING` status, and asynchronously dispatched upon network recovery.
2.3 **FLAG_SECURE Enforcement**: `WindowManager.LayoutParams.FLAG_SECURE` must remain permanently active on `MainActivity` and all dialog windows to block OS-level screenshots, screen mirroring, and thumbnail caching in the recent apps switcher.

## 3. Web3 Financial Security Invariants
3.1 **Negative & Zero Amount Rejection**: All tip, send, and swap functions must reject amounts `<= 0` before constructing transaction payloads.
3.2 **Developer Routing Exactness**: The 0.5% developer routing fee (`DEV_FEE_PERCENT = 0.005`) must be calculated using exact high-precision arithmetic to prevent rounding errors or fee bypass vectors.
3.3 **Seed Phrase Protection**: Raw BIP39 mnemonic phrases must never be cached in plaintext memory, logs, or SharedPreferences; they must be encrypted via Tink Keystore AEAD immediately upon generation.
