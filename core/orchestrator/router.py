"""
Dynamic Task Delegation & Pod Lead Decomposition Engine.
Enables Pod Managers to decompose high-level business goals and dispatch atomic sub-tasks.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from core.bus.models import TaskTicket
from core.agents.loader import AgentLoader, OmniverseAgent


class PodTaskDecomposition(BaseModel):
    """Decomposition blueprint produced by a Pod Lead."""
    goal_id: str
    goal_title: str
    lead_agent_id: str
    target_pod: str
    subtasks: List[TaskTicket] = Field(default_factory=list)


class DynamicRouter:
    """
    Dynamic task router and pod lead decomposition engine.
    """

    def __init__(self, loader: Optional[AgentLoader] = None):
        self.loader = loader or AgentLoader()
        self.agents = self.loader.load_all_agents()

    def decompose_goal(
        self,
        goal_id: str,
        goal_title: str,
        lead_agent_id: str,
        target_pod: str
    ) -> PodTaskDecomposition:
        """
        Decompose a high-level goal into domain-specialized subtasks based on pod hierarchy.
        """
        subtasks: List[TaskTicket] = []

        if target_pod in ("growth", "marketing"):
            subtasks.extend([
                TaskTicket(
                    title=f"Define Conversion Funnel & Target Corridors for {goal_title}",
                    assigned_agent_id="growth_meta_buyer",
                    assigned_pod="Growth Squad",
                    action_items=["Analyze 50-state routes", "Set up CAPI conversion events", "Draft copy spec"]
                ),
                TaskTicket(
                    title=f"Verify Attribution Telemetry for {goal_title}",
                    assigned_agent_id="data_analyst_attribution",
                    assigned_pod="Data Science",
                    dependencies=["growth_meta_buyer"],
                    action_items=["Verify analytics payload", "Validate zero-drift data constraints"]
                ),
            ])
        elif target_pod in ("engineering", "frontend", "web"):
            subtasks.extend([
                TaskTicket(
                    title=f"System Architecture & Token Specification for {goal_title}",
                    assigned_agent_id="web_frontend_julian_thorne",
                    assigned_pod="Web Frontend",
                    action_items=["Design responsive component layout", "Define non-copyable CSS rules"]
                ),
                TaskTicket(
                    title=f"Implement Component Code & Micro-Interactions for {goal_title}",
                    assigned_agent_id="frontend_component_dev",
                    assigned_pod="Web Frontend",
                    dependencies=["web_frontend_julian_thorne"],
                    action_items=["Write React component", "Integrate quote calculator form fields"]
                ),
                TaskTicket(
                    title=f"Accessibility & Typography Review for {goal_title}",
                    assigned_agent_id="frontend_a11y",
                    assigned_pod="QA & A11y",
                    dependencies=["frontend_component_dev"],
                    action_items=["Ensure zero mid-word typography wrapping", "Verify touch targets >= 48px"]
                ),
            ])
        elif target_pod in ("devops", "infrastructure"):
            subtasks.extend([
                TaskTicket(
                    title=f"Configure Security Headers & Scraper Defense for {goal_title}",
                    assigned_agent_id="security_ciso_michael_chang",
                    assigned_pod="Security",
                    action_items=["Verify HSTS max-age=31536000", "Inject Apache ripper blocking rules"]
                ),
                TaskTicket(
                    title=f"Build Static Export & Purge CDN for {goal_title}",
                    assigned_agent_id="web_devops_marcus_chen",
                    assigned_pod="DevOps SRE",
                    dependencies=["security_ciso_michael_chang"],
                    action_items=["Execute static build", "Deploy via rsync", "Purge LiteSpeed cache"]
                ),
            ])
        else:
            # General Enterprise fallback
            subtasks.append(
                TaskTicket(
                    title=f"Execute Strategic Initiative: {goal_title}",
                    assigned_agent_id=lead_agent_id,
                    assigned_pod=target_pod,
                    action_items=["Execute initiative per standard operating procedure"]
                )
            )

        return PodTaskDecomposition(
            goal_id=goal_id,
            goal_title=goal_title,
            lead_agent_id=lead_agent_id,
            target_pod=target_pod,
            subtasks=subtasks
        )
