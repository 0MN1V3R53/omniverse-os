#!/usr/bin/env python3
"""
Omniverse Live 50-State Search & Indexation Monitoring Engine
Conducts real-time synthetic uptime, TTFB latency, sitemap health, and HTTP status verification
across representative state corridors for skyautoservices.com.
"""

import os
import sys
import json
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent
LOGS_DIR = WORKSPACE_ROOT / ".agents" / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)
STATUS_FILE = WORKSPACE_ROOT / "scripts" / "seo_monitor_status.json"
TELEMETRY_LOG = LOGS_DIR / "SEO_TELEMETRY.log"

SAMPLE_STATE_CORRIDORS = [
    ("CA -> FL", "https://www.skyautoservices.com/routes/california-to-florida-auto-transport"),
    ("NY -> FL", "https://www.skyautoservices.com/routes/new-york-to-florida-auto-transport"),
    ("TX -> CA", "https://www.skyautoservices.com/routes/texas-to-california-auto-transport"),
    ("IL -> FL", "https://www.skyautoservices.com/routes/illinois-to-florida-auto-transport"),
    ("WA -> TX", "https://www.skyautoservices.com/routes/washington-to-texas-auto-transport"),
    ("MA -> FL", "https://www.skyautoservices.com/routes/massachusetts-to-florida-auto-transport"),
    ("MI -> AZ", "https://www.skyautoservices.com/routes/michigan-to-arizona-auto-transport"),
    ("OH -> FL", "https://www.skyautoservices.com/routes/ohio-to-florida-auto-transport"),
    ("GA -> CA", "https://www.skyautoservices.com/routes/georgia-to-california-auto-transport"),
    ("CO -> TX", "https://www.skyautoservices.com/routes/colorado-to-texas-auto-transport")
]

INFRA_ENDPOINTS = [
    ("Master Sitemap Index", "https://www.skyautoservices.com/sitemaps/sitemap_index.xml"),
    ("Priority Routes XML", "https://www.skyautoservices.com/sitemaps/sitemap_priority_routes.xml"),
    ("Robots.txt", "https://www.skyautoservices.com/robots.txt"),
    ("IndexNow Keyfile", "https://www.skyautoservices.com/8f3b2a1c9e4d5f6a7b8c9d0e1f2a3b4c.txt")
]

def run_health_check():
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    report = {
        "timestamp": now_iso,
        "overall_status": "HEALTHY",
        "total_endpoints_tested": len(SAMPLE_STATE_CORRIDORS) + len(INFRA_ENDPOINTS),
        "successful_responses": 0,
        "failed_responses": 0,
        "avg_ttfb_ms": 0.0,
        "corridor_results": [],
        "infra_results": []
    }

    latencies = []
    
    # 1. Test Corridors
    for label, url in SAMPLE_STATE_CORRIDORS:
        start_t = time.time()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Omniverse-Search-Monitor/2.0 (Googlebot-Compatible)"})
            with urllib.request.urlopen(req, timeout=8) as resp:
                elapsed_ms = round((time.time() - start_t) * 1000, 2)
                latencies.append(elapsed_ms)
                status = resp.status
                report["successful_responses"] += 1
                report["corridor_results"].append({
                    "corridor": label,
                    "url": url,
                    "status": status,
                    "ttfb_ms": elapsed_ms,
                    "state": "ONLINE_200_OK"
                })
        except Exception as e:
            report["failed_responses"] += 1
            report["corridor_results"].append({
                "corridor": label,
                "url": url,
                "status": 0,
                "error": str(e),
                "state": "OFFLINE_OR_ERROR"
            })

    # 2. Test Infrastructure Endpoints
    for label, url in INFRA_ENDPOINTS:
        start_t = time.time()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Omniverse-Search-Monitor/2.0"})
            with urllib.request.urlopen(req, timeout=8) as resp:
                elapsed_ms = round((time.time() - start_t) * 1000, 2)
                latencies.append(elapsed_ms)
                status = resp.status
                report["successful_responses"] += 1
                report["infra_results"].append({
                    "endpoint": label,
                    "url": url,
                    "status": status,
                    "ttfb_ms": elapsed_ms,
                    "state": "VALID_200_OK"
                })
        except Exception as e:
            report["failed_responses"] += 1
            report["infra_results"].append({
                "endpoint": label,
                "url": url,
                "status": 0,
                "error": str(e),
                "state": "ERROR"
            })

    if latencies:
        report["avg_ttfb_ms"] = round(sum(latencies) / len(latencies), 2)

    if report["failed_responses"] > 0:
        report["overall_status"] = "DEGRADED"

    # Write status JSON
    STATUS_FILE.write_text(json.dumps(report, indent=2), encoding="utf-8")

    # Append to Telemetry Log
    log_line = f"[{now_iso}] STATUS: {report['overall_status']} | Tested: {report['total_endpoints_tested']} | Success: {report['successful_responses']} | Failed: {report['failed_responses']} | Avg TTFB: {report['avg_ttfb_ms']}ms\n"
    with open(TELEMETRY_LOG, "a", encoding="utf-8") as f:
        f.write(log_line)

    print(f"📡 [Omniverse Telemetry] Heartbeat verified: {report['overall_status']} (Avg TTFB: {report['avg_ttfb_ms']}ms, {report['successful_responses']}/{report['total_endpoints_tested']} OK)")
    return report

if __name__ == "__main__":
    run_health_check()
