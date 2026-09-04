"""
Deterministic Quality Gate Evaluator for Cross-Department Workflow Handoffs.
"""

import time
import asyncio
from typing import Dict, List, Optional, Any, Callable
from pydantic import BaseModel, Field


class QualityCheck(BaseModel):
    """An atomic verification condition within a quality gate."""
    name: str
    description: str
    handler: Any  # Callable returning bool or Dict[str, Any] with 'passed'
    is_blocking: bool = True
    dri: str = "qa_auto_script"


class QualityGateResult(BaseModel):
    """Aggregated outcome of a quality gate evaluation."""
    gate_name: str
    passed: bool
    checks_run: int = 0
    passed_checks: List[str] = Field(default_factory=list)
    failed_checks: List[Dict[str, Any]] = Field(default_factory=list)
    duration_ms: float = 0.0
    dri_signoff: Optional[str] = None


class QualityGate:
    """
    Evaluates a suite of deterministic quality checks before allowing state transitions.
    """

    def __init__(self, name: str, dri: str = "qa_auto_script"):
        self.name = name
        self.dri = dri
        self.checks: List[QualityCheck] = []

    def add_check(
        self,
        name: str,
        handler: Callable,
        description: str = "",
        is_blocking: bool = True,
        dri: Optional[str] = None
    ) -> "QualityGate":
        """Chainable helper to register verification checks."""
        self.checks.append(QualityCheck(
            name=name,
            description=description,
            handler=handler,
            is_blocking=is_blocking,
            dri=dri or self.dri
        ))
        return self

    async def evaluate(self, context: Optional[Dict[str, Any]] = None) -> QualityGateResult:
        """Execute all quality checks and verify consensus."""
        ctx = context or {}
        start_time = time.perf_counter()
        
        passed_checks = []
        failed_checks = []
        overall_passed = True

        for check in self.checks:
            try:
                if asyncio.iscoroutinefunction(check.handler):
                    res = await check.handler(ctx)
                else:
                    res = check.handler(ctx)

                is_ok = False
                error_detail = None

                if isinstance(res, bool):
                    is_ok = res
                elif isinstance(res, dict):
                    is_ok = res.get("passed", res.get("success", False))
                    error_detail = res.get("error", res.get("message"))
                else:
                    is_ok = bool(res)

                if is_ok:
                    passed_checks.append(check.name)
                else:
                    failed_checks.append({
                        "check_name": check.name,
                        "is_blocking": check.is_blocking,
                        "error": error_detail or f"Verification condition '{check.name}' failed.",
                        "dri": check.dri
                    })
                    if check.is_blocking:
                        overall_passed = False

            except Exception as exc:
                failed_checks.append({
                    "check_name": check.name,
                    "is_blocking": check.is_blocking,
                    "error": f"Exception raised during check: {exc}",
                    "dri": check.dri
                })
                if check.is_blocking:
                    overall_passed = False

        duration = (time.perf_counter() - start_time) * 1000.0
        return QualityGateResult(
            gate_name=self.name,
            passed=overall_passed,
            checks_run=len(self.checks),
            passed_checks=passed_checks,
            failed_checks=failed_checks,
            duration_ms=round(duration, 2),
            dri_signoff=self.dri if overall_passed else None
        )
