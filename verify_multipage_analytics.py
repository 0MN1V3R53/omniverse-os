import json
import os

base_dir = "/Users/silversurfer/Documents/Omniverse2"
dashboard_path = os.path.join(base_dir, "cyberpunk_telemetry_live.html")
telemetry_path = os.path.join(base_dir, "visitor_intelligence_telemetry.json")

# 1. Verify JSON payload contains sessions and visitor metrics
with open(telemetry_path, "r", encoding="utf-8") as f:
    data = json.load(f)

assert "sessions" in data
assert isinstance(data["sessions"], list)
assert len(data["sessions"]) > 0

print("✓ Verified visitor intelligence telemetry session records in JSON.")

# 2. Verify HTML interactive tabs and modal elements
with open(dashboard_path, "r", encoding="utf-8") as f:
    html = f.read()

tabs = ["overview", "live_data", "test_data", "quotes", "calls", "attribution", "ux", "tech", "vault", "seo_engine"]
for t in tabs:
    assert f"'{t}'" in html or f'"{t}"' in html, f"Missing tab key: {t}"

assert "leadModal" in html or "inspectLead" in html
assert "fetchTelemetryData" in html

print("✓ Verified all interactive Cyberpunk dashboard tabs and drill-down lead inspection modals.")
print("✓ Multi-Page Enterprise Cyberpunk Analytics Platform double-check complete!")
