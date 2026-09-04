"""
Pydantic Data Models for Symbolic AST Code Graph and Navigation Primitives.
"""

import uuid
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class SymbolLocation(BaseModel):
    """Exact file and line coordinates of a code symbol."""
    file_path: str
    line_number: int
    column: int = 0
    symbol_type: str  # class, function, method, variable, import
    context_snippet: str = ""


class SymbolReferenceReport(BaseModel):
    """References, definition, and usages of a symbol across the workspace."""
    symbol_name: str
    definitions: List[SymbolLocation] = Field(default_factory=list)
    usages: List[SymbolLocation] = Field(default_factory=list)
    total_occurrences: int = 0


class TypeHierarchyReport(BaseModel):
    """Class inheritance hierarchy tree."""
    class_name: str
    bases: List[str] = Field(default_factory=list)
    methods: List[str] = Field(default_factory=list)
    fields: List[str] = Field(default_factory=list)
    subclasses: List[str] = Field(default_factory=list)


class CallGraphReport(BaseModel):
    """Call graph mapping callers and callees for a target function."""
    function_name: str
    callers: List[str] = Field(default_factory=list)
    callees: List[str] = Field(default_factory=list)


class ASTIntegrityReport(BaseModel):
    """Syntactic and structural integrity check of source code."""
    is_valid_syntax: bool = True
    error_message: Optional[str] = None
    node_count: int = 0
    defined_classes: List[str] = Field(default_factory=list)
    defined_functions: List[str] = Field(default_factory=list)
