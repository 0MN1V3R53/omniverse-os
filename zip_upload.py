import os
import subprocess

PASSWORD = "cunt3344#"
KEY_PATH = "/Users/silversurfer/.ssh/id_ed25519"
PORT = "65002"
USER = "u803913036"
HOST = "82.198.228.154"
REMOTE_DIR = "domains/skyautoservices.com/public_html"
ZIP_FILE = "public_html_upload.zip"

print("1. Zipping public_html_local (this may take a minute due to massive scale files)...")
if os.path.exists(ZIP_FILE):
    os.remove(ZIP_FILE)
subprocess.run("cd public_html_local && zip -rq ../public_html_upload.zip .", shell=True)

print("2. Uploading zip via SCP...")
expect_scp = f"""
set timeout -1
spawn scp -i {KEY_PATH} -P {PORT} -o StrictHostKeyChecking=no {ZIP_FILE} {USER}@{HOST}:{REMOTE_DIR}/{ZIP_FILE}
expect {{
    "Enter passphrase for key" {{ send "{PASSWORD}\\r"; exp_continue }}
    eof
}}
"""
with open("scp.exp", "w") as f:
    f.write(expect_scp)
subprocess.run("expect scp.exp", shell=True)
os.remove("scp.exp")

print("3. Extracting zip on server via SSH...")
expect_ssh = f"""
set timeout -1
spawn ssh -i {KEY_PATH} -p {PORT} -o StrictHostKeyChecking=no {USER}@{HOST}
expect {{
    "Enter passphrase for key" {{ send "{PASSWORD}\\r"; exp_continue }}
    "u803913036" {{ send "cd {REMOTE_DIR} && unzip -qo {ZIP_FILE} && rm {ZIP_FILE}\\r" }}
    "$ " {{ send "cd {REMOTE_DIR} && unzip -qo {ZIP_FILE} && rm {ZIP_FILE}\\r" }}
}}
expect {{
    "u803913036" {{ send "exit\\r" }}
    "$ " {{ send "exit\\r" }}
}}
expect eof
"""
with open("ssh.exp", "w") as f:
    f.write(expect_ssh)
subprocess.run("expect ssh.exp", shell=True)
os.remove("ssh.exp")

print("Deployment complete!")
