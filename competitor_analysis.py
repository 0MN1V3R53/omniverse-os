#!/usr/bin/env python3
"""
competitor_analysis.py
Scrapes competitor landing pages to analyze their on-page SEO (schema, headers).
Outputs findings to competitor_report.json.
"""

import os
import json
import logging
import requests
from bs4 import BeautifulSoup

from slack_notifier import send_notification

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(message)s")

COMPETITORS = [
    "https://www.montway.com",
    "https://www.autostartransport.com",
    "https://www.uship.com"
]

OUTPUT_FILE = "competitor_report.json"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

def analyze_page(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract H1/H2
        h1_tags = [h.get_text(strip=True) for h in soup.find_all("h1")]
        h2_tags = [h.get_text(strip=True) for h in soup.find_all("h2")]
        
        # Extract Schema (JSON-LD)
        schemas = []
        for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
            if script.string:
                try:
                    data = json.loads(script.string)
                    # Handle both single objects and lists of objects
                    if isinstance(data, list):
                        for item in data:
                            schemas.append(item.get("@type", "Unknown"))
                    elif isinstance(data, dict):
                        schemas.append(data.get("@type", "Unknown"))
                except json.JSONDecodeError:
                    pass
                    
        # Extract Internal Links (rough estimate: links starting with '/' or the domain)
        internal_links = 0
        domain_str = url.split("://")[1].split("/")[0].replace("www.", "")
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.startswith("/") or domain_str in href:
                internal_links += 1
                
        return {
            "url": url,
            "status": "Success",
            "h1_count": len(h1_tags),
            "h2_count": len(h2_tags),
            "schemas_found": schemas,
            "internal_links": internal_links
        }
    except Exception as e:
        logging.error(f"Failed to analyze {url}: {e}")
        return {
            "url": url,
            "status": f"Error: {str(e)}"
        }

def run_analysis():
    logging.info("Starting Competitor Analysis...")
    report = {}
    
    for comp in COMPETITORS:
        logging.info(f"Analyzing {comp}...")
        data = analyze_page(comp)
        report[comp] = data
        
    with open(OUTPUT_FILE, "w") as f:
        json.dump(report, f, indent=4)
        
    logging.info(f"Analysis complete. Results saved to {OUTPUT_FILE}")
    
    # Slack Notification
    success_count = sum(1 for v in report.values() if v.get("status") == "Success")
    send_notification("Competitor Analysis", {
        "Competitors Scanned": len(COMPETITORS),
        "Successful Scans": success_count
    })

if __name__ == "__main__":
    run_analysis()
