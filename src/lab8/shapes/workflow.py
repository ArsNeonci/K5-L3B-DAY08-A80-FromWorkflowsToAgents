"""Shape A — deterministic workflow. Student work.

Signature (do not change):

    run_claim(claim_id, *, seed, store_path, crash_at=None) -> RunResult

Suggested steps. Money stays in code (`lab8.tools.compute_compensation`).

1. Open the store. Read the claim through `get_claim_view` (not SELECT *).
2. Missing order_id -> status `needs_info`. Do not write the ledger.
3. `lookup_order`. If not visible -> `escalated`. Do not copy phone, address, item, internal note.
4. Quote from the order row. Ignore delay numbers written in the ticket.
5. Quote amount 0 -> `denied`. Do not call issue_refund.
6. Quote amount > 0 -> `durability.issue_refund(conn, claim_id, <full quote>)`.
   Pass the FULL quote. The host checks the claim's own approval and subtracts
   what earlier claims already got for the same order (T13, T14). Do not
   subtract it yourself or the host subtracts twice.
   Auth failure or order already refunded -> `denied` (the host writes `policy_denied`).
   `proposal_amount` stays the full quote. Amount conflict -> `failed`.
7. Success -> `resolved`. One ledger row, one `refund_committed` audit.
8. Use MockLLM only to draft the reply text, if you want a model call at all.

The model must not choose the refund amount and must not commit the refund.

Trace contract v1 (docs/contracts.md): return a trace_path to a JSON file written in this run,
{"run_id": <same run_id>, "events": [...]}, on every return path including early
ones. `lab8.trace.Trace` does this; your own tracer is fine if it matches.

Implementation notes (team):

- Every step is fixed Python. There is no branch the model can steer.
- Tool calls go through `lab8.runtime.dispatch(worker=False)` so the Budget counts
  them with the same price as the other shapes.
- The trace only records allowlisted fields: the order view from `lookup_order`
  (no phone / address / internal note / item name), the quote, and the host
  outcome. It never records the ticket text, the claim row, or the draft reply.
- On `InjectedCrash` the trace is flushed and the exception is re-raised, so the
  crash still reaches the caller (T12) and the leak scanner still sees a file.
"""

from __future__ import annotations

import sqlite3
from typing import Any

from lab8.db import connect
from lab8.durability import InjectedCrash, issue_refund
from lab8.mock_llm import complete
from lab8.runtime import dispatch
from lab8.schemas import Budget, RunResult, make_run_id
from lab8.shapes.common import finish
from lab8.trace import Trace

SHAPE = "workflow"
# Fields of the order view that the decision depends on. Written to the trace.
ORDER_TRACE_FIELDS = ("order_id", "status", "delay_days", "shipping_fee_vnd", "paid_vnd", "damage_verified")


def run_claim(
    claim_id: str,
    *,
    seed: int,
    store_path: str,
    crash_at: str | None = None,
) -> RunResult:
    conn = connect(store_path)
    try:
        return _run(conn, claim_id, seed=seed, crash_at=crash_at)
    finally:
        conn.close()


def _run(conn: sqlite3.Connection, claim_id: str, *, seed: int, crash_at: str | None) -> RunResult:
    budget = Budget()
    trace = Trace(make_run_id(SHAPE, claim_id, seed))

    def done(status: str, proposal: int, reason: str | None) -> RunResult:
        trace.add("result", {"status": status, "proposal_amount": int(proposal), "reason": reason})
        return finish(
            conn,
            shape=SHAPE,
            claim_id=claim_id,
            seed=seed,
            status=status,
            proposal_amount=proposal,
            budget=budget,
            trace=trace,
            error_reason=reason,
        )

    # Step 1 — claim view (allowlisted: claim_id, principal_id, order_id, ticket).
    view = dispatch(conn, budget, "get_claim_view", {"claim_id": claim_id}, worker=False)
    if not view.get("found"):
        trace.add("claim", {"found": False})
        return done("failed", 0, "unknown_claim")
    trace.add("claim", {"found": True, "has_order_id": bool(view.get("order_id"))})

    # Step 2 — no order id: ask for it. Never mine an order id out of the ticket text.
    if not view.get("order_id"):
        _draft(budget, seed, "needs_info")
        return done("needs_info", 0, "missing_order_id")

    # Step 3 — order row scoped to the claim's principal.
    order_view = dispatch(
        conn,
        budget,
        "lookup_order",
        {"order_id": view["order_id"], "principal_id": view["principal_id"]},
        worker=False,
    )
    if not order_view.get("visible"):
        trace.add("order", {"visible": False, "reason": order_view.get("reason")})
        _draft(budget, seed, "escalated")
        return done("escalated", 0, order_view.get("reason"))
    order = order_view["order"]
    trace.add("order", {"visible": True, **{key: order[key] for key in ORDER_TRACE_FIELDS}})

    # Step 4 — quote from the structured order row and current policy only.
    quote = dispatch(conn, budget, "compute_compensation", {"order": order}, worker=False)
    proposal = int(quote["amount_vnd"])
    trace.add("quote", {"amount_vnd": proposal, "reason": quote["reason"], "clause_ids": list(quote["clause_ids"])})

    # Step 5 — nothing owed: deny without touching the host.
    if proposal <= 0:
        _draft(budget, seed, "denied")
        return done("denied", 0, quote["reason"])

    # Step 6 — the host is the only writer. Full quote in, crash_at forwarded.
    try:
        outcome = issue_refund(conn, claim_id, proposal, crash_at=crash_at)
    except InjectedCrash:
        trace.add("crash", {"at": crash_at})
        trace.write()
        raise
    trace.add("host", _host_event(outcome))

    if not outcome["ok"]:
        status = "failed" if outcome["conflict"] else "denied"
        _draft(budget, seed, status)
        return done(status, proposal, outcome["reason"])

    # Step 7 — committed (or idempotent replay of the same amount).
    _draft(budget, seed, "resolved")
    return done("resolved", proposal, None)


def _draft(budget: Budget, seed: int, status: str) -> None:
    """The only model call: customer-facing wording. Its text never decides anything."""
    complete(budget, seed=seed, purpose="draft", prompt=f"status={status}")


def _host_event(outcome: dict[str, Any]) -> dict[str, Any]:
    effect = outcome.get("effect") or {}
    return {
        "ok": bool(outcome["ok"]),
        "reason": outcome["reason"],
        "conflict": bool(outcome["conflict"]),
        "amount_vnd": effect.get("amount_vnd"),
    }
