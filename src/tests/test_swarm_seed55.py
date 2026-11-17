"""Verify when the reference Swarm changes its quote and when the host blocks payment."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from lab8.db import connect
from lab8.durability import get_refund
from lab8.shapes.swarm_reference import run_claim as swarm
from lab8.shapes.workflow import run_claim as workflow


def _events(result) -> list[str]:
    return [e["kind"] for e in json.loads(Path(result.trace_path).read_text(encoding="utf-8"))["events"]]


@pytest.mark.parametrize("seed,fires", [(5, True), (10, True), (55, True), (11, False), (22, False), (44, False)])
def test_weakness_fires_only_on_seeds_divisible_by_five(public_db, seed, fires):
    result = swarm("C-002", seed=seed, store_path=str(public_db))
    assert ("model_override" in _events(result)) is fires
    assert result.status == ("resolved" if fires else "denied")


def test_weakness_needs_a_ticket_delay_that_disagrees_with_the_order(public_db):
    """C-001: ticket says 4 days and the order says 4. Seed 55 changes nothing."""
    result = swarm("C-001", seed=55, store_path=str(public_db))
    assert "model_override" not in _events(result)
    assert (result.status, result.proposal_amount) == ("resolved", 35000)


def test_host_still_blocks_the_inflated_quote_when_approval_is_missing(public_db):
    """Swarm believes '5 days' on seed 55 and proposes 20000, but without an approval the host writes nothing."""
    conn = connect(public_db)
    conn.execute(
        "INSERT INTO claims (claim_id, principal_id, order_id, ticket, parent_secret, raw_headers_json, approval_id) "
        "VALUES ('C-NOAPP', 'P-100', 'O-202', 'Đơn giao trễ 5 ngày.', 'CANARY_SECRET_PARENT_NOAPP', '{}', NULL)"
    )
    conn.commit()
    conn.close()
    result = swarm("C-NOAPP", seed=55, store_path=str(public_db))
    conn = connect(public_db)
    try:
        assert get_refund(conn, "C-NOAPP") is None
    finally:
        conn.close()
    assert (result.status, result.proposal_amount, result.error_reason) == ("denied", 20000, "missing_approval")


def test_workflow_does_not_share_the_weakness(public_db):
    """Same claim and seed as the swarm miss: the workflow denies."""
    result = workflow("C-002", seed=55, store_path=str(public_db))
    assert (result.status, result.proposal_amount) == ("denied", 0)
