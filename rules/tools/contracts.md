# 🛠️ Standardized Agent Tool Registry & Affordance Contracts

This document establishes the official JSON-schema affordance contracts for all autonomous tools operating across the Omniverse workspace.

---

## 1. `sandboxed_terminal_exec`
- **Purpose:** Executes shell commands within an isolated Docker container with cgroup resource limits, disposable Copy-on-Write (CoW) tmpfs overlay, network isolation (`network_mode="none"`), and automatic fallback to restricted subprocess.
- **Input Contract:**
  - `command` (string, required): Shell command line string.
  - `timeout_sec` (integer, default 60): Maximum execution window.
  - `network` (boolean, default false): Outbound network bridge policy.
  - `cwd` (string, optional): Directory context.
- **Output Contract:**
  - Returns `ContainerExecutionResult` (`command`, `stdout`, `stderr`, `exit_code`, `duration_ms`, `is_containerized`, `container_id`).

---

## 2. `fast_symbol_lookup`
- **Purpose:** Instantaneous sub-10ms symbol resolution backed by a persistent SQLite Write-Ahead Logging (WAL) memory-mapped cache with incremental delta invalidation.
- **Input Contract:**
  - `symbol_name` (string, required): Name of class, function, method, or symbol.
  - `symbol_type` (string, optional): Filter by `class`, `function`, `method`.
- **Output Contract:**
  - Returns a list of `SymbolRecord` objects (`symbol_name`, `symbol_type`, `file_path`, `line_number`, `byte_offset`, `context_snippet`).

---

## 3. `find_all_references`
- **Purpose:** Traces symbol definitions, class type hierarchies, and callers/callees across the entire repository AST.
- **Input Contract:**
  - `symbol_name` (string, required): Name of target symbol.
- **Output Contract:**
  - Returns `SymbolReferenceReport` (`symbol_name`, `definitions`, `usages`, `total_occurrences`).

---

## 4. `terminal_exec`
- **Purpose:** Executes shell commands within sandboxed sub-processes with signal timeouts, reflection loops, and output virtualization.
- **Input Contract:**
  - `command` (string, required): Shell command line string.
  - `cwd` (string, optional): Directory context.
  - `timeout_sec` (float, default 30.0): Maximum execution window.
- **Output Contract:**
  - Returns `VirtualLogDigest` (`status`, `exit_code`, `total_lines`, `total_bytes`, `head_preview`, `log_reference_path`).

---

## 5. `web_researcher`
- **Purpose:** Queries technical documentation and live web search engines, distilling content into clean markdown.
- **Input Contract:**
  - `query` (string, required): Technical query.
  - `target_url` (string, optional): Direct URL to extract.

---

## 6. `youtube_intel`
- **Purpose:** Ingests video streams, extracts timestamped transcripts (`[01:20]`), parses chapters, and isolates architectural takeaways.
- **Input Contract:**
  - `query_or_url` (string, required): Video URL or technical topic.

---

## 7. `file_system_mcp`
- **Purpose:** Atomic filesystem operations with rollback safety and AST validation.
- **Input Contract:**
  - `action` (string, required): `read`, `write_atomic`, `grep`, `list_dir`.
  - `file_path` (string, required): Target path.
  - `content` (string, optional): Code or text content.
