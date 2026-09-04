"""
Unit tests for DAG Runner and Atomic SQLite Checkpointer.
"""

import asyncio
import tempfile
import unittest
from pathlib import Path

from core.runtime.models import (
    ExecutionTicket,
    TaskNode,
    TaskEdge,
    TaskStatus,
    TicketPriority,
)
from core.runtime.checkpointer import Checkpointer
from core.runtime.dag_runner import DAGRunner, DAGValidationError


class TestDAGAndCheckpointer(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_checkpoints.sqlite"
        self.checkpointer = Checkpointer(self.db_path)
        self.runner = DAGRunner(self.checkpointer)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_checkpointer_ticket_lifecycle(self):
        ticket = ExecutionTicket(
            title="Test Ticket",
            description="Testing Checkpointer persistence",
            priority=TicketPriority.MEDIUM,
            dri_agent_id="web_frontend_julian_thorne"
        )
        self.checkpointer.save_ticket(ticket)

        loaded = self.checkpointer.get_ticket(ticket.ticket_id)
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.title, "Test Ticket")
        self.assertEqual(loaded.dri_agent_id, "web_frontend_julian_thorne")
        self.assertEqual(loaded.status, TaskStatus.PENDING)

    def test_checkpointer_transitions_and_snapshots(self):
        ticket = ExecutionTicket(title="Snapshot Test", description="Testing snapshots")
        self.checkpointer.save_ticket(ticket)

        log = self.checkpointer.log_transition(
            ticket_id=ticket.ticket_id,
            node_id="node_1",
            agent_id="test_agent",
            from_state=TaskStatus.PENDING,
            to_state=TaskStatus.RUNNING,
            metadata={"step": 1}
        )
        self.assertEqual(log.to_state, TaskStatus.RUNNING)

        snapshot = self.checkpointer.create_snapshot(
            ticket_id=ticket.ticket_id,
            node_id="node_1",
            global_context={"env": "test"},
            completed_nodes=["node_1"],
            node_outputs={"node_1": {"out": "ok"}},
            active_agents=["test_agent"]
        )
        self.assertIsNotNone(snapshot.snapshot_id)

        latest = self.checkpointer.get_latest_snapshot(ticket.ticket_id)
        self.assertEqual(latest.snapshot_id, snapshot.snapshot_id)
        self.assertEqual(latest.completed_node_ids, ["node_1"])

        # Test rollback
        rolled = self.checkpointer.rollback(ticket.ticket_id, snapshot.snapshot_id)
        self.assertEqual(rolled.snapshot_id, snapshot.snapshot_id)

    def test_dag_cycle_detection(self):
        nodes = {
            "A": TaskNode(id="A", name="Node A", agent_id="agent_a", dependencies={"B"}),
            "B": TaskNode(id="B", name="Node B", agent_id="agent_b", dependencies={"A"}),
        }
        with self.assertRaises(DAGValidationError):
            self.runner.validate_graph(nodes, [])

    async def test_dag_successful_execution(self):
        ticket = ExecutionTicket(title="DAG Run Test", description="Linear DAG")
        
        async def handler_a(inputs, ctx):
            return {"val_a": 10}

        async def handler_b(inputs, ctx):
            dep_out = inputs.get("_dependency_outputs", {}).get("A", {})
            return {"val_b": dep_out.get("val_a", 0) * 2}

        nodes = {
            "A": TaskNode(id="A", name="Node A", agent_id="agent_a", handler=handler_a),
            "B": TaskNode(id="B", name="Node B", agent_id="agent_b", dependencies={"A"}, handler=handler_b),
        }

        state = await self.runner.execute_workflow(ticket, nodes)
        self.assertTrue(state.is_completed)
        self.assertIn("A", state.completed_nodes)
        self.assertIn("B", state.completed_nodes)
        self.assertEqual(nodes["B"].outputs["val_b"], 20)

    async def test_dag_retry_and_failure(self):
        ticket = ExecutionTicket(title="DAG Retry Test", description="Testing retries")
        attempts = 0

        async def failing_handler(inputs, ctx):
            nonlocal attempts
            attempts += 1
            if attempts < 2:
                raise ValueError("Transient network blip")
            return {"recovered": True}

        nodes = {
            "retry_node": TaskNode(
                id="retry_node",
                name="Retry Node",
                agent_id="agent_retry",
                retry_limit=2,
                handler=failing_handler
            )
        }

        state = await self.runner.execute_workflow(ticket, nodes)
        self.assertTrue(state.is_completed)
        self.assertEqual(attempts, 2)
        self.assertEqual(nodes["retry_node"].retry_count, 1)


if __name__ == "__main__":
    unittest.main()
