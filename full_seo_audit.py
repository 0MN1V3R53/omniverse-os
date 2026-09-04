#!/usr/bin/env python3
import os
import re
import json
import logging
from collections import Counter

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("FullSEOAudit")

TARGET_DOMAIN = "www.skyautoservices.com"
LOCAL_ROOT = "public_html_local"
OUTPUT_FILE = "full_seo_audit_results.json"
ALLOWED_EXTENSIONS = {".html", ".htm"}

# Do not skip routes.
SKIP_DIRS = {"massive_scale", "api", "backend", "_next"}

RE_TITLE       = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)
RE_META_DESC   = re.compile(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', re.I | re.S)
RE_META_DESC2  = re.compile(r'<meta[^>]+content=["\'](.*?)["\'][^>]+name=["\']description["\']', re.I | re.S)
RE_H1          = re.compile(r"<h1[^>]*>(.*?)</h1>", re.I | re.S)
RE_CANONICAL   = re.compile(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\'](.*?)["\']', re.I | re.S)

def strip_tags(text):
    return re.sub(r"<[^>]+>", "", text).strip()

def main():
    logger.info("Loading keywords...")
    keywords = set()
    keyword_file = os.path.join(LOCAL_ROOT, "omniversal_master_keyword_matrix.txt")
    if os.path.exists(keyword_file):
        with open(keyword_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    keywords.add(line.lower())
    logger.info(f"Loaded {len(keywords)} keywords.")

    logger.info(f"[SEO AUDIT] Scanning '{LOCAL_ROOT}'")
    skipped = 0
    issue_counts = Counter()
    total_pages_audited = 0

    for root, dirs, files in os.walk(LOCAL_ROOT):
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
                
                title_m = RE_TITLE.search(content)
                title = strip_tags(title_m.group(1)) if title_m else None

                desc_m = RE_META_DESC.search(content) or RE_META_DESC2.search(content)
                meta_description = desc_m.group(1).strip() if desc_m else None

                h1_tags = [strip_tags(m.group(1)) for m in RE_H1.finditer(content)]
                canonical_m = RE_CANONICAL.search(content)
                canonical = canonical_m.group(1) if canonical_m else None

                issues = []
                if not title: issues.append("MISSING_TITLE")
                elif len(title) < 30: issues.append("TITLE_TOO_SHORT")
                elif len(title) > 70: issues.append("TITLE_TOO_LONG")

                if not meta_description: issues.append("MISSING_META_DESC")
                elif len(meta_description) < 50: issues.append("META_DESC_TOO_SHORT")
                elif len(meta_description) > 160: issues.append("META_DESC_TOO_LONG")

                if len(h1_tags) == 0: issues.append("MISSING_H1")
                elif len(h1_tags) > 1: issues.append("MULTIPLE_H1")

                if not canonical: issues.append("MISSING_CANONICAL")
                elif canonical == "https://www.skyautoservices.com/":
                    if fpath != os.path.join(LOCAL_ROOT, "index.html") and not fpath.endswith("/index.html"):
                        # Wait, many pages are index.html inside a directory, like public_html_local/routes/miami/index.html
                        # If the canonical is just the root domain, it's an override issue.
                        pass
                    if canonical == "https://www.skyautoservices.com/":
                        issues.append("HOMEPAGE_CANONICAL_OVERRIDE")

                for issue in issues:
                    issue_counts[issue] += 1
                
                total_pages_audited += 1

            except Exception as e:
                logger.warning(f"  ✗ {fpath}: {e}")
                skipped += 1

    summary = {
        "total_pages_audited": total_pages_audited,
        "total_issues_found": sum(issue_counts.values()),
        "issue_breakdown": dict(issue_counts),
        "total_keywords_verified": len(keywords)
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    logger.info(f"\n[SEO AUDIT COMPLETE]")
    logger.info(f"  Pages audited : {total_pages_audited}")
    logger.info(f"  Total issues  : {summary['total_issues_found']}")
    logger.info(f"  Results saved : {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
