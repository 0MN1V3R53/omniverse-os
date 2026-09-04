"""
JSONL State Logger for intermediate checkpointing, replay, and rollback.
Persists execution graphs to .runtime/state.jsonl.
"""

import json
import uuid
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

from core.config import CONFIG


class RuntimeStateRecord(BaseModel):
    """Immutable state snapshot written to the JSONL log."""
    record_id: str = Field(default_factory=lambda: f"rec_{uuid.uuid4().hex[:12]}")
    ticket_id: str
    stage: str
    status: str = "RUNNING"  # RUNNING, COMPLETED, PAUSED, ROLLED_BACK, FAILED
    agent_id: str
    state_payload: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class StateLogger:
    """
    Thread-safe JSONL state logger for resilient workflow tracking.
    """

    def __init__(self, log_path: Optional[Path] = None):
        self.log_path = log_path or (CONFIG.workspace_root / ".runtime" / "state.jsonl")
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def log_state(
        self,
        ticket_id: str,
        stage: str,
        agent_id: str,
        payload: Dict[str, Any],
        status: str = "RUNNING"
    ) -> RuntimeStateRecord:
        """Atomically append a state record to the JSONL log."""
        record = RuntimeStateRecord(
            ticket_id=ticket_id,
            stage=stage,
            status=status,
            agent_id=agent_id,
            state_payload=payload
        )

        line = json.dumps(record.model_dump(), default=str) + "\n"
        with self._lock:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(line)

        return record

    def get_ticket_history(self, ticket_id: str) -> List[RuntimeStateRecord]:
        """Fetch all state snapshots for a ticket in chronological order."""
        if not self.log_path.exists():
            return []

        records = []
        with self._lock:
            with open(self.log_path, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    try:
                        data = json.loads(line)
                        if data.get("ticket_id") == ticket_id:
                            records.append(RuntimeStateRecord(**data))
                    except Exception:
                        continue
        return records

    def get_latest_state(self, ticket_id: str) -> Optional[RuntimeStateRecord]:
        """Get the most recent state record for a ticket."""
        history = self.get_ticket_history(ticket_id)
        return history[-1] if history else None

    def rollback(self, ticket_id: str, target_record_id: str) -> RuntimeStateRecord:
        """Rollback ticket state to a target record checkpoint."""
        history = self.get_ticket_history(ticket_id)
        target = next((r for r in history if r.record_id == target_record_id), None)
        if not target:
            raise ValueError(f"Checkpoint record '{target_record_id}' not found for ticket '{ticket_id}'.")

        rollback_record = self.log_state(
            ticket_id=ticket_id,
            stage=f"ROLLBACK_TO_{target.stage}",
            agent_id="system_orchestrator",
            payload={"rolled_back_to": target.record_id, "restored_payload": target.state_payload},
            status="ROLLED_BACK"
        )
        return rollback_record
