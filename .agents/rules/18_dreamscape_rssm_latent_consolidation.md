# RULE 18: DREAMSCAPE RSSM LATENT WORLD DREAMING & SLEEP CONSOLIDATION

## 🚨 MANDATORY AUGMENTED INTELLIGENCE SLEEP PROTOCOL
To transcend static token completion and achieve true Augmented Intelligence, Omniverse agents utilize background dreaming and memory consolidation cycles.

---

## 1. Latent State-Space Formulation
During idle cycles or milestone transitions, the system executes the Recurrent State-Space Model (RSSM) in `.agents/dreamscape/rssm_rollout.py`:
$$s_t = (h_t, z_t)$$
$$h_t = f(h_{t-1}, z_{t-1}, a_{t-1})$$
$$z_t \sim q(z_t | h_t, x_t)$$

- **Deterministic Latent State ($h_t$)**: 128-dimensional continuous vector representing temporal execution flow.
- **Stochastic Categorical Latent State ($z_t$)**: 32 discrete classes modeling environmental uncertainty, race conditions, and boundary volatility.

---

## 2. Counterfactual Error Replay & Self-Evolution
1. **Graveyard Replay**: Ingests historical anti-patterns from `.agents/context/11_reflexion_anti_pattern_graveyard.md`.
2. **Ungrounded Latent Simulation**: Simulates 16 to 64 imaginary steps exploring counterfactual decisions ($a_{t-1}'$) to identify optimal recovery vectors.
3. **Automated Mutation Publishing**: When a superior invariant is discovered, the agent autonomously formats and commits a new Request-for-Comments (RFC) mutation document in `.agents/mutations/rfc_*.md`.

---

## 3. Operational Governance
- Dreaming cycles must never overwrite baseline immutable rules (`01` through `16`) directly without explicit Pod Lead verification.
- All synthesized mutations are queued for review and promoted to `.agents/heuristics/` upon verified test-harness pass.
