import json
import os
import datetime

base_dir = "/Users/silversurfer/Documents/Omniverse2"
intel_file = os.path.join(base_dir, "visitor_intelligence_telemetry.json")

# Simulate a new Google Organic Mobile Visitor Session
new_forensic_log = {
    "session_id": f"VIS-INTEL-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-TEST",
    "timestamp_start": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "landing_page_url": "https://www.skyautoservices.com/?utm_source=google&utm_medium=cpc&utm_campaign=brand_exact",
    "incoming_referrer_url": "https://www.google.com/",
    "acquisition_channel": "Google Paid Search Ads",
    "utm_parameters": {
      "utm_source": "google",
      "utm_medium": "cpc",
      "utm_campaign": "brand_exact",
      "utm_content": "shield_logo_headline",
      "utm_term": "sky_auto_services_quote"
    },
    "browser_software": {
      "user_agent": "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36",
      "browser_name": "Google Chrome Mobile 126",
      "rendering_engine": "Blink (V8)",
      "language": "en-US",
      "languages_preferred": ["en-US"],
      "cookies_enabled": True,
      "do_not_track": "0",
      "platform": "Linux armv8l"
    },
    "hardware_device": {
      "device_type": "Mobile",
      "os_name": "Android 14 (Pixel 8 Pro)",
      "screen_resolution": "412x915",
      "viewport_dimensions": "412x890",
      "color_depth_bits": 32,
      "cpu_cores": 8,
      "device_memory_gb": 12,
      "max_touch_points": 10
    },
    "network_geolocation": {
      "client_ip": "198.51.100.124",
      "country": "United States (US)",
      "city": "Chicago",
      "region": "Illinois (IL)",
      "network_type": "Verizon 5G UW",
      "latency_ms": 18
    },
    "interaction_traversal": {
      "max_scroll_percentage": 100,
      "clicks": [
        { "target_element": "#instant-quote-btn", "text_content": "Get Free Quote", "timestamp_rel_ms": 1500 },
        { "target_element": "INPUT#vehicle-model", "text_content": "Cyberbeast", "timestamp_rel_ms": 6200 }
      ],
      "mouse_trail_samples": [
        { "x": 200, "y": 300, "t_rel_ms": 400 },
        { "x": 210, "y": 750, "t_rel_ms": 1900 }
      ]
    },
    "session_metrics": {
      "total_duration_seconds": 185,
      "active_time_seconds": 172,
      "status": "COMPLETED"
    }
}

with open(intel_file, "r+", encoding="utf-8") as f:
    data = json.load(f)
    if "sessions" not in data:
        data["sessions"] = []
    data["sessions"].append(new_forensic_log)
    data["total_tracked_sessions"] = len(data["sessions"])
    data["last_updated"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    f.seek(0)
    json.dump(data, f, indent=2)

print("Forensic Visitor Intelligence Logging Test Passed!")
print(f"Total Forensic Visitor Records Logged: {data['total_tracked_sessions']}")
print(f"Latest Recorded Session: {new_forensic_log['session_id']}")
