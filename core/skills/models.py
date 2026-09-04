"""
Pydantic Data Models for Executable JIT Skill Vault.
"""

import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field


class JITSkill(BaseModel):
    """An executable Python/CLI skill compiled and registered by agents."""
    skill_id: str = Field(default_factory=lambda: f"SKILL-{uuid.uuid4().hex[:6].upper()}")
    name: str
    domain: str  # seo, web, devops, security, analytics, tooling
    description: str
    author_agent_id: str
    executable_path: str
    cli_command_template: str
    input_parameters: Dict[str, str] = Field(default_factory=dict)
    output_schema: Dict[str, str] = Field(default_factory=dict)
    invocations_count: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)


class SkillManifest(BaseModel):
    """Complete searchable catalog of JIT compiled skills."""
    version: str = "1.0.0"
    skills: List[JITSkill] = Field(default_factory=list)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
