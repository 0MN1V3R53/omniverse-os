"""
Associative Neural Processing Substrate & Spreading Activation Engine.
Models nodes as Agents, Tools, and Memory Heuristics with mathematical energy propagation and threshold filtering.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any
from datetime import datetime
from pydantic import BaseModel, Field

from core.config import CONFIG


class NeuralNode(BaseModel):
    """An atomic cognitive node in the associative network."""
    node_id: str
    node_type: str  # agent, tool, heuristic, domain_concept
    label: str
    activation: float = 0.0
    base_salience: float = 0.5


class SynapticEdge(BaseModel):
    """Directional associative connection between two neural nodes."""
    source_id: str
    target_id: str
    weight: float = 0.5  # 0.0 to 1.0
    last_reinforced: datetime = Field(default_factory=datetime.utcnow)


class SynapticTopology(BaseModel):
    """Persistent neural network topology and synaptic weights."""
    version: str = "1.0.0"
    nodes: Dict[str, NeuralNode] = Field(default_factory=dict)
    edges: List[SynapticEdge] = Field(default_factory=list)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class SpreadingActivationEngine:
    """
    Spreading activation engine for context pruning and associative recall.
    """

    def __init__(self, topology_path: Optional[Path] = None):
        self.topology_path = topology_path or (CONFIG.agents_dir / "memory" / "synaptic_weights.json")
        self.topology_path.parent.mkdir(parents=True, exist_ok=True)
        self.topology = self._load_topology()

    def _load_topology(self) -> SynapticTopology:
        """Load synaptic weights from JSON or initialize with enterprise seed network."""
        if self.topology_path.exists():
            try:
                data = json.loads(self.topology_path.read_text(encoding="utf-8"))
                return SynapticTopology.model_validate(data)
            except Exception:
                pass

        # Seed network
        nodes = {
            # Agents
            "agent:growth_meta_buyer": NeuralNode(node_id="agent:growth_meta_buyer", node_type="agent", label="Growth Meta Buyer"),
            "agent:web_frontend_julian_thorne": NeuralNode(node_id="agent:web_frontend_julian_thorne", node_type="agent", label="Julian Thorne (Frontend)"),
            "agent:web_devops_marcus_chen": NeuralNode(node_id="agent:web_devops_marcus_chen", node_type="agent", label="Marcus Chen (DevOps SRE)"),
            "agent:security_ciso_michael_chang": NeuralNode(node_id="agent:security_ciso_michael_chang", node_type="agent", label="Michael Chang (CISO)"),
            # Tools
            "tool:ast_navigator": NeuralNode(node_id="tool:ast_navigator", node_type="tool", label="Symbolic AST Navigator"),
            "tool:multiverse_sandbox": NeuralNode(node_id="tool:multiverse_sandbox", node_type="tool", label="Multiverse Sandbox Engine"),
            "tool:invariant_verifier": NeuralNode(node_id="tool:invariant_verifier", node_type="tool", label="Neuro-Symbolic Invariant Verifier"),
            "tool:youtube_crawler": NeuralNode(node_id="tool:youtube_crawler", node_type="tool", label="YouTube Intelligence Crawler"),
            # Domain Concepts
            "concept:route_conversion": NeuralNode(node_id="concept:route_conversion", node_type="domain_concept", label="Corridor Route Conversion"),
            "concept:syntax_refactor": NeuralNode(node_id="concept:syntax_refactor", node_type="domain_concept", label="AST Code Refactoring"),
            "concept:security_perimeter": NeuralNode(node_id="concept:security_perimeter", node_type="domain_concept", label="Zero-Drift Security Perimeter"),
        }

        edges = [
            # Route conversion cluster
            SynapticEdge(source_id="concept:route_conversion", target_id="agent:growth_meta_buyer", weight=0.95),
            SynapticEdge(source_id="agent:growth_meta_buyer", target_id="tool:youtube_crawler", weight=0.85),
            SynapticEdge(source_id="concept:route_conversion", target_id="agent:web_frontend_julian_thorne", weight=0.75),

            # Syntax refactor cluster
            SynapticEdge(source_id="concept:syntax_refactor", target_id="agent:web_frontend_julian_thorne", weight=0.95),
            SynapticEdge(source_id="agent:web_frontend_julian_thorne", target_id="tool:ast_navigator", weight=0.98),
            SynapticEdge(source_id="agent:web_frontend_julian_thorne", target_id="tool:multiverse_sandbox", weight=0.90),

            # Security cluster
            SynapticEdge(source_id="concept:security_perimeter", target_id="agent:security_ciso_michael_chang", weight=0.98),
            SynapticEdge(source_id="agent:security_ciso_michael_chang", target_id="tool:invariant_verifier", weight=0.95),
            SynapticEdge(source_id="agent:security_ciso_michael_chang", target_id="agent:web_devops_marcus_chen", weight=0.85),
        ]

        top = SynapticTopology(nodes=nodes, edges=edges)
        self._save_topology(top)
        return top

    def _save_topology(self, topology: Optional[SynapticTopology] = None) -> None:
        """Persist synaptic weights to JSON."""
        top = topology or self.topology
        top.updated_at = datetime.utcnow()
        self.topology_path.write_text(
            json.dumps(top.model_dump(), indent=2, default=str),
            encoding="utf-8"
        )

    def propagate_activation(
        self,
        seed_concepts: Dict[str, float],
        decay_factor: float = 0.85,
        iterations: int = 3
    ) -> Dict[str, float]:
        """
        Execute Spreading Activation across the neural associative graph.
        Formula: A_j(t+1) = sum(A_i(t) * w_ij) * decay_factor
        """
        # Reset activations
        for node in self.topology.nodes.values():
            node.activation = 0.0

        # Inject initial energy into seed concepts
        for concept_id, energy in seed_concepts.items():
            if concept_id in self.topology.nodes:
                self.topology.nodes[concept_id].activation = min(1.0, max(0.0, energy))

        # Iterative propagation
        for _ in range(iterations):
            next_activations = {nid: node.activation for nid, node in self.topology.nodes.items()}
            
            for edge in self.topology.edges:
                src_act = self.topology.nodes[edge.source_id].activation if edge.source_id in self.topology.nodes else 0.0
                if src_act > 0.05 and edge.target_id in self.topology.nodes:
                    incoming = src_act * edge.weight * decay_factor
                    next_activations[edge.target_id] = min(1.0, next_activations[edge.target_id] + incoming)

            # Apply updates
            for nid, act in next_activations.items():
                self.topology.nodes[nid].activation = round(act, 4)

        return {nid: node.activation for nid, node in self.topology.nodes.items()}

    def get_active_context_set(self, threshold: float = 0.70) -> List[NeuralNode]:
        """
        Extract high-salience nodes (activation >= threshold) and prune sub-threshold nodes.
        """
        return [
            node for node in self.topology.nodes.values()
            if node.activation >= threshold
        ]

    def reinforce_synapse(self, source_id: str, target_id: str, delta: float = 0.05) -> None:
        """
        Hebbian reinforcement: strengthen connection between co-active winning nodes.
        """
        for edge in self.topology.edges:
            if edge.source_id == source_id and edge.target_id == target_id:
                edge.weight = min(1.0, round(edge.weight + delta, 4))
                edge.last_reinforced = datetime.utcnow()
                self._save_topology()
                return

        # New synapse if non-existent
        new_edge = SynapticEdge(source_id=source_id, target_id=target_id, weight=min(1.0, 0.5 + delta))
        self.topology.edges.append(new_edge)
        self._save_topology()

    def decay_all_synapses(self, decay_rate: float = 0.98) -> None:
        """
        Synaptic weight decay on idle/unused pathways.
        """
        for edge in self.topology.edges:
            edge.weight = max(0.10, round(edge.weight * decay_rate, 4))
        self._save_topology()


# Global Singleton Activation Engine
GLOBAL_SPREADING_ACTIVATION = SpreadingActivationEngine()
