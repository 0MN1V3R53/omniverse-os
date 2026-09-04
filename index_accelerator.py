#!/usr/bin/env python3
"""
index_accelerator.py
Pushes all generated route URLs directly to the Google Indexing API.
Bypasses standard Googlebot crawl wait times to accelerate indexing for programmatic SEO.
"""

import os
import sys
import json
import logging
try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    GOOGLE_API_AVAILABLE = True
except ImportError:
    GOOGLE_API_AVAILABLE = False
from slack_notifier import send_notification

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(message)s")

BASE_URL = "https://www.skyautoservices.com/auto-transport"
CITIES_FILE = "sky_next/public/assets/data/cities.json"
CREDENTIALS_FILE = "credentials.json"
SCOPES = ["https://www.googleapis.com/auth/indexing"]
MAX_URLS = 10  # Reduced for safety during normal runs, can be expanded to total length

def get_indexing_service():
    if not GOOGLE_API_AVAILABLE:
        logging.error("CRITICAL: Google API client libraries not installed. Terminating.")
        sys.exit(1)
    if not os.path.exists(CREDENTIALS_FILE):
        logging.error(f"CRITICAL: Google Cloud Service Account key ({CREDENTIALS_FILE}) not found. Terminating.")
        sys.exit(1)
    try:
        creds = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
        service = build('indexing', 'v3', credentials=creds)
        return service
    except Exception as e:
        logging.error(f"CRITICAL: Failed to build Indexing API service: {e}. Terminating.")
        sys.exit(1)

def main():
    logging.info("Starting Index Acceleration Engine...")
    
    if not os.path.exists(CITIES_FILE):
        logging.error(f"{CITIES_FILE} not found.")
        return
        
    with open(CITIES_FILE, "r") as f:
        cities = json.load(f)
        
    if not cities:
        logging.error("No cities found in database.")
        return
        
    # Generate target URLs
    urls_to_index = []
    for city_data in cities:
        state_slug = city_data.get("stateSlug")
        city_slug = city_data.get("citySlug")
        if state_slug and city_slug:
            url = f"{BASE_URL}/{state_slug}/{city_slug}/"
            urls_to_index.append(url)
            
    total_urls = len(urls_to_index)
    logging.info(f"Loaded {total_urls} route URLs for indexing push.")
    
    # Process a chunk to avoid overwhelming quota
    batch = urls_to_index[:MAX_URLS]
    logging.info(f"Pushing batch of {len(batch)} URLs to Google Indexing API...")
    
    service = get_indexing_service()
    success_count = 0
    
    for url in batch:
        try:
            # Send the URL to the Indexing API
            response = service.urlNotifications().publish(
                body={
                    "url": url,
                    "type": "URL_UPDATED"
                }
            ).execute()
            logging.info(f"Successfully pushed: {url} | Response: {response}")
            success_count += 1
        except Exception as e:
            logging.error(f"Error pushing {url}: {e}")

    # Ping Google Sitemap Endpoint Actually (No Simulation)
    logging.info("Pinging Google Sitemap Endpoint...")
    import urllib.request
    try:
        urllib.request.urlopen("https://www.google.com/ping?sitemap=https://www.skyautoservices.com/sitemap.xml")
        logging.info("Successfully pinged: https://www.google.com/ping?sitemap=https://www.skyautoservices.com/sitemap.xml")
    except Exception as e:
        logging.error(f"Failed to ping sitemap: {e}")

    # Send Notification
    send_notification("Index Acceleration Engine", {
        "Total URLs in Database": total_urls,
        "URLs Pushed in Batch": len(batch),
        "Successful API Pushes": success_count,
        "Mode": "LIVE"
    })

if __name__ == "__main__":
    main()
