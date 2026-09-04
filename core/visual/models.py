"""
Declarative Scene-Graph Data Models.
Structured JSON representations of visual layouts, responsive constraints, and styling tokens.
"""

import uuid
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class NodeType(str, Enum):
    """Supported visual node types."""
    CONTAINER = "container"
    CARD = "card"
    GRID = "grid"
    TEXT = "text"
    BUTTON = "button"
    BADGE = "badge"
    IMAGE = "image"
    FORM_INPUT = "form_input"
    METRIC_CARD = "metric_card"


class LayoutConfig(BaseModel):
    """Layout and positioning parameters."""
    display: str = "flex"  # flex, grid, block
    direction: str = "column"  # row, column
    justify: str = "start"  # start, center, between, end
    align: str = "start"  # start, center, stretch, end
    width: str = "100%"
    height: str = "auto"
    padding: str = "1rem"
    margin: str = "0"
    gap: str = "1rem"
    columns: int = 1  # For grid display


class StyleConfig(BaseModel):
    """Visual design tokens and CSS attributes."""
    background: str = "transparent"
    color: str = "#0A2540"
    border: str = "none"
    border_radius: str = "0.75rem"
    shadow: str = "none"
    font_family: str = "Inter, sans-serif"
    font_size: str = "1rem"
    font_weight: str = "400"
    line_height: str = "1.5"
    user_select: str = "none"  # Non-copyable by default
    custom_classes: List[str] = Field(default_factory=list)


class ResponsiveConfig(BaseModel):
    """Responsive viewport overrides."""
    mobile: Dict[str, Any] = Field(default_factory=dict)
    tablet: Dict[str, Any] = Field(default_factory=dict)
    desktop: Dict[str, Any] = Field(default_factory=dict)


class SceneNode(BaseModel):
    """Individual node within the visual scene-graph tree."""
    id: str = Field(default_factory=lambda: f"node_{uuid.uuid4().hex[:8]}")
    node_type: NodeType = NodeType.CONTAINER
    name: str = "SceneNode"
    content: Optional[str] = None
    layout: LayoutConfig = Field(default_factory=LayoutConfig)
    style: StyleConfig = Field(default_factory=StyleConfig)
    responsive: ResponsiveConfig = Field(default_factory=ResponsiveConfig)
    children: List["SceneNode"] = Field(default_factory=list)
    attributes: Dict[str, Any] = Field(default_factory=dict)
    events: Dict[str, str] = Field(default_factory=dict)

    def add_child(self, child: "SceneNode") -> "SceneNode":
        self.children.append(child)
        return self


SceneNode.model_rebuild()


class SceneGraph(BaseModel):
    """Master Scene-Graph root object."""
    graph_id: str = Field(default_factory=lambda: f"sg_{uuid.uuid4().hex[:10]}")
    title: str = "Declarative Visual Scene"
    canvas_width: int = 1440
    canvas_height: int = 900
    root_node: SceneNode = Field(default_factory=lambda: SceneNode(name="RootContainer"))
    color_palette: Dict[str, str] = Field(default_factory=lambda: {
        "primary": "#0A2540",
        "accent": "#F59E0B",
        "surface": "#FFFFFF",
        "background": "#F8FAFC",
        "text": "#0F172A",
        "muted": "#64748B"
    })
    typography_tokens: Dict[str, str] = Field(default_factory=lambda: {
        "h1": "2.5rem font-extrabold tracking-tight",
        "h2": "1.875rem font-bold",
        "body": "1rem font-normal",
        "caption": "0.875rem font-medium text-slate-500"
    })
    meta: Dict[str, Any] = Field(default_factory=dict)
