# 🛡️ Mandatory Pre-Flight Idempotency Protocol

This protocol enforces an absolute pre-execution verification check across all Omniverse pods before accepting, designing, or generating tickets, code, or documentation.

---

## 1. The Pre-Flight Three-Pillar Check

Before an agent writes any new code, script, or markdown document, it MUST execute the following pre-flight audit:

### Pillar 1: Workspace & Memory Scan
- Search `context/`, `.agents/context/`, `.agents/heuristics/`, `.agents/logs/`, and the local codebase for:
  - Prior implementations of the requested functionality.
  - Existing data models, utility functions, or API routes.
  - Recorded pitfalls or past bug fixes in `.agents/logs/tool_learnings.md`.

### Pillar 2: Reusability Assessment
- If an existing component, module, or rule satisfies >70% of the ticket requirements:
  - DO NOT generate a duplicate component.
  - Import, extend, or link directly to the existing artifact.

### Pillar 3: Environmental State Verification
- Verify whether the current environment or system state already meets the ticket's acceptance criteria (e.g. static pages already compiled, security headers already active in `.htaccess`).
- If already satisfied, mark the ticket as `IDEMPOTENT_ALREADY_SATISFIED` with link proof rather than performing redundant operations.
