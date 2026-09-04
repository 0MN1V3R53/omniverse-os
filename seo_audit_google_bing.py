#!/usr/bin/env python3
"""
OMNIVERSE TECH MATRIX - SEO POD
Author: Dr. Emily Rivera (exec_seo_podlead_v1) & Priya Patel (seo_technical_engineer_cwv)
Directive: Execute Dual-Engine (Google + Bing) 50-State SEO Rank Audit
"""
import re
import json
import time
import random
import logging
from urllib.parse import quote_plus
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("DualEngineSEOAudit")

MEMORY_LOG_PATH = ".agents/logs/MEMORY_LOG.md"
OUR_DOMAIN = "skyautoservices.com"
OUTPUT_JSON = "seo_audit_results_multise.json"

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

def scrape_google(page, keyword, state):
    try:
        query = quote_plus(keyword)
        url = f"https://www.google.com/search?q={query}&num=20"
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        delay()
        
        result_blocks = page.query_selector_all('div.g')
        our_rank = "Not in top 20"
        
        rank_counter = 1
        for block in result_blocks:
            link_elem = block.query_selector('a[href]')
            href = link_elem.get_attribute('href') if link_elem else ""
            
            if OUR_DOMAIN in href.lower():
                if our_rank == "Not in top 20":
                    our_rank = rank_counter
                    break
            rank_counter += 1
            
        logger.info(f"🏆 Google Rank for '{keyword}' ({state}): {our_rank}")
        return our_rank
    except Exception as e:
        logger.error(f"Google Scrape Error '{keyword}': {e}")
        return "Error"

def scrape_bing(page, keyword, state):
    try:
        query = quote_plus(keyword)
        url = f"https://www.bing.com/search?q={query}&count=20"
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        delay()
        
        result_blocks = page.query_selector_all('li.b_algo')
        our_rank = "Not in top 20"
        
        rank_counter = 1
        for block in result_blocks:
            link_elem = block.query_selector('h2 a[href]')
            if not link_elem:
                link_elem = block.query_selector('a[href]')
            href = link_elem.get_attribute('href') if link_elem else ""
            
            if OUR_DOMAIN in href.lower():
                if our_rank == "Not in top 20":
                    our_rank = rank_counter
                    break
            rank_counter += 1
            
        logger.info(f"🏆 Bing Rank for '{keyword}' ({state}): {our_rank}")
        return our_rank
    except Exception as e:
        logger.error(f"Bing Scrape Error '{keyword}': {e}")
        return "Error"

def main():
    logger.info("Initializing Dual-Engine SEO Audit (Google + Bing)")
    
    states_data = parse_50_states()
    if not states_data:
        logger.error("Failed to parse 50 states from MEMORY_LOG.md")
        return
        
    logger.info(f"Loaded {len(states_data)} states for dual-engine auditing.")
    
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
            logger.info(f"🔍 Searching engines for: '{keyword}' (State: {state})")
            
            google_rank = scrape_google(page, keyword, state)
            bing_rank = scrape_bing(page, keyword, state)
            
            results.append({
                "state": state,
                "query": keyword,
                "google_rank": google_rank,
                "bing_rank": bing_rank,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            })
            
        browser.close()
    
    with open(OUTPUT_JSON, 'w') as f:
        json.dump({"results": results, "last_updated": time.strftime("%Y-%m-%d %H:%M:%S")}, f, indent=4)
    logger.info(f"💾 Saved Dual-Engine SEO Audit Data to {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
