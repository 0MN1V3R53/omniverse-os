#!/usr/bin/env python3
"""
OPERATION: GOOGLE INDEXING API PUSHER v2.0
===========================================
Omniverse Tech — SEO Pod | Lead: Dr. Sarah Lin
Author: @seo_tech_auditor

Forces URL indexation through the Google Indexing API, bypassing
the passive GSC sitemap queue. Processes all 3,148+ route URLs in
batches of 200 (Google daily quota per project).

SETUP REQUIRED:
  1. Go to https://console.cloud.google.com/
  2. Enable "Indexing API" for your project
  3. Create a Service Account → download JSON key
  4. Place JSON key at:  /Users/silversurfer/Documents/Omniverse2/service_account.json
  5. Add the service account email as an OWNER in Google Search Console

DEPENDENCIES:
  pip install google-auth google-auth-httplib2 requests
"""
import os
import sys
import json
import time
import requests
from datetime import datetime

try:
    import google.auth
    import google.auth.transport.requests
    from google.oauth2 import service_account
    GOOGLE_AUTH_AVAILABLE = True
except ImportError:
    GOOGLE_AUTH_AVAILABLE = False

DIRECTORY       = "/Users/silversurfer/Documents/Omniverse2"
AUTH_FILE       = os.path.join(DIRECTORY, "service_account.json")
ROUTES_JSON     = os.path.join(DIRECTORY, "public_html_local/assets/data/state_routes.json")
ROUTES_FALLBACK = os.path.join(DIRECTORY, "sky_next/public/assets/data/state_routes.json")
BASE_URL        = "https://skyautoservices.com"
INDEXING_ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
SCOPES          = ["https://www.googleapis.com/auth/indexing"]
BATCH_SIZE      = 200   # Google daily quota per service account
DELAY_BETWEEN_REQUESTS = 0.5  # seconds between API calls

def ts():
    return datetime.now().strftime("%H:%M:%S")

def check_dependencies():
    """Verify all required components are present before executing."""
    errors = []
    if not GOOGLE_AUTH_AVAILABLE:
        errors.append(
            "Missing google-auth library.\n"
            "  Fix: pip install google-auth google-auth-httplib2 requests"
        )
    if not os.path.exists(AUTH_FILE):
        errors.append(
            f"Missing service_account.json at:\n  {AUTH_FILE}\n\n"
            "  Fix:\n"
            "  1. Go to https://console.cloud.google.com/apis/credentials\n"
            "  2. Create a Service Account > Add Key > JSON\n"
            "  3. Save the downloaded file as:\n"
            f"     {AUTH_FILE}\n"
            "  4. Enable 'Web Search Indexing API' in your Google Cloud project\n"
            "  5. Add the service account email as Owner in Google Search Console:\n"
            "     https://search.google.com/search-console/users"
        )
    routes_path = ROUTES_JSON if os.path.exists(ROUTES_JSON) else ROUTES_FALLBACK
    if not os.path.exists(routes_path):
        errors.append(f"Cannot find routes data at:\n  {ROUTES_JSON}")
    return errors, routes_path

def get_credentials():
    """Load and refresh Google OAuth2 credentials from service account."""
    creds = service_account.Credentials.from_service_account_file(AUTH_FILE, scopes=SCOPES)
    auth_req = google.auth.transport.requests.Request()
    creds.refresh(auth_req)
    return creds

def load_urls(routes_path):
    """Extract all route URLs from state_routes.json."""
    with open(routes_path, "r", encoding="utf-8") as f:
        routes_data = json.load(f)
    urls = []
    for origin, destinations in routes_data.items():
        for route in destinations:
            slug = route.get('slug', '')
            if slug:
                url = f"{BASE_URL}/routes/{slug}"
                if not url.endswith('.html'):
                    url += '.html'
                urls.append(url)
    return urls

