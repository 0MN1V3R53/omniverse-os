#!/usr/bin/env python3
"""
OPERATION: SKY-AUTO-SEO-AUDIT (Remote Paramiko Crawler)
Omniverse Tech - Web Development, SEO & Infrastructure Division

Orchestrated by:
- Dr. Alexander Vance (CEO)
- Marcus Chen (DevOps Lead) & devops_sysadmin_1 (Junior Linux Admin)
- Dr. Sarah Lin (Chief SEO Lead) & seo_tech_auditor (Tech SEO Auditor)
- Jaxon Reed (Ops Systems Hygiene)

Establishes a secure SSH/SFTP connection to Hostinger via Paramiko,
pulls credentials safely from a local .env file, scans the remote public_html
directory, and parses HTML structure with BeautifulSoup to audit Title tags,
Meta descriptions, JSON-LD Schema structures, H1/H2 hierarchies, and internal linking.
"""

import os
import sys
import json
import logging
import stat
from urllib.parse import urlparse
from dotenv import load_dotenv

import paramiko
from bs4 import BeautifulSoup

# Setup logging
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("SkyAutoSEOAudit")

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Custom simple .env parser fallback
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip().strip("'\"")


HOSTINGER_HOST = os.getenv("HOSTINGER_HOST", "82.198.228.154")
HOSTINGER_PORT = int(os.getenv("HOSTINGER_PORT", 65002))
HOSTINGER_USER = os.getenv("HOSTINGER_USER", "u803913036")
HOSTINGER_PASSWORD = os.getenv("HOSTINGER_PASSWORD", "")

REMOTE_TARGET_DIRS = [
    "public_html",
    "domains/skyautoservices.com/public_html"
]

OUTPUT_FILE = "remote_seo_audit_results.json"
ALLOWED_EXTENSIONS = {".html", ".htm", ".php"}
SKIP_DIRS = {"wp-admin", "wp-includes", "vendor", "cache", "tmp", ".git"}


def parse_page_seo(html_content: str, remote_path: str) -> dict:
    """
    Parses HTML/PHP content using BeautifulSoup (provided by seo_tech_auditor).
    Extracts Title, Meta Description, H1/H2 headers, JSON-LD schemas,
    Canonical URLs, Robots directives, and internal linking patterns.
    """
    soup = BeautifulSoup(html_content, "html.parser")

    # 1. Title Tag
    title_tag = soup.find("title")
    title_text = title_tag.get_text(strip=True) if title_tag else None

    # 2. Meta Description
    meta_desc_tag = soup.find("meta", attrs={"name": lambda x: x and x.lower() == "description"})
    meta_description = meta_desc_tag.get("content", "").strip() if meta_desc_tag else None

    # 3. Heading Hierarchy (H1 & H2)
    h1_elements = [h.get_text(strip=True) for h in soup.find_all("h1")]
    h2_elements = [h.get_text(strip=True) for h in soup.find_all("h2")]

    # 4. JSON-LD Schema Structures
    json_ld_schemas = []
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        try:
            if script.string:
                data = json.loads(script.string.strip())
                json_ld_schemas.append(data)
        except Exception:
            json_ld_schemas.append({"raw": script.string, "error": "Invalid JSON-LD Syntax"})

    # 5. Canonical & Robots Tags
    canonical_tag = soup.find("link", attrs={"rel": lambda x: x and "canonical" in x.lower()})
    canonical_url = canonical_tag.get("href", "").strip() if canonical_tag else None

    robots_tag = soup.find("meta", attrs={"name": lambda x: x and x.lower() == "robots"})
    robots_content = robots_tag.get("content", "").strip() if robots_tag else None

    # 6. Internal vs External Linking Patterns
    internal_links = []
    external_links = []
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"].strip()
        anchor_text = a_tag.get_text(strip=True)
        parsed = urlparse(href)

        if not href or href.startswith("#") or href.startswith("javascript:"):
            continue

        if parsed.netloc == "" or "skyautoservices.com" in parsed.netloc:
            internal_links.append({"href": href, "anchor": anchor_text[:50]})
        else:
            external_links.append({"href": href, "anchor": anchor_text[:50]})

    # 7. Audit Rules & Flagged Issues
    issues = []

    if not title_text:
        issues.append("CRITICAL: Missing <title> tag")
    elif len(title_text) < 30:
        issues.append(f"WARNING: Title too short ({len(title_text)} chars)")
    elif len(title_text) > 60:
        issues.append(f"WARNING: Title too long ({len(title_text)} chars)")

    if not meta_description:
        issues.append("CRITICAL: Missing Meta Description")
    elif len(meta_description) < 50:
        issues.append(f"WARNING: Meta Description too short ({len(meta_description)} chars)")
    elif len(meta_description) > 160:
        issues.append(f"WARNING: Meta Description too long ({len(meta_description)} chars)")

    if len(h1_elements) == 0:
        issues.append("CRITICAL: Missing <h1> heading")
    elif len(h1_elements) > 1:
        issues.append(f"WARNING: Multiple <h1> headings found ({len(h1_elements)})")

    if not json_ld_schemas:
        issues.append("WARNING: Missing JSON-LD Schema markup")

    if not canonical_url:
        issues.append("WARNING: Missing Canonical URL")

    return {
        "remote_path": remote_path,
        "title": title_text,
        "title_length": len(title_text) if title_text else 0,
        "meta_description": meta_description,
        "meta_desc_length": len(meta_description) if meta_description else 0,
        "h1_count": len(h1_elements),
        "h1_samples": h1_elements[:3],
        "h2_count": len(h2_elements),
        "json_ld_count": len(json_ld_schemas),
        "json_ld_types": [s.get("@type") for s in json_ld_schemas if isinstance(s, dict) and "@type" in s],
        "canonical_url": canonical_url,
        "robots_meta": robots_content,
        "internal_link_count": len(internal_links),
        "external_link_count": len(external_links),
        "issues": issues,
        "issue_count": len(issues),
    }


