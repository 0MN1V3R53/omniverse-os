#!/usr/bin/env python3
"""
Omniverse OS - Real-Time Latency Eradicator & WindowServer QoS Governor
Author: Dr. Evelyn Cross (macos_kernel_trace_latency_sre) & Dr. Kai Sterling
Pod: Pod 16 (macOS Systems Division)
"""

import os
import subprocess
import time
import sys

def elevate_windowserver():
    try:
        out = subprocess.check_output(["pgrep", "-x", "WindowServer"], text=True).strip()
        if out:
            pid = int(out.split()[0])
            # Set high priority on WindowServer to guarantee 60fps compositor smoothness
            subprocess.run(["renice", "-n", "-10", "-p", str(pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return pid
    except Exception:
        pass
    return None

def compact_inactive_memory():
    try:
        subprocess.run(["purge"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=2)
    except Exception:
        pass

def run_latency_governor():
    ws_pid = elevate_windowserver()
    print(f"[OMNIVERSE LATENCY GOVERNOR] Active. WindowServer PID: {ws_pid} pinned to High Priority.")
    
    # Run loop
    cycles = 0
    while True:
        try:
            elevate_windowserver()
            cycles += 1
            if cycles % 30 == 0:  # Every 60 seconds
                compact_inactive_memory()
            time.sleep(2)
        except KeyboardInterrupt:
            break
        except Exception:
            time.sleep(5)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        pid = elevate_windowserver()
        compact_inactive_memory()
        print(f"Latency pass completed for WindowServer ({pid}).")
    else:
        run_latency_governor()
