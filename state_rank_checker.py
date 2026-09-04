#!/usr/bin/env python3
"""
state_rank_checker.py
Loops through the master keyword list and queries SerpApi for each state.
Saves the results to seo_audit_results.json.
"""

import os
import json
import logging
from dotenv import load_dotenv
from serpapi import GoogleSearch

from slack_notifier import send_notification

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(message)s")

load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

if not SERPAPI_KEY:
    logging.error("SERPAPI_KEY is missing from .env")
    exit(1)

TARGET_DOMAIN = "skyautoservices.com"

STATES = [
    "Alabama, United States", "Alaska, United States", "Arizona, United States", 
    "Arkansas, United States", "California, United States", "Colorado, United States", 
    "Connecticut, United States", "Delaware, United States", "Florida, United States", 
    "Georgia, United States", "Hawaii, United States", "Idaho, United States", 
    "Illinois, United States", "Indiana, United States", "Iowa, United States", 
    "Kansas, United States", "Kentucky, United States", "Louisiana, United States", 
    "Maine, United States", "Maryland, United States", "Massachusetts, United States", 
    "Michigan, United States", "Minnesota, United States", "Mississippi, United States", 
    "Missouri, United States", "Montana, United States", "Nebraska, United States", 
    "Nevada, United States", "New Hampshire, United States", "New Jersey, United States", 
    "New Mexico, United States", "New York, United States", "North Carolina, United States", 
    "North Dakota, United States", "Ohio, United States", "Oklahoma, United States", 
    "Oregon, United States", "Pennsylvania, United States", "Rhode Island, United States", 
    "South Carolina, United States", "South Dakota, United States", "Tennessee, United States", 
    "Texas, United States", "Utah, United States", "Vermont, United States", 
    "Virginia, United States", "Washington, United States", "West Virginia, United States", 
    "Wisconsin, United States", "Wyoming, United States"
]

BASE_KEYWORDS = [
    "auto transport",
    "car shipping services"
]

OUTPUT_FILE = "seo_audit_results.json"

def get_rank(keyword, location):
    params = {
        "engine": "google",
        "q": keyword,
        "location": location,
        "google_domain": "google.com",
        "gl": "us",
        "hl": "en",
        "num": 100,
        "api_key": SERPAPI_KEY
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        organic_results = results.get("organic_results", [])
        
        for item in organic_results:
            link = item.get("link", "")
            if TARGET_DOMAIN in link:
                return item.get("position"), link
                
        return None, ""
    except Exception as e:
        logging.error(f"Error querying SerpApi for {keyword} in {location}: {e}")
        return None, ""

import concurrent.futures

def check_single(kw, state):
    rank, url = get_rank(kw, state)
    return {
        "keyword": kw,
        "location": state,
        "rank": rank if rank else "Not in Top 100",
        "ranking_url": url,
        "is_number_one": rank == 1
    }

def run_audit():
    results_report = []
    tasks = [(kw, state) for state in STATES for kw in BASE_KEYWORDS]
    total_checks = len(tasks)
    completed = 0
    number_one_rankings = 0

    logging.info(f"Starting state_rank_checker for {TARGET_DOMAIN}")
    logging.info(f"Total combinations to check: {total_checks}. Running concurrently...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_task = {executor.submit(check_single, kw, state): (kw, state) for kw, state in tasks}
        
        for future in concurrent.futures.as_completed(future_to_task):
            kw, state = future_to_task[future]
            try:
                report_item = future.result()
                results_report.append(report_item)
                if report_item["is_number_one"]:
                    number_one_rankings += 1
                
                completed += 1
                logging.info(f"[{completed}/{total_checks}] {kw} in {state}: Rank {report_item['rank']}")
            except Exception as exc:
                logging.error(f"{kw} in {state} generated an exception: {exc}")

    with open(OUTPUT_FILE, "w") as f:
        json.dump(results_report, f, indent=4)

    logging.info(f"Audit complete. Results saved to {OUTPUT_FILE}")

    # Slack Notification
    send_notification("State Rank Checker", {
        "Total Checks": total_checks,
        "#1 Rankings": number_one_rankings,
        "Needs Improvement": total_checks - number_one_rankings
    })

if __name__ == "__main__":
    run_audit()
