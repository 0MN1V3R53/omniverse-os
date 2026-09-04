#!/usr/bin/env python3
import subprocess

print("🌐 Opening Omniverse Tech Matrix in Google Chrome...")

applescript = '''
tell application "Google Chrome"
    activate
    if (count of windows) = 0 then
        make new window
        set URL of active tab of front window to "file:///Users/silversurfer/.gemini/antigravity/brain/400117eb-85c1-4f5b-b7db-920a5227f941/omniverse_matrix.html"
    else
        open location "file:///Users/silversurfer/.gemini/antigravity/brain/400117eb-85c1-4f5b-b7db-920a5227f941/omniverse_matrix.html"
    end if
end tell
'''

res = subprocess.run(["osascript", "-e", applescript], capture_output=True, text=True)

if res.returncode == 0:
    print("✨ Successfully opened Omniverse Tech Matrix in Google Chrome!")
else:
    print(f"⚠️ AppleScript notice: {res.stderr}")
    subprocess.run(["open", "-a", "Google Chrome", "/Users/silversurfer/.gemini/antigravity/brain/400117eb-85c1-4f5b-b7db-920a5227f941/omniverse_matrix.html"])
    print("✨ Opened via default system open command!")
