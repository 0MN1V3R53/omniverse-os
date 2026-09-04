"""
Enterprise Workflow Orchestrator implementing cascading pod delegation
and deterministic multi-agent execution lifecycles.
"""

from typing import Dict, List, Optional, Any, Callable
from core.runtime.models import (
    ExecutionTicket,
    TaskNode,
    TaskEdge,
    TaskStatus,
    WorkflowState,
    TicketPriority,
)
from core.runtime.dag_runner import DAGRunner
from core.runtime.checkpointer import Checkpointer


class WorkflowOrchestrator:
    """
    High-level orchestrator for composing, validating, and running multi-agent
    enterprise workflows conforming to the Omniverse Pod hierarchy.
    """

    def __init__(self, checkpointer: Optional[Checkpointer] = None):
        self.checkpointer = checkpointer or Checkpointer()
        self.runner = DAGRunner(self.checkpointer)

    def create_linear_pipeline(
        self,
        ticket: ExecutionTicket,
        steps: List[Dict[str, Any]],
        context: Optional[Dict[str, Any]] = None,
    ) -> WorkflowState:
        """
        Create and build a linear sequence of agent nodes.
        `steps` format: [
            {"id": "spec", "name": "Growth Spec", "agent_id": "growth_meta_buyer", "handler": fn},
            {"id": "build", "name": "Frontend Build", "agent_id": "web_frontend_julian_thorne", "handler": fn},
            ...
        ]
        """
        nodes: Dict[str, TaskNode] = {}
        edges: List[TaskEdge] = []
        prev_node_id: Optional[str] = None

        for step in steps:
            node_id = step["id"]
            deps = set(step.get("dependencies", []))
            if prev_node_id and not deps:
                deps.add(prev_node_id)

            node = TaskNode(
                id=node_id,
                name=step.get("name", node_id),
                agent_id=step["agent_id"],
                description=step.get("description"),
                dependencies=deps,
                retry_limit=step.get("retry_limit", 2),
                timeout_seconds=step.get("timeout_seconds", 30.0),
                inputs=step.get("inputs", {}),
                handler=step.get("handler")
            )
            nodes[node_id] = node

            if prev_node_id:
                edges.append(TaskEdge(source_id=prev_node_id, target_id=node_id))
            prev_node_id = node_id

        return WorkflowState(
            ticket=ticket,
            nodes=nodes,
            edges=edges,
            context=context or {}
        )

    async def run(
        self,
        ticket: ExecutionTicket,
        nodes: Dict[str, TaskNode],
        edges: Optional[List[TaskEdge]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> WorkflowState:
        """Execute the workflow through the DAG runner."""
        return await self.runner.execute_workflow(
            ticket=ticket,
            nodes=nodes,
            edges=edges,
            initial_context=context or {}
        )
