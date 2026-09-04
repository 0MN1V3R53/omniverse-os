"""
Standardized Tool Input/Output Schemas and Affordance Contracts.
Defines strict type boundaries for Terminal, Web Research, YouTube Intel, File System MCP, Sandboxed Terminal, and Fast Symbol Lookup.
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class TerminalExecInput(BaseModel):
    """Input contract for terminal_exec tool."""
    command: str = Field(..., description="The shell command line string to execute.")
    cwd: Optional[str] = Field(None, description="Working directory for the command.")
    timeout_sec: float = Field(30.0, description="Maximum execution duration before timeout.")
    max_retries: int = Field(3, description="Maximum reflection retry attempts on non-zero exit.")


class SandboxedTerminalExecInput(BaseModel):
    """Input contract for sandboxed_terminal_exec tool."""
    command: str = Field(..., description="The shell command line string to execute in an isolated container.")
    timeout_sec: int = Field(60, description="Maximum execution duration before timeout.")
    network: bool = Field(False, description="Whether outbound network bridge is enabled.")
    cwd: Optional[str] = Field(None, description="Working directory inside the sandbox.")


class FastSymbolLookupInput(BaseModel):
    """Input contract for fast_symbol_lookup tool."""
    symbol_name: str = Field(..., description="Name of the class, function, method, or symbol to lookup.")
    symbol_type: Optional[str] = Field(None, description="Optional symbol type filter ('class', 'function', 'method').")


class FindAllReferencesInput(BaseModel):
    """Input contract for find_all_references tool."""
    symbol_name: str = Field(..., description="Name of the symbol to trace across the entire codebase.")


class WebResearcherInput(BaseModel):
    """Input contract for web_researcher tool."""
    query: str = Field(..., description="Search query or documentation topic.")
    target_url: Optional[str] = Field(None, description="Specific URL to scrape and parse into markdown.")
    extract_markdown: bool = Field(True, description="Whether to format output into clean markdown.")


class YouTubeIntelInput(BaseModel):
    """Input contract for youtube_intel tool."""
    query_or_url: str = Field(..., description="YouTube video URL or search topic.")
    extract_transcript: bool = Field(True, description="Whether to extract timestamped transcript text.")
    extract_chapters: bool = Field(True, description="Whether to parse video chapters and timestamps.")


class FileSystemMCPInput(BaseModel):
    """Input contract for file_system_mcp tool."""
    action: str = Field(..., description="File operation: 'read', 'write_atomic', 'grep', 'list_dir'")
    file_path: str = Field(..., description="Target file path.")
    content: Optional[str] = Field(None, description="Content to write if action is write_atomic.")
    pattern: Optional[str] = Field(None, description="Grep search regex pattern if action is grep.")
