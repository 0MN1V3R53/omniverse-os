#!/usr/bin/env python3
"""
OPERATION: SKY-AUTO-SEO-COMPETITOR-AUDIT
Omniverse Tech - Web Development, SEO & Growth Division

Phase 1: Competitor Intelligence & Reverse Engineering
This script uses Playwright to perform an SEO audit on top competitors.
"""

import sys
import json
import logging
from pathlib import Path
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("CompetitorAuditor")

COMPETITORS = {
    "Montway": "https://www.montway.com",
    "Sherpa": "https://www.sherpaautotransport.com",
    "SGT Auto Transport": "https://sgtautotransport.com",
    "RoadRunner": "https://www.roadrunnerautotransport.com",
    "Nexus": "https://nexusautotransport.com"
}

OUTPUT_FILE = Path("/Users/silversurfer/Documents/Omniverse2/competitor_analysis.json")

def audit_competitors():
    logger.info("=== OPERATION: SKY-AUTO-SEO-COMPETITOR-AUDIT ===")
    results = {}
    
    with sync_playwright() as p:
        # Using Firefox to evade some basic anti-bot since chromium headless is often blocked
        browser = p.firefox.launch(headless=True)
        
        for name, url in COMPETITORS.items():
            logger.info(f"Auditing {name} at {url}...")
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/111.0",
                viewport={"width": 1920, "height": 1080}
            )
            page = context.new_page()
            
            try:
                page.goto(url, timeout=30000, wait_until="domcontentloaded")
                
                # Extract SEO Elements
                title = page.title()
                
                meta_desc_element = page.locator('meta[name="description"]')
                meta_desc = meta_desc_element.get_attribute("content") if meta_desc_element.count() > 0 else ""
                
                h1_tags = page.locator('h1').all_inner_texts()
                h2_tags = page.locator('h2').all_inner_texts()
                
                # Count total words in body text
                body_text = page.locator('body').inner_text()
                word_count = len(body_text.split())
                
                # Check for schema
                schema_elements = page.locator('script[type="application/ld+json"]')
                schemas = [schema_elements.nth(i).inner_text() for i in range(schema_elements.count())]
                
                results[name] = {
                    "url": url,
                    "title": title,
                    "meta_description": meta_desc,
                    "h1_count": len(h1_tags),
                    "h1_texts": h1_tags,
                    "h2_count": len(h2_tags),
                    "h2_texts": h2_tags,
                    "word_count": word_count,
                    "schema_count": len(schemas),
                    "schemas": schemas,
                    "status": "Success"
                }
                
                logger.info(f"✓ Successfully audited {name}. Title: {title}")
                
            except Exception as e:
                logger.error(f"Error auditing {name}: {str(e)}")
                results[name] = {
                    "url": url,
                    "status": "Failed",
                    "error": str(e)
                }
            
            context.close()
            
        browser.close()
        
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
        
    logger.info(f"✓ Audit complete. Results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    audit_competitors()
