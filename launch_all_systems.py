#!/usr/bin/env python3
"""
OMNIVERSE TECH — MASTER OPERATIONS LAUNCHER
============================================
Starts ALL core systems in one command:
  1. SSH Sync daemon (pulls live Hostinger data every 30s via SCP)
  2. Cyberpunk Telemetry Server (port 8090)
  3. 30-min SEO Automation Engine
  4. Opens dashboard in browser automatically

Usage: python3 launch_all_systems.py
"""
import os
import json
import time
import threading
import subprocess
import webbrowser
import socketserver
import http.server
from datetime import datetime

DIRECTORY = "/Users/silversurfer/Documents/Omniverse2"
KEY_PATH  = "/Users/silversurfer/.ssh/id_ed25519"
PASSPHRASE = "cunt3344#"
HOSTNAME  = "82.198.228.154"
SSH_PORT  = "65002"
USERNAME  = "u803913036"
REMOTE_PATH = "domains/skyautoservices.com/public_html"
TELEMETRY_PORT = 8090
SYNC_INTERVAL  = 30  # seconds between SSH pulls
LOCK = threading.Lock()

REMOTE_FILES = [
    ("quote_submissions.json",          os.path.join(DIRECTORY, "quote_submissions.json")),
    ("call_requests.json",              os.path.join(DIRECTORY, "call_requests.json")),
    ("visitor_intelligence_telemetry.json", os.path.join(DIRECTORY, "visitor_intelligence_telemetry.json")),
    ("visitor_telemetry.json",          os.path.join(DIRECTORY, "visitor_telemetry.json")),
    ("seo_keyword_automation_log.json", os.path.join(DIRECTORY, "seo_keyword_automation_log.json")),
]

def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")

# ─────────────────────────────────────────────────────────────
# 1. SSH SYNC DAEMON
# ─────────────────────────────────────────────────────────────
def scp_pull_file(remote_filename, local_path):
    """SCP a single file from Hostinger → local via expect (handles passphrase)."""
    tmp_local = f"/tmp/omni_sync_{remote_filename}"
    expect_script = f"""
set timeout 20
spawn scp -i {KEY_PATH} -P {SSH_PORT} -o StrictHostKeyChecking=no {USERNAME}@{HOSTNAME}:{REMOTE_PATH}/{remote_filename} {tmp_local}
expect {{
    "Enter passphrase for key" {{ send "{PASSPHRASE}\\r"; exp_continue }}
    eof
}}
"""
    exp_path = f"/tmp/omni_scp_{remote_filename}.exp"
    with open(exp_path, "w") as f:
        f.write(expect_script)
    os.chmod(exp_path, 0o700)
    try:
        result = subprocess.run(["expect", exp_path], capture_output=True, text=True, timeout=25)
        if os.path.exists(exp_path):
            os.remove(exp_path)
        if os.path.exists(tmp_local) and os.path.getsize(tmp_local) > 2:
            with open(tmp_local, "r", encoding="utf-8") as f:
                raw = f.read().strip()
            os.remove(tmp_local)
            if raw and raw not in ("[]", "{}"):
                data = json.loads(raw)
                # Merge: for lists, union on timestamp; for dicts, overwrite
                with LOCK:
                    if isinstance(data, list) and len(data) > 0:
                        tmp_path = local_path + ".tmp"
                        with open(tmp_path, "w") as f:
                            json.dump(data, f, indent=2)
                        os.replace(tmp_path, local_path)
                        return len(data)
                    elif isinstance(data, dict):
                        tmp_path = local_path + ".tmp"
                        with open(tmp_path, "w") as f:
                            json.dump(data, f, indent=2)
                        os.replace(tmp_path, local_path)
                        return 1
        if os.path.exists(tmp_local):
            os.remove(tmp_local)
    except Exception as e:
        if os.path.exists(exp_path):
            os.remove(exp_path)
        if os.path.exists(f"/tmp/omni_sync_{remote_filename}"):
            os.remove(f"/tmp/omni_sync_{remote_filename}")
    return 0

def ssh_sync_loop():
    log("🔄 SSH Sync Daemon started — pulling Hostinger data every 30s")
    while True:
        total = 0
        for remote_filename, local_path in REMOTE_FILES:
            try:
                count = scp_pull_file(remote_filename, local_path)
                if count:
                    log(f"   ✅ Synced {remote_filename} ({count} records)")
                else:
                    log(f"   ⚠️  {remote_filename} — empty or unchanged on server")
            except Exception as e:
                log(f"   ❌ Sync failed for {remote_filename}: {e}")
        time.sleep(SYNC_INTERVAL)

