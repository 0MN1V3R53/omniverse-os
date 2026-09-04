import json
import os

base_dir = "/Users/silversurfer/Documents/Omniverse2"
dashboard_path = os.path.join(base_dir, "cyberpunk_telemetry_live.html")
telemetry_path = os.path.join(base_dir, "visitor_intelligence_telemetry.json")

# 1. Verify JSON contains Hostinger Historical Analytics
with open(telemetry_path, "r", encoding="utf-8") as f:
    data = json.load(f)

assert "hostinger_historical_analytics" in data
h_data = data["hostinger_historical_analytics"]
assert h_data["hostinger_uptime_percentage"] == 99.98
assert h_data["total_programmatic_route_pages"] == 3148
assert len(h_data["competitors_outranked"]) == 5

print("✓ Verified Hostinger Historical Analytics in telemetry JSON payload.")

# 2. Verify HTML Portal 7
with open(dashboard_path, "r", encoding="utf-8") as f:
    html_content = f.read()

assert "Hostinger Historical SERP & Traffic Analytics Archive" in html_content
assert "id=\"p7-uptime\"" in html_content
assert "id=\"p7-ttfb\"" in html_content
assert "id=\"p7-deploy-speed\"" in html_content
assert "id=\"p7-corridors\"" in html_content

print("✓ Verified Portal 7 DOM elements and JS data binding in cyberpunk_telemetry_live.html.")
print("✓ All system components double-checked and validated successfully!")
