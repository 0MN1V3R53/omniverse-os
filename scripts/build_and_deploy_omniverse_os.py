#!/usr/bin/env python3
"""
================================================================================
OMNIVERSE OS - NATIVE MACOS APPLICATION BUILDER, PACKAGER & LAUNCHER
================================================================================
Compiles, packages, and deploys 'Omniverse OS.app' to /Applications and ~/Desktop,
rebuilds the bootable macOS DMG, and launches the native physical GUI window.
================================================================================
"""

import os
import sys
import shutil
import subprocess
import time

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
APP_SRC_DIR = os.path.join(REPO_ROOT, "apps", "omniverse_os")
DIST_DIR = os.path.join(REPO_ROOT, "dist")
DMG_STAGING = os.path.join(DIST_DIR, "dmg_staging")
DMG_OUTPUT = os.path.join(DIST_DIR, "Omniverse_Leviathan_2026_VM.dmg")
APPLICATIONS_DIR = "/Applications"
DESKTOP_DIR = os.path.expanduser("~/Desktop")

BUNDLE_NAME = "Omniverse OS.app"
SYS_APP_PATH = os.path.join(APPLICATIONS_DIR, BUNDLE_NAME)
DESKTOP_APP_PATH = os.path.join(DESKTOP_DIR, BUNDLE_NAME)

def compile_swift_binary():
    swift_src = os.path.join(APP_SRC_DIR, "src", "OmniverseOS.swift")
    binary_out = os.path.join(APP_SRC_DIR, "src", "OmniverseOS")
    
    print(f"[*] Compiling native Swift Mach-O binary from {swift_src}...")
    cmd = [
        "/usr/bin/swiftc",
        "-O",
        swift_src,
        "-o", binary_out,
        "-framework", "Cocoa",
        "-framework", "WebKit"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[-] Compilation error:\n{res.stderr}")
        sys.exit(1)
    print(f"[+] Swift binary compiled successfully: {binary_out}")
    return binary_out

def assemble_bundle(dest_path: str, binary_path: str):
    print(f"[*] Assembling macOS Application Bundle at: {dest_path}...")
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)

    contents = os.path.join(dest_path, "Contents")
    macos_dir = os.path.join(contents, "MacOS")
    res_dir = os.path.join(contents, "Resources")
    os.makedirs(macos_dir, exist_ok=True)
    os.makedirs(res_dir, exist_ok=True)

    # 1. Copy Mach-O executable
    target_exec = os.path.join(macos_dir, "OmniverseOS")
    shutil.copy2(binary_path, target_exec)
    os.chmod(target_exec, 0o755)

    # 2. Info.plist
    plist = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>en</string>
    <key>CFBundleExecutable</key>
    <string>OmniverseOS</string>
    <key>CFBundleIdentifier</key>
    <string>com.omniverse.os.workstation</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>Omniverse OS</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>12.0</string>
    <key>CFBundleVersion</key>
    <string>2026.9995</string>
    <key>LSMinimumSystemVersion</key>
    <string>12.0</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
"""
    with open(os.path.join(contents, "Info.plist"), "w") as f:
        f.write(plist)

    # 3. Copy Resources (kernel, ui, src, tools)
    shutil.copytree(os.path.join(APP_SRC_DIR, "kernel"), os.path.join(res_dir, "kernel"))
    shutil.copytree(os.path.join(APP_SRC_DIR, "ui"), os.path.join(res_dir, "ui"))
    os.makedirs(os.path.join(res_dir, "src"), exist_ok=True)
    shutil.copy2(os.path.join(APP_SRC_DIR, "src", "main.py"), os.path.join(res_dir, "src", "main.py"))

    # Also include simulator
    sim_src = os.path.join(REPO_ROOT, ".agents", "tools", "hardware_2026_flagship_simulator.py")
    os.makedirs(os.path.join(res_dir, ".agents", "tools"), exist_ok=True)
    shutil.copy2(sim_src, os.path.join(res_dir, ".agents", "tools", "hardware_2026_flagship_simulator.py"))

    print(f"[+] Bundle assembled: {dest_path}")

def start_kernel_daemon():
    print(f"[*] Checking if Omniverse OS Kernel Daemon is running on port 8998...")
    import urllib.request
    try:
        with urllib.request.urlopen("http://127.0.0.1:8998/api/status", timeout=0.8) as resp:
            if resp.status == 200:
                print(f"[+] Kernel daemon is already active and healthy.")
                return
    except Exception:
        pass

    print(f"[*] Starting Omniverse OS Kernel Daemon in background...")
    daemon_script = os.path.join(APP_SRC_DIR, "src", "main.py")
    subprocess.Popen(
        [sys.executable, daemon_script],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        cwd=REPO_ROOT,
        start_new_session=True
    )
    # Wait for daemon to bind
    for _ in range(20):
        time.sleep(0.2)
        try:
            with urllib.request.urlopen("http://127.0.0.1:8998/api/status", timeout=0.8) as resp:
                if resp.status == 200:
                    print(f"[+] Kernel daemon successfully started on http://127.0.0.1:8998.")
                    return
        except Exception:
            pass
    print("[!] Warning: Daemon did not respond within timeout, proceeding with launch.")

def rebuild_dmg(binary_path: str):
    print(f"[*] Rebuilding master macOS DMG archive with Omniverse OS.app...")
    if os.path.exists(DMG_STAGING):
        shutil.rmtree(DMG_STAGING)
    os.makedirs(DMG_STAGING, exist_ok=True)

    # 1. Assemble Omniverse OS.app in staging
    staging_app = os.path.join(DMG_STAGING, BUNDLE_NAME)
    assemble_bundle(staging_app, binary_path)

    # 2. Add 1-click launcher command
    cmd_file = os.path.join(DMG_STAGING, "Launch_Omniverse_OS.command")
    with open(cmd_file, "w") as f:
        f.write("""#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
