#!/usr/bin/env python3
"""
MACOS LOCAL SSL DEVELOPMENT SETUP SCRIPT
Omniverse Tech - Web & Infrastructure Division

Automates local SSL/TLS certificate generation and macOS trust store integration
for HTTPS local development (Next.js, Node.js, Python, NGINX).
"""

import os
import sys
import subprocess
import shutil
import json
from pathlib import Path

# Color output helpers
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
BOLD = "\033[1m"
RESET = "\033[0m"

WORKSPACE_DIR = Path("/Users/silversurfer/Documents/Omniverse2")
SSL_DIR = WORKSPACE_DIR / "ssl"
SKY_NEXT_DIR = WORKSPACE_DIR / "sky_next"


def log(msg, level="info"):
    if level == "success":
        print(f"{GREEN}✓ {msg}{RESET}")
    elif level == "warn":
        print(f"{YELLOW}⚠️ {msg}{RESET}")
    elif level == "error":
        print(f"{RED}✖ {msg}{RESET}")
    elif level == "header":
        print(f"\n{BOLD}{BLUE}=== {msg} ==={RESET}")
    else:
        print(f"  {msg}")


def run_cmd(cmd, check=True, capture=True):
    try:
        res = subprocess.run(
            cmd,
            shell=True,
            check=check,
            stdout=subprocess.PIPE if capture else None,
            stderr=subprocess.PIPE if capture else None,
            text=True
        )
        return res
    except subprocess.CalledProcessError as e:
        if capture:
            log(f"Command failed: {cmd}\nError: {e.stderr}", level="error")
        raise e


def check_prerequisites():
    log("Checking Prerequisites", level="header")

    # Check OpenSSL
    openssl_path = shutil.which("openssl")
    if openssl_path:
        log(f"OpenSSL found at: {openssl_path}", level="success")
    else:
        log("OpenSSL not found in PATH!", level="error")
        sys.exit(1)

    # Check mkcert (optional)
    mkcert_path = shutil.which("mkcert")
    if mkcert_path:
        log(f"mkcert found at: {mkcert_path}", level="success")
        return "mkcert"
    else:
        log("mkcert not installed (will use native macOS OpenSSL + Security CLI)", level="warn")
        return "openssl"


def generate_ssl_with_mkcert():
    log("Generating Certificates using mkcert", level="header")
    run_cmd("mkcert -install", check=False, capture=False)

    domains = "localhost 127.0.0.1 ::1 skyautoservices.local *.localhost"
    cert_path = SSL_DIR / "localhost.crt"
    key_path = SSL_DIR / "localhost.key"

    cmd = f"mkcert -cert-file '{cert_path}' -key-file '{key_path}' {domains}"
    run_cmd(cmd, capture=False)
    log(f"Certificates generated in {SSL_DIR}", level="success")


def generate_ssl_with_openssl():
    log("Generating Local CA & Certificates using OpenSSL", level="header")

    ca_key = SSL_DIR / "rootCA.key"
    ca_crt = SSL_DIR / "rootCA.pem"
    server_key = SSL_DIR / "localhost.key"
    server_csr = SSL_DIR / "localhost.csr"
    server_crt = SSL_DIR / "localhost.crt"
    ext_file = SSL_DIR / "localhost.ext"

    # 1. Create Root CA Key & Certificate
    if not ca_key.exists() or not ca_crt.exists():
        log("Generating Local Development Root CA...")
        run_cmd(
            f"openssl req -x509 -nodes -new -sha256 -days 3650 "
            f"-newkey rsa:2048 "
            f"-keyout '{ca_key}' -out '{ca_crt}' "
            f"-subj '/C=US/ST=State/L=City/O=Omniverse Dev CA/CN=Omniverse Local Root CA'"
        )
        log("Created Local Root CA certificate", level="success")

    # 2. OpenSSL SAN Extension Config File
    ext_content = """authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = localhost
DNS.2 = *.localhost
DNS.3 = skyautoservices.local
DNS.4 = *.skyautoservices.local
IP.1 = 127.0.0.1
IP.2 = ::1
"""
    with open(ext_file, "w") as f:
        f.write(ext_content)

    # 3. Generate Server Private Key
    log("Generating Server Private Key (RSA 2048)...")
    run_cmd(f"openssl genrsa -out '{server_key}' 2048")

    # 4. Generate Certificate Signing Request (CSR)
    log("Generating Certificate Signing Request (CSR)...")
    run_cmd(
        f"openssl req -new -key '{server_key}' -out '{server_csr}' "
        f"-subj '/C=US/ST=State/L=City/O=Sky Auto Services Local/CN=localhost'"
    )

    # 5. Sign the Certificate with Root CA
    log("Signing Server Certificate with Local Root CA...")
    run_cmd(
        f"openssl x509 -req -in '{server_csr}' "
        f"-CA '{ca_crt}' -CAkey '{ca_key}' -CAcreateserial "
        f"-out '{server_crt}' -days 825 -sha256 -extfile '{ext_file}'"
    )

    log(f"Generated SSL Key:  {server_key}", level="success")
    log(f"Generated SSL Cert: {server_crt}", level="success")

    # 6. Offer to add Root CA to macOS Keychain
    trust_macos_keychain(ca_crt)


