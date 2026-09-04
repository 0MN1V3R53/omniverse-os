#!/usr/bin/env python3
"""
CYBERPUNK SEO DASHBOARD LAUNCHER
Omniverse Tech - Web Development, SEO & Growth Division

Launches the Cyberpunk 50-State Live Audit & SERP Inspector Console as a local HTTP server on port 8080.
Exposes endpoints for fetching physical JSON log data.
"""

import http.server
import socketserver
import os
import json
import threading
import webbrowser
import time
import logging

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("CyberpunkLauncher")

PORT = 8080
DIRECTORY = "/Users/silversurfer/Documents/Omniverse2"

class SEODashboardHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def do_GET(self):
        path = self.path.split('?')[0]
        
        if path == '/api/seo_logs':
            log_file = os.path.join(DIRECTORY, 'seo_keyword_automation_log.json')
            data = []
            if os.path.exists(log_file):
                try:
                    with open(log_file, 'r') as f:
                        data = json.load(f)
                except Exception:
                    data = []
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode('utf-8'))
            return

        elif path == '/api/seo_audit_results':
            results_file = os.path.join(DIRECTORY, 'seo_audit_results.json')
            data = []
            if os.path.exists(results_file):
                try:
                    with open(results_file, 'r') as f:
                        data = json.load(f)
                except Exception:
                    data = []
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode('utf-8'))
            return

        super().do_GET()

def start_server():
    os.chdir(DIRECTORY)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), SEODashboardHandler) as httpd:
        logger.info(f"⚡ Cyberpunk SEO Dashboard Server running at http://localhost:{PORT}/cyberpunk_seo_dashboard.html")
        httpd.serve_forever()

def main():
    logger.info("=== LAUNCHING CYBERPUNK 50-STATE SEO HUD DASHBOARD ===")
    
    t_server = threading.Thread(target=start_server, daemon=True)
    t_server.start()
    time.sleep(1)
    
    # Do not auto-open here, as open_both_htmls_in_browser.py handles it
    logger.info("✓ SEO Server initialized on port 8080.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("\nShutting down SEO server...")

if __name__ == "__main__":
    main()