open "$DIR/Omniverse OS.app"
""")
    os.chmod(cmd_file, 0o755)

    # 3. Add Hardware Specs
    specs_src = os.path.join(REPO_ROOT, "scripts", "HARDWARE_SPECIFICATIONS_2026.txt")
    if not os.path.exists(specs_src):
        specs_src = os.path.join(DIST_DIR, "dmg_staging", "HARDWARE_SPECIFICATIONS_2026.txt")
    if os.path.exists(specs_src):
        shutil.copy2(specs_src, os.path.join(DMG_STAGING, "HARDWARE_SPECIFICATIONS_2026.txt"))

    # 4. Add Applications symlink
    app_link = os.path.join(DMG_STAGING, "Applications")
    if os.path.exists(app_link) or os.path.islink(app_link):
        os.unlink(app_link)
    os.symlink("/Applications", app_link)

    # 5. Create DMG
    # Detach previous if mounted
    subprocess.run(["/usr/bin/hdiutil", "detach", "/Volumes/Omniverse 2026 Flagship VM"], capture_output=True)
    if os.path.exists(DMG_OUTPUT):
        os.remove(DMG_OUTPUT)

    cmd = [
        "/usr/bin/hdiutil", "create",
        "-volname", "Omniverse 2026 Flagship VM",
        "-srcfolder", DMG_STAGING,
        "-ov",
        "-format", "UDZO",
        DMG_OUTPUT
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[-] DMG build error:\n{res.stderr}")
    else:
        print(f"[+] Master DMG successfully built: {DMG_OUTPUT}")
        # Copy to Desktop and Home
        shutil.copy2(DMG_OUTPUT, os.path.join(DESKTOP_DIR, "Omniverse_Leviathan_2026_VM.dmg"))
        shutil.copy2(DMG_OUTPUT, os.path.expanduser("~/Omniverse_Leviathan_2026_VM.dmg"))
        print(f"[+] DMG deployed to ~/Desktop/Omniverse_Leviathan_2026_VM.dmg")

def launch_physical_window():
    print(f"[*] Launching Omniverse OS native desktop window on macOS...")
    res = subprocess.run(["/usr/bin/open", "-a", SYS_APP_PATH], capture_output=True, text=True)
    if res.returncode == 0:
        print(f"[+] PHYSICAL WINDOW OPENED SUCCESSFULLY!")
    else:
        print(f"[-] Launch warning: {res.stderr}. Attempting direct binary execution...")
        subprocess.Popen([os.path.join(SYS_APP_PATH, "Contents", "MacOS", "OmniverseOS")])
        print(f"[+] Direct binary process spawned.")

def main():
    print("=" * 80)
    print("  BUILDING & DEPLOYING OMNIVERSE OS (WINDOWS REWRITTEN - SUBSTRATE VM)")
    print("=" * 80)

    binary = compile_swift_binary()
    assemble_bundle(SYS_APP_PATH, binary)
    assemble_bundle(DESKTOP_APP_PATH, binary)
    start_kernel_daemon()
    rebuild_dmg(binary)
    launch_physical_window()

    print("=" * 80)
    print("OMNIVERSE OS DEPLOYMENT COMPLETE!")
    print(f"Application: {SYS_APP_PATH}")
    print(f"Desktop:     {DESKTOP_APP_PATH}")
    print(f"DMG Archive: {DMG_OUTPUT}")
    print("=" * 80)

if __name__ == "__main__":
    main()
