#!/usr/bin/env python3
import subprocess
import json

def inspect_editor():
    js_code = """
    (() => {
        const text = document.body.innerText;
        const sections = Array.from(document.querySelectorAll('h1, h2, h3, h4, [role="heading"], label, .title, .header'))
            .map(el => el.innerText ? el.innerText.trim() : '')
            .filter(t => t.length > 2 && t.length < 100);
            
        const assetSummary = {
            hasVideos: text.includes('Videos') || text.includes('Video'),
            hasLogos: text.includes('Logos') || text.includes('Logo'),
            hasImages: text.includes('Images') || text.includes('Image'),
            hasHeadlines: text.includes('Headlines') || text.includes('Headline'),
            hasDescriptions: text.includes('Descriptions') || text.includes('Description'),
            adStrengthText: (text.match(/Ad strength:[^\\n]+/i) || [''])[0],
            missingAlerts: Array.from(document.querySelectorAll('.error, [role="alert"], .warning, .status-message'))
                .map(el => el.innerText ? el.innerText.trim() : '')
                .filter(t => t.length > 0)
        };
        
        return JSON.stringify({
            url: window.location.href,
            summary: assetSummary,
            sections: sections.slice(0, 30),
            fullTextSample: text.substring(0, 4000)
        });
    })()
    """
    js_escaped = js_code.replace('"', '\\"')
    script = f'''tell application "Google Chrome"
    repeat with w in windows
        repeat with t in tabs of w
            if URL of t contains "ads.google.com" then
                return (execute t javascript "{js_escaped}")
            end if
        end repeat
    end repeat
end tell'''
    res = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    try:
        return json.loads(res.stdout.strip())
    except Exception:
        return {"raw": res.stdout.strip()}

if __name__ == "__main__":
    print(json.dumps(inspect_editor(), indent=2))
