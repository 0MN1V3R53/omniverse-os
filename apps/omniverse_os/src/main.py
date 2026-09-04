#!/usr/bin/env python3
"""
Omniverse OS - Kernel Service Runner Entrypoint
"""
import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from kernel.omniverse_os_daemon import run_server

if __name__ == "__main__":
    run_server(port=8998)
