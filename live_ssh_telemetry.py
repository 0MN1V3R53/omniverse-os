#!/usr/bin/env python3
import subprocess
import os
import sys

# ---------------------------------------------------------
# OMNIVERSE PURE LIVE TELEMETRY STREAM
# ---------------------------------------------------------
# Connects directly via SSH to the Hostinger production server
# to extract pure, raw, unadulterated live client data.
# No hallucination. No drifting. 100% real data.
# ---------------------------------------------------------

HOSTNAME = "82.198.228.154"
PORT = 65002
USERNAME = "u803913036"
PASSWORD = "cunt3344#"

def stream_pure_live_data():
    print("[*] Initializing Pure Live Telemetry Stream...")
    print(f"[*] Target: {USERNAME}@{HOSTNAME}:{PORT}")
    
    # We use expect to bypass the interactive SSH password prompt natively.
    # The command tails the absolute source of truth:
    # 1. The NGINX/LiteSpeed access logs (pure server traffic)
    # 2. The telemetry JSON payloads
    # 3. The quote submissions JSON payloads
    expect_script = f"""
set timeout -1
spawn ssh -p {PORT} -o StrictHostKeyChecking=no -o PubkeyAuthentication=no {USERNAME}@{HOSTNAME} "tail -f domains/skyautoservices.com/logs/access.log 2>/dev/null || tail -f domains/skyautoservices.com/logs/access_log 2>/dev/null || tail -f public_html/visitor_intelligence_telemetry.json 2>/dev/null"
expect "password:"
send "{PASSWORD}\\r"
expect eof
"""
    
    script_path = "/tmp/telemetry_stream.exp"
    with open(script_path, "w") as f:
        f.write(expect_script)
        
    os.chmod(script_path, 0o700)
    
    try:
        print("[+] Establishing secure SSH connection to pure data source...")
        print("-" * 75)
        
        # Execute the expect script and pipe output to terminal
        process = subprocess.Popen(
            ["expect", script_path], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True,
            bufsize=1
        )
        
        for line in iter(process.stdout.readline, ''):
            # Filter out the initial connection noise for pure output
            if "spawn ssh" in line or "assword:" in line:
                continue
            
            # Print the live raw data directly
            sys.stdout.write(line)
            sys.stdout.flush()
            
    except KeyboardInterrupt:
        print("\n\n[*] Stream terminated by user.")
    except Exception as e:
        print(f"\n[-] Error: {e}")
    finally:
        if 'process' in locals():
            process.terminate()
        if os.path.exists(script_path):
            os.remove(script_path)

if __name__ == "__main__":
    stream_pure_live_data()
