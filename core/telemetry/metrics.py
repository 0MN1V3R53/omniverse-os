"""
Execution Metrics and Token Consumption Tracker for Multi-Agent Workflows.
"""

from datetime import datetime
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field


class AgentMetric(BaseModel):
    agent_id: str
    invocations: int = 0
    estimated_input_tokens: int = 0
    estimated_output_tokens: int = 0
    total_execution_ms: float = 0.0
    tool_calls: int = 0
    errors: int = 0


class ExecutionMetricsTracker:
    """
    Accumulates runtime telemetry, calculates token throughput, and provides SLA analytics.
    """

    def __init__(self):
        self.agent_metrics: Dict[str, AgentMetric] = {}
        self.start_time: datetime = datetime.utcnow()
        self.end_time: Optional[datetime] = None

    def record_agent_turn(
        self,
        agent_id: str,
        input_tokens: int,
        output_tokens: int,
        execution_ms: float,
        tool_calls: int = 0,
        has_error: bool = False
    ) -> None:
        """Record an execution step for an agent."""
        if agent_id not in self.agent_metrics:
            self.agent_metrics[agent_id] = AgentMetric(agent_id=agent_id)

        m = self.agent_metrics[agent_id]
        m.invocations += 1
        m.estimated_input_tokens += input_tokens
        m.estimated_output_tokens += output_tokens
        m.total_execution_ms += execution_ms
        m.tool_calls += tool_calls
        if has_error:
            m.errors += 1

    def get_summary(self) -> Dict[str, Any]:
        """Compile holistic execution summary."""
        total_invocations = sum(m.invocations for m in self.agent_metrics.values())
        total_input_tokens = sum(m.estimated_input_tokens for m in self.agent_metrics.values())
        total_output_tokens = sum(m.estimated_output_tokens for m in self.agent_metrics.values())
        total_tool_calls = sum(m.tool_calls for m in self.agent_metrics.values())
        total_errors = sum(m.errors for m in self.agent_metrics.values())
        total_ms = sum(m.total_execution_ms for m in self.agent_metrics.values())

        return {
            "total_agents_involved": len(self.agent_metrics),
            "total_invocations": total_invocations,
            "total_input_tokens": total_input_tokens,
            "total_output_tokens": total_output_tokens,
            "total_tokens": total_input_tokens + total_output_tokens,
            "total_tool_calls": total_tool_calls,
            "total_errors": total_errors,
            "total_execution_ms": round(total_ms, 2),
            "agent_breakdown": {
                aid: m.model_dump() if hasattr(m, "model_dump") else m.dict()
                for aid, m in self.agent_metrics.items()
            }
        }
