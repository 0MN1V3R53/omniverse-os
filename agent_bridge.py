import json
import time
import os
import subprocess

SPOOL_FILE = "/Users/silversurfer/Documents/Omniverse2/public_html_local/assets/data/chat_spool.json"

def get_spool():
    if not os.path.exists(SPOOL_FILE):
        return []
    try:
        with open(SPOOL_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return []

def send_to_ide(text):
    prompt = f"[FORWARDED FROM HTML] Director says: {text} | INSTRUCTION: Reply by using your tool to append your response to chat_spool.json with role 'agent'."
    # Escape quotes for AppleScript
    prompt = prompt.replace('"', '\\"')
    
    applescript = f'''
    tell application "Code" to activate
    delay 0.5
    tell application "System Events"
        keystroke "{prompt}"
        delay 0.5
        keystroke return
    end tell
    '''
    subprocess.run(["osascript", "-e", applescript])

def main():
    print("Agent Bridge started. Monitoring chat_spool.json...")
    last_count = len(get_spool())
    
    while True:
        time.sleep(2)
        spool = get_spool()
        if len(spool) > last_count:
            # Check the new messages
            for i in range(last_count, len(spool)):
                msg = spool[i]
                if msg.get("role") == "user" and not msg.get("_processed"):
                    print(f"Forwarding to IDE: {msg['text']}")
                    send_to_ide(msg['text'])
                    # Mark as processed so we don't send again if restarted
                    msg["_processed"] = True
            
            # Save back processed flags
            with open(SPOOL_FILE, 'w') as f:
                json.dump(spool, f, indent=4)
                
            last_count = len(spool)

if __name__ == "__main__":
    main()
