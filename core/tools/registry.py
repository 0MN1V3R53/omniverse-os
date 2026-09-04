"""
Tool Registry and Decorator for automatic Pydantic schema extraction and tool registration.
"""

import inspect
from typing import Dict, List, Optional, Any, Callable, Type
from pydantic import BaseModel, create_model
from core.tools.protocol import ToolDefinition, ToolCallResult, JSONRPCRequest, JSONRPCResponse, JSONRPCError


class ToolRegistry:
    """Central registry for all MCP and runtime tools."""
    
    def __init__(self):
        self._tools: Dict[str, Dict[str, Any]] = {}

    def register(
        self,
        name: str,
        handler: Callable,
        description: str,
        input_model: Type[BaseModel],
        risk_level: str = "LOW",
        timeout_seconds: float = 30.0,
        dri: str = "web_devops_marcus_chen",
    ) -> None:
        """Register a tool handler with its Pydantic input model and metadata."""
        schema = input_model.model_json_schema() if hasattr(input_model, "model_json_schema") else input_model.schema()
        definition = ToolDefinition(
            name=name,
            description=description,
            input_schema=schema,
            risk_level=risk_level,
            timeout_seconds=timeout_seconds,
            dri_agent_id=dri,
        )
        self._tools[name] = {
            "definition": definition,
            "handler": handler,
            "input_model": input_model,
            "dri": dri,
            "timeout": timeout_seconds,
            "risk_level": risk_level,
        }

    def get_tool(self, name: str) -> Optional[Dict[str, Any]]:
        """Retrieve tool entry by name."""
        return self._tools.get(name)

    def list_tool_definitions(self) -> List[ToolDefinition]:
        """Return list of all registered tool definitions."""
        return [entry["definition"] for entry in self._tools.values()]

    def list_tools(self) -> List[Dict[str, Any]]:
        """Return MCP-compliant list of tools."""
        return [
            {
                "name": entry["definition"].name,
                "description": entry["definition"].description,
                "inputSchema": entry["definition"].input_schema,
                "riskLevel": entry["definition"].risk_level,
                "dri": entry["definition"].dri_agent_id,
            }
            for entry in self._tools.values()
        ]

    def has_tool(self, name: str) -> bool:
        return name in self._tools


# Global tool registry singleton
GLOBAL_TOOL_REGISTRY = ToolRegistry()


def tool(
    name: Optional[str] = None,
    description: Optional[str] = None,
    input_model: Optional[Type[BaseModel]] = None,
    risk_level: str = "LOW",
    timeout_seconds: float = 30.0,
    dri: str = "web_devops_marcus_chen",
    registry: Optional[ToolRegistry] = None,
):
    """
    Decorator to register a function as an MCP tool with schema validation.
    """
    reg = registry or GLOBAL_TOOL_REGISTRY

    def decorator(fn: Callable):
        tool_name = name or fn.__name__
        tool_desc = description or (inspect.getdoc(fn) or f"Execute {tool_name}")
        
        # If no explicit input model is provided, generate one dynamically from type hints
        model = input_model
        if model is None:
            sig = inspect.signature(fn)
            fields = {}
            for param_name, param in sig.parameters.items():
                if param_name in ["self", "cls"]:
                    continue
                annotation = param.annotation if param.annotation != inspect.Parameter.empty else Any
                default_val = param.default if param.default != inspect.Parameter.empty else ...
                fields[param_name] = (annotation, default_val)
            model = create_model(f"{tool_name}_Input", **fields)

        reg.register(
            name=tool_name,
            handler=fn,
            description=tool_desc,
            input_model=model,
            risk_level=risk_level,
            timeout_seconds=timeout_seconds,
            dri=dri,
        )
        return fn

    return decorator
