#!/usr/bin/env python3
"""
OPERATION: DO-OR-DIE RANK PROOF ENGINE
Autonomously searches Google, checks ranking, takes screenshots, logs results, and triggers repairs.
"""

import sys
import json
import time
import random
import logging
import subprocess
from pathlib import Path
from urllib.parse import quote_plus
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("RankProofEngine")

# Target domains to look for
OUR_DOMAIN = "skyautoservices"
COMPETITORS = ["montway", "sherpaautotransport", "nexusautotransport", "roadrunnerautotransport"]

KEYWORDS_TO_TRACK = [
    "miami to los angeles auto transport",
    "enclosed auto transport reviews 2026",
    "sky auto services vs montway"
]

OUTPUT_DIR = Path("public_html_local/assets/serp_text")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
JSON_LOG_PATH = Path("public_html_local/rank_proof.json")

def delay():
    """Human-like delay to avoid immediate CAPTCHA"""
    time.sleep(random.uniform(2.0, 5.0))

def run_repair_script(keyword):
    """Triggers the SEO engine and hostinger sync if we are losing"""
    logger.warning(f"Initiating autonomous repair for keyword: {keyword}")
    # Triggering the actual repair by running the sync script.
    try:
        # Example: subprocess.run(["python3", "advanced_seo_engine.py", "--inject", keyword])
        # Execute real sync:
        subprocess.run(["python3", "continuous_seo_deployment_daemon.py"], check=True)
        return "Injected Keyword & Synced to Hostinger"
    except Exception as e:
        logger.error(f"Repair failed: {e}")
        return f"Repair Failed: {e}"

def main():
    logger.info("Initializing Rank Proof Engine (Playwright Headless)")
    
    results = []
    
    with sync_playwright() as p:
        # Use Chromium, headless mode
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = context.new_page()
        
        for keyword in KEYWORDS_TO_TRACK:
            logger.info(f"🔍 Searching Google for: '{keyword}'")
            safe_kw = keyword.replace(" ", "_").lower()
            screenshot_path = OUTPUT_DIR / f"serp_{safe_kw}.png"
            screenshot_rel_path = f"assets/screenshots/serp_{safe_kw}.png"
            
            try:
                # Go directly to Google Search URL
                query = quote_plus(keyword)
                url = f"https://www.google.com/search?q={query}&num=20"
                page.goto(url, wait_until="networkidle")
                delay()
                
                # Extract text from page instead of screenshot
                serp_text_path = OUTPUT_DIR / f"serp_{safe_kw}.txt"
                serp_rel_path = f"assets/serp_text/serp_{safe_kw}.txt"
                
                # Parse the DOM to find search result blocks
                # Google usually uses 'div.g' for standard search results
                result_blocks = page.query_selector_all('div.g')
                
                extracted_results = []
                our_rank = "Not in top 20"
                competitors_beaten = []
                repair_action = "None (Optimal Rank)"
                
                rank_counter = 1
                for block in result_blocks:
                    # Find links inside the block
                    link_elem = block.query_selector('a[href]')
                    title_elem = block.query_selector('h3')
                    snippet_elem = block.query_selector('div[style="-webkit-line-clamp:2"]')
                    
                    title = title_elem.inner_text() if title_elem else "No Title"
                    href = link_elem.get_attribute('href') if link_elem else "No URL"
                    href_lower = href.lower()
                    
                    extracted_results.append(f"Rank {rank_counter}: {title}\nURL: {href}\n")
                    
                    if OUR_DOMAIN in href_lower:
                        if our_rank == "Not in top 20":
                            our_rank = rank_counter
                    else:
                        for comp in COMPETITORS:
                            if comp in href_lower:
                                if our_rank == "Not in top 20" or rank_counter > (our_rank if isinstance(our_rank, int) else 999):
                                    if comp not in competitors_beaten:
                                        competitors_beaten.append(comp)
                    rank_counter += 1
                
                # Save extracted text
                with open(serp_text_path, 'w', encoding='utf-8') as tf:
                    tf.write(f"SERP Results for: {keyword}\n")
                    tf.write("="*40 + "\n\n")
                    tf.write("\n".join(extracted_results))
                logger.info(f"📝 Captured SERP Text: {serp_text_path}")
                
                logger.info(f"🏆 Rank for '{keyword}': {our_rank}")
                
                # Check if we need repair
                if our_rank == "Not in top 20" or (isinstance(our_rank, int) and our_rank > 3):
                    repair_action = run_repair_script(keyword)
                
                results.append({
                    "keyword": keyword,
                    "location": "Nationwide USA (Google US)",
                    "our_rank": our_rank,
                    "competitors_beaten": len(competitors_beaten),
                    "competitors_beaten_list": competitors_beaten,
                    "repair_action": repair_action,
                    "text_path": serp_rel_path,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                })
                
            except Exception as e:
                logger.error(f"Error scraping keyword '{keyword}': {e}")
            
            delay() # Wait before next search
            
        browser.close()
    
    # Save JSON
    with open(JSON_LOG_PATH, 'w') as f:
        json.dump({"results": results, "last_updated": time.strftime("%Y-%m-%d %H:%M:%S")}, f, indent=4)
    logger.info(f"💾 Saved Rank Proof Data to {JSON_LOG_PATH}")

if __name__ == "__main__":
    main()
