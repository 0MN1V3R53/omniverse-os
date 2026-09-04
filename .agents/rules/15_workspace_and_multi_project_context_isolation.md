# RULE 15: WORKSPACE AUTO-DETECTION & MULTI-PROJECT CONTEXT ISOLATION

## 1. Principle of Universal Portability
The `.agents/` directory is an autonomous, universal operating system designed to function with zero friction across ANY project workspace (e.g., Full-Stack Web, Online Casino/Gaming, SAP & Warehouse Management Systems, Mobile Apps, SEO, Financial Terminals).

---

## 2. Mandatory Stage 0: Dynamic Workspace Resolution
Prior to reading or emitting any file modification, every agent MUST execute the following 4-step dynamic workspace resolution protocol:

1. **Detect Workspace Directory Name**:
   - Inspect the absolute path of the Current Working Directory (`Cwd`) and extract the root directory name (e.g. `Aegis shield of the gods`, `Omniverse 2`, `casino-platform`, `wms-sap-core`).
2. **Namespace Memory Lookups & Updates**:
   - In individual memory files (`.agents/omniverse_memories/<agent_id>.md`), strictly read and write under the corresponding project section:
     ```markdown
     ## 📌 Multi-Project Workspace Memory Bank
     ### Project: [<Detected_Workspace_Name>]
     - Active Objectives: [...]
     - File Landmarks: [...]
     - Context Commits: [...]
     ```
   - If the detected workspace name does not yet exist in the memory file, the agent must initialize a new clean `### Project: [<Detected_Workspace_Name>]` block immediately.
3. **Domain Blueprint Binding**:
   - Query `.agents/context/00_universal_workspace_router_and_domain_index.md` to load the appropriate domain context (e.g., Gaming/Casino, SAP/WMS, Web/SEO, Mobile/Web3).
4. **Anti-Contamination Invariant**:
   - **NEVER** assume files, dependencies, database entities, or cryptographic schemes from previous projects exist in the current workspace.
   - Every file reference must be verified against the active workspace AST and filesystem.

---

## 3. Strict Prohibitions
- **PROHIBITED**: Overwriting or deleting past project memory blocks when switching to a new workspace.
- **PROHIBITED**: Importing project-specific symbols (e.g. Android Kotlin classes in a Next.js or SAP project) unless explicitly present in the active workspace.
- **PROHIBITED**: Bleeding API credentials, RPC endpoints, or database tables across different workspace partitions.
