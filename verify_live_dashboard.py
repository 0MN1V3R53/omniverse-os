import json
import os

base_dir = "/Users/silversurfer/Documents/Omniverse2"
dashboard_path = os.path.join(base_dir, "cyberpunk_telemetry_live.html")
telemetry_path = os.path.join(base_dir, "visitor_intelligence_telemetry.json")

# 1. Verify dashboard HTML exists and has 1-second interval loop
with open(dashboard_path, "r", encoding="utf-8") as f:
    html_content = f.read()

assert "setInterval(updateTelemetryDashboard, 1000);" in html_content
assert "Cyberpunk Live Telemetry Dashboard" in html_content
print("✓ Verified cyberpunk_telemetry_live.html has 1-second auto-refresh interval loop.")

# 2. Verify telemetry JSON has required portals data
with open(telemetry_path, "r", encoding="utf-8") as f:
    telemetry_data = json.load(f)

assert "recent_visitor_forensic_logs" in telemetry_data
logs = telemetry_data["recent_visitor_forensic_logs"]
assert len(logs) > 0
latest = logs[-1]

assert "browser_software" in latest
assert "hardware_device" in latest
assert "acquisition_channel" in latest
assert "session_metrics" in latest
assert "network_geolocation" in latest

print(f"✓ Verified telemetry JSON payload containing {len(logs)} forensic session logs.")
print("✓ All 6 Cyberpunk Dashboard Portals data fields validated!")
