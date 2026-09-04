# RULE 02: RECURSIVE RE-PROMPTING & CONTEXT INGESTION MANDATE

## 1. Mandatory Autonomous Self-Reprompting Loop
1.1 Prior to formulating any architectural plan, generating code, or auditing pull requests, every active agent MUST execute an internal self-reprompting cycle:
    ```
    [Self-Reprompt Step 1: Identity & Scope Confirmation]
    - Identify current persona: <agent_id> & reporting line.
    - Validate specific operational mandate against CEO directives.

    [Self-Reprompt Step 2: Context Vault Retrieval]
    - Scan and load authoritative domain context from `.agents/context/`.
    - Retrieve relevant prior state from `.agents/omniverse_memories/<agent_id>.md`.

    [Self-Reprompt Step 3: Constraint & Invariant Verification]
    - Verify cryptographic, database, concurrency, and theme constraints.
    - Check for edge cases, nullability, thread boundaries, and lifecycle states.
    ```

## 2. Ingestion of `.agents/context/` Core Vault
2.1 The `.agents/context/` directory represents the single source of truth for repository architecture, crypto invariants, database schemas, Web3 routing, WebRTC signaling, and theme tokens.
2.2 Agents are strictly forbidden from inventing API signatures, encryption flows, database tables, or protocol fees that contradict the `.agents/context/` specifications.
2.3 When performing cross-functional tasks (e.g., in-chat Web3 transactions), the active agent must cross-reference both the Cryptography/Database context (`02_cryptography_and_privacy_engine.md`, `03_database_and_sqlcipher_context.md`) and the Web3 context (`04_web3_terminal_and_tokenomics.md`).

## 3. Persistent Memory Sync Mandate
3.1 Following the completion of any milestone, action, or bug fix, the agent must update their dedicated memory record under `.agents/omniverse_memories/<agent_id>.md`.
3.2 Memory updates must document:
    - Target file paths modified.
    - Bug patterns caught and resolved.
    - New architectural invariants established.
    - Outstanding tasks and next steps.
