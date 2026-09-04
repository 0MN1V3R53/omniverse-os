#!/usr/bin/env python3
"""
OPERATION: SSH-FILE-SYNC
Python SSH/SFTP deployment script for uploading local files.
IMPORTANT: Do not commit actual IP addresses or passwords. 
Variables have been replaced with placeholders.
"""

import os
import paramiko
import re
import time
from dotenv import load_dotenv

load_dotenv()

# Placeholder configuration - modify these in your local .env or hardcode safely
HOST = os.getenv("HOSTINGER_HOST", "YOUR_SERVER_IP")
PORT = int(os.getenv("HOSTINGER_PORT", "65002"))
USER = os.getenv("HOSTINGER_USER", "YOUR_USERNAME")
PASSWORD = os.getenv("HOSTINGER_PASSWORD", None)
REMOTE_ROOT = "public_html"
LOCAL_ROOT = "public_html_local"

def inject_cache_busters(local_dir):
    version = str(int(time.time()))
    print(f"Injecting cache buster v={version} into HTML files...")
    
    for root, dirs, files in os.walk(local_dir):
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Add ?v=version to static assets
                content = re.sub(r'(href|src)="([^"]+\.(css|js|png|jpg|jpeg|svg|webp))"', r'\1="\2?v=' + version + r'"', content)
                
                # Add no-cache meta tags if not already there
                if '<meta http-equiv="Cache-Control"' not in content:
                    meta_tags = '<meta http-equiv="Cache-Control" content="no-store, no-cache, must-revalidate, max-age=0"><meta http-equiv="Pragma" content="no-cache"><meta http-equiv="Expires" content="0">'
                    content = content.replace('</head>', f'{meta_tags}</head>')
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)


def sync_local_to_remote(sftp, local_dir, remote_dir):
    for item in os.listdir(local_dir):
        local_path = os.path.join(local_dir, item)
        remote_path = f"{remote_dir}/{item}"
        
        if os.path.isdir(local_path):
            try:
                sftp.mkdir(remote_path)
            except IOError:
                pass # Directory likely already exists
            sync_local_to_remote(sftp, local_path, remote_path)
        else:
            print(f"Uploading {local_path} -> {remote_path}")
            sftp.put(local_path, remote_path)

def main():
    print(f"Connecting to {HOST}:{PORT}...")
    
    # Using paramiko to connect via SSH key (assuming ~/.ssh/id_ed25519 is loaded in ssh-agent)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        if PASSWORD:
            ssh.connect(hostname=HOST, port=PORT, username=USER, password=PASSWORD, look_for_keys=True)
        else:
            ssh.connect(hostname=HOST, port=PORT, username=USER, look_for_keys=True)
        sftp = ssh.open_sftp()
        
        print("Starting upload...")
        inject_cache_busters(LOCAL_ROOT)
        sync_local_to_remote(sftp, LOCAL_ROOT, REMOTE_ROOT)
        
        sftp.close()
        ssh.close()
        print("Upload completed successfully.")
        
    except Exception as e:
        print(f"Deployment failed: {e}")

if __name__ == "__main__":
    main()
