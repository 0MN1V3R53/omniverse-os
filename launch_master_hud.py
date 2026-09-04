import http.server
import socketserver
import os
import json
import threading

PORT = 8080
DIRECTORY = "/Users/silversurfer/Documents/Omniverse2"
LOCK = threading.Lock()

class TelemetryRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        path = self.path.split('?')[0]
        if path in ['/api/save_quote', '/api/save_quote.php']:
            quote_file = os.path.join(DIRECTORY, 'quote_submissions.json')
            data = []
            if os.path.exists(quote_file):
                try:
                    with open(quote_file, 'r') as f:
                        data = json.load(f)
                except Exception:
                    data = []
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode('utf-8'))
            return

        elif path in ['/api/save_call', '/api/save_call.php']:
            calls_file = os.path.join(DIRECTORY, 'call_requests.json')
            data = []
            if os.path.exists(calls_file):
                try:
                    with open(calls_file, 'r') as f:
                        data = json.load(f)
                except Exception:
                    data = []
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode('utf-8'))
            return

        elif path in ['/api/telemetry', '/api/visitor_intelligence.php']:
            tel_file = os.path.join(DIRECTORY, 'visitor_intelligence_telemetry.json')
            data = {}
            if os.path.exists(tel_file):
                try:
                    with open(tel_file, 'r') as f:
                        data = json.load(f)
                except Exception:
                    data = {}
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode('utf-8'))
            return


        elif path == '/api/seo_logs':
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
            self.send_header('Access-Control-Allow-Origin', '*')
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
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode('utf-8'))
            return

        super().do_GET()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            payload = json.loads(post_data.decode('utf-8'))
        except Exception:
            payload = {}

        path = self.path.split('?')[0]

        if path in ['/api/save_quote', '/api/save_quote.php']:
            with LOCK:
                quote_file = os.path.join(DIRECTORY, 'quote_submissions.json')
                existing = []
                if os.path.exists(quote_file):
                    try:
                        with open(quote_file, 'r') as f:
                            existing = json.load(f)
                    except Exception:
                        existing = []

                if not isinstance(existing, list):
                    existing = []

                payload['data_source_type'] = 'WEBSITE_DIRECT_INTAKE'
                payload['source_label'] = 'LIVE DATA'
                payload['is_live'] = True
                # Prepend new quote payload
                existing.insert(0, payload)
                
                with open(quote_file, 'w') as f:
                    json.dump(existing, f, indent=2)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True, 'quote_id': payload.get('submission_id', 'CONFIRMED')}).encode('utf-8'))
            return

        elif path in ['/api/save_call', '/api/save_call.php']:
            with LOCK:
                calls_file = os.path.join(DIRECTORY, 'call_requests.json')
                existing = []
                if os.path.exists(calls_file):
                    try:
                        with open(calls_file, 'r') as f:
                            existing = json.load(f)
                    except Exception:
                        existing = []

                if not isinstance(existing, list):
                    existing = []

                payload['data_source_type'] = 'WEBSITE_DIRECT_INTAKE'
                payload['is_live'] = True
                
                existing.insert(0, payload)
                with open(calls_file, 'w') as f:
                    json.dump(existing, f, indent=2)

                # Also update phone_call_clicks in visitor_intelligence_telemetry.json
                tel_file = os.path.join(DIRECTORY, 'visitor_intelligence_telemetry.json')
                tel_data = {}
                if os.path.exists(tel_file):
                    try:
                        with open(tel_file, 'r') as f:
                            tel_data = json.load(f)
                    except Exception:
                        tel_data = {}
                
                if 'phone_call_clicks' not in tel_data or not isinstance(tel_data['phone_call_clicks'], list):
                    tel_data['phone_call_clicks'] = []
                
                tel_data['phone_call_clicks'].insert(0, payload)
                tel_data['last_updated'] = payload.get('timestamp')
                
                with open(tel_file, 'w') as f:
                    json.dump(tel_data, f, indent=2)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True, 'call_id': payload.get('call_id', 'CALL-LOGGED')}).encode('utf-8'))
            return

        elif path in ['/api/telemetry', '/visitor_intelligence.php', '/api/visitor_intelligence.php']:
            with LOCK:
                tel_file = os.path.join(DIRECTORY, 'visitor_intelligence_telemetry.json')
                tel_data = {}
                if os.path.exists(tel_file):
                    try:
                        with open(tel_file, 'r') as f:
                            tel_data = json.load(f)
                    except Exception:
                        tel_data = {}
                
                if not isinstance(tel_data, dict):
                    tel_data = {}
                if 'sessions' not in tel_data or not isinstance(tel_data['sessions'], list):
                    tel_data['sessions'] = []
                
                tel_data['sessions'].insert(0, payload)
                tel_data['last_updated'] = payload.get('timestamp')
                tel_data['total_active_visitors'] = len(tel_data['sessions'])
                
                with open(tel_file, 'w') as f:
                    json.dump(tel_data, f, indent=2)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True, 'event': payload.get('event', 'telemetry_received')}).encode('utf-8'))
            return

        else:
            self.send_response(404)
            self.end_headers()

def run_server():
    os.chdir(DIRECTORY)
    from live_hostinger_sync import start_background_sync_loop
    from seo_30min_keyword_engine import start_30min_seo_engine
    start_background_sync_loop(interval=3)
    start_30min_seo_engine(interval_sec=1800)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), TelemetryRequestHandler) as httpd:
        print(f"⚡ MASTER OMNIVERSE HUD Server running at http://localhost:{PORT}/master_dashboard.html")
        print("⚡ API endpoints active: POST /api/save_quote, POST /api/save_call")
        print("⚡ Live Hostinger Production Telemetry Streaming: ACTIVE")
        print("⚡ 30-Minute Automated SEO Keyword Optimization Engine: ACTIVE & ONLINE")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()

