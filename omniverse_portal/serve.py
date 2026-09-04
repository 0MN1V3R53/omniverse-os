#!/usr/bin/env python3
import http.server
import socketserver
import os
import sys

PORT = 3333
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
        
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

def run_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"==================================================")
        print(f"  OMNIVERSE TECH FLAGSHIP PORTAL RUNNING LOCALLY  ")
        print(f"  Localhost URL: http://localhost:{PORT}")
        print(f"  Directory: {DIRECTORY}")
        print(f"==================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer shutting down gracefully.")
            httpd.server_close()

if __name__ == "__main__":
    run_server()
