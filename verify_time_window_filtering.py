#!/usr/bin/env python3
import json
import os
from datetime import datetime

WINDOW_MS = {
    '5h': 5 * 3600,
    '10h': 10 * 3600,
    '24h': 24 * 3600,
    '2d': 2 * 86400,
    '3d': 3 * 86400,
    '4d': 4 * 86400,
    '5d': 5 * 86400,
    '10d': 10 * 86400,
    '20d': 20 * 86400,
    '30d': 30 * 86400,
    'all': float('inf')
}

DIRECTORY = "/Users/silversurfer/Documents/Omniverse2"

def parse_ts(ts_str):
    if not ts_str: return None
    ts_str = str(ts_str).replace("Z", "").split("+")[0].split(".")[0]
    try:
        return datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%S")
    except Exception:
        return None

def safe_read_json(filepath, default):
    if not os.path.exists(filepath): return default
    for _ in range(3):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            time.sleep(0.1)
    return default

quotes = safe_read_json(os.path.join(DIRECTORY, "quote_submissions.json"), [])
calls = safe_read_json(os.path.join(DIRECTORY, "call_requests.json"), [])
visitor = safe_read_json(os.path.join(DIRECTORY, "visitor_intelligence_telemetry.json"), {})
sessions = visitor.get('sessions', []) if isinstance(visitor, dict) else []

now = datetime.utcnow()

print("=========================================================================")
print("⚡ VERIFYING TIME WINDOW FILTER DYNAMIC RECALCULATION ENGINE")
print("=========================================================================")

for window_key, allowed_sec in WINDOW_MS.items():
    q_count = 0
    c_count = 0
    v_count = 0

    for q in quotes:
        dt = parse_ts(q.get('timestamp') or q.get('received_at'))
        if dt and (window_key == 'all' or (now - dt).total_seconds() <= allowed_sec):
            q_count += 1

    for c in calls:
        dt = parse_ts(c.get('timestamp') or c.get('received_at'))
        if dt and (window_key == 'all' or (now - dt).total_seconds() <= allowed_sec):
            c_count += 1

    for s in sessions:
        dt = parse_ts(s.get('timestamp'))
        if dt and (window_key == 'all' or (now - dt).total_seconds() <= allowed_sec):
            v_count += 1

    print(f"[+] Time Window '{window_key.upper()}': {q_count} Quotes | {c_count} Call Leads | {v_count} Visitors")

print("=========================================================================")