def trust_macos_keychain(ca_crt_path):
    log("macOS Keychain Trust Integration", level="header")
    log("To eliminate browser 'Not Secure' warnings in Chrome/Safari, the Root CA must be trusted.")

    login_keychain = Path.home() / "Library/Keychains/login.keychain-db"

    # Command to add to user keychain
    cmd_user = f"security add-trusted-cert -d -r trustRoot -k '{login_keychain}' '{ca_crt_path}'"

    log("Adding Root CA to User Login Keychain...")
    res = run_cmd(cmd_user, check=False)
    if res.returncode == 0:
        log("Root CA successfully trusted in macOS Login Keychain!", level="success")
    else:
        log("User Keychain trust command executed (or already trusted).", level="info")


def configure_nextjs():
    log("Configuring Next.js for HTTPS Development", level="header")

    package_json_path = SKY_NEXT_DIR / "package.json"
    if package_json_path.exists():
        with open(package_json_path, "r") as f:
            data = json.load(f)

        scripts = data.get("scripts", {})
        key_rel = "../ssl/localhost.key"
        crt_rel = "../ssl/localhost.crt"

        scripts["dev:https"] = f"next dev --experimental-https --experimental-https-key {key_rel} --experimental-https-cert {crt_rel}"
        data["scripts"] = scripts

        with open(package_json_path, "w") as f:
            json.dump(data, f, indent=2)

        log("Updated sky_next/package.json with 'npm run dev:https' script!", level="success")


def print_usage_guide():
    log("Local SSL Setup Complete!", level="header")
    print(f"""
{BOLD}Certificates Location:{RESET}
  📁 {SSL_DIR}/
     ├── localhost.key  (Private Key)
     ├── localhost.crt  (Signed Certificate)
     └── rootCA.pem     (Local Root CA)

{BOLD}How to Run Local HTTPS Servers:{RESET}

1. {BOLD}Next.js App (sky_next):{RESET}
   $ cd sky_next
   $ npm run dev:https
   👉 Open {BLUE}https://localhost:3000{RESET} or {BLUE}https://skyautoservices.local:3000{RESET}

2. {BOLD}Python HTTPS Server:{RESET}
   $ python3 -m http.server 8443 --bind 127.0.0.1 --directory public_html_local \\
       --ssl-keyfile ssl/localhost.key --ssl-certfile ssl/localhost.crt

3. {BOLD}Node.js / Express HTTPS Server:{RESET}
   const https = require('https');
   const fs = require('fs');
   const options = {{
     key: fs.readFileSync('./ssl/localhost.key'),
     cert: fs.readFileSync('./ssl/localhost.crt')
   }};
   https.createServer(options, app).listen(443);
""")


def main():
    log("Starting Local SSL Development Environment Setup for macOS", level="header")
    SSL_DIR.mkdir(parents=True, exist_ok=True)

    tool = check_prerequisites()

    if tool == "mkcert":
        generate_ssl_with_mkcert()
    else:
        generate_ssl_with_openssl()

    configure_nextjs()
    print_usage_guide()


if __name__ == "__main__":
    main()
