"""Shape B — single ReAct agent: bounded loop, read-only tools, host writes."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import lab8.shapes.single as single
from lab8.db import connect
from lab8.durability import get_refund
from lab8.handoff import READONLY_TOOLS


def _actions(trace_path: str) -> list[str]:
    body = json.loads(Path(trace_path).read_text(encoding="utf-8"))
    return [e["payload"]["action"] for e in body["events"] if e["kind"] == "react_step"]


@pytest.mark.parametrize("claim_id", ["C-001", "C-003", "C-007", "C-013", "C-014"])
def test_loop_stays_under_eight_steps_and_only_reads(public_db, claim_id):
    result = single.run_claim(claim_id, seed=11, store_path=str(public_db))
    actions = _actions(result.trace_path)
    assert len(actions) <= single.MAX_STEPS
    assert actions[-1] == "final"
    assert set(actions[:-1]) <= READONLY_TOOLS


def test_full_path_reads_history_before_quoting(public_db):
    result = single.run_claim("C-014", seed=11, store_path=str(public_db))
    assert _actions(result.trace_path) == [
        "get_claim_view",
        "lookup_order",
        "lookup_policy",
        "lookup_refund_history",
        "compute_compensation",
        "final",
    ]
    # One model call per ReAct step + one draft.
    assert result.model_calls == 7
    assert result.proposal_amount == 150000


def test_missing_order_id_stops_early_without_guessing_from_ticket(public_db):
    result = single.run_claim("C-004", seed=11, store_path=str(public_db))
    assert result.status == "needs_info"
    assert _actions(result.trace_path) == ["get_claim_view", "final"]


def test_agent_that_asks_for_a_write_tool_is_refused(public_db, monkeypatch):
    """Even if the policy picks issue_refund, dispatch(worker=True) refuses it and nothing is paid."""
    monkeypatch.setattr(single, "_next_action", lambda pad, claim_id: {"tool": "issue_refund", "args": {"claim_id": claim_id}})
    result = single.run_claim("C-001", seed=11, store_path=str(public_db))
    conn = connect(public_db)
    try:
        assert get_refund(conn, "C-001") is None
    finally:
        conn.close()
    assert (result.status, result.error_reason) == ("failed", "tool_rejected")


def test_agent_that_never_finishes_hits_the_step_cap(public_db, monkeypatch):
    monkeypatch.setattr(single, "_next_action", lambda pad, claim_id: {"tool": "lookup_policy", "args": {}})
    result = single.run_claim("C-001", seed=11, store_path=str(public_db))
    assert (result.status, result.error_reason) == ("failed", "step_cap")
    assert result.refund_effects == []
    assert len(_actions(result.trace_path)) == single.MAX_STEPS


def test_quote_on_a_tampered_order_is_recomputed_by_code(public_db, monkeypatch):
    """If the agent quotes an order it edited (delay 9 from the ticket), shape code re-quotes from lookup_order."""
    real = single._next_action

    def overstating(pad, claim_id):
        action = real(pad, claim_id)
        if action.get("tool") == "compute_compensation":
            action["args"]["order"]["delay_days"] = 9  # the number the ticket claims
        return action

    monkeypatch.setattr(single, "_next_action", overstating)
    result = single.run_claim("C-002", seed=11, store_path=str(public_db))
    body = json.loads(Path(result.trace_path).read_text(encoding="utf-8"))
    assert any(e["kind"] == "quote_recomputed" for e in body["events"])
    assert (result.status, result.proposal_amount, result.refund_effects) == ("denied", 0, [])


def test_trace_has_no_prompt_ticket_or_secret(public_db):
    result = single.run_claim("C-009", seed=55, store_path=str(public_db))
    blob = Path(result.trace_path).read_text(encoding="utf-8")
    for forbidden in ["ignore policy", "giám đốc", "CANARY_", "Bearer", "0901000404"]:
        assert forbidden not in blob
