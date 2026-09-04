#!/usr/bin/env python3
"""
crawl_audit.py
Technical crawl audit script to parse robots.txt and XML sitemaps.
Outputs findings to crawl_audit_report.json.
"""

import os
import json
import logging
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from urllib.parse import urljoin

from slack_notifier import send_notification

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(message)s")

TARGET_DOMAIN = "skyautoservices.com"
BASE_URL = f"https://{TARGET_DOMAIN}"
OUTPUT_FILE = "crawl_audit_report.json"

def fetch_url(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'})
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode('utf-8'), response.getcode()
    except urllib.error.URLError as e:
        code = getattr(e, 'code', str(e))
        logging.error(f"Failed to fetch {url}: {code}")
        return None, code
    except Exception as e:
        logging.error(f"Unexpected error fetching {url}: {e}")
        return None, "Error"

def check_robots_txt():
    url = urljoin(BASE_URL, "/robots.txt")
    content, code = fetch_url(url)
    
    status = "OK" if code == 200 else f"Failed ({code})"
    
    has_user_agent = False
    has_disallow = False
    sitemaps = []
    
    if content:
        lines = content.split('\n')
        for line in lines:
            line = line.strip().lower()
            if line.startswith('user-agent:'):
                has_user_agent = True
            elif line.startswith('disallow:'):
                has_disallow = True
            elif line.startswith('sitemap:'):
                parts = line.split('sitemap:', 1)
                if len(parts) > 1:
                    sitemaps.append(parts[1].strip())
                    
    return {
        "status": status,
        "has_user_agent": has_user_agent,
        "has_disallow": has_disallow,
        "declared_sitemaps": sitemaps
    }, sitemaps

def check_sitemaps(sitemaps):
    urls = []
    sitemap_data = []
    
    if not sitemaps:
        # Fallback to default
        sitemaps = [urljoin(BASE_URL, "/sitemap.xml")]
        
    for sitemap in sitemaps:
        content, code = fetch_url(sitemap)
        status = "OK" if code == 200 else f"Failed ({code})"
        
        page_count = 0
        if content:
            try:
                root = ET.fromstring(content)
                # XML namespaces handling can be tricky, naive search for 'loc'
                for elem in root.iter():
                    if 'loc' in elem.tag.lower():
                        if elem.text:
                            urls.append(elem.text)
                            page_count += 1
            except ET.ParseError:
                status = "XML Parse Error"
                
        sitemap_data.append({
            "url": sitemap,
            "status": status,
            "page_count": page_count
        })
        
    return sitemap_data, len(urls)

def run_audit():
    logging.info(f"Starting crawl audit for {BASE_URL}...")
    
    robots_data, discovered_sitemaps = check_robots_txt()
    sitemap_data, total_pages = check_sitemaps(discovered_sitemaps)
    
    # Estimate crawl budget based on a rough heuristic (e.g. 500 pages/day for a standard low-tier site)
    estimated_crawl_days = round(total_pages / 500.0, 1) if total_pages > 0 else 0
    
    report = {
        "domain": TARGET_DOMAIN,
        "robots_txt": robots_data,
        "sitemaps": sitemap_data,
        "total_urls_discovered": total_pages,
        "estimated_crawl_days": estimated_crawl_days,
        "issues": []
    }
    
    if not robots_data["has_user_agent"]:
        report["issues"].append("robots.txt missing User-Agent directive.")
    if total_pages == 0:
        report["issues"].append("No URLs discovered in sitemaps.")
        
    with open(OUTPUT_FILE, "w") as f:
        json.dump(report, f, indent=4)
        
    logging.info(f"Audit complete. Results saved to {OUTPUT_FILE}")
    
    # Send Notification
    send_notification("Technical Crawl Audit", {
        "Robots.txt": robots_data["status"],
        "Sitemaps Found": len(sitemap_data),
        "Total URLs": total_pages,
        "Issues": len(report["issues"])
    })

if __name__ == "__main__":
    run_audit()
