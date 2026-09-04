import os
from datetime import datetime

MEM_DIR = ".agents/omniverse_memories"
AGENTS_TO_UPDATE = {
    "exec_ceo_alexander_vance.md": "Assigned the Dual-Engine (Google+Bing) SEO Audit task to SEO Pod Lead Dr. Emily Rivera to establish Rank Proof across 50 states.",
    "exec_seo_podlead_v1.md": "Received CEO directive to build a dual-engine SEO scraper. Coordinated with Priya Patel to write seo_audit_google_bing.py and the Design Pod for 50_state_seo_report.html.",
    "seo_technical_engineer_cwv.md": "Authored seo_audit_google_bing.py using Playwright to scrape both Google and Bing for all 50 states.",
    "web_frontend_engineer_ui.md": "Designed the 50_state_seo_report.html UI to display side-by-side Google and Bing rankings in a premium Cyberpunk layout."
}

def update_memories():
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    for agent, action in AGENTS_TO_UPDATE.items():
        path = os.path.join(MEM_DIR, agent)
        if os.path.exists(path):
            with open(path, "a") as f:
                f.write(f"\n\n### ACTION LOG ENTRY: {now}\n")
                f.write(f"- {action}\n")
            print(f"Updated {agent}")
        else:
            print(f"Skipped {agent} (Not Found)")

if __name__ == "__main__":
    update_memories()