def scan_remote_dir(sftp, remote_dir: str, results: list):
    """
    Recursively scans the remote directory over SFTP for HTML/PHP files.
    """
    try:
        items = sftp.listdir_attr(remote_dir)
    except Exception as e:
        logger.warning(f"Could not list directory {remote_dir}: {e}")
        return

    for item in items:
        remote_path = f"{remote_dir}/{item.filename}"

        if stat.S_ISDIR(item.st_mode):
            if item.filename in SKIP_DIRS or item.filename.startswith("."):
                continue
            scan_remote_dir(sftp, remote_path, results)
        elif stat.S_ISREG(item.st_mode):
            ext = os.path.splitext(item.filename)[1].lower()
            if ext in ALLOWED_EXTENSIONS:
                try:
                    with sftp.open(remote_path, "r") as f:
                        content = f.read().decode("utf-8", errors="ignore")
                    seo_record = parse_page_seo(content, remote_path)
                    results.append(seo_record)
                    logger.info(f"  ✓ Processed {remote_path} (Issues: {seo_record['issue_count']})")
                except Exception as ex:
                    logger.error(f"  ✗ Failed reading {remote_path}: {ex}")


def main():
    logger.info("=== OPERATION: SKY-AUTO-SEO-AUDIT ===")
    logger.info(f"Connecting to Hostinger SSH at {HOSTINGER_HOST}:{HOSTINGER_PORT} as {HOSTINGER_USER}...")

    if not HOSTINGER_PASSWORD:
        logger.error("Error: HOSTINGER_PASSWORD missing from .env file!")
        sys.exit(1)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(
            hostname=HOSTINGER_HOST,
            port=HOSTINGER_PORT,
            username=HOSTINGER_USER,
            password=HOSTINGER_PASSWORD,
            timeout=15
        )
        logger.info("✓ Secure SSH Connection Established!")
    except Exception as e:
        logger.error(f"SSH Connection Failed: {e}")
        sys.exit(1)

    sftp = ssh.open_sftp()
    results = []

    for target_dir in REMOTE_TARGET_DIRS:
        logger.info(f"\nScanning remote path: {target_dir}...")
        scan_remote_dir(sftp, target_dir, results)

    sftp.close()
    ssh.close()

    # Deduplicate results if paths overlap
    seen_paths = set()
    unique_results = []
    for r in results:
        if r["remote_path"] not in seen_paths:
            seen_paths.add(r["remote_path"])
            unique_results.append(r)

    unique_results.sort(key=lambda x: x["issue_count"], reverse=True)

    summary = {
        "operation": "SKY-AUTO-SEO-AUDIT",
        "target_host": HOSTINGER_HOST,
        "total_pages_audited": len(unique_results),
        "total_issues_found": sum(r["issue_count"] for r in unique_results),
        "pages_with_issues": sum(1 for r in unique_results if r["issue_count"] > 0),
        "audit_timestamp": os.popen("date").read().strip(),
        "pages": unique_results
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    logger.info("\n=== SEO AUDIT COMPLETED ===")
    logger.info(f"Total Pages Audited : {len(unique_results)}")
    logger.info(f"Total Issues Found  : {summary['total_issues_found']}")
    logger.info(f"Results Saved To    : {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
