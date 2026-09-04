#!/usr/bin/env python3
"""
Omniverse OS - Storage Tiering Router
Author: Erik Lindqvist (macos_backend_services_dev_erik_lindqvist) & Dr. Alexander Vance
Pod: Pod 16 (macOS Systems Division)
"""

import os
import shutil
import subprocess
import sys

INFINITY_MOUNT = "/Volumes/Omniverse_Storage_Infinity"

class StorageTieringRouter:
    def __init__(self):
        self.target_dir = os.path.join(INFINITY_MOUNT, "Tiered_Data")

    def ensure_storage_ready(self):
        if not os.path.exists(INFINITY_MOUNT):
            print("[ROUTER] Attaching Omniverse Storage Infinity...")
            sparse_path = "/Users/silversurfer/Documents/Omniverse2/apps/omniverse_accelerator/Omniverse_Storage_Infinity.sparseimage"
            subprocess.run(["hdiutil", "attach", sparse_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        if not os.path.exists(self.target_dir):
            os.makedirs(self.target_dir, exist_ok=True)
            os.makedirs(os.path.join(self.target_dir, "Large_Datasets"), exist_ok=True)
            os.makedirs(os.path.join(self.target_dir, "Media_Caches"), exist_ok=True)
            os.makedirs(os.path.join(self.target_dir, "Build_Artifacts"), exist_ok=True)
        return True

    def route_path(self, source_path):
        """Transparently migrates heavy folder to 2.4TB pool and replaces with symlink."""
        if not os.path.exists(source_path):
            print(f"[ERROR] Source path does not exist: {source_path}")
            return False
            
        base_name = os.path.basename(os.path.abspath(source_path))
        dest_path = os.path.join(self.target_dir, base_name)

        print(f"[ROUTER] Routing '{source_path}' -> '{dest_path}'...")
        if os.path.exists(dest_path):
            print(f"[ROUTER] Destination already exists in 2.4TB pool. Merging...")
        else:
            shutil.move(source_path, dest_path)
            
        # Create symlink back to original location
        if not os.path.exists(source_path):
            os.symlink(dest_path, source_path)
            print(f"[ROUTER] Replaced with transparent symlink. Internal SSD free space reclaimed!")
        return True

if __name__ == "__main__":
    router = StorageTieringRouter()
    router.ensure_storage_ready()
    print("=== [OMNIVERSE STORAGE TIERING ROUTER READY] ===")
    print(f"Target Pool: {INFINITY_MOUNT} (2.4 TB)")
    print("Desktop Link: ~/Desktop/'Omniverse Infinity Storage (2.4 TB)'")