def push_batch(urls_batch, creds, batch_num, total_batches):
    """Submit one batch of URLs to Google Indexing API."""
    auth_req = google.auth.transport.requests.Request()
    if not creds.valid:
        creds.refresh(auth_req)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {creds.token}"
    }
    success_count = 0
    error_count = 0
    print(f"\n[{ts()}] --- BATCH {batch_num}/{total_batches} ({len(urls_batch)} URLs) ---")
    for url in urls_batch:
        payload = {"url": url, "type": "URL_UPDATED"}
        try:
            resp = requests.post(INDEXING_ENDPOINT, json=payload, headers=headers, timeout=8)
            if resp.status_code == 200:
                print(f"  [{ts()}] ✅ {url}")
                success_count += 1
            elif resp.status_code == 429:
                print(f"  [{ts()}] ⏸  RATE LIMIT hit — sleeping 60s...")
                time.sleep(60)
                # Retry once
                resp2 = requests.post(INDEXING_ENDPOINT, json=payload, headers=headers, timeout=8)
                if resp2.status_code == 200:
                    success_count += 1
                else:
                    print(f"  [{ts()}] ❌ Retry failed: {url} → {resp2.status_code}")
                    error_count += 1
            else:
                print(f"  [{ts()}] ❌ {resp.status_code} {url} → {resp.text[:120]}")
                error_count += 1
        except requests.exceptions.Timeout:
            print(f"  [{ts()}] ⏱  TIMEOUT: {url}")
            error_count += 1
        except Exception as e:
            print(f"  [{ts()}] ❌ ERROR: {url} → {str(e)}")
            error_count += 1
        time.sleep(DELAY_BETWEEN_REQUESTS)
    return success_count, error_count

def push_urls_to_indexing_api(start_batch=0, max_batches=None):
    """
    Main entry point.
    start_batch: Resume from a specific batch (0-indexed) — useful if quota was hit mid-run.
    max_batches: Limit the number of batches to push (None = all).
    """
    print("=" * 60)
    print("  OMNIVERSE TECH — Google Indexing API Pusher v2.0")
    print("  SEO Pod Lead: Dr. Sarah Lin | @seo_tech_auditor")
    print("=" * 60)

    # Pre-flight checks
    errors, routes_path = check_dependencies()
    if errors:
        print("\n🚨 [ZERO-DRIFT ERROR] Pre-flight checks failed:\n")
        for err in errors:
            print(f"  • {err}\n")
        sys.exit(1)

    print(f"[{ts()}] ✅ All dependencies verified. Loading route URLs...")
    urls = load_urls(routes_path)
    print(f"[{ts()}] ✅ Loaded {len(urls)} route URLs from {os.path.basename(routes_path)}")

    batches = [urls[i:i + BATCH_SIZE] for i in range(0, len(urls), BATCH_SIZE)]
    total_batches = len(batches)
    print(f"[{ts()}] 📦 {total_batches} batches of {BATCH_SIZE} URLs each.")
    print(f"[{ts()}] ⚠️  Note: Google daily quota is typically 200 URL_UPDATED per day per service account.")
    print(f"[{ts()}] 🔑 Loading Google Service Account credentials...")

    creds = get_credentials()
    print(f"[{ts()}] ✅ OAuth2 token acquired. Service account: {creds.service_account_email}")

    total_success = 0
    total_errors  = 0
    batches_to_run = batches[start_batch:]
    if max_batches:
        batches_to_run = batches_to_run[:max_batches]

    for i, batch in enumerate(batches_to_run):
        batch_num = start_batch + i + 1
        s, e = push_batch(batch, creds, batch_num, total_batches)
        total_success += s
        total_errors  += e

    print(f"\n{'=' * 60}")
    print(f"  ✅ COMPLETE: {total_success} URLs pushed successfully")
    print(f"  ❌ ERRORS:   {total_errors} failures")
    print(f"  📦 Remaining batches: {total_batches - (start_batch + len(batches_to_run))}")
    print(f"  ℹ️  Run again tomorrow with: start_batch={start_batch + len(batches_to_run)}")
    print("=" * 60)

if __name__ == "__main__":
    # Optionally pass start_batch as CLI arg: python3 seo_google_indexing_api.py 5
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    push_urls_to_indexing_api(start_batch=start, max_batches=1)  # 1 batch = 200 URLs per day
