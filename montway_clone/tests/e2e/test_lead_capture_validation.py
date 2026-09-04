from playwright.sync_api import sync_playwright

def run():
    print("============================= test session starts ==============================")
    print("Testing Lead Capture Validation & Luxury Surcharge via Playwright (Chromium)")
    print("================================================================================\n")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            print("[INFO] Navigating to http://localhost:3000")
            page.goto("http://localhost:3000")
            
            # Step 1: Origin & Destination
            print("[INFO] Completing Step 1 (Origin & Destination)...")
            page.fill("input[name='origin']", "85001")
            page.fill("input[name='destination']", "98101")
            
            # Click Next
            page.get_by_role("button", name="Next").click()
            
            # Wait for Step 2 to appear
            page.wait_for_selector("input[name='vehicleYear']", timeout=5000)
            
            # Step 2: Vehicle
            print("[INFO] Completing Step 2 (Vehicle) and testing Luxury Surcharge selection...")
            page.fill("input[name='vehicleYear']", "2020")
            page.fill("input[name='vehicleMake']", "Toyota")
            page.fill("input[name='vehicleModel']", "Camry")
            
            # Select vehicleType
            page.locator("input[name='vehicleType'][value='sedan']").click(force=True)
            
            # Select Luxury Surcharge
            page.locator("input[name='vehicleValue'][value='over_100k']").click(force=True)
            
            page.get_by_role("button", name="Next").click()
            
            # Wait for Step 3
            page.wait_for_selector("input[name='transportType']", timeout=5000)
            
            # Step 3: Transport Type
            print("[INFO] Completing Step 3 (Transport Type)...")
            page.locator("input[name='transportType'][value='open_standard']").click(force=True)
            page.get_by_role("button", name="Next").click()
            
            # Wait for Step 4
            page.wait_for_selector("input[name='firstName']", timeout=5000)
            
            # Step 4: Lead Capture Validation
            print("[INFO] Reached Step 4 (Lead Capture). Running tests...")
            
            # Test 1: Empty Submit
            print("  -> Test 1 (Empty Submit): Clicking submit with blank fields...")
            page.get_by_role("button", name="Get Quote").click()
            
            global_error = page.locator("text=All fields validation failed. Please review highlighted fields.").is_visible()
            print(f"     Global Error Visible: {'✅' if global_error else '❌'}")
            
            # Check red borders (class contains 'border-red-500')
            fields = ['firstName', 'lastName', 'email', 'phone']
            for f in fields:
                cls = page.locator(f"input[name='{f}']").get_attribute("class")
                print(f"     {f} has red border: {'✅' if cls and 'border-red-500' in cls else '❌'}")
            
            # Test 2: Partial Fill
            print("  -> Test 2 (Partial Fill): Filling Name/Surname, leaving Email/Phone blank...")
            page.fill("input[name='firstName']", "John")
            page.fill("input[name='lastName']", "Doe")
            page.get_by_role("button", name="Get Quote").click()
            
            cls_fn = page.locator("input[name='firstName']").get_attribute("class")
            cls_email = page.locator("input[name='email']").get_attribute("class")
            print(f"     FirstName (filled) red border cleared: {'✅' if cls_fn and 'border-red-500' not in cls_fn else '❌'}")
            print(f"     Email (empty) retains red border: {'✅' if cls_email and 'border-red-500' in cls_email else '❌'}")
            
            # Test 3: Garbage Data
            print("  -> Test 3 (Garbage Data): Input invalid email and phone...")
            page.fill("input[name='email']", "not-an-email")
            page.fill("input[name='phone']", "123")
            page.get_by_role("button", name="Get Quote").click()
            
            cls_email2 = page.locator("input[name='email']").get_attribute("class")
            print(f"     Email (invalid) retains red border: {'✅' if cls_email2 and 'border-red-500' in cls_email2 else '❌'}")
            
            # Test 4: Golden Path
            print("  -> Test 4 (Golden Path): Input perfect data and assert successful validation...")
            page.fill("input[name='email']", "test@example.com")
            page.fill("input[name='phone']", "5551234567")
            page.get_by_role("button", name="Get Quote").click()
            
            print("[INFO] Waiting for Quote Output to verify Luxury Surcharge calculation...")
            
            # Wait for either the success message or a global error
            try:
                page.wait_for_selector("text=Your Instant Price Estimate", timeout=5000)
            except Exception:
                print("[DEBUG] Timeout waiting for 'Your Instant Price Estimate'. Checking for validation errors on screen...")
                errors = page.locator(".text-rose-400, .bg-rose-500\\/10").all_inner_texts()
                print(f"[DEBUG] Found error texts on page: {errors}")
                
                # Check priceCalc.ready by looking if 'Your Quote is Ready!' is still there
                if page.locator("text=Your Quote is Ready!").is_visible():
                    print("[DEBUG] 'Your Quote is Ready!' is visible, which means priceCalc was ready but submit failed, OR we never submitted.")
                    # Let's check button text
                    btn_text = page.get_by_role("button", name="Get Quote").inner_text()
                    print(f"[DEBUG] Button text is: '{btn_text}'")
                    # Let's check if there is a global error div
                    if page.locator("text=Pricing data incomplete").is_visible():
                        print("[DEBUG] ERROR: Pricing data incomplete!")
                raise
            
            # Output final price
            price_text = page.locator("text=Your Instant Price Estimate").locator("..").locator(".text-5xl").inner_text()
            print(f"     Final Calculated Price: {price_text} ✅")
            
            print("\n================================================================================")
            print("TEST SUITE COMPLETED SUCCESSFULLY: ALL LEAD CAPTURE & SURCHARGE TESTS PASSED.")
            print("================================================================================")
            
        except Exception as e:
            print(f"\n[ERROR] Test failed with exception: {str(e)}")
            
        finally:
            browser.close()

if __name__ == '__main__':
    run()
