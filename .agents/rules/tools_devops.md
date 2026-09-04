# 🛠️ Tool Affordance Contract: DevOps & SRE Pod (`web_devops_marcus_chen`)

## Enabled Tools
- `terminal_exec`: Building static exports (`npm run build`), rsync deployments (`./sync.sh`), systemctl service checks, curl probes.
- `file_system_mcp`: Atomic updates to `.htaccess`, `sync.sh`, Apache configs, and build manifests.
- `grep_scratchpad`: Fast analysis of compilation error traces and deployment logs.

## Activation Triggers
- Production builds (`npm run build`) upon PR handoff from Engineering.
- Automated incident alerts from `ClosedLoopTelemetryMonitor`.
- Cache invalidation and live endpoint verification.

## Prohibited Actions
- NEVER run unrestricted destructive commands (`rm -rf /`, raw drop database).
- NEVER deploy code with non-zero exit code without triggering self-healing reflection.
