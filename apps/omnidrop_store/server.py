#!/usr/bin/env python3
"""
Omniverse E-Commerce Dropshipping Enterprise
Real-Time Transaction Ledger Server & Executive Command Hub (Port 8995)
Author: Dr. Alexander Vance & Julian Thorne
"""

import http.server
import socketserver
import json
import os
import sys
import time
from urllib.parse import urlparse

# Import rotator & payment config
from src.product_rotator_engine import ProductRotatorEngine
from src.payment_gateway_config import PaymentGatewayRouter

PORT = 8995
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UI_DIR = os.path.join(BASE_DIR, "ui")

rotator_engine = ProductRotatorEngine()
gateway_router = PaymentGatewayRouter()

class OmniDropStoreHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=UI_DIR, **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        
        # 1. Product Catalog API (20 Winning SKUs)
        if parsed.path == "/api/products":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(rotator_engine.get_catalog()).encode("utf-8"))
            return

        # 2. Real-Time Portfolio & Command Center Analytics API (From Real Ledger)
        elif parsed.path == "/api/analytics":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            status = rotator_engine.get_portfolio_status()
            status["gateway_info"] = gateway_router.get_gateway_blueprint()
            self.wfile.write(json.dumps(status).encode("utf-8"))
            return

        # 3. Status API
        elif parsed.path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ONLINE", "service": "OmniDrop D2C Storefront & Real Ledger Engine 1.0"}).encode("utf-8"))
            return

        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)

        # 1. Real Order Processing API
        if parsed.path == "/api/order/create":
            content_len = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_len).decode("utf-8")
            payload = json.loads(body) if body else {}

            product_id = payload.get("product_id", "luminaglow-pro")
            product_name = payload.get("product_name", "LuminaGlow™ Pro 4-in-1 Red Light Sculptor")
            price = float(payload.get("price", 49.95))
            customer_email = payload.get("email", "buyer@example.com")
            shipping_addr = payload.get("shipping_address", "742 Evergreen Terrace, Los Angeles, CA 90001")
            attribution = payload.get("attribution", {})

            # Record in Persistent Real Ledger
            order_record = rotator_engine.record_order({
                "product_id": product_id,
                "product_name": product_name,
                "total": price,
                "customer_email": customer_email,
                "shipping_address": shipping_addr,
                "attribution": attribution
            })

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "SUCCESS", "order": order_record}).encode("utf-8"))
            return

        # 2. Automated Product Rotator Evaluation API
        elif parsed.path == "/api/rotator/evaluate":
            res = rotator_engine.evaluate_and_prune()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode("utf-8"))
            return

        # 3. Rotator Toggle API
        elif parsed.path == "/api/rotator/toggle":
            content_len = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_len).decode("utf-8")
            payload = json.loads(body) if body else {}
            enabled = payload.get("enabled", True)
            res = rotator_engine.toggle_rotator(enabled)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()

def run_store_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), OmniDropStoreHandler) as httpd:
        print(f"=== [OMNIDROP REAL-TIME LEDGER SERVER ONLINE ON PORT {PORT}] ===")
        print(f"Storefront:     http://localhost:{PORT}/index.html")
        print(f"Command Center: http://localhost:{PORT}/dashboard.html")
        httpd.serve_forever()

if __name__ == "__main__":
    run_store_server()
