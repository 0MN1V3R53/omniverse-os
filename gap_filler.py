#!/usr/bin/env python3
"""
gap_filler.py
Reads seo_audit_results.json and competitor_report.json to find content gaps.
Generates actionable instructions for the backend in content_gap_instructions.json.
"""

import os
import json
import logging
from slack_notifier import send_notification

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(message)s")

SEO_RESULTS = "seo_audit_results.json"
COMPETITOR_REPORT = "competitor_report.json"
OUTPUT_FILE = "content_gap_instructions.json"

def run_gap_filler():
    logging.info("Starting Gap Filler analysis...")
    
    if not os.path.exists(SEO_RESULTS):
        logging.error(f"{SEO_RESULTS} not found.")
        return
    if not os.path.exists(COMPETITOR_REPORT):
        logging.error(f"{COMPETITOR_REPORT} not found.")
        return
        
    with open(SEO_RESULTS, "r") as f:
        rankings = json.load(f)
        
    with open(COMPETITOR_REPORT, "r") as f:
        competitors = json.load(f)
        
    # Analyze competitor schema baseline
    comp_schemas = set()
    avg_h2 = 0
    comp_count = 0
    for comp_url, data in competitors.items():
        if data.get("status") == "Success":
            comp_count += 1
            for schema in data.get("schemas_found", []):
                comp_schemas.add(schema)
            avg_h2 += data.get("h2_count", 0)
            
    if comp_count > 0:
        avg_h2 = avg_h2 // comp_count
        
    logging.info(f"Competitor Baseline -> Schemas: {comp_schemas}, Avg H2s: {avg_h2}")
    
    instructions = []
    
    # Check each ranking that isn't #1
    for rank_data in rankings:
        if not rank_data.get("is_number_one"):
            kw = rank_data.get("keyword")
            loc = rank_data.get("location")
            
            actions = []
            if "FAQPage" in comp_schemas:
                actions.append({"type": "add_schema", "schema": "FAQPage", "topic": kw})
            if "LocalBusiness" in comp_schemas:
                actions.append({"type": "add_schema", "schema": "LocalBusiness", "location": loc})
            
            actions.append({"type": "ensure_keyword_density", "keyword": kw, "target_h2_count": avg_h2})
            
            instructions.append({
                "target_keyword": kw,
                "target_location": loc,
                "recommended_actions": actions
            })
            
    with open(OUTPUT_FILE, "w") as f:
        json.dump(instructions, f, indent=4)
        
    logging.info(f"Gap filling complete. Instructions saved to {OUTPUT_FILE}")
    
    # Slack Notification
    send_notification("Content Gap Generator", {
        "Instructions Generated": len(instructions),
        "Missing Schemas Identified": len(comp_schemas)
    })

if __name__ == "__main__":
    run_gap_filler()
