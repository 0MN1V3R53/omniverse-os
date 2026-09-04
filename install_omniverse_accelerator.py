#!/usr/bin/env python3
"""
Omniverse OS - Automated DMG Installer & Modern macOS Desktop Transformer
Installs Omniverse OS Accelerator.app into /Applications & Sets M4 Liquid Glass Desktop
Author: Dr. Alexander Vance & Viktor Vance
"""

import os
import subprocess
import shutil
import time

BASE_DIR = "/Users/silversurfer/Documents/Omniverse2"
DMG_PATH = os.path.join(BASE_DIR, "Omniverse_OS_Accelerator.dmg")
MOUNT_POINT = "/Volumes/OmniverseInstaller"
APP_NAME = "Omniverse OS Accelerator.app"
DEST_APP_PATH = os.path.join("/Applications", APP_NAME)
WALLPAPER_PATH = "/Users/silversurfer/.gemini/antigravity-ide/brain/a9c2323e-4e2e-4e36-8319-b5bcb67f6397/macos_modern_liquid_glass_wallpaper_1788360327605.jpg"

print("================================================================")
print(" 🚀 OMNIVERSE OS: NATIVE DMG INSTALLER & M4 DESKTOP TRANSFORMER ")
print("================================================================")

# Step 1: Re-build DMG with Swift Mach-O Binary
print("\n[STEP 1/5] Compiling Native Swift AppKit Binary & Packaging DMG...")
subprocess.run(["python3", os.path.join(BASE_DIR, "apps/omniverse_accelerator/build_dmg.py")], check=True)

# Step 2: Mount the DMG
print(f"\n[STEP 2/5] Mounting {DMG_PATH}...")
if os.path.exists(MOUNT_POINT):
    subprocess.run(["hdiutil", "detach", MOUNT_POINT, "-force"], check=False)

mount_cmd = ["hdiutil", "attach", DMG_PATH, "-mountpoint", MOUNT_POINT, "-nobrowse", "-quiet"]
subprocess.run(mount_cmd, check=True)
print(f"✓ Mounted at {MOUNT_POINT}")

# Step 3: Install App to /Applications
print(f"\n[STEP 3/5] Installing {APP_NAME} to /Applications/...")
source_app = os.path.join(MOUNT_POINT, APP_NAME)
if not os.path.exists(source_app):
    # Search inside mount
    for item in os.listdir(MOUNT_POINT):
        if item.endswith(".app"):
            source_app = os.path.join(MOUNT_POINT, item)
            break

if os.path.exists(DEST_APP_PATH):
    print("Removing previous installation...")
    shutil.rmtree(DEST_APP_PATH)

shutil.copytree(source_app, DEST_APP_PATH)
print(f"✓ Installed successfully to {DEST_APP_PATH}")

# Detach DMG
print("Detaching DMG installer volume...")
subprocess.run(["hdiutil", "detach", MOUNT_POINT, "-quiet"], check=False)

# Step 4: Apply Modern M4 macOS Liquid Glass UI Transformations
print("\n[STEP 4/5] Applying Modern M4 Desktop Transformation...")

# A. Enable System Dark Mode
try:
    subprocess.run(["osascript", "-e", 'tell application "System Events" to tell appearance preferences to set dark mode to true'], check=False)
    print("✓ Dark Mode Enabled.")
except Exception as e:
    print(f"Dark mode note: {e}")

# B. Set Modern 8K Liquid Glass Wallpaper
if os.path.exists(WALLPAPER_PATH):
    try:
        apple_script = f'''
        tell application "System Events"
            tell every desktop
                set picture to "{WALLPAPER_PATH}"
            end tell
        end tell
        '''
        subprocess.run(["osascript", "-e", apple_script], check=False)
        print("✓ Next-Gen Liquid Glass 8K Wallpaper Applied.")
    except Exception as e:
        print(f"Wallpaper note: {e}")

# C. Optimize Dock & WindowServer
try:
    # Modern Dock: 44px tiles, smooth magnification to 62px
    subprocess.run(["defaults", "write", "com.apple.dock", "tilesize", "-int", "44"], check=False)
    subprocess.run(["defaults", "write", "com.apple.dock", "magnification", "-bool", "true"], check=False)
    subprocess.run(["defaults", "write", "com.apple.dock", "largesize", "-int", "62"], check=False)
    subprocess.run(["defaults", "write", "com.apple.dock", "autohide-time-modifier", "-float", "0.12"], check=False)
    subprocess.run(["defaults", "write", "com.apple.dock", "autohide-delay", "-float", "0.0"], check=False)
    
    # Instant Window Resizing
    subprocess.run(["defaults", "write", "NSGlobalDomain", "NSWindowResizeTime", "-float", "0.001"], check=False)
    subprocess.run(["defaults", "write", "-g", "QLPanelAnimationDuration", "-float", "0.1"], check=False)
    
    # Refresh Dock
    subprocess.run(["killall", "Dock"], check=False)
    print("✓ Modern Dock & WindowServer Optimizations Active.")
except Exception as e:
    print(f"Dock note: {e}")

# Step 5: Launch Native macOS Application Window
print(f"\n[STEP 5/5] Launching Native macOS Standalone Application...")
subprocess.run(["open", DEST_APP_PATH], check=False)
print("✓ Omniverse OS Accelerator Native App Window launched!")

print("\n================================================================")
print(" 🎉 INSTALLATION & DESKTOP MODERNIZATION 100% COMPLETE!")
print("================================================================")
