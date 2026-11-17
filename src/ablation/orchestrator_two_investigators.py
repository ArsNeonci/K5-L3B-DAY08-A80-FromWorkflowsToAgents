"""Ablation R1 (research card): orchestrator with TWO read-only investigators.

Only one variable changes versus shape C: the number of investigators. Same
MockLLM, tools, claims, seeds, prices, evaluator, and host. The four read tools
are split into two independent groups; each investigator gets its own
sanitized handoff.v1 and its own model call.

    python -m lab8.benchmark --shapes orchestrator,orchestrator_2inv \
        --extra-shape orchestrator_2inv=ablation.orchestrator_two_investigators:run_claim \
        --seeds 11,22,33,44,55 --out reports/ablation_r1.json
"""

from __future__ import annotations

from lab8.db import connect
from lab8.schemas import RunResult
from lab8.shapes import orchestrator

SHAPE = "orchestrator_2inv"
# compute_compensation depends on lookup_order, so they stay in the same group.
GROUPS = [
    ["lookup_order", "compute_compensation"],
    ["lookup_policy", "lookup_refund_history"],
]


def run_claim(
    claim_id: str,
    *,
    seed: int,
    store_path: str,
    crash_at: str | None = None,
) -> RunResult:
    conn = connect(store_path)
    try:
        return orchestrator._run(
            conn, claim_id, seed=seed, crash_at=crash_at, shape=SHAPE, investigator_groups=GROUPS
        )
    finally:
        conn.close()
