#!/usr/bin/env python3
"""
Omniverse OS - Native macOS Application Bundle & DMG Packaging Engine
Compiles Native Swift AppKit Cocoa Window & Builds DMG Installer
Author: Marcus Chen & Viktor Vance
"""

import os
import subprocess
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")
APP_NAME = "Omniverse OS Accelerator"
APP_BUNDLE = os.path.join(BASE_DIR, f"{APP_NAME}.app")
DMG_OUTPUT = os.path.join(BASE_DIR, "Omniverse_OS_Accelerator.dmg")
ROOT_DMG_OUTPUT = "/Users/silversurfer/Documents/Omniverse2/Omniverse_OS_Accelerator.dmg"

print(f"=== [1. COMPILING NATIVE SWIFT APPKIT EXECUTABLE] ===")
swift_src = os.path.join(SRC_DIR, "OmniverseAccelerator.swift")
contents_dir = os.path.join(APP_BUNDLE, "Contents")
macos_dir = os.path.join(contents_dir, "MacOS")
resources_dir = os.path.join(contents_dir, "Resources")

os.makedirs(macos_dir, exist_ok=True)
os.makedirs(resources_dir, exist_ok=True)

binary_output = os.path.join(macos_dir, "OmniverseAccelerator")
compile_cmd = [
    "swiftc",
    swift_src,
    "-O",
    "-o", binary_output
]
print(f"Executing: {' '.join(compile_cmd)}")
subprocess.run(compile_cmd, check=True)
os.chmod(binary_output, 0o755)

# 2. Write Info.plist
info_plist_content = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>OmniverseAccelerator</string>
    <key>CFBundleIdentifier</key>
    <string>com.omniverse.os.accelerator</string>
    <key>CFBundleName</key>
    <string>Omniverse OS Accelerator</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundleVersion</key>
    <string>100</string>
    <key>LSMinimumSystemVersion</key>
    <string>12.0</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>NSAppTransportSecurity</key>
    <dict>
        <key>NSAllowsArbitraryLoads</key>
        <true/>
    </dict>
</dict>
</plist>
"""
with open(os.path.join(contents_dir, "Info.plist"), "w", encoding="utf-8") as f:
    f.write(info_plist_content)

# Copy src to Resources
src_dst = os.path.join(resources_dir, "src")
if os.path.exists(src_dst):
    shutil.rmtree(src_dst)
shutil.copytree(SRC_DIR, src_dst)

print(f"SUCCESS: Built Native Cocoa Application at {APP_BUNDLE}")

print("=== [2. PACKAGING COMPRESSED .DMG INSTALLER] ===")
dmg_staging = os.path.join(BASE_DIR, ".dmg_staging")
if os.path.exists(dmg_staging):
    shutil.rmtree(dmg_staging)
os.makedirs(dmg_staging, exist_ok=True)

# Copy app to staging
shutil.copytree(APP_BUNDLE, os.path.join(dmg_staging, f"{APP_NAME}.app"))

# Symlink Applications folder
os.symlink("/Applications", os.path.join(dmg_staging, "Applications"))

# README
readme = """OMNIVERSE OS: HARDWARE ACCELERATOR & KERNEL GOVERNOR (v1.0)
=============================================================
Native macOS Application & AMD Adrenalin Hardware Tuning Center.

FEATURES:
- Standalone Native Cocoa/AppKit Window (No browser tab required).
- AMD Adrenalin-style live 60 FPS hardware telemetry oscilloscopes.
- 8-bit to 1024-bit vector mode execution governor.
- Darwin XNU thread QoS priority management.
- Mach VM memory compressor active reclamation.
- Apple SMC active cooling manager (3,800 RPM curve).
- CoreAudio 32-bit floating-point psychoacoustic bass limiter.
- Direct Antigravity IDE AI Chat Bridge.

INSTALLATION:
Drag 'Omniverse OS Accelerator.app' into the Applications folder.
"""
with open(os.path.join(dmg_staging, "README.txt"), "w", encoding="utf-8") as f:
    f.write(readme)

if os.path.exists(DMG_OUTPUT):
    os.remove(DMG_OUTPUT)

cmd = [
    "hdiutil", "create",
    "-volname", "Omniverse OS Accelerator",
    "-srcfolder", dmg_staging,
    "-ov",
    "-format", "UDZO",
    DMG_OUTPUT
]
subprocess.run(cmd, check=True)
shutil.copy2(DMG_OUTPUT, ROOT_DMG_OUTPUT)

# Clean staging
shutil.rmtree(dmg_staging)

print(f"SUCCESS: Generated DMG at {DMG_OUTPUT} and {ROOT_DMG_OUTPUT}")
print(f"DMG Size: {os.path.getsize(DMG_OUTPUT) / (1024*1024):.2f} MB")
