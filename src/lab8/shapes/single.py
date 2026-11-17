"""Shape B — one ReAct agent. Student work.

Use `lab8.runtime.run_react` with max_steps=8. `decide` may pick a read tool.
It must not call `issue_refund`. After the loop, the host validates the quote
and is the only writer.

A decide() that trusts ticket text over the order row will fail hidden claims
where the customer overstates the delay or cites a superseded clause.

Per-order cap: an order may already have been refunded by an earlier claim.
The read tool `lookup_refund_history` shows how much. The host still enforces
the cap, so pass the full quote to `durability.issue_refund`, not a net amount.

Caps: stop at 8 steps. Count model calls in the Budget so cost stays comparable.

Trace contract v1 (docs/contracts.md): return a trace_path to a JSON file written in this run,
{"run_id": <same run_id>, "events": [...]}, on every return path including early
ones. `lab8.trace.Trace` does this; your own tracer is fine if it matches.

Implementation notes (team):

- The agent is a `decide(observation)` policy driven by MockLLM: every step is one
  model call (`purpose="react"`), then the agent picks ONE read tool or a final.
  `run_react` runs with `worker=True`, so `dispatch` refuses any tool outside the
  read-only registry even if decide() asked for it.
- `run_react` only hands back the last tool result, so the agent keeps a small
  scratchpad (`_Scratchpad`) of tool outputs. Those outputs come from code, not
  from model text.
- The agent never reads numbers from the ticket. The quote is requested with the
  order dict returned by `lookup_order`.
- After the loop, shape code (not the agent) re-checks that the quote was computed
  on the same order the lookup returned, recomputes it if not, and is the only
  caller of `durability.issue_refund` with the FULL quote.
- The trace keeps tool names and allowlisted summaries per step. It never keeps
  the ticket, the prompt, the claim row, or the model text.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass, field
from typing import Any

from lab8.db import connect
from lab8.durability import InjectedCrash, issue_refund
from lab8.mock_llm import complete
from lab8.runtime import ToolRejected, dispatch, run_react
from lab8.schemas import Budget, RunResult, make_run_id
from lab8.shapes.common import finish
from lab8.trace import Trace

SHAPE = "single"
MAX_STEPS = 8
ORDER_TRACE_FIELDS = ("order_id", "status", "delay_days", "shipping_fee_vnd", "paid_vnd", "damage_verified")


@dataclass
class _Scratchpad:
    """What the agent has learned from tools so far. Only tool output lands here."""

    claim: dict[str, Any] | None = None
    order_view: dict[str, Any] | None = None
    policy: dict[str, Any] | None = None
    history: dict[str, Any] | None = None
    quote: dict[str, Any] | None = None
    quote_order: dict[str, Any] | None = None
    tools_called: list[str] = field(default_factory=list)


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
    pad = _Scratchpad()

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

    decide = _make_decide(budget, trace, pad, claim_id=claim_id, seed=seed)
    try:
        loop = run_react(
            conn,
            budget,
            observation={"claim_id": claim_id},
            decide=decide,
            max_steps=MAX_STEPS,
            worker=True,  # read-only registry: write tools are refused by dispatch
        )
    except ToolRejected as exc:
        trace.add("tool_rejected", {"reason": str(exc)[:80]})
        return done("failed", 0, "tool_rejected")

    final = loop["final"]
    trace.add("react_end", {"stopped": loop["stopped"], "decision": final.get("decision"), "steps": len(pad.tools_called)})
    if loop["stopped"] != "final":
        return done("failed", 0, "step_cap")

    decision = final.get("decision")
    if decision == "unknown_claim":
        return done("failed", 0, "unknown_claim")
    if decision == "needs_info":
        _draft(budget, seed, "needs_info")
        return done("needs_info", 0, "missing_order_id")
    if decision == "escalate":
        _draft(budget, seed, "escalated")
        return done("escalated", 0, (pad.order_view or {}).get("reason"))
    if decision != "quote" or pad.order_view is None or not pad.order_view.get("visible"):
        return done("failed", 0, "agent_final_without_quote")

    # ---- Host side. The agent is done; code validates the quote and writes. ----
    order = pad.order_view["order"]
    quote = pad.quote
    if quote is None or pad.quote_order != order:
        # The quote must come from compute_compensation on the order lookup_order returned.
        quote = dispatch(conn, budget, "compute_compensation", {"order": order}, worker=True)
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


def _make_decide(budget: Budget, trace: Trace, pad: _Scratchpad, *, claim_id: str, seed: int):
    """Build the agent policy. One MockLLM call per step; the next action depends on tool output only."""

    def decide(seen: dict[str, Any]) -> dict[str, Any]:
        _remember(pad, trace, seen)
        # The model "thinks" over what it has seen. Text is not parsed for decisions.
        complete(budget, seed=seed, purpose="react", prompt=json.dumps(seen, ensure_ascii=False, default=str))
        action = _next_action(pad, claim_id)
        trace.add("react_step", {"step": len(pad.tools_called) + 1, "action": action.get("tool") or "final"})
        if "tool" in action:
            pad.tools_called.append(action["tool"])
            if action["tool"] == "compute_compensation":
                # Remember exactly which order the agent asked to quote; the host side compares it.
                pad.quote_order = dict((action.get("args") or {}).get("order") or {})
        return action

    return decide


def _next_action(pad: _Scratchpad, claim_id: str) -> dict[str, Any]:
    if pad.claim is None:
        return {"tool": "get_claim_view", "args": {"claim_id": claim_id}}
    if not pad.claim.get("found"):
        return {"final": {"decision": "unknown_claim"}}
    if not pad.claim.get("order_id"):
        # Missing order id: ask. Never extract an order id from the ticket text.
        return {"final": {"decision": "needs_info"}}
    if pad.order_view is None:
        return {
            "tool": "lookup_order",
            "args": {"order_id": pad.claim["order_id"], "principal_id": pad.claim["principal_id"]},
        }
    if not pad.order_view.get("visible"):
        return {"final": {"decision": "escalate"}}
    if pad.policy is None:
        return {"tool": "lookup_policy", "args": {}}
    if pad.history is None:
        return {
            "tool": "lookup_refund_history",
            "args": {"order_id": pad.claim["order_id"], "principal_id": pad.claim["principal_id"]},
        }
    if pad.quote is None:
        # Quote from the structured order row, not from numbers in the ticket.
        return {"tool": "compute_compensation", "args": {"order": dict(pad.order_view["order"])}}
    return {"final": {"decision": "quote"}}


def _remember(pad: _Scratchpad, trace: Trace, seen: dict[str, Any]) -> None:
    """Store the last tool result and trace an allowlisted summary of it."""
    name = seen.get("last_tool")
    result = seen.get("last_result")
    if not name or not isinstance(result, dict):
        return
    if name == "get_claim_view":
        pad.claim = result
        summary = {"found": bool(result.get("found")), "has_order_id": bool(result.get("order_id"))}
    elif name == "lookup_order":
        pad.order_view = result
        if result.get("visible"):
            summary = {"visible": True, **{key: result["order"][key] for key in ORDER_TRACE_FIELDS}}
        else:
            summary = {"visible": False, "reason": result.get("reason")}
    elif name == "lookup_policy":
        pad.policy = result
        summary = {"policy_ids": [p["policy_id"] for p in result.get("policies") or []]}
    elif name == "lookup_refund_history":
        pad.history = result
        summary = {
            "visible": bool(result.get("visible")),
            "refund_count": result.get("refund_count"),
            "refunded_vnd": result.get("refunded_vnd"),
        }
    elif name == "compute_compensation":
        pad.quote = result
        summary = {"amount_vnd": result.get("amount_vnd"), "reason": result.get("reason")}
    else:
        summary = {}
    trace.add("observation", {"tool": name, **summary})


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
