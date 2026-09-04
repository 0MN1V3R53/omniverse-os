#!/usr/bin/env python3
"""
OPERATION: LOCAL-SEO-AUDIT (Fast Mode)
Omniverse Tech - Web & SEO Division
Uses html.parser (no lxml overhead) and skips routes/ and massive_scale/
"""

import os
import re
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("LocalSEOAudit")

TARGET_DOMAIN = "www.skyautoservices.com"
LOCAL_ROOT = "public_html_local"
OUTPUT_FILE = "seo_audit_results.json"
ALLOWED_EXTENSIONS = {".html", ".htm"}

# NEVER scan these — too many files, burns tokens & time
SKIP_DIRS = {"routes", "massive_scale", "api", "backend"}

# Regex-based fast extractors (no DOM parser needed for large files)
RE_TITLE       = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)
RE_META_DESC   = re.compile(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', re.I | re.S)
RE_META_DESC2  = re.compile(r'<meta[^>]+content=["\'](.*?)["\'][^>]+name=["\']description["\']', re.I | re.S)
RE_H1          = re.compile(r"<h1[^>]*>(.*?)</h1>", re.I | re.S)
RE_H2          = re.compile(r"<h2[^>]*>(.*?)</h2>", re.I | re.S)
RE_JSON_LD     = re.compile(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.I | re.S)
RE_CANONICAL   = re.compile(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\'](.*?)["\']', re.I | re.S)
RE_ROBOTS_META = re.compile(r'<meta[^>]+name=["\']robots["\'][^>]+content=["\'](.*?)["\']', re.I | re.S)
RE_OG_TITLE    = re.compile(r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\'](.*?)["\']', re.I | re.S)

def strip_tags(text):
    return re.sub(r"<[^>]+>", "", text).strip()


def extract_seo_metadata(content: str, file_path: str) -> dict:
    title_m = RE_TITLE.search(content)
    title = strip_tags(title_m.group(1)) if title_m else None

    desc_m = RE_META_DESC.search(content) or RE_META_DESC2.search(content)
    meta_description = desc_m.group(1).strip() if desc_m else None

    h1_tags = [strip_tags(m.group(1)) for m in RE_H1.finditer(content)]
    h2_count = len(RE_H2.findall(content))

    json_ld_list = []
    for m in RE_JSON_LD.finditer(content):
        try:
            json_ld_list.append(json.loads(m.group(1).strip()))
        except Exception:
            json_ld_list.append({"error": "Invalid JSON-LD"})

    canonical_m = RE_CANONICAL.search(content)
    canonical = canonical_m.group(1) if canonical_m else None

    robots_m = RE_ROBOTS_META.search(content)
    robots = robots_m.group(1) if robots_m else None

    og_title_m = RE_OG_TITLE.search(content)
    og_title = og_title_m.group(1) if og_title_m else None

    # SEO issue flags
    issues = []
    if not title:
        issues.append("MISSING_TITLE")
    elif len(title) < 30:
        issues.append("TITLE_TOO_SHORT")
    elif len(title) > 70:
        issues.append("TITLE_TOO_LONG")

    if not meta_description:
        issues.append("MISSING_META_DESC")
    elif len(meta_description) < 50:
        issues.append("META_DESC_TOO_SHORT")
    elif len(meta_description) > 160:
        issues.append("META_DESC_TOO_LONG")

    if len(h1_tags) == 0:
        issues.append("MISSING_H1")
    elif len(h1_tags) > 1:
        issues.append("MULTIPLE_H1")

    if not canonical:
        issues.append("MISSING_CANONICAL")

    if not json_ld_list:
        issues.append("NO_JSON_LD_SCHEMA")

    return {
        "file": file_path,
        "title": title,
        "title_length": len(title) if title else 0,
        "meta_description": meta_description,
        "meta_desc_length": len(meta_description) if meta_description else 0,
        "h1_count": len(h1_tags),
        "h1_tags": h1_tags[:3],
        "h2_count": h2_count,
        "json_ld_count": len(json_ld_list),
        "canonical": canonical,
        "robots": robots,
        "og_title": og_title,
        "issues": issues,
        "issue_count": len(issues),
    }


def main():
    logger.info(f"[SEO AUDIT] Scanning '{LOCAL_ROOT}' (skipping: {SKIP_DIRS})")
    results = []
    skipped = 0

    for root, dirs, files in os.walk(LOCAL_ROOT):
        # Prune in-place — os.walk will NEVER descend into these
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for fname in files:
            if os.path.splitext(fname)[1].lower() not in ALLOWED_EXTENSIONS:
                continue
            if fname == "googled015412ff0dfd42c.html":
                continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                record = extract_seo_metadata(content, fpath)
                results.append(record)
                logger.info(f"  ✓ {fpath}  issues={record['issue_count']}")
            except Exception as e:
                logger.warning(f"  ✗ {fpath}: {e}")
                skipped += 1

    # Sort by issue count descending so worst pages are first
    results.sort(key=lambda x: x["issue_count"], reverse=True)

    summary = {
        "total_pages_audited": len(results),
        "total_issues_found": sum(r["issue_count"] for r in results),
        "pages_with_issues": sum(1 for r in results if r["issue_count"] > 0),
        "skipped_files": skipped,
        "pages": results
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    logger.info(f"\n[SEO AUDIT COMPLETE]")
    logger.info(f"  Pages audited : {len(results)}")
    logger.info(f"  Total issues  : {summary['total_issues_found']}")
    logger.info(f"  Results saved : {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
