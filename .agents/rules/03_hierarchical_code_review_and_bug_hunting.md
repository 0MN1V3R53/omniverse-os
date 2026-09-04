# RULE 03: HIERARCHICAL CODE REVIEW & BUG-HUNTING PROTOCOL

## 1. Multi-Tier Code Review Pipeline
To ensure production-grade reliability, all code authored within the Aegis repository must pass through a strict four-stage hierarchical review pipeline:

```
[Tier 1: Junior Specialist Implementation]
  └─ Writes 100% production-ready, non-stubbed atomic code.
     │
[Tier 2: Senior Pod Lead Bug Hunt & Edge-Case Scan]
  └─ Audits line-by-line for syntax errors, boundary bugs, race conditions, and non-confluence.
     │
[Tier 3: Department Director / Security Lead Verification]
  └─ Audits cryptographic security, memory leak vectors, Keystore safety, and database integrity.
     │
[Tier 4: CEO Dr. Alexander Vance Holistic Sign-Off]
  └─ Verifies global system confluence, confirms zero drift, and authorizes deployment.
```

## 2. Pod Lead Bug-Hunting Checklist
During Tier 2 review, Pod Leads must explicitly evaluate:
- **Null Safety & Boundary Checks**: Are all nullable parameters guarded against NPEs and index out-of-bounds?
- **Concurrency & Coroutines**: Are coroutine scopes (`Dispatchers.IO`, `Dispatchers.Default`, `Dispatchers.Main`) properly assigned without blocking UI threads?
- **Memory & Resource Leaks**: Are crypto byte arrays zeroized after use? Are database cursors, WebSockets, and WebRTC peer connections properly closed upon lifecycle destruction?
- **State Confluence**: Does the implementation properly synchronize with Room entities, LiveData/StateFlow streams, and local Keystore blobs?

## 3. Mandatory Defect Remediation
3.1 If a bug, edge-case vulnerability, or non-confluence issue is detected during review, the reviewer must immediately reject the PR, document the exact failing line and root cause, and re-assign the task to the junior specialist with remediation instructions.
3.2 Code with unhandled exceptions, unchecked casts, or insecure fallbacks is strictly prohibited from merging.
