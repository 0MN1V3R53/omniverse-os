import sys
import time
import subprocess
from playwright.sync_api import sync_playwright

def start_server_if_needed():
    import urllib.request
    try:
        urllib.request.urlopen("http://localhost:8080/cyberpunk_seo_dashboard.html", timeout=1)
        print("Server is already running on port 8080.")
        return None
    except Exception:
        print("Starting server on port 8080...")
        process = subprocess.Popen([sys.executable, "launch_cyberpunk_dashboard.py"])
        time.sleep(2)
        return process

def run_audit():
    server_process = start_server_if_needed()
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            errors = []
            page.on("pageerror", lambda err: errors.append(f"Page Error: {err}"))
            page.on("console", lambda msg: errors.append(f"Console {msg.type}: {msg.text}") if msg.type in ['error', 'warning'] else None)
            
            print("Navigating to http://localhost:8080/cyberpunk_seo_dashboard.html...")
            page.goto("http://localhost:8080/cyberpunk_seo_dashboard.html")
            
            # Wait for data to load
            page.wait_for_timeout(3000)
            
            print(f"Page Title: {page.title()}")
            
            print("\n--- Auditing Console Errors ---")
            if errors:
                for e in errors:
                    print(e)
            else:
                print("No console errors detected.")
                
            print("\n--- Auditing Elements ---")
            
            # Check SEO time filter buttons
            try:
                active_btn = page.locator(".seo-time-btn.active").first
                print(f"Active Time Filter Button: {active_btn.inner_text()}")
            except Exception as e:
                print("Failed to find active time filter button.")
                
            # Check slider
            try:
                slider = page.locator("#route-slider")
                print(f"Slider max value: {slider.get_attribute('max')}")
            except Exception as e:
                print("Failed to inspect slider.")
                
            # Check route card
            try:
                card_title = page.locator("#card-route-title").inner_text()
                print(f"Current Route Title in Card: {card_title}")
            except Exception as e:
                print("Failed to inspect route card title.")
                
            # Try moving the slider
            print("\n--- Interacting with Slider ---")
            page.evaluate("if(document.getElementById('route-slider')){document.getElementById('route-slider').value = 1; updateRouteCard(1);}")
            page.wait_for_timeout(500)
            card_title2 = page.locator("#card-route-title").inner_text()
            print(f"Route Title after moving slider to index 1: {card_title2}")
            
            browser.close()
    finally:
        if server_process:
            server_process.terminate()

if __name__ == "__main__":
    run_audit()
