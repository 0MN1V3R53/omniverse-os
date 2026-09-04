"""
OMNIVERSE FRONTIER TIME-SERIES FOUNDATION MODEL (TSFM) SCHEMAS
=============================================================
Defines tokenization protocols, patch embeddings, quantile loss structures,
and inference request/response payloads for Timer-XL, TSLib, and Time-MoE.
"""

from datetime import datetime
from typing import Dict, List, Optional, Union, Literal, Any
from pydantic import BaseModel, Field


class PatchTokenizationConfig(BaseModel):
    """Configuration for patching continuous temporal scalar series."""
    patch_length: int = Field(default=32, description="Number of contiguous time steps per input patch token (P_in)")
    stride: int = Field(default=32, description="Stride step between adjacent patches")
    output_patch_length: int = Field(default=128, description="Number of steps predicted per output patch (P_out)")
    channel_independent: bool = Field(default=True, description="Whether multivariate series are tokenized independently per channel")
    normalization: Literal["revin", "standard", "none"] = Field(default="revin", description="Reversible Instance Normalization method")


class TSFMModelSpec(BaseModel):
    """Specification of target time-series foundation model."""
    model_name: Literal["Timer-XL", "Time-MoE", "TSLib-PatchTST", "TimesFM-2.5", "Chronos-Bolt"] = "Timer-XL"
    architecture: Literal["decoder_only", "encoder_only", "moe_decoder", "encoder_decoder"] = "decoder_only"
    model_dim: int = Field(default=1280, description="Latent hidden dimension (D_model)")
    num_layers: int = Field(default=20, description="Transformer decoder depth")
    num_heads: int = Field(default=16, description="Attention head count")
    num_experts: Optional[int] = Field(default=8, description="Expert count for Time-MoE models")
    top_k_experts: Optional[int] = Field(default=2, description="Active experts per token in MoE routing")
    max_context_length: int = Field(default=16384, description="Maximum receptive field context length")


class TimeSeriesForecastRequest(BaseModel):
    """Zero-shot time series forecast query payload."""
    series_id: str = Field(description="Unique identifier for the telemetry or business metric stream")
    timestamps: Optional[List[datetime]] = Field(default=None, description="ISO-8601 timestamps for historical points")
    historical_values: List[float] = Field(description="Chronological historical observation values")
    forecast_horizon: int = Field(default=32, description="Target forecast steps into the future (H)")
    frequency: Literal["minutely", "hourly", "daily", "weekly", "monthly", "unspecified"] = "daily"
    exogenous_covariates: Optional[Dict[str, List[float]]] = Field(default=None, description="Dynamic future/past covariates (XReg)")
    quantiles: List[float] = Field(default=[0.1, 0.5, 0.9], description="Target quantile percentiles (Pinball loss evaluation)")
    allow_statistical_fallback: bool = Field(default=True, description="Fallback to Holt-Winters/Auto-ARIMA on accelerator failure")


class TimeSeriesForecastResponse(BaseModel):
    """Result payload emitted by the TSFM inference engine."""
    request_id: str
    series_id: str
    model_used: str
    forecast_horizon: int
    point_forecast: List[float] = Field(description="Median / Mean expected trajectory (q50)")
    quantile_forecasts: Dict[str, List[float]] = Field(default_factory=dict, description="Quantile bands e.g. q10, q50, q90")
    execution_latency_ms: float
    fallback_engaged: bool = False
    timestamp: datetime = Field(default_factory=datetime.utcnow)
