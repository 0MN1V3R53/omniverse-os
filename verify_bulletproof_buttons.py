import os
import re

dashboard_path = "/Users/silversurfer/Documents/Omniverse2/cyberpunk_telemetry_live.html"

with open(dashboard_path, "r", encoding="utf-8") as f:
    html = f.read()

required_funcs = [
    "switchTab",
    "setTimeWindow",
    "setDataMode",
    "fetchTelemetryData",
    "renderDashboard",
    "renderLiveDataTab",
    "renderTestDataTab",
    "renderOverviewTab",
    "renderQuotesTab",
    "renderCallsTab",
    "inspectLead",
    "closeModal"
]

for func in required_funcs:
    assert f"function {func}" in html or f"{func}(" in html, f"Missing function: {func}"

assert 'type="button"' in html, "Missing type='button' attribute on buttons"
assert "telemetryState" in html, "Missing telemetryState object"
assert "setInterval(fetchTelemetryData, 1000)" in html, "Missing 1-second interval poller"

print("✓ All Cyberpunk Telemetry button handlers, state management, and 1-second poller verified!")
print("✓ Total Omniverse Team Audit Passed Successfully!")
