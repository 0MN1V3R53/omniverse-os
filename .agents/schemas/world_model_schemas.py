"""
OMNIVERSE RECURRENT STATE-SPACE WORLD MODEL & LATENT DREAMING SCHEMAS
====================================================================
Defines state representations, transition functions, discrete latent categoricals,
and generative video dynamics for DreamerV3 (RSSM) and Wan 2.1 (DiT).
"""

from datetime import datetime
from typing import Dict, List, Optional, Union, Literal, Tuple, Any
from pydantic import BaseModel, Field


class RSSMState(BaseModel):
    """
    DreamerV3 Recurrent State-Space Model (RSSM) Combined State s_t = (h_t, z_t).
    h_t: Deterministic continuous GRU/Transformer state.
    z_t: Stochastic discrete categorical representation (32 classes x 32 categorical dimensions).
    """
    step_index: int = 0
    deterministic_state_dim: int = Field(default=512, description="Continuous recurrent latent state vector size (h_t)")
    stochastic_classes: int = Field(default=32, description="Categorical class count per discrete variable (K)")
    stochastic_variables: int = Field(default=32, description="Number of discrete categorical variables (C)")
    latent_vector: List[float] = Field(default_factory=list, description="Flattened continuous + discrete representation")
    reward_estimate: float = 0.0
    continuation_probability: float = 1.0


class RSSMRolloutConfig(BaseModel):
    """Configuration for latent world dreaming without environmental feedback."""
    imagination_horizon: int = Field(default=32, ge=16, le=128, description="Number of ungrounded imaginary rollout steps")
    action_dim: int = Field(default=16, description="Action / control space vector dimension")
    actor_critic_discount: float = Field(default=0.997, description="Symlog temporal value discount factor gamma")
    temperature: float = Field(default=1.0, description="Softmax sampling temperature for discrete latents")


class RSSMRolloutTrajectory(BaseModel):
    """A simulated counterfactual trajectory in latent space."""
    trajectory_id: str
    scenario_prompt: str
    imagined_steps: int
    states: List[RSSMState] = Field(default_factory=list)
    cumulative_imagined_reward: float = 0.0
    divergence_risk_score: float = Field(default=0.0, description="KL divergence from empirical observation distribution")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class WanVideoDiffusionConfig(BaseModel):
    """Diffusion Transformer (DiT) configuration for Wan 2.1 video generation dynamics."""
    model_name: Literal["Wan2.1-T2V-14B", "Wan2.1-I2V-14B", "Wan2.1-Latent-Light"] = "Wan2.1-T2V-14B"
    num_frames: int = Field(default=81, description="Temporal frame depth (e.g. 5 seconds at 16fps)")
    resolution: Tuple[int, int] = Field(default=(720, 1280), description="Height x Width frame resolution")
    guidance_scale: float = Field(default=6.0, description="Classifier-Free Guidance (CFG) multiplier")
    inference_steps: int = Field(default=40, description="Flow-matching diffusion denoising steps")
    flow_shift: float = Field(default=3.0, description="Time-step shift for high-resolution flow matching")
    use_causal_attention: bool = Field(default=True, description="Enables causal temporal attention for real-time streaming")
