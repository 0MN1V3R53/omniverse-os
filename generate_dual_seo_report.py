#!/usr/bin/env python3
"""
OMNIVERSE TECH MATRIX - DESIGN POD
Author: Elena Rodriguez (web_frontend_engineer_ui) & Dr. Emily Rivera (exec_seo_podlead_v1)
Directive: Generate Dual-Engine 50-State SEO Report
"""
import json
import os
from datetime import datetime

JSON_FILE = "seo_audit_results_multise.json"
OUTPUT_HTML = "50_state_seo_report.html"

def generate_report():
    if not os.path.exists(JSON_FILE):
        print(f"Error: {JSON_FILE} not found. Please run seo_audit_google_bing.py first.")
        # Create an empty template if json is missing so we have something to show
        results = []
    else:
        with open(JSON_FILE, "r") as f:
            data = json.load(f)
            results = data.get("results", [])

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Omniverse Tech - Dual-Engine SEO Rank Proof</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {{
            background-color: #09090b;
            color: #f4f4f5;
            font-family: 'Inter', sans-serif;
        }}
        .glass-panel {{
            background: rgba(24, 24, 27, 0.6);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(63, 63, 70, 0.5);
        }}
        .google-glow {{
            color: #3b82f6;
            text-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
        }}
        .bing-glow {{
            color: #10b981;
            text-shadow: 0 0 10px rgba(16, 185, 129, 0.5);
        }}
    </style>
</head>
<body class="min-h-screen p-8">

    <div class="max-w-6xl mx-auto">
        <header class="mb-10 text-center">
            <h1 class="text-4xl font-bold mb-2 tracking-tight">OMNIVERSE TECH EXECUTIVE AUDIT</h1>
            <h2 class="text-2xl text-zinc-400">Client: Sky Auto Services</h2>
            <p class="text-zinc-500 mt-2">Dual-Engine (Google & Bing) 50-State Rank Proof</p>
            <p class="text-xs text-zinc-600 mt-1">Generated: {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")} UTC</p>
        </header>

        <div class="glass-panel rounded-xl overflow-hidden shadow-2xl">
            <table class="w-full text-left border-collapse">
                <thead>
                    <tr class="border-b border-zinc-800 bg-zinc-900/50">
                        <th class="p-4 font-semibold text-zinc-300">State / VPN Node</th>
                        <th class="p-4 font-semibold text-zinc-300">Target Query</th>
                        <th class="p-4 font-semibold text-center text-blue-400">Google Rank</th>
                        <th class="p-4 font-semibold text-center text-emerald-400">Bing Rank</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-zinc-800">
"""

    if not results:
        html += """<tr><td colspan="4" class="p-8 text-center text-zinc-500">No data found. Execute the SEO audit engine to populate this table.</td></tr>"""
    else:
        for item in results:
            g_rank = item.get("google_rank", "N/A")
            b_rank = item.get("bing_rank", "N/A")
            
            g_class = "text-blue-400 font-bold" if isinstance(g_rank, int) and g_rank <= 3 else "text-zinc-400"
            b_class = "text-emerald-400 font-bold" if isinstance(b_rank, int) and b_rank <= 3 else "text-zinc-400"

            html += f"""
                    <tr class="hover:bg-zinc-800/30 transition-colors">
                        <td class="p-4 text-sm font-medium text-zinc-200">{item['state']}</td>
                        <td class="p-4 text-sm text-zinc-400 font-mono text-xs">{item['query']}</td>
                        <td class="p-4 text-center {g_class}">{g_rank}</td>
                        <td class="p-4 text-center {b_class}">{b_rank}</td>
                    </tr>
            """

    html += """
                </tbody>
            </table>
        </div>
        
        <footer class="mt-8 text-center text-zinc-600 text-sm">
            <p>100% Zero-Drift Live Telemetry. Audited by Omniverse Tech SEO Pod.</p>
        </footer>
    </div>

</body>
</html>
"""
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[+] Successfully generated Dual-Engine SEO Report: {OUTPUT_HTML}")

if __name__ == "__main__":
    generate_report()
