#!/usr/bin/env python3
"""
================================================================================
OMNIVERSE OS - KERNEL DAEMON & REST/WEBSOCKET DISPATCHER
================================================================================
Bridges the Omniverse OS kernel, HAL, VMM, DirectStorage, and WDDM subsystems
to the graphical desktop user interface and external diagnostic clients.

Listens on: http://127.0.0.1:8998
================================================================================
"""

import os
import sys
import json
import time
import mimetypes
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from typing import Dict, Any

# Ensure parent path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
UI_DIR = os.path.join(APP_DIR, "ui")

from .omniverse_hal import GLOBAL_HAL
from .omniverse_nt_kernel import GLOBAL_KERNEL
from .omniverse_vmm import GLOBAL_VMM
from .omniverse_storport import GLOBAL_STORAGE
from .omniverse_wddm import GLOBAL_WDDM

PORT = 8998

class OmniverseOSRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress routine GET logging to avoid console clutter
        return

    def _send_json(self, data: Any, status: int = 200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/status":
            self._send_json({
                "status": "ONLINE",
                "os": "Omniverse OS",
                "kernel_build": "12.0.2026.9995-Sovereign",
                "hardware": "AMD Threadripper PRO 9995WX + WRX90 + RTX 5090",
                "timestamp": time.time()
            })
            return

        elif path == "/api/system/specs":
            specs = GLOBAL_HAL.query_hardware_tree()
            self._send_json(specs)
            return

        elif path == "/api/system/telemetry":
            telemetry = GLOBAL_KERNEL.get_system_telemetry()
            self._send_json(telemetry)
            return

        elif path == "/api/processes":
            procs = GLOBAL_KERNEL.get_process_list()
            self._send_json({"processes": procs, "count": len(procs)})
            return

        elif path == "/api/memory/vmm":
            vmm_data = GLOBAL_VMM.query_memory_state()
            self._send_json(vmm_data)
            return

        elif path == "/api/storage/directstorage":
            storage_data = GLOBAL_STORAGE.query_storage_status()
            self._send_json(storage_data)
            return

        elif path == "/api/gpu/wddm":
            wddm_data = GLOBAL_WDDM.query_gpu_status()
            self._send_json(wddm_data)
            return

        # Serve Static UI Files
        if path == "/" or path == "":
            rel_file = "index.html"
        else:
            rel_file = path.lstrip("/")

        file_path = os.path.join(UI_DIR, rel_file)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            content_type, _ = mimetypes.guess_type(file_path)
            content_type = content_type or "application/octet-stream"
            try:
                with open(file_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(content)))
                self.send_header("Cache-Control", "no-cache")
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                self.send_error(500, f"Error reading file: {e}")
        else:
            self.send_error(404, f"File not found: {path}")

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        content_len = int(self.headers.get("Content-Length", 0))
        post_body = self.rfile.read(content_len).decode("utf-8") if content_len > 0 else "{}"
        try:
            payload = json.loads(post_body) if post_body else {}
        except Exception:
            payload = {}

        if path == "/api/benchmark/run":
            test_type = payload.get("test", "all").lower()
            if test_type == "cpu":
                res = GLOBAL_HAL.dispatch_avx512_workload(matrix_size=payload.get("matrix_size", 1024))
            elif test_type == "ram":
                res = GLOBAL_HAL.dispatch_stream_memcpy(data_size_gb=payload.get("data_size_gb", 64.0))
            elif test_type == "storage":
                res = GLOBAL_HAL.dispatch_nvme_io_burst(block_size_kb=1024, count_blocks=20000)
            elif test_type == "gpu":
                res = GLOBAL_HAL.dispatch_blackwell_inference(model_params_b=payload.get("model_params_b", 70.0))
            else:
                res = GLOBAL_HAL.execute_full_diagnostic()
            self._send_json(res)
            return

        elif path == "/api/terminal/execute":
            cmd = payload.get("command", "")
            res = GLOBAL_KERNEL.execute_terminal_command(cmd)
            self._send_json(res)
            return

        elif path == "/api/memory/trim":
            res = GLOBAL_KERNEL.execute_terminal_command("Clear-Memory")
            self._send_json(res)
            return

        else:
            self.send_error(404, "Unknown API endpoint")

def run_server(port: int = PORT):
    server = HTTPServer(("127.0.0.1", port), OmniverseOSRequestHandler)
    print(f"================================================================================")
    print(f"  OMNIVERSE OS KERNEL DAEMON ONLINE ON http://127.0.0.1:{port}")
    print(f"  Kernel: Omniverse NT 12.0 (Build 2026.9995)")
    print(f"  Substrate: AMD Threadripper PRO 9995WX | ASUS WRX90 | DDR5-6400 | RTX 5090")
    print(f"================================================================================")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Shutting down Omniverse OS kernel daemon...")
        server.server_close()

if __name__ == "__main__":
    run_server()
