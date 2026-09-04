"""
Distributed Local Tracing Engine.
Generates OpenTelemetry-compatible spans and parent-child causality graphs for multi-agent workflows.
"""

import json
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

from core.config import CONFIG


class Span(BaseModel):
    """An individual operation span within a workflow trace."""
    span_id: str = Field(default_factory=lambda: f"span_{uuid.uuid4().hex[:12]}")
    trace_id: str
    parent_span_id: Optional[str] = None
    name: str
    agent_id: str
    start_time: datetime = Field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = None
    duration_ms: float = 0.0
    status: str = "OK"  # "OK" or "ERROR"
    error_message: Optional[str] = None
    attributes: Dict[str, Any] = Field(default_factory=dict)
    events: List[Dict[str, Any]] = Field(default_factory=list)

    def add_event(self, name: str, payload: Optional[Dict[str, Any]] = None):
        self.events.append({
            "name": name,
            "timestamp": datetime.utcnow().isoformat(),
            "payload": payload or {}
        })

    def finish(self, status: str = "OK", error: Optional[str] = None):
        self.end_time = datetime.utcnow()
        self.duration_ms = round((self.end_time - self.start_time).total_seconds() * 1000.0, 2)
        self.status = status
        self.error_message = error


class Trace(BaseModel):
    """Complete trace graph for an entire ticket execution."""
    trace_id: str = Field(default_factory=lambda: f"tr_{uuid.uuid4().hex[:16]}")
    ticket_id: str
    name: str
    spans: List[Span] = Field(default_factory=list)
    start_time: datetime = Field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = None
    total_duration_ms: float = 0.0


class LocalTracer:
    """
    Local filesystem tracer appending trace records to JSONL log.
    """

    def __init__(self, log_path: Optional[Path] = None):
        self.log_path = log_path or CONFIG.traces_log_path
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.active_traces: Dict[str, Trace] = {}

    def start_trace(self, ticket_id: str, name: str) -> Trace:
        """Initialize a new trace for a ticket."""
        trace = Trace(ticket_id=ticket_id, name=name)
        self.active_traces[trace.trace_id] = trace
        return trace

    def start_span(
        self,
        trace_id: str,
        name: str,
        agent_id: str,
        parent_span_id: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None
    ) -> Span:
        """Create a new child span within a trace."""
        span = Span(
            trace_id=trace_id,
            name=name,
            agent_id=agent_id,
            parent_span_id=parent_span_id,
            attributes=attributes or {}
        )
        if trace_id in self.active_traces:
            self.active_traces[trace_id].spans.append(span)
        return span

    def end_span(self, span: Span, status: str = "OK", error: Optional[str] = None) -> None:
        """Close an active span."""
        span.finish(status=status, error=error)

    def finish_trace(self, trace_id: str) -> Optional[Trace]:
        """Finalize and persist a trace to disk."""
        trace = self.active_traces.pop(trace_id, None)
        if not trace:
            return None

        trace.end_time = datetime.utcnow()
        trace.total_duration_ms = round((trace.end_time - trace.start_time).total_seconds() * 1000.0, 2)

        # Append to JSONL
        trace_dict = trace.model_dump() if hasattr(trace, "model_dump") else trace.dict()
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(trace_dict, default=str) + "\n")

        return trace

    def render_ascii_tree(self, trace: Trace) -> str:
        """Generate human-readable ASCII hierarchy of delegation spans."""
        lines = [f"Trace: {trace.name} (Ticket: {trace.ticket_id}, Total: {trace.total_duration_ms}ms)"]
        
        # Group by parent
        children_map: Dict[Optional[str], List[Span]] = {}
        for sp in trace.spans:
            children_map.setdefault(sp.parent_span_id, []).append(sp)

        def print_subtree(parent_id: Optional[str], depth: int = 0):
            for child in children_map.get(parent_id, []):
                indent = "  " * depth + "└── "
                status_glyph = "✅" if child.status == "OK" else "❌"
                lines.append(f"{indent}{status_glyph} [{child.agent_id}] {child.name} ({child.duration_ms}ms)")
                print_subtree(child.span_id, depth + 1)

        print_subtree(None)
        return "\n".join(lines)
