"""
Standardized Tool Protocols, MCP Registry, and Execution Harness Package.
"""

from .protocol import (
    JSONRPCRequest,
    JSONRPCResponse,
    JSONRPCError,
    ToolDefinition,
    ToolCallResult,
)
from .registry import ToolRegistry, tool
from .harness import GuardedToolHarness
from .builtin_tools import (
    ReadFileTool,
    WriteFileAtomicTool,
    RunShellTool,
    ASTValidateCodeTool,
    GitStatusTool,
    HttpProbeTool,
    MemoryLogSyncTool,
)

__all__ = [
    "JSONRPCRequest",
    "JSONRPCResponse",
    "JSONRPCError",
    "ToolDefinition",
    "ToolCallResult",
    "ToolRegistry",
    "tool",
    "GuardedToolHarness",
    "ReadFileTool",
    "WriteFileAtomicTool",
    "RunShellTool",
    "ASTValidateCodeTool",
    "GitStatusTool",
    "HttpProbeTool",
    "MemoryLogSyncTool",
]
