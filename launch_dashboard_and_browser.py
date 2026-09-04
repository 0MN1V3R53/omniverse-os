import os
import webbrowser
import threading
import time
import subprocess
import socketserver
from launch_cyberpunk_telemetry_live import TelemetryRequestHandler, PORT, DIRECTORY

def start_server():
    os.chdir(DIRECTORY)
    from live_hostinger_sync import start_background_sync_loop
    start_background_sync_loop(interval=3)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), TelemetryRequestHandler) as httpd:
        print(f"⚡ Cyberpunk Live Telemetry Stream Server running at http://localhost:{PORT}/cyberpunk_telemetry_live.html")
        print("⚡ Live Pixel Intake API active: POST /api/save_quote, POST /api/save_call")
        print("⚡ Live Hostinger Production Telemetry Streaming: ACTIVE")
        httpd.serve_forever()

if __name__ == "__main__":
    print("[*] Launching Pure Live Telemetry Console & Real-Time Pixel Ingestion Engine...")
    
    # Start HTTP server in background thread
    t_server = threading.Thread(target=start_server, daemon=True)
    t_server.start()
    time.sleep(1)
    
    url = f"http://localhost:{PORT}/cyberpunk_telemetry_live.html"
    print(f"🚀 Launching Telemetry Dashboard in Default Browser: {url}")
    webbrowser.open(url)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down telemetry engine and server...")

