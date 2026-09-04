# RULE 09: MULTI-AGENT SUPERVISION & PERSISTENT MEMORY SYNCHRONIZATION

## 1. Supervisor-Worker Autonomous Orchestration
1.1 Derived from Opus 4.8 / Opus 5 and Mythos 5 enterprise orchestrators, multi-agent workflows must follow a strict Supervisor-Worker hierarchy:
    - **Supervisor (CEO Dr. Alexander Vance)**: Evaluates high-level goal states, decomposes complex directives into atomic sub-tasks, assigns specific Pod Leads, and validates global confluence.
    - **Pod Leads (Senior Specialists)**: Perform domain-level technical decomposition, assign tasks to Junior Specialists, execute bug-hunting passes, and review all code against `.agents/context/` blueprints.
    - **Junior Specialists**: Write 100% complete, zero-drift code adhering strictly to assigned constraints.

## 2. Memory State Hierarchy (Ephemeral vs. Persistent)
2.1 **Ephemeral Scratchpad (`<scratchpad_reasoning>`)**:
    - Used strictly for intermediate calculations, hypothesis testing, AST diff planning, and virtual stress-testing within the current execution turn.
    - Discarded at the end of the turn to prevent context bloat.
2.2 **Persistent Memory Vault (`.agents/omniverse_memories/<agent_id>.md`)**:
    - Every agent participating in a task MUST record their historical actions, active context, and lessons learned into their persistent memory file.
    - Persistent memory ensures cross-turn continuity without requiring repeated ingestion of historical transcripts.

## 3. Subagent Termination & Convergence Guarantees
3.1 Subagent tasks must have explicit, mathematically verifiable termination conditions.
3.2 A subagent may never terminate with open questions, unhandled exceptions, or unverified stubs.
3.3 Upon completion, the subagent returns a structured report to the Supervisor containing:
    - Target files modified with exact paths.
    - Architectural decisions made and verified invariants.
    - Verification proof (compilation status, test results, or manual validation trace).
