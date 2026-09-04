"""
JSON-RPC 2.0 and MCP (Model Context Protocol) Schema Definitions.
"""

from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field


class JSONRPCRequest(BaseModel):
    """JSON-RPC 2.0 Request Object."""
    jsonrpc: str = "2.0"
    method: str
    params: Optional[Dict[str, Any]] = Field(default_factory=dict)
    id: Optional[Union[str, int]] = None


class JSONRPCErrorDetail(BaseModel):
    code: int
    message: str
    data: Optional[Any] = None


class JSONRPCResponse(BaseModel):
    """JSON-RPC 2.0 Response Object."""
    jsonrpc: str = "2.0"
    result: Optional[Any] = None
    error: Optional[JSONRPCErrorDetail] = None
    id: Optional[Union[str, int]] = None


class JSONRPCError(BaseModel):
    """JSON-RPC 2.0 Error Factory."""
    @staticmethod
    def invalid_params(message: str, data: Any = None, req_id: Any = None) -> JSONRPCResponse:
        return JSONRPCResponse(
            error=JSONRPCErrorDetail(code=-32602, message=message, data=data),
            id=req_id
        )

    @staticmethod
    def method_not_found(method: str, req_id: Any = None) -> JSONRPCResponse:
        return JSONRPCResponse(
            error=JSONRPCErrorDetail(code=-32601, message=f"Method '{method}' not found"),
            id=req_id
        )

    @staticmethod
    def internal_error(message: str, data: Any = None, req_id: Any = None) -> JSONRPCResponse:
        return JSONRPCResponse(
            error=JSONRPCErrorDetail(code=-32603, message=message, data=data),
            id=req_id
        )


class ToolDefinition(BaseModel):
    """MCP Tool Definition metadata with JSON schema and risk levels."""
    name: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Optional[Dict[str, Any]] = None
    risk_level: str = "LOW"  # "LOW", "MEDIUM", "HIGH" (guarded sandbox)
    timeout_seconds: float = 30.0
    dri_agent_id: str = "web_devops_marcus_chen"


class ToolCallResult(BaseModel):
    """Standardized tool invocation outcome."""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    execution_time_ms: float = 0.0
    dri: str = "UNKNOWN"
    metadata: Dict[str, Any] = Field(default_factory=dict)
