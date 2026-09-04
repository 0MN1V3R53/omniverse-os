"""
Autonomous Heartbeat & Proactive Initiative Daemon.
Periodically assesses domain performance and drafts proactive architectural RFC proposals.
"""

import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

from core.config import CONFIG


class HeartbeatProposal(BaseModel):
    """Proactive proposal drafted by a Pod Lead on heartbeat tick."""
    rfc_id: str = Field(default_factory=lambda: f"RFC-{uuid.uuid4().hex[:6].upper()}")
    origin_pod: str
    lead_agent_id: str
    title: str
    problem_statement: str
    proposed_solution: str
    impacted_pods: List[str] = Field(default_factory=list)
    estimated_credit_cost: float = 15.0
    status: str = "DRAFT"  # DRAFT, REVIEW, APPROVED, EXECUTED
    persisted_path: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)


class HeartbeatTickReport(BaseModel):
    """Summary of actions taken during a heartbeat cycle."""
    tick_id: str = Field(default_factory=lambda: f"TICK-{uuid.uuid4().hex[:8].upper()}")
    scanned_pods: List[str] = Field(default_factory=list)
    detected_opportunities: int = 0
    proposals_generated: List[HeartbeatProposal] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class HeartbeatDaemon:
    """
    Background initiator activating Pod Leads to take autonomous, unprompted action.
    """

    def __init__(self, proposals_dir: Optional[Path] = None):
        self.proposals_dir = proposals_dir or (CONFIG.workspace_root / "Omniverse" / "proposals")
        self.proposals_dir.mkdir(parents=True, exist_ok=True)

    def run_heartbeat_cycle(self) -> HeartbeatTickReport:
        """
        Execute one proactive assessment tick across all departmental pods.
        """
        pods = ["Growth Squad", "Web Engineering", "DevOps SRE", "Security Pod"]
        proposals: List[HeartbeatProposal] = []

        # Example: Growth Pod assesses corridor conversion performance
        growth_rfc = HeartbeatProposal(
            origin_pod="Growth Squad",
            lead_agent_id="growth_meta_buyer",
            title="Accelerate East-to-West Route Corridor Conversions via Declarative Banners",
            problem_statement="East-to-West auto transport routes (FL->CA, NY->TX) experience a 2.4% conversion drop on mobile devices due to unanchored rate cards.",
            proposed_solution="Deploy compiled SceneGraph reactive banners with instant quote lock and zero-drift rate transparency.",
            impacted_pods=["Growth Squad", "Web Engineering", "DevOps SRE"],
            estimated_credit_cost=18.5
        )

        # Persist markdown RFC file in Omniverse/proposals/
        rfc_filename = f"{growth_rfc.rfc_id}_{growth_rfc.title.lower()[:30].replace(' ', '_')}.md"
        rfc_file = self.proposals_dir / rfc_filename

        md_content = f"""# 📜 {growth_rfc.rfc_id}: {growth_rfc.title}
*Proposed by `{growth_rfc.lead_agent_id}` ({growth_rfc.origin_pod}) on {growth_rfc.created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}*
*Status: `{growth_rfc.status}` | Budget Cost: `{growth_rfc.estimated_credit_cost}` Credits*

---

## 1. Problem Statement
{growth_rfc.problem_statement}

## 2. Proposed Solution & Architecture
{growth_rfc.proposed_solution}

## 3. Impacted Departments & Pods
{", ".join(growth_rfc.impacted_pods)}

## 4. Governance & Voting
- **Growth Squad:** `PENDING`
- **Web Engineering:** `PENDING`
- **DevOps SRE:** `PENDING`
"""
        rfc_file.write_text(md_content, encoding="utf-8")
        growth_rfc.persisted_path = str(rfc_file)
        proposals.append(growth_rfc)

        return HeartbeatTickReport(
            scanned_pods=pods,
            detected_opportunities=len(proposals),
            proposals_generated=proposals
        )
