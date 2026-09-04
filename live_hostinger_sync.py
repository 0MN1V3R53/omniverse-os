#!/usr/bin/env python3
import os
import json
import time
import subprocess
import urllib.request
import threading

DIRECTORY = "/Users/silversurfer/Documents/Omniverse2"
LOCK = threading.Lock()

KEY_PATH = "/Users/silversurfer/.ssh/id_ed25519"
PASSPHRASE = "cunt3344#"
HOSTNAME = "82.198.228.154"
PORT = "65002"
USERNAME = "u803913036"

# Endpoints
REMOTE_BASE_URL = "https://skyautoservices.com"

def fetch_json_https(endpoint):
    url = f"{REMOTE_BASE_URL}/{endpoint}?t={int(time.time() * 1000)}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Omniverse-Telemetry-Client/3.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                return data
    except Exception as e:
        print(f"[-] HTTPS fetch error for {url}: {e}")
    return None

def fetch_file_ssh(remote_filename):
    local_tmp = f"/tmp/remote_sync_{remote_filename}"
    expect_script = f"""
set timeout 15
spawn scp -i {KEY_PATH} -P {PORT} -o StrictHostKeyChecking=no {USERNAME}@{HOSTNAME}:domains/skyautoservices.com/public_html/{remote_filename} {local_tmp}
expect {{
    "Enter passphrase for key" {{ send "{PASSPHRASE}\\r"; exp_continue }}
    eof
}}
"""
    script_path = f"/tmp/scp_{remote_filename}.exp"
    with open(script_path, "w") as f:
        f.write(expect_script)
    os.chmod(script_path, 0o700)
    
    try:
        res = subprocess.run(["expect", script_path], capture_output=True, text=True, timeout=18)
        if os.path.exists(script_path):
            os.remove(script_path)
            
        if os.path.exists(local_tmp):
            with open(local_tmp, "r", encoding="utf-8") as f:
                data = json.load(f)
            os.remove(local_tmp)
            return data
    except Exception as e:
        if os.path.exists(script_path):
            os.remove(script_path)
        if os.path.exists(local_tmp):
            os.remove(local_tmp)
    return None

def atomic_json_write(filepath, data):
    tmp_path = filepath + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp_path, filepath)

def sync_hostinger_data_once():
    # Sync quote_submissions.json
    quotes = fetch_json_https("quote_submissions.json") or fetch_file_ssh("quote_submissions.json")
    if quotes and isinstance(quotes, list) and len(quotes) > 0:
        with LOCK:
            local_path = os.path.join(DIRECTORY, "quote_submissions.json")
            atomic_json_write(local_path, quotes)

    # Sync call_requests.json
    calls = fetch_json_https("call_requests.json") or fetch_file_ssh("call_requests.json")
    if calls and isinstance(calls, list) and len(calls) > 0:
        with LOCK:
            local_path = os.path.join(DIRECTORY, "call_requests.json")
            atomic_json_write(local_path, calls)

    # Sync visitor_intelligence_telemetry.json
    visitor = fetch_json_https("visitor_intelligence_telemetry.json") or fetch_file_ssh("visitor_intelligence_telemetry.json")
    if visitor and isinstance(visitor, dict) and len(visitor.get("sessions", [])) > 0:
        with LOCK:
            local_path = os.path.join(DIRECTORY, "visitor_intelligence_telemetry.json")
            atomic_json_write(local_path, visitor)

    # Sync seo_keyword_automation_log.json
    seo_log = fetch_json_https("seo_keyword_automation_log.json") or fetch_file_ssh("seo_keyword_automation_log.json")
    if seo_log and isinstance(seo_log, dict) and len(seo_log.get("logs", [])) >= 0:
        with LOCK:
            local_path = os.path.join(DIRECTORY, "seo_keyword_automation_log.json")
            atomic_json_write(local_path, seo_log)

def start_background_sync_loop(interval=3):
    def loop():
        while True:
            try:
                sync_hostinger_data_once()
            except Exception as e:
                print(f"[-] Sync loop error: {e}")
            time.sleep(interval)
            
    t = threading.Thread(target=loop, daemon=True)
    t.start()
    print("⚡ Background Hostinger Live Telemetry Sync Thread active (3-second poll loop).")

if __name__ == "__main__":
    print("[*] Running manual one-time Hostinger live sync test...")
    sync_hostinger_data_once()
    print("[+] Sync test complete.")
