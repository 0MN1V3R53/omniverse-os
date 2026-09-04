"""
OMNIVERSE SPATIAL MESHING & OPENUSD SCENE GRAPH SCHEMAS
======================================================
Defines 3D geometry generation payloads, PBR material bindings,
USD Prim hierarchy structures, and transform stabilization matrices.
"""

from datetime import datetime
from typing import Dict, List, Optional, Union, Literal, Tuple, Any
from pydantic import BaseModel, Field


class PBRMaterialSpec(BaseModel):
    """Physically Based Rendering (PBR) metallic-roughness material definition."""
    material_name: str = "PBR_Default"
    albedo_hex: str = "#00f0ff"
    roughness: float = Field(default=0.35, ge=0.0, le=1.0)
    metallic: float = Field(default=0.85, ge=0.0, le=1.0)
    emission_hex: Optional[str] = "#002030"
    emission_intensity: float = 1.0
    opacity: float = 1.0
    double_sided: bool = True


class MeshGeometryPayload(BaseModel):
    """Raw vertex and face index geometry payload."""
    vertex_count: int
    face_count: int
    vertices: List[float] = Field(description="Flattened x,y,z vertex coordinate buffer")
    face_vertex_indices: List[int] = Field(description="Polygon vertex index buffer")
    face_vertex_counts: List[int] = Field(default_factory=list, description="Vertex count per polygon (default 3 for triangles)")
    normals: Optional[List[float]] = None
    uv_coordinates: Optional[List[float]] = None


class USDPrimDefinition(BaseModel):
    """OpenUSD (Universal Scene Description) Prim Node Specification."""
    prim_path: str = Field(description="Hierarchical scene graph path e.g. /World/Agents/Agent_01")
    prim_type: Literal["Xform", "Mesh", "Scope", "Material", "Shader", "Camera", "Light"] = "Mesh"
    transform_matrix_4x4: List[float] = Field(
        default=[
            1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 1.0
        ],
        description="Flattened 4x4 affine transformation matrix"
    )
    collision_enabled: bool = True
    collision_approximation: Literal["convexHull", "mesh", "boundingCube", "boundingSphere"] = "convexHull"
    material: Optional[PBRMaterialSpec] = None


class Hunyuan3DGenerationRequest(BaseModel):
    """Request payload for Tencent Hunyuan3D-2 multi-view reconstruction."""
    prompt_text: str = Field(description="Descriptive textual prompt for spatial asset generation")
    seed: int = 42
    target_format: Literal["usda", "usdc", "gltf", "obj"] = "usda"
    poly_count_target: int = Field(default=50000, description="Target decimated triangle polygon budget")
    generate_pbr_textures: bool = True
    texture_resolution: int = Field(default=2048, description="PBR texture map resolution in pixels")


class USDStageManifest(BaseModel):
    """Manifest of an active OpenUSD Stage."""
    stage_id: str
    up_axis: Literal["Y", "Z"] = "Y"
    meters_per_unit: float = 1.0
    root_prims: List[USDPrimDefinition] = Field(default_factory=list)
    output_filepath: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
