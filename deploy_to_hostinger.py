#!/usr/bin/env python3
import os
import subprocess
import sys

HOSTNAME = "82.198.228.154"
PORT = 65002
USERNAME = "u803913036"
KEY_PATH = "/Users/silversurfer/.ssh/id_ed25519"
PASSPHRASE = "cunt3344#"

print("[*] Deploying updated code to Hostinger (preserving live JSON data files)...")

expect_script = f"""
set timeout 300
spawn ssh -i {KEY_PATH} -p {PORT} -o StrictHostKeyChecking=no {USERNAME}@{HOSTNAME} "rm -rf domains/skyautoservices.com/public_html/_next public_html/_next"
expect {{
    "Enter passphrase for key" {{ send "{PASSPHRASE}\\r"; exp_continue }}
    eof
}}

spawn rsync -avz --exclude='.DS_Store' -e "ssh -p {PORT} -i {KEY_PATH} -o StrictHostKeyChecking=no" public_html_local/ {USERNAME}@{HOSTNAME}:domains/skyautoservices.com/public_html/
expect {{
    "Enter passphrase for key" {{ send "{PASSPHRASE}\\r"; exp_continue }}
    eof
}}

spawn rsync -avz --exclude='.DS_Store' -e "ssh -p {PORT} -i {KEY_PATH} -o StrictHostKeyChecking=no" public_html_local/ {USERNAME}@{HOSTNAME}:public_html/
expect {{
    "Enter passphrase for key" {{ send "{PASSPHRASE}\\r"; exp_continue }}
    eof
}}

spawn ssh -i {KEY_PATH} -p {PORT} -o StrictHostKeyChecking=no {USERNAME}@{HOSTNAME} "cd domains/skyautoservices.com/public_html && touch .litespeed_purge && rm -f .litespeed_purge && cd ~/public_html && touch .litespeed_purge && rm -f .litespeed_purge"
expect {{
    "Enter passphrase for key" {{ send "{PASSPHRASE}\\r"; exp_continue }}
    eof
}}
"""

script_path = "deploy_hostinger.exp"
with open(script_path, "w") as f:
    f.write(expect_script)
os.chmod(script_path, 0o700)

res = subprocess.run(["expect", script_path])
if os.path.exists(script_path):
    os.remove(script_path)

if res.returncode == 0:
    print("[+] Code deployment to Hostinger complete (Live data files preserved)!")
else:
    print(f"[-] Deployment failed with code {res.returncode}")
    sys.exit(res.returncode)
