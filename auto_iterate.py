#!/usr/bin/env python3
"""
auto_iterate.py
Orchestrates the entire SEO Dominance loop:
1. Rank Tracking
2. Crawl Audit
3. Competitor Analysis
4. Gap Filler
5. Apply Updates
6. Index Acceleration

Continues looping until all keywords are ranked #1, or up to MAX_ITERATIONS.
"""

import os
import json
import logging
import subprocess
import time
from slack_notifier import send_notification

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(message)s")

MAX_ITERATIONS = 3
SEO_RESULTS = "seo_audit_results.json"

def check_if_done():
    if not os.path.exists(SEO_RESULTS):
        return False
        
    with open(SEO_RESULTS, "r") as f:
        rankings = json.load(f)
        
    if not rankings:
        return False
        
    # Check if all rankings are #1
    for rank in rankings:
        if not rank.get("is_number_one"):
            return False
            
    return True

def run_script(script_name):
    logging.info(f"==> Running {script_name}...")
    try:
        subprocess.run(["python3", script_name], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running {script_name}: {e}")
        raise

def main():
    logging.info("Starting Full-Scale SEO Dominance Orchestration")
    send_notification("Orchestrator Started", "Initiating the Auto-Iterate Loop.")
    
    iteration = 1
    while iteration <= MAX_ITERATIONS:
        logging.info(f"--- ITERATION {iteration} / {MAX_ITERATIONS} ---")
        
        # Step 1: Rank Tracking
        run_script("state_rank_checker.py")
        
        # Step 2: Check condition
        if check_if_done():
            logging.info("SUCCESS: All tracked keywords are ranking #1!")
            send_notification("Orchestrator Success", "All keywords have reached Position #1.")
            break
            
        # Step 3: Crawl Audit
        run_script("crawl_audit.py")
        
        # Step 4: Competitor Analysis
        run_script("competitor_analysis.py")
        
        # Step 5: Gap Filler
        run_script("gap_filler.py")
        
        # Step 6: Apply Updates
        run_script("apply_updates.py")

        # Step 7: Index Acceleration
        run_script("index_accelerator.py")
        
        logging.info(f"--- END OF ITERATION {iteration} ---")
        iteration += 1
        
        if iteration <= MAX_ITERATIONS:
            logging.info("Sleeping before next iteration to allow changes to settle and avoid rate limits...")
            # For demonstration we sleep only 10s, but in reality this would be days/weeks.
            time.sleep(10)
            
    if iteration > MAX_ITERATIONS:
        logging.warning("Orchestrator halted: Reached max iterations without hitting 100% #1 rankings.")
        send_notification("Orchestrator Halted", f"Reached max iterations ({MAX_ITERATIONS}).")

if __name__ == "__main__":
    main()
