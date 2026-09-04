"""
Symbolic AST Code Graph and Navigation Primitives Engine.
Provides programmatic AST inspection to verify code integrity and track symbol references.
"""

import ast
import os
from pathlib import Path
from typing import Dict, List, Optional, Set, Any

from core.config import CONFIG
from core.ast_engine.models import (
    SymbolLocation,
    SymbolReferenceReport,
    TypeHierarchyReport,
    CallGraphReport,
    ASTIntegrityReport
)



class ASTNavigator:
    """
    Programmatic AST inspection and symbol navigator for engineering agents.
    """

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = workspace_root or CONFIG.workspace_root

    def verify_ast_integrity(self, source_code: str) -> ASTIntegrityReport:
        """
        Verify that source code parses into a valid Python AST without syntax errors.
        """
        try:
            tree = ast.parse(source_code)
            classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
            functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            node_count = sum(1 for _ in ast.walk(tree))
            return ASTIntegrityReport(
                is_valid_syntax=True,
                node_count=node_count,
                defined_classes=classes,
                defined_functions=functions
            )
        except SyntaxError as e:
            return ASTIntegrityReport(
                is_valid_syntax=False,
                error_message=f"SyntaxError at line {e.lineno}, col {e.offset}: {e.msg}"
            )
        except Exception as e:
            return ASTIntegrityReport(
                is_valid_syntax=False,
                error_message=f"AST Parse Error: {str(e)}"
            )

    def get_symbol_references(
        self,
        symbol_name: str,
        search_dir: Optional[Path] = None
    ) -> SymbolReferenceReport:
        """
        Locate all definitions and usages of a symbol across workspace Python files.
        """
        target_dir = search_dir or (self.workspace_root / "core")
        definitions: List[SymbolLocation] = []
        usages: List[SymbolLocation] = []

        for py_file in target_dir.glob("**/*.py"):
            try:
                code = py_file.read_text(encoding="utf-8", errors="replace")
                tree = ast.parse(code)
                lines = code.splitlines()

                for node in ast.walk(tree):
                    # Definition check: ClassDef or FunctionDef
                    if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                        if node.name == symbol_name:
                            snippet = lines[node.lineno - 1].strip() if 0 < node.lineno <= len(lines) else ""
                            definitions.append(SymbolLocation(
                                file_path=str(py_file.relative_to(self.workspace_root)),
                                line_number=node.lineno,
                                column=node.col_offset,
                                symbol_type="class" if isinstance(node, ast.ClassDef) else "function",
                                context_snippet=snippet
                            ))
                    # Usage check: Name or Attribute
                    elif isinstance(node, ast.Name):
                        if node.id == symbol_name and not isinstance(getattr(node, 'ctx', None), ast.Store):
                            snippet = lines[node.lineno - 1].strip() if 0 < node.lineno <= len(lines) else ""
                            usages.append(SymbolLocation(
                                file_path=str(py_file.relative_to(self.workspace_root)),
                                line_number=node.lineno,
                                column=node.col_offset,
                                symbol_type="name_usage",
                                context_snippet=snippet
                            ))
            except Exception:
                continue

        return SymbolReferenceReport(
            symbol_name=symbol_name,
            definitions=definitions,
            usages=usages,
            total_occurrences=len(definitions) + len(usages)
        )

    def get_type_hierarchy(
        self,
        class_name: str,
        search_dir: Optional[Path] = None
    ) -> TypeHierarchyReport:
        """
        Inspect class base classes, declared methods, and fields.
        """
        target_dir = search_dir or (self.workspace_root / "core")
        bases: List[str] = []
        methods: List[str] = []
        fields: List[str] = []

        for py_file in target_dir.glob("**/*.py"):
            try:
                code = py_file.read_text(encoding="utf-8", errors="replace")
                tree = ast.parse(code)
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef) and node.name == class_name:
                        for b in node.bases:
                            if isinstance(b, ast.Name):
                                bases.append(b.id)
                            elif isinstance(b, ast.Attribute):
                                bases.append(b.attr)
                        for item in node.body:
                            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                                methods.append(item.name)
                            elif isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                                fields.append(item.target.id)
            except Exception:
                continue

        return TypeHierarchyReport(
            class_name=class_name,
            bases=bases,
            methods=methods,
            fields=fields,
            subclasses=[]
        )

    def find_callers_and_callees(
        self,
        function_name: str,
        search_dir: Optional[Path] = None
    ) -> CallGraphReport:
        """
        Find caller functions and callees for a target function.
        """
        target_dir = search_dir or (self.workspace_root / "core")
        callers: List[str] = []
        callees: List[str] = []

        for py_file in target_dir.glob("**/*.py"):
            try:
                code = py_file.read_text(encoding="utf-8", errors="replace")
                tree = ast.parse(code)
                for node in ast.walk(tree):
                    # Check what the target function calls (callees)
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        if node.name == function_name:
                            for subnode in ast.walk(node):
                                if isinstance(subnode, ast.Call):
                                    if isinstance(subnode.func, ast.Name):
                                        callees.append(subnode.func.id)
                                    elif isinstance(subnode.func, ast.Attribute):
                                        callees.append(subnode.func.attr)
                        else:
                            # Check if this function calls our target (caller)
                            for subnode in ast.walk(node):
                                if isinstance(subnode, ast.Call):
                                    call_name = ""
                                    if isinstance(subnode.func, ast.Name):
                                        call_name = subnode.func.id
                                    elif isinstance(subnode.func, ast.Attribute):
                                        call_name = subnode.func.attr
                                    if call_name == function_name:
                                        callers.append(node.name)
            except Exception:
                continue

        return CallGraphReport(
            function_name=function_name,
            callers=list(set(callers)),
            callees=list(set(callees))
        )


# Global AST Navigator Singleton
GLOBAL_AST_NAVIGATOR = ASTNavigator()

