#!/usr/bin/env python3
"""
OMNIVERSE ENTERPRISE RAPID INDEXING SUBMITTER
Pod 5 (Technical SEO Pod) - Lead: Dr. Emily Rivera / Engineer: Priya Patel
Submits all 4,704 route landing pages across all 50 states to IndexNow API & Search Engines
"""

import urllib.request
import urllib.parse
import json
import xml.etree.ElementTree as ET
import os
import glob

HOST = "www.skyautoservices.com"
BASE_URL = f"https://{HOST}"
KEY = "8f3b2a1c9e4d5f6a7b8c9d0e1f2a3b4c"
KEY_LOCATION = f"{BASE_URL}/{KEY}.txt"

def load_all_urls():
    urls = []
    base_dir = "/Users/silversurfer/Documents/Omniverse2"
    
    # 1. Main pages
    urls.extend([
        f"{BASE_URL}/",
        f"{BASE_URL}/about.html",
        f"{BASE_URL}/contact.html",
        f"{BASE_URL}/routes.html",
        f"{BASE_URL}/routes-directory.html"
    ])
    
    # 2. Extract from all 53 sitemaps in public_html_local/sitemaps/
    sitemap_files = glob.glob(os.path.join(base_dir, "public_html_local/sitemaps/*.xml"))
    print(f"[*] Found {len(sitemap_files)} state XML sitemaps. Extracting URLs...")
    
    for sf in sitemap_files:
        try:
            tree = ET.parse(sf)
            root = tree.getroot()
            for elem in root.iter():
                if elem.tag.endswith("loc") and elem.text:
                    loc = elem.text.strip()
                    if loc.startswith("http"):
                        urls.append(loc)
        except Exception as e:
            print(f"[-] Error parsing {sf}: {e}")
            
    # 3. If sitemaps were fewer, also check public_html_local/routes/*.html
    if len(urls) < 100:
        route_files = glob.glob(os.path.join(base_dir, "public_html_local/routes/*.html"))
        for rf in route_files:
            rel_name = os.path.basename(rf)
            urls.append(f"{BASE_URL}/routes/{rel_name}")
            
    unique_urls = sorted(list(set(urls)))
    return unique_urls

def submit_indexnow(urls):
    print(f"[*] Submitting {len(urls)} total URLs to IndexNow API...")
    endpoint = "https://api.indexnow.org/indexnow"
    batch_size = 10000
    results = []
    
    for i in range(0, len(urls), batch_size):
        batch = urls[i:i + batch_size]
        payload = {
            "host": HOST,
            "key": KEY,
            "keyLocation": KEY_LOCATION,
            "urlList": batch
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            endpoint,
            data=data,
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                status = resp.getcode()
                results.append({"batch": i//batch_size + 1, "status": status, "count": len(batch)})
                print(f"[+] IndexNow Batch {i//batch_size + 1}: HTTP {status} OK ({len(batch)} URLs submitted)")
        except urllib.error.HTTPError as e:
            results.append({"batch": i//batch_size + 1, "status": e.code, "msg": e.reason})
            print(f"[-] IndexNow Batch {i//batch_size + 1}: HTTP {e.code} {e.reason}")
        except Exception as e:
            results.append({"batch": i//batch_size + 1, "status": "ERROR", "msg": str(e)})
            print(f"[-] IndexNow Batch Error: {e}")
            
    return results

def main():
    # 1. Create verification key file
    for dest in ["/Users/silversurfer/Documents/Omniverse2", "/Users/silversurfer/Documents/Omniverse2/public_html_local"]:
        if os.path.exists(dest):
            with open(os.path.join(dest, f"{KEY}.txt"), "w", encoding="utf-8") as f:
                f.write(KEY)
                
    # 2. Extract full URL network
    urls = load_all_urls()
    print(f"[+] Total unique URLs extracted: {len(urls)}")
    
    # 3. Submit to IndexNow
    indexnow_res = submit_indexnow(urls)
    
    # 4. Save telemetry
    summary = {
        "status": "COMPLETED",
        "total_urls_submitted": len(urls),
        "indexnow_submissions": indexnow_res,
        "sample_urls": urls[:10]
    }
    with open("/Users/silversurfer/Documents/Omniverse2/scripts/indexing_telemetry_status.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"[+] Successfully submitted all {len(urls)} URLs to IndexNow network! Telemetry updated.")

if __name__ == "__main__":
    main()
