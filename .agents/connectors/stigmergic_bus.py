"""
OMNIVERSE STIGMERGIC AGENT BUS & MATRIX COORDINATION ENGINE
===========================================================
AgentScope-inspired environmental stigmergy communication engine.
Enables autonomous agents across all 15 Pods to read and write state markers
to .agents/memory/matrix_state.json without central lock contention.
"""

import json
import uuid
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

# Ensure .agents root is in sys.path
_AGENTS_ROOT = Path(__file__).resolve().parent.parent
if str(_AGENTS_ROOT) not in sys.path:
    sys.path.insert(0, str(_AGENTS_ROOT))

from schemas.stigmergy_schemas import (
    StigmergicMarker,
    MatrixState,
    ToolCallInvocation,
    ToolCallResult
)


class OmniverseStigmergicBus:
    """
    Decentralized stigmergic bus managing matrix memory traces and tool dispatching.
    """

    def __init__(self, matrix_path: Optional[Path] = None):
        self.matrix_path = matrix_path or Path("/Users/silversurfer/Documents/aether Core 999/.agents/memory/matrix_state.json")
        self.matrix_path.parent.mkdir(parents=True, exist_ok=True)
        self.state = self._load_matrix_state()

    def _load_matrix_state(self) -> MatrixState:
        """Load active matrix state from disk or initialize empty state."""
        if self.matrix_path.exists():
            try:
                data = json.loads(self.matrix_path.read_text(encoding="utf-8"))
                return MatrixState.model_validate(data)
            except Exception:
                pass
        
        state = MatrixState(
            version="2.0.0",
            active_workspace_hub="aether Core 999",
            active_markers=[],
            global_entropy_score=0.042,
            last_checkpoint_id="CKPT-FRONTIER-INIT"
        )
        self._save_matrix_state(state)
        return state

    def _save_matrix_state(self, state: Optional[MatrixState] = None) -> None:
        """Atomically persist matrix state."""
        s = state or self.state
        s.updated_at = datetime.utcnow()
        self.matrix_path.write_text(
            json.dumps(s.model_dump(), indent=2, default=str),
            encoding="utf-8"
        )

    def deposit_marker(
        self,
        author_agent_id: str,
        domain: str,
        action_type: str,
        payload: Dict[str, Any],
        salience: float = 1.0
    ) -> StigmergicMarker:
        """
        Deposits an environmental stigmergic trace onto the shared matrix.
        """
        marker = StigmergicMarker(
            marker_id=f"MARKER-{uuid.uuid4().hex[:6].upper()}",
            author_agent_id=author_agent_id,
            domain=domain,
            action_type=action_type,
            state_payload=payload,
            salience_weight=salience
        )
        self.state.active_markers.append(marker)
        
        if len(self.state.active_markers) > 100:
            self.state.active_markers = self.state.active_markers[-100:]
            
        self._save_matrix_state()
        return marker

    def scan_markers(
        self,
        domain: Optional[str] = None,
        min_salience: float = 0.3
    ) -> List[StigmergicMarker]:
        """
        Scans environmental markers matching a domain filter and salience threshold.
        """
        results = []
        for m in self.state.active_markers:
            if m.salience_weight >= min_salience:
                if domain is None or m.domain == domain:
                    results.append(m)
        return results

    def decay_markers(self, decay_factor: float = 0.95) -> None:
        """Applies temporal evaporation to marker salience."""
        for m in self.state.active_markers:
            m.salience_weight = round(m.salience_weight * decay_factor, 4)
        self.state.active_markers = [m for m in self.state.active_markers if m.salience_weight > 0.05]
        self._save_matrix_state()


# Global Singleton Bus
GLOBAL_STIGMERGIC_BUS = OmniverseStigmergicBus()
