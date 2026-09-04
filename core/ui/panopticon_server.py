"""
Panopticon Visual Control Plane & Telemetry Server.
Serves a sleek cyberpunk real-time dashboard and REST telemetry endpoints for the Omniverse agent runtime.
"""

import json
import http.server
import socketserver
import threading
from pathlib import Path
from typing import Dict, Any, Optional

from core.config import CONFIG
from core.economy.ledger import GLOBAL_LEDGER
from core.cognition.causal_graph import GLOBAL_CAUSAL_GRAPH
from core.skills.vault import GLOBAL_SKILL_VAULT
from core.environment.observer import EnvironmentObserver


PANOPTICON_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Omniverse Panopticon // Visual Control Plane</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=Outfit:wght@400;600;800&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-base: #0a0d14;
      --bg-card: rgba(18, 24, 38, 0.85);
      --border: rgba(56, 189, 248, 0.2);
      --accent: #38bdf8;
      --accent-glow: rgba(56, 189, 248, 0.35);
      --success: #34d399;
      --warning: #fbbf24;
      --text-main: #f1f5f9;
      --text-dim: #94a3b8;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: radial-gradient(circle at 50% 0%, #151e33 0%, var(--bg-base) 75%);
      color: var(--text-main);
      font-family: 'Outfit', sans-serif;
      min-height: 100vh;
      padding: 2rem;
    }
    header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 2rem;
      border-bottom: 1px solid var(--border);
      margin-bottom: 2rem;
    }
    .logo-badge {
      display: flex;
      align-items: center;
      gap: 1rem;
    }
    .logo-badge h1 {
      font-size: 1.5rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      background: linear-gradient(135deg, #fff, var(--accent));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .pulse-dot {
      width: 10px;
      height: 10px;
      background: var(--success);
      border-radius: 50%;
      box-shadow: 0 0 12px var(--success);
      animation: pulse 2s infinite;
    }
    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(1.2); }
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 1.5rem;
    }
    .card {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1.5rem;
      backdrop-filter: blur(12px);
      box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    }
    .card-title {
      font-size: 0.85rem;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: var(--accent);
      margin-bottom: 1rem;
      display: flex;
      justify-content: space-between;
    }
    .metric-value {
      font-size: 2.2rem;
      font-weight: 800;
      color: #fff;
      font-family: 'JetBrains Mono', monospace;
    }
    .metric-sub {
      font-size: 0.85rem;
      color: var(--text-dim);
      margin-top: 0.5rem;
    }
    .feed {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.8rem;
      line-height: 1.6;
      color: #cbd5e1;
      max-height: 240px;
      overflow-y: auto;
    }
    .feed-item {
      padding: 0.4rem 0;
      border-bottom: 1px solid rgba(255,255,255,0.05);
    }
  </style>
</head>
<body>
  <header>
    <div class="logo-badge">
      <div class="pulse-dot"></div>
      <h1>OMNIVERSE // PANOPTICON</h1>
    </div>
    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: var(--accent);">
      RUNTIME: ACTIVE // CHECKPOINT 5 SYNCHRONIZED
    </div>
  </header>

  <div class="grid">
    <div class="card">
      <div class="card-title">Active Enterprise Workforce <span>81 Agents</span></div>
      <div class="metric-value" id="val-agents">81</div>
      <div class="metric-sub">Distributed across 12 Autonomous Pods</div>
    </div>

    <div class="card">
      <div class="card-title">Causal Knowledge Links <span>Bayesian Graph</span></div>
      <div class="metric-value" id="val-causal">--</div>
      <div class="metric-sub">Empirical Action-Outcome Connections</div>
    </div>

    <div class="card">
      <div class="card-title">JIT Skill Vault <span>Executable Tools</span></div>
      <div class="metric-value" id="val-skills">--</div>
      <div class="metric-sub">Self-Compiled Multi-Step Primitives</div>
    </div>

    <div class="card" style="grid-column: 1 / -1;">
      <div class="card-title">Live Workspace Telemetry & Causal Strategies</div>
      <div class="feed" id="feed-log">
        <div class="feed-item">Fetching live state snapshot from /api/telemetry...</div>
      </div>
    </div>
  </div>

  <script>
    async function loadTelemetry() {
      try {
        const res = await fetch('/api/telemetry');
        const data = await res.json();
        document.getElementById('val-agents').innerText = data.active_agents;
        document.getElementById('val-causal').innerText = data.causal_links_count;
        document.getElementById('val-skills').innerText = data.jit_skills_count;
        
        let html = '';
        html += '<div class="feed-item">> [ENVIRONMENT] Branch: ' + data.git_branch + ' | Uncommitted: ' + data.uncommitted_files + '</div>';
        html += '<div class="feed-item">> [CREDITS] Growth: ' + (data.credit_balances['Growth Squad'] || 'N/A') + ' | Web: ' + (data.credit_balances['Web Engineering'] || 'N/A') + ' | SRE: ' + (data.credit_balances['DevOps SRE'] || 'N/A') + '</div>';
        data.causal_sample_links.forEach(l => {
          html += '<div class="feed-item">> [CAUSAL] ' + l.context_state + ' -> ' + l.action_taken + ' (Conf: ' + l.confidence_score + ')</div>';
        });
        document.getElementById('feed-log').innerHTML = html;
      } catch (e) {
        document.getElementById('feed-log').innerHTML = '<div class="feed-item" style="color:#ef4444;">Error connecting to telemetry feed: ' + e + '</div>';
      }
    }
    loadTelemetry();
    setInterval(loadTelemetry, 5000);
  </script>
</body>
</html>
"""


class PanopticonRequestHandler(http.server.BaseHTTPRequestHandler):
    """HTTP Request Handler serving dashboard and REST endpoints."""

    def log_message(self, format, *args):
        # Silence default server logging
        return

    def do_GET(self):
        if self.path in ("/", "/panopticon"):
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(PANOPTICON_HTML.encode("utf-8"))
        elif self.path == "/api/telemetry":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            
            # Fetch live snapshot
            obs = EnvironmentObserver()
            snap = obs.get_live_snapshot()
            causal = GLOBAL_CAUSAL_GRAPH
            skills = GLOBAL_SKILL_VAULT
            ledger = GLOBAL_LEDGER

            data = {
                "active_agents": snap.active_agent_count,
                "git_branch": snap.git_branch,
                "uncommitted_files": snap.uncommitted_changes_count,
                "causal_links_count": len(causal.matrix.links),
                "jit_skills_count": len(skills.manifest.skills),
                "credit_balances": {
                    "Growth Squad": ledger.get_budget("Growth Squad").available_credits,
                    "Web Frontend": ledger.get_budget("Web Frontend").available_credits,
                    "DevOps SRE": ledger.get_budget("DevOps SRE").available_credits,
                },

                "causal_sample_links": [
                    {
                        "context_state": l.context_state,
                        "action_taken": l.action_taken,
                        "confidence_score": l.confidence_score
                    }
                    for l in causal.matrix.links[:4]
                ]
            }
            self.wfile.write(json.dumps(data).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()


class PanopticonServer:
    """
    Lightweight background or foreground server for the Panopticon Visual Control Plane.
    """

    def __init__(self, port: int = 8088):
        self.port = port
        self.server: Optional[socketserver.TCPServer] = None
        self._thread: Optional[threading.Thread] = None

    def start_background(self) -> None:
        """Start server on a background daemon thread."""
        socketserver.TCPServer.allow_reuse_address = True
        self.server = socketserver.TCPServer(("", self.port), PanopticonRequestHandler)
        self._thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Stop background server."""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.server = None
