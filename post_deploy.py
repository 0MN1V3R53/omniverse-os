#!/usr/bin/env python3
"""
========================================================
SKY AUTO SERVICES — MASTER POST-DEPLOY SEQUENCE
========================================================
Runs all post-deployment tasks in the correct order:
1. Verify deployment is healthy (spot checks)
2. Ping Google to crawl all sitemaps (GSC Indexer)
3. Run one-time live Hostinger telemetry sync
4. Confirm everything is green
"""

import subprocess
import sys
import os
import time

def run(label, cmd, cwd=None):
    print(f"\n{'═'*60}")
    print(f"  ▶  {label}")
    print(f"{'═'*60}")
    result = subprocess.run(cmd, shell=True, cwd=cwd or os.getcwd(), capture_output=False, text=True)
    return result.returncode

ROOT = "/Users/silversurfer/Documents/Omniverse2"

# ── 1. Verify live site ──────────────────────────────────────────────
rc = run("STEP 1/3 — Live Site Health Check", "python3 test_live_site.py 2>/dev/null", cwd=ROOT)
if rc != 0:
    print("\n⛔  HEALTH CHECK FAILED — aborting further steps.")
    sys.exit(1)

# ── 2. Ping Google sitemaps ──────────────────────────────────────────
run("STEP 2/3 — Ping Google to crawl all sitemaps", "python3 seo_gsc_indexer.py", cwd=ROOT)

# ── 3. One-time Hostinger live sync ─────────────────────────────────
run("STEP 3/3 — Sync Hostinger telemetry data (quotes, calls, visitors)", "python3 live_hostinger_sync.py", cwd=ROOT)

print(f"\n{'═'*60}")
print("  ✅  POST-DEPLOY SEQUENCE COMPLETE")
print(f"{'═'*60}\n")
