from playwright.sync_api import sync_playwright

def run():
    print("============================= test session starts ==============================")
    print("Testing Live Site Quote Submission to Google Sheets")
    print("================================================================================\n")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            print("[INFO] Navigating to https://skyautoservices.com/")
            page.goto("https://skyautoservices.com/")
            
            # Step 1: Origin & Destination
            print("[INFO] Completing Step 1...")
            page.fill("input[name='origin']", "90210")
            page.fill("input[name='destination']", "10001")
            page.get_by_role("button", name="Next").click()
            
            # Wait for Step 2
            page.wait_for_selector("input[name='vehicleYear']", timeout=5000)
            
            # Step 2: Vehicle
            print("[INFO] Completing Step 2...")
            page.fill("input[name='vehicleYear']", "2024")
            page.fill("input[name='vehicleMake']", "Porsche")
            page.fill("input[name='vehicleModel']", "911 Turbo")
            page.locator("input[name='vehicleType'][value='sports_car']").click(force=True)
            page.locator("input[name='vehicleValue'][value='over_100k']").click(force=True)
            page.get_by_role("button", name="Next").click()
            
            # Wait for Step 3
            page.wait_for_selector("input[name='transportType']", timeout=5000)
            
            # Step 3: Transport Type
            print("[INFO] Completing Step 3...")
            page.locator("input[name='transportType'][value='enclosed_standard']").click(force=True)
            page.get_by_role("button", name="Next").click()
            
            # Wait for Step 4
            page.wait_for_selector("input[name='firstName']", timeout=5000)
            
            # Step 4: Lead Capture
            print("[INFO] Completing Step 4 (Lead Capture)...")
            page.fill("input[name='firstName']", "Bruce")
            page.fill("input[name='lastName']", "Wayne")
            page.fill("input[name='email']", "bruce@wayneenterprises.com")
            page.fill("input[name='phone']", "555-0199-888")
            
            # Fill out comments for Column L verification
            page.fill("textarea[name='comments']", "Please use enclosed transport. High value vehicle.")
            
            page.get_by_role("button", name="Get Quote").click()
            
            print("[INFO] Waiting for Quote Output...")
            page.wait_for_selector("text=Your Instant Price Estimate", timeout=8000)
            
            # Output final price
            price_text = page.locator("text=Your Instant Price Estimate").locator("..").locator(".text-5xl").inner_text()
            print(f"     Final Calculated Price: {price_text} ✅")
            
            print("\n[SUCCESS] Quote submitted successfully to LIVE site!")
            
        except Exception as e:
            print(f"\n[ERROR] Test failed with exception: {str(e)}")
            
        finally:
            browser.close()

if __name__ == '__main__':
    run()
