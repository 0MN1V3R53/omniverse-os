import subprocess
import time
import os
import sys
import webbrowser

def launch():
    print("Launching Montway Clone on port 3003...")
    montway = subprocess.Popen(["npm", "run", "dev", "--", "-p", "3003"], cwd="/Users/silversurfer/Documents/Omniverse2/montway_clone")
    
    print("Launching Sherpa Clone on port 3004...")
    sherpa = subprocess.Popen(["npm", "run", "dev", "--", "-p", "3004"], cwd="/Users/silversurfer/Documents/Omniverse2/sherpa_clone")
    
    try:
        print("Waiting for Next.js to compile...")
        time.sleep(5)
        print("Opening in Chrome...")
        subprocess.call(["open", "-a", "Google Chrome", "http://localhost:3003"])
        subprocess.call(["open", "-a", "Google Chrome", "http://localhost:3004"])
        print("Both prototypes are running.")
        print("Montway Clone: http://localhost:3003")
        print("Sherpa Clone: http://localhost:3004")
        print("Press Ctrl+C to stop.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down servers...")
        montway.terminate()
        sherpa.terminate()
        sys.exit(0)

if __name__ == "__main__":
    launch()
