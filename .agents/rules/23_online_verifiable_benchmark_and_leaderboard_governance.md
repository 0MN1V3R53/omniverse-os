# RULE 23: ONLINE VERIFIABLE BENCHMARK & THIRD-PARTY LEADERBOARD GOVERNANCE

## 1. Purpose & Scope
This rule codifies the authoritative operating standards for evaluating and submitting the **Omniverse OS** (`.agents/` cognitive engine, context blueprints, rules, heuristics, connectors, and multi-agent cascading delegation) to third-party, publicly verified AI benchmark leaderboards.

Omniverse OS supports four third-party verified evaluation tracks:
- **Track A (SWE-bench Verified)**: Princeton NLP / `swebench.com` (500 real-world repository issue tasks).
- **Track B (GAIA Benchmark)**: Hugging Face Spaces / Meta AI (`gaia-benchmark/leaderboard`) (Multi-modal assistant, tool use, web research).
- **Track C (LiveCodeBench)**: `livecodebench.github.io` / Hugging Face (Contamination-free algorithmic code generation from LeetCode, Codeforces, AtCoder).
- **Track D (`pwn.college` Online Dojo)**: ASU SEFCOM / Dr. Yan Shoshitaishvili (Live binary exploitation and CTF flag verification API).

---

## 2. Anti-Contamination & Anti-Simulation Invariants
1. **Zero Mock Invariant**: Under no circumstances shall synthetic, mocked, or fabricated benchmark scores be presented as third-party verified results.
2. **Zero Memorization Invariant**: Test split tasks must never be hardcoded into prompt prefixes or persistent memories. All outputs must be derived dynamically through authentic runtime agentic execution.
3. **Cryptographic Proof Manifest**: Every evaluated task must produce an auditable cryptographic proof tuple:
   $$\text{Proof} = \mathcal{H}_{\text{SHA-256}}\Big(\text{TaskID} \parallel \text{Timestamp} \parallel \text{ModelID} \parallel \text{OutputPayload}\Big)$$
   Recorded in `.agents/output/benchmark_submissions/audit_manifest.jsonl`.
4. **Target Model Identifier**: All official submissions must be tagged with the standardized model identifier:
   `omniverse-os-leviathan-999` (or division-specific tag `omniverse-code-v5.1` for Track D).

---

## 3. Track-Specific Submission Standards

### Track A: SWE-bench Verified (Princeton NLP)
1. **Output Schema (`preds.json`)**:
   ```json
   {
     "<instance_id>": {
       "model_name_or_path": "omniverse-os-leviathan-999",
       "model_patch": "<git unified diff>"
     }
   }
   ```
2. **Patch Invariants**:
   - Must be a valid unified diff parseable by `git apply --check`.
   - Zero stub comments (`// TODO`, `pass`, `/* placeholder */`) in the emitted diff.
   - Must modify only files relevant to the issue description.
3. **PR Submission Structure**:
   Target repository: `princeton-nlp/SWE-bench` (branch `evaluation/omniverse-os-leviathan-999`).
   Required assets:
   - `preds.json`: 500 instance diffs.
   - `metadata.yaml`: System architecture details, tool afforadances, test-time compute parameters.
   - `README.md`: Reproduction commands and evaluation telemetry.

### Track B: GAIA Leaderboard (Hugging Face Spaces)
1. **Output Schema (`submission.jsonl`)**:
   Each line must be a self-contained JSON object:
   ```json
   {"task_id": "<uuid>", "model_answer": "<normalized_answer_string>"}
   ```
2. **Answer Normalization Standards**:
   - Number answers: Stripped of currency symbols, commas, and trailing zero decimals (e.g., `1450.5`).
   - String answers: Lowercase, stripped of punctuation, whitespace trimmed.
   - List answers: Comma-separated sorted items (e.g., `alpha, beta, gamma`).
3. **Submission Endpoint**: Uploaded directly via Hugging Face Hub API or web portal to Space `gaia-benchmark/leaderboard`.

### Track C: LiveCodeBench (Continuous Algorithmic Synthesis)
1. **Output Schema (`lcb_generations.jsonl`)**:
   ```json
   {
     "question_id": "<str>",
     "code": "<syntactically complete python3/c++ solution>",
     "model": "omniverse-os-leviathan-999",
     "timestamp": "<iso8601>"
   }
   ```
2. **AST Gating**:
   - Every candidate solution must pass in-memory Python AST validation (`ast.parse`) or Clang AST syntax check.
   - Must satisfy $O(N)$ or optimal time-complexity bounds for LeetCode/Codeforces test cases.

### Track D: `pwn.college` Live Dojo (ASU SEFCOM)
1. **Connection Protocol**: Live TCP socket (`socket.create_connection`) or SSH tunnel to `pwn.college` challenge containers (`dojo.pwn.college`).
2. **Flag Regex & Validation**:
   - Pattern: `pwn\.college\{[A-Za-z0-9_\-]+\}`
   - Proof of Flag capture logged with server challenge ID and submission timestamp.
3. **Scoreboard API Dispatch**:
   - Endpoint: `https://pwn.college/api/v1/challenges/attempt`
   - Payload: `{"challenge_id": "<id>", "submission": "pwn.college{...}"}`
   - Result: Public scoreboard points verified and recorded.

---

## 4. Cascading Execution & Supervision Matrix
1. **CEO Dr. Alexander Vance**: Receives evaluation mandate, authorizes target track, verifies cryptographic proof manifest, and signs off on public PR/API submission.
2. **Pod 13 Lead (Dr. Aris Thorne - Frontier Agentic Systems)**: Enforces PRM step gating ($PRM \ge 0.95$), MCTS tree search allocation, and KV-cache prefix optimization.
3. **Pod 16 Lead (Prof. Lucas Mercer - Omniverse Code)**: Supervises Track A (SWE-bench unified diffs) and Track D (`pwn.college` binary exploitation & flag extraction).
4. **Pod 01/02 Leads (Julian Thorne / Priya Patel - Full-Stack Web & Systems)**: Oversee schema compliance, JSONL normalization, and network transmission pipelines.
