import os
import subprocess
import sys

def install_playwright_drivers():
    """
    Downloads and installs the necessary browser drivers (Chromium, Firefox, WebKit) 
    required for automated browser control on an Apple Mac (iMac).
    """
    print("🍏 Starting installation for Apple Mac (iMac)...")
    
    try:
        # Step 1: Install the playwright Python package
        print("\n📦 Step 1: Installing the 'playwright' Python package (Version 1.43.0 for macOS 12 WebKit compatibility)...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright==1.43.0"])
        
        # Step 2: Install the browser binaries (drivers)
        print("\n🌐 Step 2: Downloading and installing browser drivers (Chromium, Firefox, WebKit)...")
        # This command pulls down the actual browser binaries needed to run the automation
        subprocess.check_call([sys.executable, "-m", "playwright", "install"])
        
        print("\n✅ Success! All drivers have been downloaded and installed.")
        print("You are now ready to run automated browser scripts on your iMac.")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ An error occurred during installation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_playwright_drivers()
