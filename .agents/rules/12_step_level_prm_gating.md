# RULE 12: STEP-LEVEL PROCESS REWARD MODEL (PRM) GATING

## 1. Mandatory Step Evaluation Invariant
Before calling any state-modifying tool (e.g., `replace_file_content`, `write_to_file`, `run_command`), the agent MUST evaluate the proposed candidate action against the four Process Reward Model dimensions defined in `.agents/context/10_in_context_process_reward_rubric.md`.

---

## 2. In-Stream Evaluation Block Format
Agents must log an explicit evaluation block inside their `<Deep_Reasoning_Stream>`:

```xml
<prm_evaluation>
  <dimension name="ast_syntax" score="1.0" note="Validated Kotlin 2.0 / JS / Python AST, balanced braces, correct imports" />
  <dimension name="crypto_security" score="1.0" note="ByteArray zeroization guaranteed in finally block, Tink AEAD sealed" />
  <dimension name="concurrency_thread" score="1.0" note="Flow bound to Dispatchers.IO, mutex lock held, OWNS file leases respected" />
  <dimension name="token_diff_precision" score="1.0" note="Surgical replacement, zero document truncation, zero placeholder" />
  <dimension name="unlazy_gate_oracle" score="1.0" note="GATES.md runnable checks verified, exit code 0, SHA-256 evidence logged" />
  <composite_score value="1.0" status="PASS" />
</prm_evaluation>
```

---

## 3. Rejection & Self-Correction Loop
- If `composite_score < 0.95`, the tool call or task turn completion is prohibited.
- If an active `GATES.md` contains unverified or failed runnable gates, `unlazy_gate_oracle` is set to `0.0`, triggering an automatic rejection.
- The agent must state the failure reason, branch to an alternate implementation path, and re-evaluate until a score $\ge 0.95$ is achieved.

