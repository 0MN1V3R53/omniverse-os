"""
Speculative Multiverse Sandbox & Container Isolation Package.
"""

from .models import CandidateBranch, BenchmarkScore, MultiverseEvaluationResult
from .multiverse import MultiverseSandboxEngine, GLOBAL_MULTIVERSE_SANDBOX
from .container_runner import (
    ContainerConfig,
    ContainerExecutionResult,
    DockerSandboxRunner,
    GLOBAL_SANDBOX_RUNNER
)

__all__ = [
    "CandidateBranch",
    "BenchmarkScore",
    "MultiverseEvaluationResult",
    "MultiverseSandboxEngine",
    "GLOBAL_MULTIVERSE_SANDBOX",
    "ContainerConfig",
    "ContainerExecutionResult",
    "DockerSandboxRunner",
    "GLOBAL_SANDBOX_RUNNER",
]
