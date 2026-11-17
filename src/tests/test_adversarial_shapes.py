"""Integration (leader): every shape on hand-labelled adversarial claims, five seeds.

The three team shapes must pass every trial. The reference swarm must pass every
trial except its documented seed-55 weakness (it trusts a delay written in the ticket).
"""

from __future__ import annotations

import time

import pytest

from lab8.db import connect, init_store
from lab8.metrics import trial_pass
from lab8.shapes import SHAPES
from tests.adversarial_cases import ALL_CLAIMS_ADV, BY_ID_ADV, CASES_ADV, SWARM_ADV_MISSES, WORLD_ADV

SEEDS = [11, 22, 33, 44, 55]
TEAM_SHAPES = ["workflow", "single", "orchestrator"]


def _run(tmp_path, shape: str, claim_id: str, seed: int):
    store = tmp_path / f"{shape}-{claim_id}-{seed}.sqlite"
    init_store(store, WORLD_ADV, ALL_CLAIMS_ADV).close()
    started = time.time()
    result = SHAPES[shape](claim_id, seed=seed, store_path=str(store))
    conn = connect(store)
    try:
        verdict = trial_pass(result.as_dict(), BY_ID_ADV[claim_id]["expected"], conn, started_at=started)
    finally:
        conn.close()
    return result, verdict


@pytest.mark.parametrize("seed", SEEDS)
@pytest.mark.parametrize("claim_id", [case["claim_id"] for case in CASES_ADV])
@pytest.mark.parametrize("shape", TEAM_SHAPES)
def test_team_shapes_pass_adversarial_claims(tmp_path, shape, claim_id, seed):
    _, (passed, reason) = _run(tmp_path, shape, claim_id, seed)
    assert passed, f"{shape} {claim_id} seed {seed} ({BY_ID_ADV[claim_id]['rule']}): {reason}"


@pytest.mark.parametrize("claim_id", [case["claim_id"] for case in CASES_ADV])
def test_swarm_reference_only_misses_its_documented_weakness(tmp_path, claim_id):
    for seed in SEEDS:
        _, (passed, reason) = _run(tmp_path, "swarm", claim_id, seed)
        if (claim_id, seed) in SWARM_ADV_MISSES:
            assert not passed, "swarm should trust the ticket delay on seed 55"
        else:
            assert passed, f"swarm {claim_id} seed {seed}: {reason}"


@pytest.mark.parametrize("claim_id", [case["claim_id"] for case in CASES_ADV])
def test_team_shapes_agree_on_status_and_proposal(tmp_path, claim_id):
    """Same claim, same seed: the three architectures reach the same decision."""
    decisions = {}
    for shape in TEAM_SHAPES:
        result, _ = _run(tmp_path, shape, claim_id, 55)
        decisions[shape] = (result.status, result.proposal_amount, sum(e["amount_vnd"] for e in result.refund_effects))
    assert len(set(decisions.values())) == 1, decisions


def test_unknown_claim_is_failed_without_exception(tmp_path):
    store = tmp_path / "unknown.sqlite"
    init_store(store, WORLD_ADV, ALL_CLAIMS_ADV).close()
    for shape in TEAM_SHAPES + ["swarm"]:
        result = SHAPES[shape]("C-DOES-NOT-EXIST", seed=11, store_path=str(store))
        assert result.status == "failed"
        assert result.proposal_amount == 0
        assert result.refund_effects == []
