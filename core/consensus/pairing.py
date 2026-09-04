"""
Agent Pair Registry for Communicative De-Hallucination Loops.
Pre-configures dual-agent verification partnerships across Omniverse departments.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class AgentPair(BaseModel):
    """Pair specification binding a Producer agent to a Reviewer/Auditor agent."""
    pair_id: str
    domain: str
    producer_agent_id: str
    reviewer_agent_id: str
    default_checklist: List[str] = Field(default_factory=list)
    max_review_rounds: int = 3


# Standard Enterprise Pairings conforming to ChatDev & Silicon Valley Review Standards
ENTERPRISE_PAIRS: Dict[str, AgentPair] = {
    "frontend_ui_pair": AgentPair(
        pair_id="frontend_ui_pair",
        domain="Frontend & UI Architecture",
        producer_agent_id="web_frontend_julian_thorne",
        reviewer_agent_id="frontend_a11y",
        default_checklist=[
            "Zero mid-word typography wrapping (break-normal, atomic whitespace-nowrap)",
            "Responsive layout across 320px to 2560px viewports",
            "Touch target size >= 48px on mobile controls",
            "Non-copyable styling with text input whitelist"
        ]
    ),
    "devops_security_pair": AgentPair(
        pair_id="devops_security_pair",
        domain="DevOps & Infrastructure Security",
        producer_agent_id="web_devops_marcus_chen",
        reviewer_agent_id="security_ciso_michael_chang",
        default_checklist=[
            "HSTS header present with max-age=31536000 and includeSubDomains",
            "Anti-Scraping / Bot-Ripper User-Agent block rules in .htaccess",
            "Zero plaintext credentials in repository or commit history",
            "LiteSpeed cache invalidation trigger configured"
        ]
    ),
    "growth_data_pair": AgentPair(
        pair_id="growth_data_pair",
        domain="Growth Strategy & Conversion Analytics",
        producer_agent_id="growth_meta_buyer",
        reviewer_agent_id="data_analyst_attribution",
        default_checklist=[
            "Target corridor list covers verified 50-state routes",
            "Primary CTA element is clearly demarcated with unique DOM id",
            "Zero-drift adherence (no simulated or mock metrics)",
            "CAPI conversion events mapped to server endpoints"
        ]
    ),
    "executive_cpo_pair": AgentPair(
        pair_id="executive_cpo_pair",
        domain="Executive Strategic Alignment",
        producer_agent_id="exec_ceo_alexander_vance",
        reviewer_agent_id="product_cpo_sarah_jenkins",
        default_checklist=[
            "Clear DRI ownership assigned per ticket",
            "Adherence to Google L3-L8 leveling standard",
            "Customer friction eliminated in quote funnel"
        ]
    )
}


def get_agent_pair(pair_id: str) -> Optional[AgentPair]:
    """Retrieve pre-configured agent pair."""
    return ENTERPRISE_PAIRS.get(pair_id)
