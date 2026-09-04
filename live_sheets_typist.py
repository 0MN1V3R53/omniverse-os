#!/usr/bin/env python3
import subprocess
import time
import json
import os
import sys

url = "https://docs.google.com/spreadsheets/d/1wKV8oJCdYzz9C6fuRH78diTPrNoSsip7QOFqUkjCaq4/edit?pli=1&gid=0#gid=0"

def type_val(val):
    if val is None:
        val = ""
    safe_val = str(val).replace('"', '\\"').replace('\n', ' ')
    script = f'''
    set the clipboard to "{safe_val}"
    tell application "System Events"
        keystroke "v" using command down
        delay 0.15
        keystroke tab
        delay 0.15
    end tell
    '''
    subprocess.run(["osascript", "-e", script])

def setup_headers():
    print("Opening Google Sheets and setting up headers...")
    applescript_open = f'''
    tell application "Google Chrome"
        activate
        if (count of windows) = 0 then
            make new window
            set URL of active tab of front window to "{url}"
        else
            open location "{url}"
        end if
    end tell
    '''
    subprocess.run(["osascript", "-e", applescript_open])
    time.sleep(8)
    
    as_goto_a1 = '''
    tell application "System Events"
        key code 126 using {command down} -- Up
        delay 0.5
        key code 123 using {command down} -- Left
        delay 0.5
    end tell
    '''
    subprocess.run(["osascript", "-e", as_goto_a1])
    
    headers = [
        "Quote ID", "Received At", "Full Name", "Email", "Phone", 
        "Origin", "Destination", "Miles", "Vehicle", "Type", 
        "Condition", "Transport", "Date", "Price", "Range", "ETA"
    ]
    
    for h in headers:
        type_val(h)
        
    subprocess.run(["osascript", "-e", 'tell application "System Events" to key code 36'])
    time.sleep(1)

def type_quote(quote):
    print(f"Typing quote {quote.get('id')} into Google Sheets...")
    applescript_focus = '''
    tell application "Google Chrome"
        activate
    end tell
    '''
    subprocess.run(["osascript", "-e", applescript_focus])
    time.sleep(1)
    
    as_nav = '''
    tell application "System Events"
        key code 125 using {command down} -- Cmd+Down (bottom of data)
        delay 0.5
        key code 125 -- Down arrow (new row)
        delay 0.5
        key code 123 using {command down} -- Cmd+Left (Column A)
        delay 0.5
    end tell
    '''
    subprocess.run(["osascript", "-e", as_nav])
    
    price_lo = quote.get('price_estimate_low', '')
    price_hi = quote.get('price_estimate_high', '')
    rng = f"${price_lo} - ${price_hi}" if price_lo and price_hi else ""
    
    fields = [
        quote.get("id", ""),
        quote.get("received_at", ""),
        quote.get("full_name", ""),
        quote.get("email", ""),
        quote.get("phone", ""),
        quote.get("origin", ""),
        quote.get("destination", ""),
        quote.get("distance_miles", ""),
        quote.get("vehicle", ""),
        quote.get("vehicle_type", ""),
        quote.get("vehicle_condition", ""),
        quote.get("transport_type", ""),
        quote.get("pickup_date", ""),
        quote.get("price", ""),
        rng,
        quote.get("eta", "")
    ]
    
    for val in fields:
        type_val(val)
        
    subprocess.run(["osascript", "-e", 'tell application "System Events" to key code 36'])

def main():
    if "--setup" in sys.argv:
        setup_headers()
        print("Setup complete. You can run without --setup to watch for new quotes.")
        return

    quote_file = "/Users/silversurfer/Documents/Omniverse2/quote_submissions.json"
    seen_ids = set()
    
    if os.path.exists(quote_file):
        with open(quote_file, "r") as f:
            try:
                data = json.load(f)
                for q in data:
                    seen_ids.add(q["id"])
            except:
                pass
                
    print(f"Monitoring {quote_file} for new quotes... (Found {len(seen_ids)} existing)")
    
    try:
        while True:
            time.sleep(2)
            if os.path.exists(quote_file):
                with open(quote_file, "r") as f:
                    try:
                        data = json.load(f)
                        new_quotes = [q for q in data if q["id"] not in seen_ids]
                        for q in reversed(new_quotes):
                            type_quote(q)
                            seen_ids.add(q["id"])
                    except Exception as e:
                        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("Stopping watcher.")

if __name__ == "__main__":
    main()
