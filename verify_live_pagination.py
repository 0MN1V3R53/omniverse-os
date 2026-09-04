import json
import os

base_dir = "/Users/silversurfer/Documents/Omniverse2"
dashboard_path = os.path.join(base_dir, "cyberpunk_telemetry_live.html")
quotes_path = os.path.join(base_dir, "quote_submissions.json")

# 1. Verify quotes JSON dataset length
with open(quotes_path, "r", encoding="utf-8") as f:
    quotes = json.load(f)

assert len(quotes) >= 15
print(f"✓ Verified {len(quotes)} quote lead records in quote_submissions.json.")

# 2. Verify HTML elements & handlers
with open(dashboard_path, "r", encoding="utf-8") as f:
    html = f.read()

assert 'renderQuotesTab' in html
assert 'search-input' in html
assert 'btn-inspect' in html
assert 'inspectLead' in html

print("✓ Verified Cyberpunk Live Data Table, Search Filter, and Inspection Handlers in cyberpunk_telemetry_live.html.")
print("✓ Live Table Data and Lead Inspection system double-check complete!")
