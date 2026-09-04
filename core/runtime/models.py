"""
Core Pydantic models for the DAG runtime, state transitions, and execution tickets.
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Set, Callable
from pydantic import BaseModel, Field
import uuid


class TaskStatus(str, Enum):
    """Execution status of a task node in the DAG."""
    PENDING = "PENDING"
    READY = "READY"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    ROLLED_BACK = "ROLLED_BACK"
    BLOCKED = "BLOCKED"
    SKIPPED = "SKIPPED"


class TicketPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ExecutionTicket(BaseModel):
    """Master ticket tracking enterprise objectives and cross-pod missions."""
    ticket_id: str = Field(default_factory=lambda: f"OMNI-{uuid.uuid4().hex[:8].upper()}")
    title: str
    description: str
    priority: TicketPriority = TicketPriority.HIGH
    requested_by: str = "exec_ceo_alexander_vance"
    assigned_pod: str = "web_division_sync"
    dri_agent_id: str = "web_frontend_julian_thorne"
    status: TaskStatus = TaskStatus.PENDING
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskNode(BaseModel):
    """An executable node within the multi-agent DAG."""
    id: str
    name: str
    agent_id: str
    description: Optional[str] = None
    dependencies: Set[str] = Field(default_factory=set)
    status: TaskStatus = TaskStatus.PENDING
    retry_limit: int = 3
    retry_count: int = 0
    timeout_seconds: float = 30.0
    inputs: Dict[str, Any] = Field(default_factory=dict)
    outputs: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None
    span_id: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    
    # Non-serialized execution handler reference
    handler: Optional[Any] = None

    class Config:
        arbitrary_types_allowed = True


class TaskEdge(BaseModel):
    """Directed edge representing causality or conditional branch execution."""
    source_id: str
    target_id: str
    condition: Optional[str] = None  # Expression or predicate name


class StateTransitionLog(BaseModel):
    """Immutable audit entry for state transitions across DAG execution."""
    log_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    ticket_id: str
    node_id: str
    agent_id: str
    from_state: TaskStatus
    to_state: TaskStatus
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    snapshot_id: Optional[str] = None


class ExecutionSnapshot(BaseModel):
    """Atomic state snapshot for rollback and deterministic replay."""
    snapshot_id: str = Field(default_factory=lambda: f"snap_{uuid.uuid4().hex[:12]}")
    ticket_id: str
    node_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    global_context: Dict[str, Any] = Field(default_factory=dict)
    completed_node_ids: List[str] = Field(default_factory=list)
    node_outputs: Dict[str, Any] = Field(default_factory=dict)
    active_agent_ids: List[str] = Field(default_factory=list)


class WorkflowState(BaseModel):
    """Aggregated workflow state passed through the DAG runner."""
    ticket: ExecutionTicket
    nodes: Dict[str, TaskNode] = Field(default_factory=dict)
    edges: List[TaskEdge] = Field(default_factory=list)
    context: Dict[str, Any] = Field(default_factory=dict)
    completed_nodes: Set[str] = Field(default_factory=set)
    failed_nodes: Set[str] = Field(default_factory=set)
    current_snapshot_id: Optional[str] = None
    is_completed: bool = False
    error: Optional[str] = None
