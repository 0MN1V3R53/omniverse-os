# 🛠️ Tool Affordance Contract: Security & CISO Pod (`security_ciso_michael_chang`)

## Enabled Tools
- `terminal_exec`: Running security linters, SSL certificate audits, and dependency vulnerability scans.
- `file_system_mcp`: Enforcing `.htaccess` bot scraper rules, security headers, and non-copyable tokens.
- `grep_scratchpad`: Inspecting access logs and potential intrusion/scraping traces.

## Activation Triggers
- Security review stage in SOP pipeline.
- Scraper user-agent detection or unauthorized data copying alerts.

## Prohibited Actions
- NEVER approve a deployment lacking HSTS, clickjacking shields, or anti-scraping blocks.
- NEVER bypass dual-agent verification with the DevOps SRE Lead.
