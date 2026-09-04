#!/usr/bin/env python3
import subprocess
import json
import os

def diagnose():
    js_code = """
    (function() {
        var results = {};
        
        // 1. Search for all elements containing ad blocker text
        var allElements = Array.from(document.querySelectorAll("*"));
        var blockerElements = allElements.filter(function(el) {
            return el.children.length === 0 && (el.innerText || "").toLowerCase().includes("ad blocker");
        });
        
        results.elementsFound = blockerElements.map(function(el) {
            var rect = el.getBoundingClientRect();
            var style = window.getComputedStyle(el);
            var parent = el.parentElement;
            var parentStyle = parent ? window.getComputedStyle(parent) : null;
            return {
                tagName: el.tagName,
                text: el.innerText.trim(),
                className: el.className,
                isVisible: rect.width > 0 && rect.height > 0 && style.display !== "none" && style.visibility !== "hidden" && style.opacity !== "0",
                boundingBox: {top: rect.top, left: rect.left, width: rect.width, height: rect.height},
                display: style.display,
                visibility: style.visibility,
                opacity: style.opacity,
                parentTag: parent ? parent.tagName : null,
                parentClass: parent ? parent.className : null
            };
        });
        
        // 2. Check if Google Ads main components and tables loaded properly
        results.campaignTableLoaded = !!document.querySelector("[role='table'], [role='grid'], .particle-table, table, ess-table");
        results.scriptsCount = document.querySelectorAll("script").length;
        
        // 3. Test if doubleclick.net / googleadservices.com can be fetched via JavaScript fetch API
        results.testFetch = "pending";
        
        return JSON.stringify(results, null, 2);
    })()
    """
    
    js_escaped = js_code.replace('\\', '\\\\').replace('"', '\\"')
    script = f'''
    tell application "Google Chrome"
        repeat with w in windows
            repeat with t in tabs of w
                if URL of t contains "ads.google.com" then
                    return (execute t javascript "{js_escaped}")
                end if
            end repeat
        end repeat
        return "ADS_TAB_NOT_FOUND"
    end tell
    '''
    
    res = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=8)
    if res.returncode != 0:
        return {"error": res.stderr.strip()}
    return res.stdout.strip()

if __name__ == "__main__":
    out = diagnose()
    print(out)
