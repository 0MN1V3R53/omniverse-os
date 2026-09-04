"""
Omniverse Core Frontier Foundation Models Substrate
===================================================
Exports:
- TimesFM25Engine: Google TimesFM 2.5 Time-Series Foundation Model
- DeepSeekFrontierEngine: DeepSeek-V3/R1 MLA + DeepSeekMoE + GRPO Reasoning Substrate
- UniversalAgentTrainer: Cross-Workforce Training & Tool Injection Engine
"""

from .timesfm_engine import TimesFM25Engine, TimeSeriesPatchConfig, ForecastResult
from .deepseek_frontier_engine import DeepSeekFrontierEngine, MLALatentConfig, MoERoutingConfig, GRPOResult
from .universal_agent_trainer import UniversalAgentTrainer, AgentModelCapability

__all__ = [
    "TimesFM25Engine",
    "TimeSeriesPatchConfig",
    "ForecastResult",
    "DeepSeekFrontierEngine",
    "MLALatentConfig",
    "MoERoutingConfig",
    "GRPOResult",
    "UniversalAgentTrainer",
    "AgentModelCapability"
]
