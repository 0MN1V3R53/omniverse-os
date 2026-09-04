"""
Guarded Tool Execution Harness with Timeout Sandboxing and DRI Attribution.
"""

import time
import asyncio
from typing import Dict, Any, Optional, Union
from pydantic import ValidationError

from core.tools.protocol import (
    ToolCallResult,
    JSONRPCRequest,
    JSONRPCResponse,
    JSONRPCError,
)
from core.tools.registry import ToolRegistry, GLOBAL_TOOL_REGISTRY


class GuardedToolHarness:
    """
    Executes registered tools with strict Pydantic input validation,
    concurrency safeguards, timeout traps, and error boundaries.
    """

    def __init__(self, registry: Optional[ToolRegistry] = None):
        self.registry = registry or GLOBAL_TOOL_REGISTRY

    async def execute_tool(
        self,
        tool_name: str,
        params: Dict[str, Any],
        agent_id: str = "web_devops_marcus_chen",
        timeout_override: Optional[float] = None,
    ) -> ToolCallResult:
        """
        Execute a tool by name with strict validation and sandboxed timeout.
        """
        tool_entry = self.registry.get_tool(tool_name)
        if not tool_entry:
            return ToolCallResult(
                success=False,
                error=f"Tool '{tool_name}' is not registered in runtime.",
                dri=agent_id,
            )

        handler = tool_entry["handler"]
        input_model = tool_entry["input_model"]
        timeout_sec = timeout_override or tool_entry["timeout"]
        dri = tool_entry["dri"]

        # Step 1: Validate Inputs using Pydantic
        try:
            validated_input = input_model(**params)
        except ValidationError as val_err:
            return ToolCallResult(
                success=False,
                error=f"Invalid arguments for tool '{tool_name}': {val_err}",
                dri=dri,
            )
        except Exception as exc:
            return ToolCallResult(
                success=False,
                error=f"Input parsing error for tool '{tool_name}': {exc}",
                dri=dri,
            )

        # Step 2: Execute with Timeout Sandbox
        start_time = time.perf_counter()
        try:
            kwargs = validated_input.model_dump() if hasattr(validated_input, "model_dump") else validated_input.dict()
            
            if asyncio.iscoroutinefunction(handler):
                result_data = await asyncio.wait_for(handler(**kwargs), timeout=timeout_sec)
            else:
                # Synchronous functions run in threadpool to prevent event loop blocking
                loop = asyncio.get_event_loop()
                result_data = await asyncio.wait_for(
                    loop.run_in_executor(None, lambda: handler(**kwargs)),
                    timeout=timeout_sec
                )

            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return ToolCallResult(
                success=True,
                data=result_data,
                execution_time_ms=round(elapsed_ms, 2),
                dri=dri,
                metadata={"agent_id": agent_id, "tool_name": tool_name}
            )

        except asyncio.TimeoutError:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return ToolCallResult(
                success=False,
                error=f"Tool '{tool_name}' timed out after {timeout_sec}s.",
                execution_time_ms=round(elapsed_ms, 2),
                dri=dri,
                metadata={"agent_id": agent_id, "timeout": timeout_sec}
            )
        except Exception as exc:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return ToolCallResult(
                success=False,
                error=f"Tool '{tool_name}' failed with error: {str(exc)}",
                execution_time_ms=round(elapsed_ms, 2),
                dri=dri,
                metadata={"agent_id": agent_id, "exception_type": type(exc).__name__}
            )

    async def handle_jsonrpc(self, request_payload: Union[Dict[str, Any], str]) -> JSONRPCResponse:
        """Process incoming JSON-RPC 2.0 / MCP tool invocation."""
        if isinstance(request_payload, str):
            import json
            try:
                request_dict = json.loads(request_payload)
            except Exception as e:
                return JSONRPCError.internal_error(f"Invalid JSON: {e}")
        else:
            request_dict = request_payload

        try:
            req = JSONRPCRequest(**request_dict)
        except ValidationError as val_err:
            return JSONRPCError.invalid_params(str(val_err))

        res = await self.execute_tool(
            tool_name=req.method,
            params=req.params or {},
            agent_id="MCP_CLIENT"
        )

        if res.success:
            return JSONRPCResponse(result=res.data, id=req.id)
        else:
            return JSONRPCError.internal_error(res.error or "Unknown error", data=res.metadata, req_id=req.id)
