"""
Closed-Loop Telemetry Ingestion and Incident Automation Package.
Ingests real-time telemetry streams and automatically triggers multi-agent remediation tickets.
"""

from .models import (
    TelemetryMetricEvent,
    IncidentTrigger,
)
from .monitor import ClosedLoopTelemetryMonitor

__all__ = [
    "TelemetryMetricEvent",
    "IncidentTrigger",
    "ClosedLoopTelemetryMonitor",
]
