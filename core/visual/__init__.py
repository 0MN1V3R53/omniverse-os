"""
Declarative Scene-Graph, Transpilation & Visual Regression Package.
"""

from .models import (
    NodeType,
    LayoutConfig,
    StyleConfig,
    ResponsiveConfig,
    SceneNode,
    SceneGraph,
)
from .scene_graph import SceneGraphCompiler
from .vision_gate import (
    VisualDiffBoundingBox,
    VisualDiffResult,
    VisionRegressionGate,
    GLOBAL_VISION_GATE
)

__all__ = [
    "NodeType",
    "LayoutConfig",
    "StyleConfig",
    "ResponsiveConfig",
    "SceneNode",
    "SceneGraph",
    "SceneGraphCompiler",
    "VisualDiffBoundingBox",
    "VisualDiffResult",
    "VisionRegressionGate",
    "GLOBAL_VISION_GATE",
]
