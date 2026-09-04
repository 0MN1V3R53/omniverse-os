import json
import os
import datetime

base_dir = "/Users/silversurfer/Documents/Omniverse2"
quote_file = os.path.join(base_dir, "quote_submissions.json")
telemetry_file = os.path.join(base_dir, "visitor_telemetry.json")

# 1. Simulate Quote Submission
new_quote = {
    "submission_id": f"QUOTE-{datetime.datetime.now().strftime('%Y%m%d')}-003",
    "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "customer_name": "Alexander Vance Test Client",
    "email": "dr.vance.test@skyautoservices.com",
    "phone": "+1 (555) 999-0000",
    "origin_city_state": "Seattle, WA (98101)",
    "destination_city_state": "Miami, FL (33101)",
    "vehicle_info": "2026 Tesla Cyberbeast (Enclosed Transport)",
    "deposit_terms": "$0 Upfront Deposit Guaranteed",
    "ip_address": "198.51.100.42",
    "country_geolocation": "United States (US)",
    "status": "RECORDED_IN_BACKGROUND"
}

with open(quote_file, "r+", encoding="utf-8") as f:
    quotes = json.load(f)
    quotes.append(new_quote)
    f.seek(0)
    json.dump(quotes, f, indent=2)

print(f"Successfully recorded quote: {new_quote['submission_id']}")
print(f"Total quotes recorded in background: {len(quotes)}")

# 2. Verify Visitor Telemetry Data
with open(telemetry_file, "r", encoding="utf-8") as f:
    telemetry = json.load(f)

print(f"Telemetry Engine: {telemetry['telemetry_engine']}")
print(f"Total tracked sessions: {telemetry['total_tracked_sessions']}")
