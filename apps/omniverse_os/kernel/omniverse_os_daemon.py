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

        elif path == "/api/audio/status":
            self._send_json({
                "subsystem": "OMNIVERSE_HIGH_DEFINITION_AUDIO_ENGINE",
                "hardware_controller": "Realtek ALC4080 + ESS SABRE 9018Q2C DAC (ASUS WRX90 SAGE)",
                "sample_rate_hz": 384000,
                "bit_depth": "32-bit Floating Point",
                "channels": "7.1 Surround + Direct Spatial Audio",
                "active_codecs": [
                    {"codec": "PCM_32BIT_FLOAT", "latency_ms": 0.4, "status": "HARDWARE_NATIVE"},
                    {"codec": "FLAC_LOSSLESS_24BIT_192KHZ", "latency_ms": 0.8, "status": "ACTIVE"},
                    {"codec": "OPUS_1_4_LOW_LATENCY", "latency_ms": 1.2, "status": "ACTIVE"},
                    {"codec": "AAC_LC_SURROUND", "latency_ms": 1.8, "status": "ACTIVE"},
                    {"codec": "DOLBY_ATMOS_SPATIAL_DSP", "latency_ms": 1.5, "status": "HARDWARE_OFFLOAD"}
                ],
                "master_volume_pct": 85,
                "mute": False,
                "signal_to_noise_ratio_db": 120.0
            })
            return

        elif path == "/api/apps/catalog":
            self._send_json({
                "catalog": [
                    {"id": "vscode", "name": "Visual Studio Code", "version": "1.93.0", "category": "Development", "size_mb": 115, "installed": True, "description": "High-performance code editor optimized for Zen 5 192-thread compilation."},
                    {"id": "pytorch", "name": "PyTorch 2.5 + CUDA 13", "version": "2.5.0-cu13", "category": "AI / ML", "size_mb": 2450, "installed": True, "description": "Native Blackwell RTX 5090 FP8/FP4 acceleration runtime."},
                    {"id": "blender", "name": "Blender 4.2 LTS", "version": "4.2.1", "category": "Graphics / 3D", "size_mb": 340, "installed": False, "description": "Cycles GPU OptiX ray tracing on 170 RT Cores."},
                    {"id": "wireshark", "name": "Wireshark 4.4", "version": "4.4.0", "category": "Networking", "size_mb": 85, "installed": False, "description": "10GbE line-rate packet analysis on Intel X710-AT2."},
                    {"id": "rust", "name": "Rust Toolchain 1.82", "version": "1.82.0", "category": "Development", "size_mb": 420, "installed": True, "description": "Zero-cost abstractions with AVX-512 target flags."},
                    {"id": "vlc", "name": "VLC Media Player Pro", "version": "3.0.21", "category": "Media", "size_mb": 75, "installed": False, "description": "Hardware AV1/HEVC 8K decoding on Blackwell NVDEC."}
                ]
            })
            return

        elif path == "/api/browser/proxy":
            query = parse_qs(parsed.query)
            target_url = query.get("url", ["https://example.com"])[0]
            if not target_url.startswith("http://") and not target_url.startswith("https://"):
                target_url = "https://" + target_url

            import urllib.request
            try:
                req = urllib.request.Request(
                    target_url,
                    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Omniverse/12.0 Chromium/128.0.6613.120"}
                )
                with urllib.request.urlopen(req, timeout=5.0) as resp:
                    html = resp.read().decode("utf-8", errors="ignore")
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(html.encode("utf-8"))
                    return
            except Exception as e:
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(f"""<!DOCTYPE html><html><body style="font-family:sans-serif;background:#0d1322;color:#fff;padding:40px;">
                    <h2>Omniverse Chromium Engine</h2>
                    <p style="color:#94a3b8;">Unable to connect directly to <code>{target_url}</code>: {e}</p>
                    <p>Enter a public HTTPS URL in the address bar above to browse.</p>
                </body></html>""".encode("utf-8"))
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

        elif path == "/api/apps/install":
            app_id = payload.get("id", "")
            app_name = payload.get("name", "Unknown Software")
            # Register new process in kernel
            pid = 3000 + (len(GLOBAL_KERNEL.processes) * 10)
            GLOBAL_KERNEL.processes[pid] = sys.modules["apps.omniverse_os.kernel.omniverse_nt_kernel"].KernelProcess(
                pid=pid,
                name=f"{app_id}.exe",
                threads_count=16,
                ram_mb=512.0,
                is_system=False
            )
            self._send_json({
                "status": "SOFTWARE_INSTALLED_SUCCESS",
                "app_id": app_id,
                "app_name": app_name,
                "pid_allocated": pid,
                "executable_path": f"C:\\Program Files\\Omniverse\\{app_id}\\{app_id}.exe"
            })
            return

        elif path == "/api/audio/configure":
            vol = payload.get("volume", 85)
            mute = payload.get("mute", False)
            self._send_json({
                "status": "AUDIO_CONFIGURED",
                "master_volume": vol,
                "mute_state": mute,
                "dac_clock": "384 kHz Ultra-Precision Locked"
            })
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
