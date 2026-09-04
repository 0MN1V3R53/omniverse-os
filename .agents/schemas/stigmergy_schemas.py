"""
OMNIVERSE STIGMERGIC AGENT BUS & REASONING SCHEMAS
=================================================
Defines JSON-RPC tool calling protocols (DeepSeek-V3/R1 & Qwen2.5-Coder)
and environmental stigmergy markers for decentralized agent coordination.
"""

from datetime import datetime
from typing import Dict, List, Optional, Union, Literal, Any
from pydantic import BaseModel, Field


class FunctionParameterSpec(BaseModel):
    """Parameter schema definition for LLM tool invocation."""
    name: str
    type: str
    description: str
    required: bool = True
    enum_values: Optional[List[str]] = None


class ToolDefinition(BaseModel):
    """DeepSeek-V3 / Qwen2.5-Coder JSON Schema for tools."""
    name: str
    description: str
    parameters: Dict[str, Any] = Field(default_factory=dict)


class ToolCallInvocation(BaseModel):
    """Structured tool execution request emitted by the reasoning model."""
    call_id: str
    tool_name: str
    arguments: Dict[str, Any] = Field(default_factory=dict)


class ToolCallResult(BaseModel):
    """Tool execution response payload."""
    call_id: str
    tool_name: str
    status: Literal["success", "error", "skipped"]
    result_payload: Any
    error_message: Optional[str] = None
    execution_time_ms: float = 0.0


class StigmergicMarker(BaseModel):
    """
    An environmental trace left by an autonomous agent on the shared matrix.
    Agents observe and react to markers without centralized lock contention.
    """
    marker_id: str
    author_agent_id: str
    domain: str  # D1_AST, D4_SEO, D13_LOGISTICS, D10_WORLD_MODEL
    action_type: str  # TASK_COMPLETED, INVARIANT_LOCKED, MODEL_ROLLOUT_READY, TELEMETRY_MUTATED
    state_payload: Dict[str, Any] = Field(default_factory=dict)
    salience_weight: float = Field(default=1.0, ge=0.0, le=1.0)
    decay_rate: float = 0.95
    created_at: datetime = Field(default_factory=datetime.utcnow)


class MatrixState(BaseModel):
    """Persistent shared stigmergy state across all agents and pods."""
    version: str = "2.0.0"
    active_workspace_hub: str = "aether Core 999"
    active_markers: List[StigmergicMarker] = Field(default_factory=list)
    global_entropy_score: float = 0.0
    last_checkpoint_id: str = "CKPT-INITIAL"
    updated_at: datetime = Field(default_factory=datetime.utcnow)
