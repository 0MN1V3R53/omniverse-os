#!/usr/bin/env python3
"""
slack_notifier.py
Sends SEO progress updates to a designated Slack Webhook.
"""

import os
import json
import logging
import requests
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

load_dotenv()

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def send_notification(phase, data):
    if not SLACK_WEBHOOK_URL:
        logging.warning("SLACK_WEBHOOK_URL not set. Skipping Slack notification.")
        return False
        
    message = f"*SEO Pipeline Update: {phase}*\n"
    if isinstance(data, dict):
        for k, v in data.items():
            message += f"• *{k}*: {v}\n"
    else:
        message += str(data)

    payload = {"text": message}
    
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=10)
        response.raise_for_status()
        logging.info("Slack notification sent successfully.")
        return True
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send Slack notification: {e}")
        return False

if __name__ == "__main__":
    send_notification("Test Phase", {"Status": "Active", "Coverage": "0%"})
