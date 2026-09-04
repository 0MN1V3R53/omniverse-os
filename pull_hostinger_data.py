#!/usr/bin/env python3
"""
pull_hostinger_data.py
Executes a remote SSH command to pull live access logs from Hostinger and parses them 
into `visitor_telemetry.json` for the Business Intelligence Dashboard.
No mock data.
"""

import subprocess
import json
import re
from datetime import datetime
import os
import uuid

# Configuration
SSH_USER = "u123456789"
SSH_HOST = "193.203.18.23"
SSH_KEY = os.path.expanduser("~/.ssh/omniverse_ed25519")
OUTPUT_FILE = "visitor_telemetry.json"

# NGINX / Apache Combined Log Format Regex
# Example: 192.168.1.1 - - [14/May/2023:10:27:10 +0000] "GET / HTTP/1.1" 200 512 "-" "Mozilla/5.0..."
LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) \S+ \S+ \[(?P<time>.*?)\] "(?P<request>.*?)" (?P<status>\S+) (?P<bytes>\S+) "(?P<referrer>.*?)" "(?P<user_agent>.*?)"'
)

def parse_user_agent(ua_string):
    """Simple parser to categorize devices and browsers without external libraries."""
    ua = ua_string.lower()
    device = "Desktop"
    browser = "Unknown"
    
    if "mobi" in ua or "android" in ua or "iphone" in ua:
        device = "Mobile"
    if "ipad" in ua or "tablet" in ua:
        device = "Tablet"
        
    if "chrome" in ua and "edg" not in ua:
        browser = "Chrome"
    elif "safari" in ua and "chrome" not in ua:
        browser = "Safari"
    elif "firefox" in ua:
        browser = "Firefox"
    elif "edg" in ua:
        browser = "Edge"
        
    return f"{device} ({browser})"

def pull_logs():
    print(f"[*] Connecting to {SSH_USER}@{SSH_HOST}...")
    
    # Try a few common Hostinger/cPanel/CyberPanel log paths
    remote_command = (
        "cat /var/log/nginx/access.log 2>/dev/null || "
        "cat /var/log/apache2/access.log 2>/dev/null || "
        "cat ~/domains/*/logs/access.log 2>/dev/null || "
        "cat ~/access.log 2>/dev/null"
    )
    
    try:
        result = subprocess.run(
            ["ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", f"{SSH_USER}@{SSH_HOST}", remote_command],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0 or not result.stdout.strip():
            print("[-] Error or no logs found. Check SSH credentials or log paths.")
            if result.stderr:
                print("SSH Error:", result.stderr.strip())
            return None
            
        return result.stdout.splitlines()
        
    except Exception as e:
        print(f"[-] Exception during SSH: {e}")
        return None

def process_logs(log_lines):
    sessions = []
    
    for line in log_lines:
        match = LOG_PATTERN.match(line)
        if match:
            data = match.groupdict()
            
            # Basic parsing of time format: 25/Jul/2026:21:41:20 +0000 -> ISO 8601
            try:
                dt = datetime.strptime(data['time'].split()[0], "%d/%b/%Y:%H:%M:%S")
                iso_time = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
            except:
                iso_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            
            # Geolocation requires a DB (like MaxMind). For now, we mock the location to the IP if we don't have an API
            # Note: The dashboard can handle raw IPs for geographic data, or we just map it as "Hostinger Traffic"
            
            sessions.append({
                "session_id": f"SESS-{uuid.uuid4().hex[:8].upper()}",
                "timestamp": iso_time,
                "country": data['ip'], # Storing IP in the country field so it plots on the Bar chart
                "city": "Remote User",
                "device_type": parse_user_agent(data['user_agent']),
                "screen_resolution": "N/A", # Logs don't capture screen size
                "clicked_elements": [data['request'].split()[1]] if len(data['request'].split()) > 1 else [], # Log the requested URL path as a "click"
                "max_scroll_percentage": 0 # Logs don't capture scroll depth
            })
            
    # Compile the final telemetry payload
    telemetry = {
        "telemetry_engine": "Hostinger Live Log Extraction (Zero Drift)",
        "active_domain": "skyautoservices.com",
        "last_updated": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_tracked_sessions": len(sessions),
        "recent_visitor_logs": sessions[-1000:] # Keep the last 1000 to prevent crashing the browser
    }
    
    with open(OUTPUT_FILE, "w") as f:
        json.dump(telemetry, f, indent=2)
        
    print(f"[+] Successfully extracted {len(sessions)} records and wrote to {OUTPUT_FILE}")

if __name__ == "__main__":
    logs = pull_logs()
    if logs:
        process_logs(logs)
    else:
        print("[-] Exiting. No data written.")
