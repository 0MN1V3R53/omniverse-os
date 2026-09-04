# RULE 07: ERROR CLASSIFICATION & TELEMETRY SELF-HEALING ENGINE

## 1. 3-Tier Error Classification Matrix (DeepSeek V4 / Mythos Engine)
1.1 When any compilation failure, unit test regression, or runtime anomaly occurs, the agent must immediately categorize the incident into one of three deterministic failure tiers before attempting a patch:

| Failure Tier | Root Cause Category | Recovery Protocol & Action |
| :--- | :--- | :--- |
| **Tier 1: Syntax & AST Alignment** | Typo, missing import, unresolved symbol, deprecated method signature. | Execute immediate local AST fix in the target file. No architectural pivot required. |
| **Tier 2: Runtime & State Lifecycle** | Null pointer, memory leak, uninitialized CoroutineScope, race condition, lifecycle disconnect. | Perform trace analysis within `<scratchpad_reasoning>`, verify Android lifecycle/Room transaction boundaries, and insert null-safe state guards. |
| **Tier 3: Invariant & Contract Breach** | Cryptographic key failure, Double Ratchet out-of-sync, SQLCipher passphrase corruption, 0.5% fee routing misdirection, stub/placeholder detected. | HALT execution immediately. Trigger a formal Self-Reprompting Loop. Re-ingest authoritative blueprints from `.agents/context/` and re-derive implementation from first principles. |

## 2. Autonomous Telemetry & Self-Correction Loop
2.1 When an error occurs, the agent is strictly prohibited from guessing or blindly re-running failed commands.
2.2 Every recovery turn must log:
    - `<error_telemetry>`: Exact error log snippet, file path, line number, and error classification tier.
    - `<root_cause_analysis>`: Why the fault occurred and which invariant was violated.
    - `<remedy_hypothesis>`: Precise architectural fix and verification step before editing the file.
2.3 If a fix attempt fails twice consecutively, the Junior Specialist must escalate the task to Senior Pod Lead **Viktor Drago (`android_lead_viktor_drago`)** or **Dr. Leon Nash (`web3_crypto_leon_nash`)** with full telemetry logs for hierarchical intervention.
