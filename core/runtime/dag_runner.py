"""
Asynchronous Directed Acyclic Graph (DAG) Execution Engine.
Provides deterministic topological scheduling, concurrent node dispatch, retry loops,
and atomic checkpointing.
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Set, Optional, Any, Callable
from collections import defaultdict, deque

from core.runtime.models import (
    TaskNode,
    TaskEdge,
    TaskStatus,
    WorkflowState,
    ExecutionTicket,
    ExecutionSnapshot,
)
from core.runtime.checkpointer import Checkpointer

logger = logging.getLogger("Omniverse.DAGRunner")


class DAGValidationError(Exception):
    """Raised when DAG graph contains cycles or unresolved dependencies."""
    pass


class DAGRunner:
    """
    Deterministic Async DAG Runner for multi-agent workflows.
    """

    def __init__(self, checkpointer: Optional[Checkpointer] = None):
        self.checkpointer = checkpointer or Checkpointer()

    def validate_graph(self, nodes: Dict[str, TaskNode], edges: List[TaskEdge]) -> List[str]:
        """
        Validate DAG for cycles and return topological ordering using Kahn's algorithm.
        """
        in_degree: Dict[str, int] = {node_id: 0 for node_id in nodes}
        adj_list: Dict[str, List[str]] = defaultdict(list)

        # Build graph structure from dependencies and explicit edges
        for node_id, node in nodes.items():
            for dep_id in node.dependencies:
                if dep_id not in nodes:
                    raise DAGValidationError(f"Node '{node_id}' depends on non-existent node '{dep_id}'.")
                adj_list[dep_id].append(node_id)
                in_degree[node_id] += 1

        for edge in edges:
            if edge.source_id not in nodes or edge.target_id not in nodes:
                raise DAGValidationError(f"Edge ({edge.source_id} -> {edge.target_id}) references non-existent node.")
            if edge.target_id not in adj_list[edge.source_id]:
                adj_list[edge.source_id].append(edge.target_id)
                in_degree[edge.target_id] += 1

        # Queue of nodes with 0 dependencies
        zero_in_degree = deque([node_id for node_id, deg in in_degree.items() if deg == 0])
        topological_order: List[str] = []

        while zero_in_degree:
            curr = zero_in_degree.popleft()
            topological_order.append(curr)
            for neighbor in adj_list[curr]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    zero_in_degree.append(neighbor)

        if len(topological_order) != len(nodes):
            unresolved = [n for n, deg in in_degree.items() if deg > 0]
            raise DAGValidationError(f"Cyclic dependency detected involving nodes: {unresolved}")

        return topological_order

    async def execute_workflow(
        self,
        ticket: ExecutionTicket,
        nodes: Dict[str, TaskNode],
        edges: Optional[List[TaskEdge]] = None,
        initial_context: Optional[Dict[str, Any]] = None,
    ) -> WorkflowState:
        """
        Execute an entire multi-agent workflow DAG with atomic checkpointing and retries.
        """
        edges = edges or []
        # Validate topological ordering first
        topological_order = self.validate_graph(nodes, edges)

        # Save ticket in checkpointer
        ticket.status = TaskStatus.RUNNING
        self.checkpointer.save_ticket(ticket)

        state = WorkflowState(
            ticket=ticket,
            nodes=nodes,
            edges=edges,
            context=initial_context or {},
            completed_nodes=set(),
            failed_nodes=set(),
        )

        # Node dependency map
        node_dependencies: Dict[str, Set[str]] = {
            node_id: set(node.dependencies) for node_id, node in nodes.items()
        }
        for edge in edges:
            node_dependencies[edge.target_id].add(edge.source_id)

        # Active tracking
        pending_nodes: Set[str] = set(nodes.keys())
        running_tasks: Dict[str, asyncio.Task] = {}
        node_outputs: Dict[str, Any] = {}

        while pending_nodes or running_tasks:
            # Find all nodes that are READY (all dependencies completed successfully)
            ready_nodes = [
                nid for nid in pending_nodes
                if node_dependencies[nid].issubset(state.completed_nodes) and nid not in running_tasks
            ]

            # Dispatch ready nodes concurrently
            for node_id in ready_nodes:
                node = nodes[node_id]
                pending_nodes.remove(node_id)
                
                # Gather inputs from dependency outputs
                dep_inputs = {
                    dep: node_outputs.get(dep, {})
                    for dep in node_dependencies[node_id]
                }
                combined_inputs = {**state.context, **node.inputs, "_dependency_outputs": dep_inputs}
                node.inputs = combined_inputs

                task = asyncio.create_task(
                    self._execute_node_with_retry(ticket.ticket_id, node, state.context)
                )
                running_tasks[node_id] = task

            if not running_tasks:
                # If there are pending nodes but nothing can run, we have blocked tasks
                if pending_nodes:
                    state.error = f"Workflow stalled. Blocked pending nodes: {list(pending_nodes)}"
                    for nid in pending_nodes:
                        nodes[nid].status = TaskStatus.BLOCKED
                    break
                else:
                    break

            # Wait for at least one running task to complete
            done, _ = await asyncio.wait(
                running_tasks.values(),
                return_when=asyncio.FIRST_COMPLETED
            )

            # Process completed tasks
            for node_id, task in list(running_tasks.items()):
                if task in done:
                    del running_tasks[node_id]
                    try:
                        node_result = await task
                        node_outputs[node_id] = node_result.outputs
                        state.completed_nodes.add(node_id)
                        
                        # Create checkpoint snapshot
                        snapshot = self.checkpointer.create_snapshot(
                            ticket_id=ticket.ticket_id,
                            node_id=node_id,
                            global_context=state.context,
                            completed_nodes=list(state.completed_nodes),
                            node_outputs=node_outputs,
                            active_agents=[n.agent_id for n in nodes.values() if n.status == TaskStatus.SUCCESS]
                        )
                        state.current_snapshot_id = snapshot.snapshot_id
                        
                    except Exception as exc:
                        state.failed_nodes.add(node_id)
                        nodes[node_id].status = TaskStatus.FAILED
                        nodes[node_id].error = str(exc)
                        state.error = f"Execution failed at node '{node_id}' ({nodes[node_id].agent_id}): {exc}"
                        logger.error(state.error)
                        
                        # Mark downstream dependencies as SKIPPED
                        self._cascade_skip(node_id, nodes, edges, pending_nodes)
                        break

            if state.failed_nodes:
                break

        # Finalize workflow state
        if not state.failed_nodes and not state.error:
            state.is_completed = True
            ticket.status = TaskStatus.SUCCESS
        else:
            ticket.status = TaskStatus.FAILED

        self.checkpointer.save_ticket(ticket)
        return state

    async def _execute_node_with_retry(
        self,
        ticket_id: str,
        node: TaskNode,
        global_context: Dict[str, Any]
    ) -> TaskNode:
        """
        Execute an individual TaskNode with exponential backoff and transition logging.
        """
        node.start_time = datetime.utcnow()
        self.checkpointer.log_transition(
            ticket_id=ticket_id,
            node_id=node.id,
            agent_id=node.agent_id,
            from_state=node.status,
            to_state=TaskStatus.RUNNING
        )
        node.status = TaskStatus.RUNNING

        attempt = 0
        last_error: Optional[Exception] = None

        while attempt <= node.retry_limit:
            attempt += 1
            node.retry_count = attempt - 1
            try:
                if node.handler is None:
                    # Default mock-free pass-through execution
                    outputs = {"status": "SUCCESS", "message": f"Default handler executed by {node.agent_id}"}
                elif asyncio.iscoroutinefunction(node.handler):
                    outputs = await asyncio.wait_for(
                        node.handler(node.inputs, global_context),
                        timeout=node.timeout_seconds
                    )
                else:
                    outputs = node.handler(node.inputs, global_context)

                node.outputs = outputs if isinstance(outputs, dict) else {"result": outputs}
                node.status = TaskStatus.SUCCESS
                node.end_time = datetime.utcnow()

                self.checkpointer.log_transition(
                    ticket_id=ticket_id,
                    node_id=node.id,
                    agent_id=node.agent_id,
                    from_state=TaskStatus.RUNNING,
                    to_state=TaskStatus.SUCCESS,
                    metadata={"attempt": attempt}
                )
                self.checkpointer.record_node_execution(ticket_id, node)
                return node

            except Exception as exc:
                last_error = exc
                logger.warning(
                    f"Node '{node.id}' attempt {attempt}/{node.retry_limit + 1} failed: {exc}"
                )
                if attempt <= node.retry_limit:
                    backoff = 0.1 * (2 ** (attempt - 1))
                    await asyncio.sleep(backoff)

        # Max retries exhausted
        node.status = TaskStatus.FAILED
        node.error = str(last_error)
        node.end_time = datetime.utcnow()

        self.checkpointer.log_transition(
            ticket_id=ticket_id,
            node_id=node.id,
            agent_id=node.agent_id,
            from_state=TaskStatus.RUNNING,
            to_state=TaskStatus.FAILED,
            metadata={"error": str(last_error), "attempts": attempt}
        )
        self.checkpointer.record_node_execution(ticket_id, node)
        raise last_error or RuntimeError(f"Node '{node.id}' failed execution.")

    def _cascade_skip(
        self,
        failed_node_id: str,
        nodes: Dict[str, TaskNode],
        edges: List[TaskEdge],
        pending_nodes: Set[str]
    ) -> None:
        """Mark all transitive downstream dependents of a failed node as SKIPPED."""
        adj = defaultdict(list)
        for n in nodes.values():
            for d in n.dependencies:
                adj[d].append(n.id)
        for e in edges:
            adj[e.source_id].append(e.target_id)

        queue = deque([failed_node_id])
        while queue:
            curr = queue.popleft()
            for dep_target in adj[curr]:
                if dep_target in pending_nodes:
                    pending_nodes.remove(dep_target)
                    nodes[dep_target].status = TaskStatus.SKIPPED
                    queue.append(dep_target)
