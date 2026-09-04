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

def set_clipboard(text):
    p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    p.communicate(input=text.encode('utf-8'))

def get_clipboard():
    p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
    data, _ = p.communicate()
    return data.decode('utf-8')

def send_to_ide(text):
    # Prepare the message for the IDE Agent
    prompt = f"[FORWARDED FROM HTML] Director says: {text}\\n\\nINSTRUCTION: Reply by running terminal command: echo \"your response\" | pbcopy"
    set_clipboard(prompt)
    time.sleep(0.5)
    
    # Use AppleScript to paste and hit enter in Electron IDE
    applescript = '''
    tell application "Electron" to activate
    delay 0.5
    tell application "System Events"
        keystroke "v" using command down
        delay 0.5
        keystroke return
    end tell
    '''
    subprocess.run(["osascript", "-e", applescript])

def main():
    print("Ghost Operator started. Monitoring chat_spool.json for Zero-API Bridge...")
    last_count = len(get_spool())
    
    while True:
        time.sleep(2)
        spool = get_spool()
        if len(spool) > last_count:
            # Check for new user messages
            for i in range(last_count, len(spool)):
                msg = spool[i]
                if msg.get("role") == "user" and not msg.get("_processed"):
                    print(f"User sent: {msg['text']}")
                    
                    # 1. Send to IDE via copy/paste
                    send_to_ide(msg['text'])
                    
                    # 2. Wait for Agent to reply via pbcopy
                    set_clipboard("WAITING_FOR_AGENT")
                    print("Waiting for agent reply on clipboard...")
                    
                    reply = ""
                    while True:
                        time.sleep(2)
                        current_clip = get_clipboard().strip()
                        if current_clip and current_clip != "WAITING_FOR_AGENT" and "[FORWARDED FROM HTML]" not in current_clip:
                            reply = current_clip
                            print(f"Received agent reply: {reply}")
                            break
                    
                    # 3. Append reply to spool
                    spool.append({
                        "role": "agent",
                        "text": reply
                    })
                    
                    msg["_processed"] = True
            
            # Save back to spool
            with open(SPOOL_FILE, 'w') as f:
                json.dump(spool, f, indent=4)
                
            last_count = len(spool)

if __name__ == "__main__":
    main()
