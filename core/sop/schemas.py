"""
Canonical Input/Output Schemas for Departmental SOP Handoffs.
Guarantees zero manual re-formatting between upstream producers and downstream consumers.
"""

import uuid
from enum import Enum
from datetime import datetime
from typing import Dict, List, Optional, Any, Set
from pydantic import BaseModel, Field


class SOPStage(str, Enum):
    """Lifecycle stages in the enterprise SOP state machine."""
    INTAKE = "INTAKE"
    PRD_SPEC = "PRD_SPEC"
    SYSTEM_DESIGN = "SYSTEM_DESIGN"
    CODE_IMPLEMENTATION = "CODE_IMPLEMENTATION"
    PAIR_REVIEW = "PAIR_REVIEW"
    PRODUCTION_DEPLOYMENT = "PRODUCTION_DEPLOYMENT"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class GrowthPRD(BaseModel):
    """Output of Growth Squad -> Direct input to Architecture & Engineering."""
    prd_id: str = Field(default_factory=lambda: f"PRD-{uuid.uuid4().hex[:8].upper()}")
    feature_name: str
    target_kpi: str
    target_corridors: List[str] = Field(default_factory=list)
    cta_text: str = "Instant Quote"
    user_pain_points: List[str] = Field(default_factory=list)
    required_dom_elements: List[str] = Field(default_factory=list)
    author: str = "growth_meta_buyer"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class EngineeringDesign(BaseModel):
    """Output of Principal Architect -> Direct input to Specialist Developers."""
    design_id: str = Field(default_factory=lambda: f"DES-{uuid.uuid4().hex[:8].upper()}")
    prd_ref: str
    affected_files: List[str] = Field(default_factory=list)
    component_tree: List[str] = Field(default_factory=list)
    css_tokens: Dict[str, str] = Field(default_factory=dict)
    state_mutations: List[str] = Field(default_factory=list)
    lead_architect: str = "web_frontend_julian_thorne"


class ImplementationBundle(BaseModel):
    """Output of Developers -> Direct input to QA & Reviewers."""
    bundle_id: str = Field(default_factory=lambda: f"BND-{uuid.uuid4().hex[:8].upper()}")
    design_ref: str
    files_modified: Dict[str, str] = Field(default_factory=dict)  # filepath -> new content
    css_changes: List[str] = Field(default_factory=list)
    syntax_validated: bool = True
    developer_agent: str = "web_frontend_julian_thorne"


class QualityAuditSignoff(BaseModel):
    """Output of QA & Dual-Agent Reviewers -> Direct input to DevOps."""
    audit_id: str = Field(default_factory=lambda: f"AUD-{uuid.uuid4().hex[:8].upper()}")
    bundle_ref: str
    checklist_passed: Dict[str, bool] = Field(default_factory=dict)
    unresolved_defects: List[str] = Field(default_factory=list)
    quality_gate_passed: bool = True
    reviewer_agent: str = "qa_auto_script"
    signoff_token: str = Field(default_factory=lambda: f"TOKEN-{uuid.uuid4().hex[:10].upper()}")


class DeploymentReceipt(BaseModel):
    """Output of DevOps -> Direct input to CEO & Executive Suite."""
    receipt_id: str = Field(default_factory=lambda: f"REC-{uuid.uuid4().hex[:8].upper()}")
    audit_ref: str
    deployment_status: str = "SUCCESS"
    synced_routes: int = 2806
    cache_purged: bool = True
    live_url: str = "https://www.skyautoservices.com"
    devops_engineer: str = "web_devops_marcus_chen"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
