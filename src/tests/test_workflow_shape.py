"""Shape A — workflow: fixed steps, code owns money, model only drafts text."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import lab8.shapes.workflow as workflow
from lab8.db import connect
from lab8.durability import InjectedCrash, committed_audit_count, get_refund
from tests.conftest import BY_ID


def _spy_issue_refund(monkeypatch):
    calls = []
    real = workflow.issue_refund

    def spy(conn, claim_id, proposed_vnd, *, crash_at=None):
        calls.append((claim_id, proposed_vnd, crash_at))
        return real(conn, claim_id, proposed_vnd, crash_at=crash_at)

    monkeypatch.setattr(workflow, "issue_refund", spy)
    return calls


def test_full_quote_goes_to_the_host_not_the_net_amount(public_db, monkeypatch):
    """T14: 150000 entitlement, 30000 already paid. The host, not the shape, subtracts."""
    calls = _spy_issue_refund(monkeypatch)
    result = workflow.run_claim("C-014", seed=11, store_path=str(public_db))
    assert calls == [("C-014", 150000, None)]
    assert result.status == "resolved"
    assert result.proposal_amount == 150000
    assert result.refund_effects[0]["amount_vnd"] == 120000


@pytest.mark.parametrize("claim_id", ["C-002", "C-004", "C-005", "C-006", "C-009"])
def test_zero_quote_and_early_exits_never_call_the_host(public_db, monkeypatch, claim_id):
    calls = _spy_issue_refund(monkeypatch)
    result = workflow.run_claim(claim_id, seed=55, store_path=str(public_db))
    assert calls == []
    assert result.status == BY_ID[claim_id]["expected"]["status"]
    assert result.proposal_amount == 0


@pytest.mark.parametrize("seed", [11, 22, 33, 44, 55])
def test_ticket_delay_is_ignored_on_every_seed(public_db, seed):
    """T02 ticket says 5 days, order row says 2. Unlike the swarm, seed 55 changes nothing."""
    result = workflow.run_claim("C-002", seed=seed, store_path=str(public_db))
    assert (result.status, result.proposal_amount, result.refund_effects) == ("denied", 0, [])


def test_model_is_called_once_and_only_to_draft(public_db, monkeypatch):
    purposes = []
    real = workflow.complete

    def spy(budget, *, seed, purpose, prompt):
        purposes.append(purpose)
        return real(budget, seed=seed, purpose=purpose, prompt=prompt)

    monkeypatch.setattr(workflow, "complete", spy)
    result = workflow.run_claim("C-001", seed=11, store_path=str(public_db))
    assert purposes == ["draft"]
    assert result.model_calls == 1
    assert result.tool_calls == 3  # get_claim_view, lookup_order, compute_compensation


def test_crash_before_effect_then_resume_pays_once(public_db):
    with pytest.raises(InjectedCrash):
        workflow.run_claim("C-012", seed=11, store_path=str(public_db), crash_at="before_effect")
    conn = connect(public_db)
    try:
        assert get_refund(conn, "C-012") is None
    finally:
        conn.close()
    result = workflow.run_claim("C-012", seed=11, store_path=str(public_db))
    conn = connect(public_db)
    try:
        assert result.status == "resolved"
        assert int(get_refund(conn, "C-012")["amount_vnd"]) == 35000
        assert committed_audit_count(conn, "C-012") == 1
    finally:
        conn.close()


def test_crash_still_flushes_a_clean_trace(public_db):
    with pytest.raises(InjectedCrash):
        workflow.run_claim("C-012", seed=22, store_path=str(public_db), crash_at="after_checkpoint")
    body = json.loads(Path("traces/R-workflow-C-012-s22.json").read_text(encoding="utf-8"))
    assert body["run_id"] == "R-workflow-C-012-s22"
    assert body["events"][-1] == {"kind": "crash", "payload": {"at": "after_checkpoint"}}


def test_trace_never_contains_ticket_text_or_pii(public_db):
    result = workflow.run_claim("C-010", seed=11, store_path=str(public_db))
    blob = Path(result.trace_path).read_text(encoding="utf-8")
    for forbidden in ["giao trễ", "CANARY_", "0901000107", "12 Le Loi", "Ao thun", "principal_id"]:
        assert forbidden not in blob
