#!/usr/bin/env python3
"""
Omniverse OS - macOS Hardware Accelerator & System Studio Daemon (Port 8990)
Author: Charlotte Duval & Viktor Vance
Pod: Pod 16 (macOS Systems Division)
"""

import http.server
import socketserver
import json
import os
import sys
from urllib.parse import urlparse

from kernel_governor import KernelGovernor

PORT = 8990
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UI_DIR = os.path.join(BASE_DIR, "ui")

governor = KernelGovernor()

class HardwareAcceleratorHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=UI_DIR, **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)

        # 1. Real Hardware Telemetry API
        if parsed.path == "/api/telemetry":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            data = governor.get_hardware_telemetry()
            self.wfile.write(json.dumps(data).encode("utf-8"))
            return

        # 2. Real Process Manager API
        elif parsed.path == "/api/processes":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            procs = governor.get_top_processes(15)
            self.wfile.write(json.dumps(procs).encode("utf-8"))
            return

        # 3. Status Check API
        elif parsed.path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ONLINE", "service": "Omniverse OS Hardware Governor Pro 2.0"}).encode("utf-8"))
            return

        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        content_len = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_len).decode("utf-8")
        payload = json.loads(body) if body else {}

        # 1. Purge Mach Memory
        if parsed.path == "/api/system/purge-memory":
            res = governor.purge_memory()
            self._send_json(res)
            return

        # 2. Flush DNS
        elif parsed.path == "/api/system/flush-dns":
            res = governor.flush_dns()
            self._send_json(res)
            return

        # 3. Clean Caches
        elif parsed.path == "/api/system/clean-caches":
            res = governor.clean_caches()
            self._send_json(res)
            return

        # 4. Kill Process
        elif parsed.path == "/api/system/kill-process":
            pid = int(payload.get("pid", 0))
            res = governor.kill_process(pid)
            self._send_json(res)
            return

        # 5. Toggle Governor
        elif parsed.path == "/api/system/toggle-governor":
            key = payload.get("key")
            val = payload.get("val")
            res = governor.toggle_governor(key, val)
            self._send_json(res)
            return

        self.send_response(404)
        self.end_headers()

    def _send_json(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

def run_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), HardwareAcceleratorHandler) as httpd:
        print(f"=== [OMNIVERSE OS HARDWARE ACCELERATOR PRO DAEMON ONLINE ON PORT {PORT}] ===")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
