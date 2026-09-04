import os
import sys

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    files_to_open = [
        "competitor_mockups/montway_layout/index.html",
        "competitor_mockups/montway_layout/state_template.html",
        "competitor_mockups/sherpa_layout/index.html",
        "competitor_mockups/sherpa_layout/state_template.html"
    ]
    
    print("Launching mockups in Google Chrome...")
    
    for relative_path in files_to_open:
        full_path = os.path.join(base_dir, relative_path)
        
        if os.path.exists(full_path):
            # Uses macOS 'open' command to specifically target Google Chrome
            command = f"open -a 'Google Chrome' '{full_path}'"
            os.system(command)
            print(f"Opened: {relative_path}")
        else:
            print(f"Error: File not found -> {full_path}")

if __name__ == "__main__":
    main()
