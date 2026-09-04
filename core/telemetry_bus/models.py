"""
Data models for Closed-Loop Telemetry Ingestion and Autonomous Incident Triggers.
"""

import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class TelemetryMetricEvent(BaseModel):
    """Raw metric observation emitted from production or testing environments."""
    metric_id: str = Field(default_factory=lambda: f"MET-{uuid.uuid4().hex[:8].upper()}")
    subsystem: str  # e.g. "quote_calculator", "marketing_funnel", "litespeed_cdn"
    metric_name: str  # e.g. "conversion_rate", "p95_latency_ms", "5xx_error_rate"
    current_value: float
    threshold: float
    operator: str = "<"  # "<" means breach if current < threshold, ">" means breach if current > threshold
    severity: str = "WARNING"  # INFO, WARNING, CRITICAL
    raw_payload: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    @property
    def is_breach(self) -> bool:
        if self.operator == "<":
            return self.current_value < self.threshold
        elif self.operator == ">":
            return self.current_value > self.threshold
        elif self.operator == "<=":
            return self.current_value <= self.threshold
        elif self.operator == ">=":
            return self.current_value >= self.threshold
        elif self.operator == "==":
            return self.current_value == self.threshold
        return False


class IncidentTrigger(BaseModel):
    """Automated incident dispatch ticket generated from telemetry breach."""
    incident_id: str = Field(default_factory=lambda: f"INC-{uuid.uuid4().hex[:8].upper()}")
    source_metric_id: str
    subsystem: str
    severity: str
    title: str
    description: str
    target_pod: str  # "growth", "devops", "engineering", "security"
    assigned_dri: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