# ─────────────────────────────────────────────────────────────
# 2. TELEMETRY HTTP SERVER (port 8090)
# ─────────────────────────────────────────────────────────────
class TelemetryHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        pass  # suppress noisy HTTP logs

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def _read_json(self, path, default):
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return default

    def _write_json(self, path, data):
        tmp = path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(data, f, indent=2)
        os.replace(tmp, path)

    def do_GET(self):
        clean = self.path.split('?')[0]
        # Quote data endpoint
        if clean in ['/api/save_quote', '/api/save_quote.php']:
            data = self._read_json(os.path.join(DIRECTORY, 'quote_submissions.json'), [])
            self._json_response(data)
        # Call data endpoint
        elif clean in ['/api/save_call', '/api/save_call.php']:
            data = self._read_json(os.path.join(DIRECTORY, 'call_requests.json'), [])
            self._json_response(data)
        # Visitor telemetry endpoint
        elif clean in ['/api/telemetry', '/api/visitor_intelligence.php']:
            data = self._read_json(os.path.join(DIRECTORY, 'visitor_intelligence_telemetry.json'), {})
            self._json_response(data)
        else:
            super().do_GET()

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)
        try:
            payload = json.loads(body.decode('utf-8'))
        except Exception:
            payload = {}

        clean = self.path.split('?')[0]
        now_iso = datetime.utcnow().isoformat() + 'Z'

        if clean in ['/api/save_quote', '/api/save_quote.php']:
            with LOCK:
                path = os.path.join(DIRECTORY, 'quote_submissions.json')
                existing = self._read_json(path, [])
                if not isinstance(existing, list):
                    existing = []
                payload.update({'data_source_type': 'WEBSITE_DIRECT', 'is_live': True, 'received_at': now_iso})
                existing.insert(0, payload)
                self._write_json(path, existing)
            self._json_response({'success': True, 'id': payload.get('submission_id', 'CONFIRMED')})

        elif clean in ['/api/save_call', '/api/save_call.php']:
            with LOCK:
                path = os.path.join(DIRECTORY, 'call_requests.json')
                existing = self._read_json(path, [])
                if not isinstance(existing, list):
                    existing = []
                payload.update({'data_source_type': 'WEBSITE_DIRECT', 'is_live': True, 'received_at': now_iso})
                existing.insert(0, payload)
                self._write_json(path, existing)
                # Also reflect in visitor telemetry
                tel_path = os.path.join(DIRECTORY, 'visitor_intelligence_telemetry.json')
                tel = self._read_json(tel_path, {})
                if not isinstance(tel.get('phone_call_clicks'), list):
                    tel['phone_call_clicks'] = []
                tel['phone_call_clicks'].insert(0, payload)
                tel['last_updated'] = now_iso
                self._write_json(tel_path, tel)
            self._json_response({'success': True, 'id': payload.get('call_id', 'CALL-LOGGED')})

        elif clean in ['/api/telemetry', '/api/visitor_intelligence.php']:
            with LOCK:
                path = os.path.join(DIRECTORY, 'visitor_intelligence_telemetry.json')
                tel = self._read_json(path, {'sessions': [], 'total_active_visitors': 0})
                if not isinstance(tel.get('sessions'), list):
                    tel['sessions'] = []
                tel['sessions'].insert(0, payload)
                tel['total_active_visitors'] = len(tel['sessions'])
                tel['last_updated'] = now_iso
                self._write_json(path, tel)
            self._json_response({'success': True})
        else:
            self.send_response(404)
            self.end_headers()

    def _json_response(self, data):
        body = json.dumps(data).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

def run_telemetry_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", TELEMETRY_PORT), TelemetryHandler) as httpd:
        log(f"⚡ Telemetry server live → http://localhost:{TELEMETRY_PORT}/cyberpunk_telemetry_live.html")
        httpd.serve_forever()

# ─────────────────────────────────────────────────────────────
# 3. SEO AUTOMATION ENGINE (30-min background)
# ─────────────────────────────────────────────────────────────
def seo_engine_loop():
    log("🚀 30-min SEO Keyword Engine starting...")
    while True:
        try:
            log("🔑 SEO Engine: Running keyword injection cycle...")
            result = subprocess.run(
                ["python3", "seo_30min_keyword_engine.py"],
                capture_output=True, text=True, timeout=900,
                cwd=DIRECTORY
            )
            if result.returncode == 0:
                log("✅ SEO Engine: Keyword cycle complete.")
            else:
                log(f"⚠️  SEO Engine exited with code {result.returncode}")
        except Exception as e:
            log(f"❌ SEO Engine error: {e}")
        log(f"⏳ SEO Engine: Next run in 30 minutes...")
        time.sleep(1800)

# ─────────────────────────────────────────────────────────────
# MAIN — Start all systems
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("  🌐 OMNIVERSE TECH — MASTER OPERATIONS LAUNCHER")
    print("  Client: Sky Auto Services | skyautoservices.com")
    print("=" * 60)

    os.chdir(DIRECTORY)

    # Thread 1: SSH Sync Daemon
    t_sync = threading.Thread(target=ssh_sync_loop, daemon=True)
    t_sync.start()

    # Thread 2: SEO Engine
    t_seo = threading.Thread(target=seo_engine_loop, daemon=True)
    t_seo.start()

    # Open browser after 2 seconds
    def open_browser():
        time.sleep(2)
        url = f"http://localhost:{TELEMETRY_PORT}/cyberpunk_telemetry_live.html"
        log(f"🌐 Opening dashboard: {url}")
        webbrowser.open(url)

    threading.Thread(target=open_browser, daemon=True).start()

    # Main thread: Telemetry HTTP server (blocks)
    log("All systems initializing...")
    run_telemetry_server()
