import http.server
import socketserver
import webbrowser
import threading
import os
import time

PORT = 8092
DIRECTORY = "/Users/silversurfer/Documents/Omniverse2/public_html_local"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def start_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    time.sleep(1)
    webbrowser.open(f'http://localhost:{PORT}/omniverse_office.html')
    
    print("Office simulation launched in browser.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
