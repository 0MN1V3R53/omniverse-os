#!/usr/bin/env python3
import urllib.request
import json
import os
import sys

def verify_live_telemetry_endpoints():
    print("=========================================================")
    print("⚡ VERIFYING LIVE HOSTINGER PRODUCTION TELEMETRY ENDPOINTS")
    print("=========================================================")
    
    urls = [
        "https://skyautoservices.com/quote_submissions.json",
        "https://skyautoservices.com/call_requests.json",
        "https://skyautoservices.com/visitor_intelligence_telemetry.json"
    ]
    
    all_passed = True
    for url in urls:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Omniverse-Verification/3.0'})
            with urllib.request.urlopen(req, timeout=8) as res:
                status = res.status
                content = res.read().decode('utf-8')
                data = json.loads(content)
                item_count = len(data) if isinstance(data, list) else (len(data.get('sessions', [])) if isinstance(data, dict) else 1)
                print(f"[+] HTTP {status} OK | {url} | Items: {item_count}")
        except Exception as e:
            print(f"[-] ERROR fetching {url}: {e}")
            all_passed = False
            
    return all_passed

def verify_50_state_seo_entrypoints():
    print("\n=========================================================")
    print("📌 VERIFYING 50 US STATES SEO DIRECTORY ENTRYPOINTS")
    print("=========================================================")
    
    audit_files = [
        "/Users/silversurfer/Documents/Omniverse2/index.html",
        "/Users/silversurfer/Documents/Omniverse2/client_seo_audit_report.html"
    ]
    
    states = [
        "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia",
        "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland",
        "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
        "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
        "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
    ]
    
    all_seo_passed = True
    for file_path in audit_files:
        if not os.path.exists(file_path):
            print(f"[-] Missing file: {file_path}")
            all_seo_passed = False
            continue
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        found_states = [s for s in states if s in content]
        print(f"[+] {file_path}: Contains {len(found_states)}/50 US States verified.")
        if len(found_states) < 50:
            print(f"    [-] Missing states: {set(states) - set(found_states)}")
            all_seo_passed = False

    # Check 3,148 Route pages
    routes_dir = "/Users/silversurfer/Documents/Omniverse2/public_html_local/routes"
    if os.path.exists(routes_dir):
        route_files = [f for f in os.listdir(routes_dir) if f.endswith(".html")]
        print(f"[+] Project 1 (skyautoservices.com): {len(route_files)}/3,148 Programmatic Route Pages Verified.")
        if len(route_files) < 3148:
            all_seo_passed = False
    else:
        print("[-] Missing routes directory")
        all_seo_passed = False
            
    return all_seo_passed

if __name__ == "__main__":
    t_ok = verify_live_telemetry_endpoints()
    s_ok = verify_50_state_seo_entrypoints()
    if t_ok and s_ok:
        print("\n🎉 ALL VERIFICATION CHECKS PASSED PERFECTLY!")
        sys.exit(0)
    else:
        print("\n❌ VERIFICATION FAILED FOR SOME ITEMS.")
        sys.exit(1)
