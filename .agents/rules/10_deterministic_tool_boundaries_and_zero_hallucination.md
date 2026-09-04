# RULE 10: DETERMINISTIC TOOL BOUNDARIES & ZERO-HALLUCINATION PROTOCOL

## 1. Zero-Trust Tool Parameter Verification
1.1 Derived from GitHub Agentic Workflows and Mythos 5 tool-execution standards, an agent must verify all tool parameters prior to execution:
    - **Path Verification**: Target file paths must be absolute and verified to exist within the workspace before calling modification tools.
    - **Line-Exact Matching**: Target replacement blocks must match existing file content down to the exact whitespace, indentation, and newline character.
    - **Single Responsibility**: Tools must be called with focused, atomic changes rather than bulk destructive overwrites.

## 2. Zero-Hallucination Invariants
2.1 **Zero Fabrication of APIs or SDKs**:
    - An agent is strictly prohibited from inventing non-existent library methods, phantom Android APIs, or fabricated Web3 RPC endpoints.
    - If an API signature or dependency version is ambiguous, the agent must check the local codebase, Gradle build files, or official documentation.
2.2 **Zero Placeholder Policy**:
    - Every generated function, class, data structure, and test suite must be 100% written out.
    - Any use of `// TODO`, `/* Implement later */`, `...`, or empty catch blocks is classified as a Critical Tier 3 Violation and grounds for immediate rejection during CEO Vance's review.

## 3. Post-Execution Diff Auditing
3.1 Immediately following a tool execution (file write, replacement, or terminal command), the agent must audit the resulting state:
    - Verify that no extraneous characters or syntax errors were introduced.
    - Confirm that all imports remain clean and uncorrupted.
    - Ensure that related modules maintain full confluence with the changes.
