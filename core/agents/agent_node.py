"""
Agent Task Node Builder for DAG Graph Integration.
Wraps an agent with their system prompt, tools, and execution handler.
"""

from typing import Dict, Any, Optional, Callable, Set
from core.runtime.models import TaskNode, TaskStatus
from core.agents.loader import AgentLoader, OmniverseAgent
from core.tools.harness import GuardedToolHarness


def create_agent_task_node(
    node_id: str,
    name: str,
    agent_id: str,
    handler: Callable,
    dependencies: Optional[Set[str]] = None,
    timeout_seconds: float = 30.0,
    retry_limit: int = 2,
    inputs: Optional[Dict[str, Any]] = None,
    loader: Optional[AgentLoader] = None,
) -> TaskNode:
    """
    Factory function to instantiate an agent-backed DAG TaskNode.
    """
    agent_loader = loader or AgentLoader()
    agent_profile = agent_loader.load_agent(agent_id)

    node_inputs = inputs or {}
    if agent_profile:
        node_inputs["_agent_name"] = agent_profile.name
        node_inputs["_agent_role"] = agent_profile.role
        node_inputs["_agent_level"] = agent_profile.level

    return TaskNode(
        id=node_id,
        name=name,
        agent_id=agent_id,
        description=f"Task executed by {agent_profile.name if agent_profile else agent_id} ({agent_id})",
        dependencies=dependencies or set(),
        retry_limit=retry_limit,
        timeout_seconds=timeout_seconds,
        inputs=node_inputs,
        handler=handler
    )
