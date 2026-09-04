import os
import json
from dotenv import load_dotenv
from serpapi import GoogleSearch

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

if not SERPAPI_KEY:
    print("ERROR: SERPAPI_KEY is missing from .env")
    print("Please add your SerpApi key to the .env file and run this script again.")
    exit(1)

TARGET_DOMAIN = "skyautoservices.com"

KEYWORDS = [
    {"query": "auto transport Chicago IL", "location": "Chicago, Illinois, United States"},
    {"query": "car shipping services Miami FL", "location": "Miami, Florida, United States"},
    {"query": "auto transport Dallas TX", "location": "Dallas, Texas, United States"},
    {"query": "car shipping Los Angeles CA", "location": "Los Angeles, California, United States"},
    {"query": "auto transport New York NY", "location": "New York, New York, United States"},
    {"query": "auto transport", "location": "United States"},
    {"query": "car shipping services", "location": "United States"}
]

results_report = []

print(f"Starting Rank Tracker for {TARGET_DOMAIN} using SerpApi...")
print("-" * 60)
print(f"{'Keyword':<35} | {'Target Geo':<25} | {'Rank'}")
print("-" * 60)

for target in KEYWORDS:
    params = {
        "engine": "google",
        "q": target["query"],
        "location": target["location"],
        "google_domain": "google.com",
        "gl": "us",
        "hl": "en",
        "num": 100, # search top 100 results
        "api_key": SERPAPI_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    
    organic_results = results.get("organic_results", [])
    
    rank = "Not in Top 100"
    target_url = ""
    
    for item in organic_results:
        link = item.get("link", "")
        if TARGET_DOMAIN in link:
            rank = item.get("position", "Found (No position)")
            target_url = link
            break
            
    report_item = {
        "keyword": target["query"],
        "location": target["location"],
        "rank": rank,
        "ranking_url": target_url
    }
    results_report.append(report_item)
    
    print(f"{target['query']:<35} | {target['location'].split(',')[0]:<25} | {rank}")

# Save to JSON
output_file = "rankings_report.json"
with open(output_file, "w") as f:
    json.dump(results_report, f, indent=4)

print("-" * 60)
print(f"Baseline tracking complete. Results saved to {output_file}")
