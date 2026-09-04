import re
import json
import time
import random
import logging
from pathlib import Path
from urllib.parse import quote_plus
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("RealWorldSEOAudit")

MEMORY_LOG_PATH = ".agents/logs/MEMORY_LOG.md"
OUR_DOMAIN = "skyautoservices.com"
OUTPUT_JSON = "actual_seo_audit_results.json"

def delay():
    """Human-like delay to avoid immediate CAPTCHA"""
    time.sleep(random.uniform(2.0, 4.0))

def parse_50_states():
    with open(MEMORY_LOG_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Example line: 1. **Alabama (AL)** — VPN: Birmingham / Montgomery | Query: `"Alabama to Florida auto transport"`
    pattern = r'\d+\.\s+\*\*(.*?)\*\*\s+—\s+VPN:\s+(.*?)\s+\|\s+Query:\s+`"(.*?)"`'
    matches = re.findall(pattern, content)
    
    states_data = []
    for match in matches:
        state_info, vpn_info, query = match
        states_data.append({
            "state": state_info,
            "vpn": vpn_info,
            "query": query
        })
    return states_data

def main():
    logger.info("Initializing Real-World SEO Audit Engine (Playwright Headless)")
    
    states_data = parse_50_states()
    if not states_data:
        logger.error("Failed to parse 50 states from MEMORY_LOG.md")
        return
        
    logger.info(f"Loaded {len(states_data)} states for auditing.")
    
    results = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = context.new_page()
        
        for item in states_data:
            state = item["state"]
            keyword = item["query"]
            logger.info(f"🔍 Searching Google for: '{keyword}' (State: {state})")
            
            try:
                query = quote_plus(keyword)
                url = f"https://www.google.com/search?q={query}&num=20"
                page.goto(url, wait_until="networkidle")
                delay()
                
                result_blocks = page.query_selector_all('div.g')
                
                our_rank = "Not in top 20"
                
                rank_counter = 1
                for block in result_blocks:
                    link_elem = block.query_selector('a[href]')
                    href = link_elem.get_attribute('href') if link_elem else ""
                    href_lower = href.lower()
                    
                    if OUR_DOMAIN in href_lower:
                        if our_rank == "Not in top 20":
                            our_rank = rank_counter
                            break # Found highest rank
                    rank_counter += 1
                
                logger.info(f"🏆 Rank for '{keyword}' ({state}): {our_rank}")
                
                results.append({
                    "state": state,
                    "query": keyword,
                    "rank": our_rank,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                })
                
            except Exception as e:
                logger.error(f"Error scraping keyword '{keyword}': {e}")
                results.append({
                    "state": state,
                    "query": keyword,
                    "rank": "Error",
                    "error": str(e),
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                })
            
        browser.close()
    
    with open(OUTPUT_JSON, 'w') as f:
        json.dump({"results": results, "last_updated": time.strftime("%Y-%m-%d %H:%M:%S")}, f, indent=4)
    logger.info(f"💾 Saved Real-World SEO Audit Data to {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
