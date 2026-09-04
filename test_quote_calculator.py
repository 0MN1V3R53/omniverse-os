import math
import subprocess
import os

def price_calc(miles, vehicle_id, transport_id, inoperable=False):
    if miles <= 199:
        rate = 2.45  # Short haul rate between $2.00 and $3.00 / mile
    elif miles <= 500:
        rate = 0.80
    elif miles <= 1000:
        rate = 0.73
    elif miles <= 1500:
        rate = 0.70
    elif miles <= 2000:
        rate = 0.48
    else:
        rate = 0.35
    
    base_cost = miles * rate
    
    surcharges = {
        "sedan": 0, "suv_small": 125, "suv_large": 150, "pickup_half": 175, 
        "pickup_heavy": 200, "van": 75, "sports_car": 100, "classic": 100, 
        "motorcycle": -100, "ev": 100, "heavy": 300, "boat_atv": 250
    }
    
    base_cost += surcharges.get(vehicle_id, 0)
    
    if inoperable:
        base_cost += 150
        
    transport_multipliers = {
        "open_standard": 1.0,
        "enclosed_standard": 1.50,
        "enclosed_liftgate": 1.70,
        "express_expedited": 1.95
    }
    transport_mins = {
        "open_standard": 399,
        "enclosed_standard": 599,
        "enclosed_liftgate": 799,
        "express_expedited": 999
    }
    
    cost = base_cost * transport_multipliers.get(transport_id, 1.0)
    cost = max(cost, transport_mins.get(transport_id, 399), 399)
    
    return max(399, round(cost / 5) * 5)

def main():
    print("--- 2026 Quote Calculator Pricing Verification ---")
    
    # Test 1
    # Route: 60601→46201 (~185 miles), Sedan, Open
    # Expected: $455 (185 * 2.45 = 453.25 -> round to $455, starting from $399+)
    miles1 = 185
    cost1 = price_calc(miles1, "sedan", "open_standard")
    expected1 = 455
    print(f"Test 1 (Short haul): {miles1}mi, sedan, open_standard -> ${cost1} (Expected: ~${expected1}) {'✅' if cost1 == expected1 else '❌'}")

    # Test 2
    # Route: 90001→10001 (~2,775 miles), Sedan, Open
    # Expected: 2775 * 0.35 = 971.25 -> round to $970 or $975 (mid) -> (971.25 / 5 = 194.25 -> 194 * 5 = 970)
    miles2 = 2775
    cost2 = price_calc(miles2, "sedan", "open_standard")
    expected2 = 970
    print(f"Test 2 (Cross-country): {miles2}mi, sedan, open_standard -> ${cost2} (Expected: ~${expected2}) {'✅' if cost2 == expected2 else '❌'}")

    # Test 3
    # Route: 33101→98101 (~3,300 miles), Large SUV, Enclosed
    # Expected: (3300 * 0.35 + 150) * 1.5 = 1957.5 -> round to $1960
    miles3 = 3300
    cost3 = price_calc(miles3, "suv_large", "enclosed_standard")
    expected3 = 1960
    print(f"Test 3 (Enclosed SUV): {miles3}mi, suv_large, enclosed_standard -> ${cost3} (Expected: ~${expected3}) {'✅' if cost3 == expected3 else '❌'}")

    print("\n--- Running Next.js Build ---")
    app_dir = os.path.join(os.path.dirname(__file__), "montway_clone")
    
    if os.path.exists(app_dir):
        os.chdir(app_dir)
        try:
            result = subprocess.run(["npm", "run", "build"], check=True)
            if result.returncode == 0:
                print("Build successful! ✅")
        except subprocess.CalledProcessError:
            print("Build failed! ❌")
            return
    else:
        print("sky_next directory not found! ❌")
        
    print("\n--- Opening Staging Server ---")
    try:
        subprocess.run(["open", "-a", "Safari", "http://localhost:3000"])
        print("Opened Safari ✅")
    except Exception as e:
        print(f"Could not open Safari: {e}")

if __name__ == "__main__":
    main()
