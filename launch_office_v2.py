import http.server
import socketserver
import webbrowser
import threading
import json
import os
import time
from urllib.parse import urlparse, parse_qs

PORT = 8092
DIRECTORY = "/Users/silversurfer/Documents/Omniverse2/public_html_local"
SPOOL_FILE = os.path.join(DIRECTORY, "assets", "data", "chat_spool.json")

def init_spool():
    if not os.path.exists(SPOOL_FILE):
        os.makedirs(os.path.dirname(SPOOL_FILE), exist_ok=True)
        with open(SPOOL_FILE, 'w') as f:
            json.dump([], f)

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
        
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/api/chat':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            with open(SPOOL_FILE, 'r') as f:
                data = f.read()
            self.wfile.write(data.encode('utf-8'))
        else:
            super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == '/api/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            msg = json.loads(post_data.decode('utf-8'))
            
            with open(SPOOL_FILE, 'r') as f:
                spool = json.load(f)
                
            spool.append({
                "role": "user",
                "text": msg.get("text", "")
            })
            
            with open(SPOOL_FILE, 'w') as f:
                json.dump(spool, f, indent=4)
                
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def start_server():
    init_spool()
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    time.sleep(1)
    webbrowser.open(f'http://localhost:{PORT}/omniverse_office.html')
    
    print("Office interface launched in browser.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
