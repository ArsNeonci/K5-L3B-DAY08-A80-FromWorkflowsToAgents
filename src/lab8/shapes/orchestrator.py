"""Shape C — orchestrator plus read-only investigators. Student work.

1. Build a handoff with `lab8.handoff.make_handoff`. Allowed tools are read-only.
   Never put parent_secret, raw headers, or the full claim row into facts.
2. `lab8.runtime.run_readonly_investigators` runs those tools.
3. The orchestrator quotes from the investigator's order view and calls
   `durability.issue_refund`. Investigators have no write registry.
   Pass the full quote; the host subtracts earlier refunds on the same order.
   `lookup_refund_history` is a read-only tool you may hand to an investigator.
4. Trace the sanitized handoff, not the parent context.

An LLM summary of the parent context is not a sanitizer. Use the allowlist.

Trace contract v1 (docs/contracts.md): return a trace_path to a JSON file written in this run,
{"run_id": <same run_id>, "events": [...]}, on every return path including early
ones. `lab8.trace.Trace` does this; your own tracer is fine if it matches.

Implementation notes (team):

- Orchestrator (parent): reads the claim view, routes `needs_info` / unknown claim
  itself, plans with one MockLLM call, then delegates. It is the only actor that
  may call `durability.issue_refund`.
- Investigator (worker): receives ONLY the `handoff.v1` payload built by
  `make_handoff` (allowlist + canary check + read-only tools). Its model call sees
  the sanitized handoff, never the ticket or the claim row. It runs through
  `run_readonly_investigators`, whose dispatch uses `worker=True`.
- `allowed_tools` order matters: `lookup_order` must come before
  `compute_compensation`, because the investigator quotes the order it looked up.
- The orchestrator re-checks the investigator's report: the quote must exist and
  be computed on the order the investigator returned; otherwise it recomputes
  from that order with the deterministic tool. Model text never sets the amount.
- Trace: claim flags, sanitized handoff, an allowlisted investigator summary,
  quote, host outcome, result. No ticket text, no parent context, no PII.
"""

from __future__ import annotations

import sqlite3
from typing import Any

from lab8.db import connect
from lab8.durability import InjectedCrash, issue_refund
from lab8.handoff import make_handoff
from lab8.mock_llm import complete
from lab8.runtime import dispatch, run_readonly_investigators
from lab8.schemas import Budget, RunResult, make_run_id
from lab8.shapes.common import finish, safe_dump
from lab8.trace import Trace

SHAPE = "orchestrator"
INVESTIGATOR_TOOLS = ["lookup_order", "lookup_policy", "lookup_refund_history", "compute_compensation"]
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


def _run(
    conn: sqlite3.Connection,
    claim_id: str,
    *,
    seed: int,
    crash_at: str | None,
    shape: str = SHAPE,
    investigator_groups: list[list[str]] | None = None,
) -> RunResult:
    """`investigator_groups` exists for the research-card ablation (1 vs 2 investigators).

    The graded shape always runs with the default: one investigator, INVESTIGATOR_TOOLS.
    """
    groups = investigator_groups or [list(INVESTIGATOR_TOOLS)]
    budget = Budget()
    trace = Trace(make_run_id(shape, claim_id, seed))

    def done(status: str, proposal: int, reason: str | None) -> RunResult:
        trace.add("result", {"status": status, "proposal_amount": int(proposal), "reason": reason})
        return finish(
            conn,
            shape=shape,
            claim_id=claim_id,
            seed=seed,
            status=status,
            proposal_amount=proposal,
            budget=budget,
            trace=trace,
            error_reason=reason,
        )

    # ---- Orchestrator: read the claim view and route the trivial cases. ----
    view = dispatch(conn, budget, "get_claim_view", {"claim_id": claim_id}, worker=False)
    if not view.get("found"):
        trace.add("claim", {"found": False})
        return done("failed", 0, "unknown_claim")
    trace.add("claim", {"found": True, "has_order_id": bool(view.get("order_id"))})
    if not view.get("order_id"):
        _draft(budget, seed, "needs_info")
        return done("needs_info", 0, "missing_order_id")

    # Plan. The orchestrator reads the ticket here; the plan text is not traced and
    # does not change which tools run or what amount is paid.
    complete(budget, seed=seed, purpose="plan", prompt=f"{claim_id}\n{view.get('ticket', '')}")

    tools: dict[str, Any] = {}
    for index, allowed in enumerate(groups):
        # ---- Handoff: allowlist built in code. No parent_secret, headers, or claim row. ----
        handoff = make_handoff(
            request_id=f"REQ-{claim_id}-s{seed}" + (f"-i{index}" if len(groups) > 1 else ""),
            claim_id=claim_id,
            task="verify_eligibility_and_quote",
            facts={},
            allowed_tools=list(allowed),
        )
        trace.add("handoff", safe_dump(handoff))

        # ---- Investigator: read-only, sees only the handoff. ----
        complete(budget, seed=seed, purpose="investigate", prompt=str(sorted(handoff.items())))
        report = run_readonly_investigators(conn, budget, handoff, principal_id=view["principal_id"])
        tools.update(report["tools"])
    order_view = tools.get("lookup_order") or {}
    trace.add("investigator", _investigator_summary(tools))

    # ---- Orchestrator: review the report, then the host writes. ----
    if not order_view.get("visible"):
        _draft(budget, seed, "escalated")
        return done("escalated", 0, order_view.get("reason"))

    order = order_view["order"]
    quote = tools.get("compute_compensation")
    if not isinstance(quote, dict) or "amount_vnd" not in quote:
        quote = dispatch(conn, budget, "compute_compensation", {"order": order}, worker=False)
        trace.add("quote_recomputed", {"amount_vnd": int(quote["amount_vnd"])})
    proposal = int(quote["amount_vnd"])
    trace.add("quote", {"amount_vnd": proposal, "reason": quote["reason"], "clause_ids": list(quote["clause_ids"])})

    if proposal <= 0:
        _draft(budget, seed, "denied")
        return done("denied", 0, quote["reason"])

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
    _draft(budget, seed, "resolved")
    return done("resolved", proposal, None)


def _investigator_summary(tools: dict[str, Any]) -> dict[str, Any]:
    """Allowlisted view of the investigator report for the trace."""
    summary: dict[str, Any] = {"tools_run": sorted(tools)}
    order_view = tools.get("lookup_order") or {}
    if order_view.get("visible"):
        summary["order"] = {key: order_view["order"][key] for key in ORDER_TRACE_FIELDS}
    else:
        summary["order"] = {"visible": False, "reason": order_view.get("reason")}
    policy = tools.get("lookup_policy") or {}
    summary["policy_ids"] = [p["policy_id"] for p in policy.get("policies") or []]
    history = tools.get("lookup_refund_history") or {}
    if history.get("visible"):
        summary["refunded_vnd"] = history.get("refunded_vnd")
    return summary


def _draft(budget: Budget, seed: int, status: str) -> None:
    complete(budget, seed=seed, purpose="draft", prompt=f"status={status}")


def _host_event(outcome: dict[str, Any]) -> dict[str, Any]:
    effect = outcome.get("effect") or {}
    return {
        "ok": bool(outcome["ok"]),
        "reason": outcome["reason"],
        "conflict": bool(outcome["conflict"]),
        "amount_vnd": effect.get("amount_vnd"),
    }
