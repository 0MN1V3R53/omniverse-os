"""
Internal Compute Credit Ledger.
Tracks token expenditure per departmental Pod and persists transactions to JSONL.
"""

import json
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

from core.config import CONFIG
from core.economy.models import ComputeTransaction, PodBudget


class InsufficientCreditsError(Exception):
    """Raised when a Pod exhausts its compute credit quota."""
    pass


class CreditLedger:
    """
    Virtual credit ledger managing pod compute allocations and usage.
    """

    def __init__(self, ledger_path: Optional[Path] = None):
        self.ledger_path = ledger_path or (CONFIG.workspace_root / ".runtime" / "compute_ledger.jsonl")
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        
        self._budgets: Dict[str, PodBudget] = {
            "Web Frontend": PodBudget(pod_name="Web Frontend", allocated_credits=2500.0),
            "DevOps SRE": PodBudget(pod_name="DevOps SRE", allocated_credits=2000.0),
            "Growth Squad": PodBudget(pod_name="Growth Squad", allocated_credits=2000.0),
            "Security Pod": PodBudget(pod_name="Security Pod", allocated_credits=1500.0),
            "Executive Suite": PodBudget(pod_name="Executive Suite", allocated_credits=5000.0),
            "Data Science": PodBudget(pod_name="Data Science", allocated_credits=2000.0),
            "QA Pod": PodBudget(pod_name="QA Pod", allocated_credits=1500.0),
        }
        self._load_transactions()

    def _load_transactions(self) -> None:
        """Replay existing transaction log to calculate current spent balances."""
        if not self.ledger_path.exists():
            return
        with open(self.ledger_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                    tx = ComputeTransaction(**data)
                    budget = self._budgets.get(tx.pod_name)
                    if budget:
                        budget.spent_credits = round(budget.spent_credits + tx.credits_deducted, 4)
                except Exception:
                    continue

    def get_budget(self, pod_name: str) -> PodBudget:
        """Get or initialize budget for a pod."""
        if pod_name not in self._budgets:
            self._budgets[pod_name] = PodBudget(pod_name=pod_name, allocated_credits=1000.0)
        return self._budgets[pod_name]

    def get_all_budgets(self) -> Dict[str, PodBudget]:
        """Return all pod budgets."""
        return self._budgets

    def charge_compute(
        self,
        agent_id: str,
        pod_name: str,
        ticket_id: str,
        tokens_consumed: int,
        rate_per_k: float = 0.05
    ) -> ComputeTransaction:
        """
        Record a compute token charge and deduct credits from the pod budget.
        """
        credits_to_deduct = round((tokens_consumed / 1000.0) * rate_per_k, 4)

        with self._lock:
            budget = self.get_budget(pod_name)
            if budget.available_credits < credits_to_deduct:
                # Quota exceeded
                raise InsufficientCreditsError(
                    f"Pod '{pod_name}' has insufficient compute credits: {budget.available_credits} available, required {credits_to_deduct}."
                )

            budget.spent_credits = round(budget.spent_credits + credits_to_deduct, 4)

            tx = ComputeTransaction(
                agent_id=agent_id,
                pod_name=pod_name,
                ticket_id=ticket_id,
                tokens_consumed=tokens_consumed,
                credits_deducted=credits_to_deduct,
                rate_per_k_token=rate_per_k
            )

            # Append to JSONL
            line = json.dumps(tx.model_dump(), default=str) + "\n"
            with open(self.ledger_path, "a", encoding="utf-8") as f:
                f.write(line)

        return tx


GLOBAL_LEDGER = CreditLedger()

