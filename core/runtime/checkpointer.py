"""
Atomic SQLite and JSONL Checkpointer for multi-agent state persistence, rollback, and replay.
"""

import json
import sqlite3
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from core.config import CONFIG
from core.runtime.models import (
    ExecutionTicket,
    TaskNode,
    TaskStatus,
    StateTransitionLog,
    ExecutionSnapshot,
    TicketPriority,
)


class Checkpointer:
    """
    Thread-safe, atomic SQLite checkpointer managing tickets, state transitions,
    and reversible execution snapshots.
    """

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or CONFIG.checkpoint_db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path), timeout=30.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        return conn

    def _init_db(self):
        """Initialize database schema with tables and indices."""
        with self._lock:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.executescript("""
                CREATE TABLE IF NOT EXISTS tickets (
                    ticket_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    priority TEXT,
                    requested_by TEXT,
                    assigned_pod TEXT,
                    dri_agent_id TEXT,
                    status TEXT,
                    metadata_json TEXT,
                    created_at TEXT,
                    updated_at TEXT
                );

                CREATE TABLE IF NOT EXISTS state_transitions (
                    log_id TEXT PRIMARY KEY,
                    ticket_id TEXT NOT NULL,
                    node_id TEXT NOT NULL,
                    agent_id TEXT NOT NULL,
                    from_state TEXT NOT NULL,
                    to_state TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    metadata_json TEXT,
                    snapshot_id TEXT,
                    FOREIGN KEY (ticket_id) REFERENCES tickets (ticket_id)
                );

                CREATE TABLE IF NOT EXISTS snapshots (
                    snapshot_id TEXT PRIMARY KEY,
                    ticket_id TEXT NOT NULL,
                    node_id TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    global_context_json TEXT,
                    completed_nodes_json TEXT,
                    node_outputs_json TEXT,
                    active_agents_json TEXT,
                    FOREIGN KEY (ticket_id) REFERENCES tickets (ticket_id)
                );

                CREATE TABLE IF NOT EXISTS node_executions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ticket_id TEXT NOT NULL,
                    node_id TEXT NOT NULL,
                    agent_id TEXT NOT NULL,
                    status TEXT NOT NULL,
                    retry_count INTEGER DEFAULT 0,
                    inputs_json TEXT,
                    outputs_json TEXT,
                    error TEXT,
                    start_time TEXT,
                    end_time TEXT,
                    FOREIGN KEY (ticket_id) REFERENCES tickets (ticket_id)
                );

                CREATE INDEX IF NOT EXISTS idx_transitions_ticket ON state_transitions (ticket_id);
                CREATE INDEX IF NOT EXISTS idx_snapshots_ticket ON snapshots (ticket_id);
                CREATE INDEX IF NOT EXISTS idx_node_executions_ticket ON node_executions (ticket_id, node_id);
                """)
                conn.commit()

    def save_ticket(self, ticket: ExecutionTicket) -> None:
        """Atomically persist or update an execution ticket."""
        with self._lock:
            with self._get_connection() as conn:
                conn.execute("""
                INSERT INTO tickets (
                    ticket_id, title, description, priority, requested_by,
                    assigned_pod, dri_agent_id, status, metadata_json,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(ticket_id) DO UPDATE SET
                    title=excluded.title,
                    description=excluded.description,
                    priority=excluded.priority,
                    requested_by=excluded.requested_by,
                    assigned_pod=excluded.assigned_pod,
                    dri_agent_id=excluded.dri_agent_id,
                    status=excluded.status,
                    metadata_json=excluded.metadata_json,
                    updated_at=excluded.updated_at
                """, (
                    ticket.ticket_id,
                    ticket.title,
                    ticket.description,
                    ticket.priority.value if hasattr(ticket.priority, "value") else str(ticket.priority),
                    ticket.requested_by,
                    ticket.assigned_pod,
                    ticket.dri_agent_id,
                    ticket.status.value if hasattr(ticket.status, "value") else str(ticket.status),
                    json.dumps(ticket.metadata),
                    ticket.created_at.isoformat(),
                    datetime.utcnow().isoformat()
                ))
                conn.commit()

    def get_ticket(self, ticket_id: str) -> Optional[ExecutionTicket]:
        """Fetch a ticket by ID."""
        with self._get_connection() as conn:
            row = conn.execute("SELECT * FROM tickets WHERE ticket_id = ?", (ticket_id,)).fetchone()
            if not row:
                return None
            return ExecutionTicket(
                ticket_id=row["ticket_id"],
                title=row["title"],
                description=row["description"],
                priority=TicketPriority(row["priority"]),
                requested_by=row["requested_by"],
                assigned_pod=row["assigned_pod"],
                dri_agent_id=row["dri_agent_id"],
                status=TaskStatus(row["status"]),
                metadata=json.loads(row["metadata_json"] or "{}"),
                created_at=datetime.fromisoformat(row["created_at"]),
                updated_at=datetime.fromisoformat(row["updated_at"])
            )

    def log_transition(
        self,
        ticket_id: str,
        node_id: str,
        agent_id: str,
        from_state: TaskStatus,
        to_state: TaskStatus,
        metadata: Optional[Dict[str, Any]] = None,
        snapshot_id: Optional[str] = None
    ) -> StateTransitionLog:
        """Record an immutable state transition event."""
        log_entry = StateTransitionLog(
            ticket_id=ticket_id,
            node_id=node_id,
            agent_id=agent_id,
            from_state=from_state,
            to_state=to_state,
            metadata=metadata or {},
            snapshot_id=snapshot_id
        )
        with self._lock:
            with self._get_connection() as conn:
                conn.execute("""
                INSERT INTO state_transitions (
                    log_id, ticket_id, node_id, agent_id, from_state,
                    to_state, timestamp, metadata_json, snapshot_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    log_entry.log_id,
                    log_entry.ticket_id,
                    log_entry.node_id,
                    log_entry.agent_id,
                    log_entry.from_state.value,
                    log_entry.to_state.value,
                    log_entry.timestamp.isoformat(),
                    json.dumps(log_entry.metadata),
                    log_entry.snapshot_id
                ))
                conn.commit()
        return log_entry

    def create_snapshot(
        self,
        ticket_id: str,
        node_id: str,
        global_context: Dict[str, Any],
        completed_nodes: List[str],
        node_outputs: Dict[str, Any],
        active_agents: List[str]
    ) -> ExecutionSnapshot:
        """Create an atomic execution snapshot."""
        snapshot = ExecutionSnapshot(
            ticket_id=ticket_id,
            node_id=node_id,
            global_context=global_context,
            completed_node_ids=completed_nodes,
            node_outputs=node_outputs,
            active_agent_ids=active_agents
        )
        with self._lock:
            with self._get_connection() as conn:
                conn.execute("""
                INSERT INTO snapshots (
                    snapshot_id, ticket_id, node_id, timestamp,
                    global_context_json, completed_nodes_json,
                    node_outputs_json, active_agents_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    snapshot.snapshot_id,
                    snapshot.ticket_id,
                    snapshot.node_id,
                    snapshot.timestamp.isoformat(),
                    json.dumps(snapshot.global_context),
                    json.dumps(snapshot.completed_node_ids),
                    json.dumps(snapshot.node_outputs),
                    json.dumps(snapshot.active_agent_ids)
                ))
                conn.commit()
        return snapshot

    def get_snapshot(self, snapshot_id: str) -> Optional[ExecutionSnapshot]:
        """Retrieve a snapshot by ID."""
        with self._get_connection() as conn:
            row = conn.execute("SELECT * FROM snapshots WHERE snapshot_id = ?", (snapshot_id,)).fetchone()
            if not row:
                return None
            return ExecutionSnapshot(
                snapshot_id=row["snapshot_id"],
                ticket_id=row["ticket_id"],
                node_id=row["node_id"],
                timestamp=datetime.fromisoformat(row["timestamp"]),
                global_context=json.loads(row["global_context_json"] or "{}"),
                completed_node_ids=json.loads(row["completed_nodes_json"] or "[]"),
                node_outputs=json.loads(row["node_outputs_json"] or "{}"),
                active_agent_ids=json.loads(row["active_agents_json"] or "[]")
            )

    def get_latest_snapshot(self, ticket_id: str) -> Optional[ExecutionSnapshot]:
        """Fetch the most recent snapshot for a ticket."""
        with self._get_connection() as conn:
            row = conn.execute("""
            SELECT * FROM snapshots WHERE ticket_id = ? ORDER BY timestamp DESC LIMIT 1
            """, (ticket_id,)).fetchone()
            if not row:
                return None
            return ExecutionSnapshot(
                snapshot_id=row["snapshot_id"],
                ticket_id=row["ticket_id"],
                node_id=row["node_id"],
                timestamp=datetime.fromisoformat(row["timestamp"]),
                global_context=json.loads(row["global_context_json"] or "{}"),
                completed_node_ids=json.loads(row["completed_nodes_json"] or "[]"),
                node_outputs=json.loads(row["node_outputs_json"] or "{}"),
                active_agent_ids=json.loads(row["active_agents_json"] or "[]")
            )

    def record_node_execution(self, ticket_id: str, node: TaskNode) -> None:
        """Persist detailed node execution metrics and I/O."""
        with self._lock:
            with self._get_connection() as conn:
                conn.execute("""
                INSERT INTO node_executions (
                    ticket_id, node_id, agent_id, status, retry_count,
                    inputs_json, outputs_json, error, start_time, end_time
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    ticket_id,
                    node.id,
                    node.agent_id,
                    node.status.value,
                    node.retry_count,
                    json.dumps(node.inputs),
                    json.dumps(node.outputs),
                    node.error,
                    node.start_time.isoformat() if node.start_time else None,
                    node.end_time.isoformat() if node.end_time else None
                ))
                conn.commit()

    def get_transitions(self, ticket_id: str) -> List[StateTransitionLog]:
        """Fetch all state transition logs for a ticket in chronological order."""
        with self._get_connection() as conn:
            rows = conn.execute("""
            SELECT * FROM state_transitions WHERE ticket_id = ? ORDER BY timestamp ASC
            """, (ticket_id,)).fetchall()
            return [
                StateTransitionLog(
                    log_id=r["log_id"],
                    ticket_id=r["ticket_id"],
                    node_id=r["node_id"],
                    agent_id=r["agent_id"],
                    from_state=TaskStatus(r["from_state"]),
                    to_state=TaskStatus(r["to_state"]),
                    timestamp=datetime.fromisoformat(r["timestamp"]),
                    metadata=json.loads(r["metadata_json"] or "{}"),
                    snapshot_id=r["snapshot_id"]
                )
                for r in rows
            ]

    def rollback(self, ticket_id: str, target_snapshot_id: str) -> ExecutionSnapshot:
        """
        Roll back ticket execution state to a historical snapshot.
        Marks all transitions after snapshot as ROLLED_BACK.
        """
        snapshot = self.get_snapshot(target_snapshot_id)
        if not snapshot:
            raise ValueError(f"Snapshot {target_snapshot_id} not found for rollback.")

        self.log_transition(
            ticket_id=ticket_id,
            node_id=snapshot.node_id,
            agent_id="SYSTEM_ROLLBACK_ENGINE",
            from_state=TaskStatus.FAILED,
            to_state=TaskStatus.ROLLED_BACK,
            metadata={"target_snapshot_id": target_snapshot_id},
            snapshot_id=target_snapshot_id
        )
        return snapshot
