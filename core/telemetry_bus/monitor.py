"""
Closed-Loop Telemetry Monitor & Autonomous Incident Dispatcher.
Detects runtime metric breaches and automatically fires emergency tickets on the MessageBus.
"""

from typing import Dict, List, Optional, Callable
from core.bus.bus import MessageBus, GLOBAL_MESSAGE_BUS
from core.bus.models import EventMessage, InfrastructureAlert, TaskTicket
from core.telemetry_bus.models import TelemetryMetricEvent, IncidentTrigger


class ClosedLoopTelemetryMonitor:
    """
    Monitors streaming metrics and dispatches automated incident tickets upon threshold breach.
    """

    def __init__(self, bus: Optional[MessageBus] = None):
        self.bus = bus or GLOBAL_MESSAGE_BUS
        self.incident_history: List[IncidentTrigger] = []

    async def ingest_metric(self, metric: TelemetryMetricEvent) -> Optional[IncidentTrigger]:
        """
        Ingest a telemetry metric and trigger autonomous remediation ticket if a threshold is breached.
        """
        if not metric.is_breach:
            return None

        # 1. Determine Pod routing based on subsystem & metric
        if "conversion" in metric.metric_name or "funnel" in metric.subsystem:
            target_pod = "growth"
            assigned_dri = "growth_meta_buyer"
            title = f"Conversion Funnel Anomaly Detected: {metric.metric_name} dropped to {metric.current_value}%"
        elif "security" in metric.subsystem or "scraper" in metric.metric_name:
            target_pod = "security"
            assigned_dri = "security_ciso_michael_chang"
            title = f"Security Perimeter Alert: {metric.metric_name} exceeded threshold ({metric.current_value})"
        else:
            target_pod = "devops"
            assigned_dri = "web_devops_marcus_chen"
            title = f"Infrastructure SRE Incident: {metric.metric_name} breached threshold ({metric.current_value})"

        incident = IncidentTrigger(
            source_metric_id=metric.metric_id,
            subsystem=metric.subsystem,
            severity=metric.severity,
            title=title,
            description=f"Observed value {metric.current_value} violated threshold {metric.threshold} ({metric.operator}). Emergency remediation required.",
            target_pod=target_pod,
            assigned_dri=assigned_dri
        )
        self.incident_history.append(incident)

        # 2. Publish InfrastructureAlert to MessageBus
        alert = InfrastructureAlert(
            severity=metric.severity,
            subsystem=metric.subsystem,
            error_message=incident.description,
            telemetry_snapshot={"metric": metric.metric_name, "value": metric.current_value, "threshold": metric.threshold}
        )
        await self.bus.publish(EventMessage.create(
            topic=f"incident.{target_pod}",
            sender_id="closed_loop_telemetry_monitor",
            payload_obj=alert,
            tags={target_pod, "incident", "alert"}
        ))

        # 3. Publish TaskTicket directly to assigned DRI agent
        ticket = TaskTicket(
            ticket_id=incident.incident_id,
            title=incident.title,
            assigned_agent_id=incident.assigned_dri,
            assigned_pod=incident.target_pod,
            action_items=[
                "Analyze root cause from telemetry payload",
                "Execute corrective SOP workflow",
                "Deploy fix and verify metric normalization"
            ]
        )
        await self.bus.publish(EventMessage.create(
            topic=f"tasks.{assigned_dri}",
            sender_id="closed_loop_telemetry_monitor",
            payload_obj=ticket,
            tags={target_pod, "ticket", "emergency"},
            target_agent=assigned_dri
        ))

        return incident
