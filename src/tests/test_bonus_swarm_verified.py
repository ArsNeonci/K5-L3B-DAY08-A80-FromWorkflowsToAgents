"""B3 regression, safety, and single-round verification tests."""
import json
import time
from pathlib import Path

import pytest

from bonus import swarm_verified as variant
from lab8.app import prepare_store
from lab8.db import connect, init_store
from lab8.durability import InjectedCrash, committed_audit_count, get_refund
from lab8.metrics import artifact_blob, trial_pass
from lab8.schemas import Budget
from lab8.shapes.swarm_reference import run_claim as swarm
from lab8.tools import compute_compensation, lookup_order

ROOT = Path(__file__).resolve().parents[1]
CASES = [json.loads(s) for s in (ROOT/'bonus/cases.jsonl').read_text(encoding='utf-8').splitlines()]
WORLD = json.loads((ROOT/'bonus/world.json').read_text(encoding='utf-8'))


@pytest.mark.parametrize('seed', [11, 22, 33, 44, 55])
@pytest.mark.parametrize('claim', CASES, ids=lambda c: c['claim_id'])
def test_hand_labelled_adversarial_cases(tmp_path, claim, seed):
    db = tmp_path/'case.sqlite'
    init_store(db, WORLD, CASES).close()
    started = time.time()
    result = variant.run_claim(claim['claim_id'], seed=seed, store_path=str(db))
    conn = connect(db)
    try:
        ok, reason = trial_pass(result.as_dict(), claim['expected'], conn, started_at=started)
        assert ok, reason
    finally:
        conn.close()


@pytest.mark.parametrize('field,value', [('delay_days', 9), ('status', 'in_transit'), ('damage_verified', True)])
def test_verifier_checks_all_three_required_fields(public_db, field, value):
    conn = connect(public_db)
    try:
        trusted = lookup_order(conn, 'O-202', 'P-100')['order']
        candidate = dict(trusted, **{field: value})
        quote = compute_compensation(conn, candidate)
        budget = Budget()
        corrected, changed = variant.verify_quote(conn, budget, candidate, quote, trusted)
        assert changed == [field]
        assert corrected == compute_compensation(conn, trusted)
        assert budget.tool_calls == 1
        again, changed_again = variant.verify_quote(conn, budget, trusted, corrected, trusted)
        assert again == corrected and changed_again == []
        assert budget.tool_calls == 1
    finally:
        conn.close()


def test_overstated_ticket_is_fixed_before_any_refund(public_db):
    result = variant.run_claim('C-002', seed=55, store_path=str(public_db))
    body = json.loads(Path(result.trace_path).read_text(encoding='utf-8'))
    overrides = [e for e in body['events'] if e['kind'] == 'verifier_override']
    assert len(overrides) == 1 and overrides[0]['payload']['repair_rounds'] == 1
    assert (result.status, result.proposal_amount, result.refund_effects) == ('denied', 0, [])


def test_no_mismatch_keeps_swarm_calls_and_only_adds_read_cost(tmp_path):
    results = []
    for name, run in [('baseline', swarm), ('verified', variant.run_claim)]:
        db = tmp_path/(name+'.sqlite')
        prepare_store(db)
        results.append(run('C-001', seed=11, store_path=str(db)))
    a, b = results
    assert a.status == b.status == 'resolved'
    assert a.proposal_amount == b.proposal_amount == 35000
    assert b.model_calls == a.model_calls
    assert b.tool_calls == a.tool_calls + 1
    assert b.cost_estimate > a.cost_estimate


@pytest.mark.parametrize('point', ['before_effect', 'after_effect_before_checkpoint', 'after_checkpoint'])
def test_crash_resume_and_repeated_retry_are_safe(public_db, point):
    with pytest.raises(InjectedCrash):
        variant.run_claim('C-001', seed=55, store_path=str(public_db), crash_at=point)
    for _ in range(2):
        result = variant.run_claim('C-001', seed=55, store_path=str(public_db))
        assert result.status == 'resolved'
    conn = connect(public_db)
    try:
        assert get_refund(conn, 'C-001')['amount_vnd'] == 35000
        assert committed_audit_count(conn, 'C-001') == 1
        assert conn.execute("SELECT COUNT(*) FROM refund_ledger WHERE claim_id='C-001'").fetchone()[0] == 1
    finally:
        conn.close()


def test_ticket_canary_never_enters_output_or_trace(public_db):
    conn = connect(public_db)
    try:
        conn.execute("UPDATE claims SET ticket=ticket || ' CANARY_SECRET_B3_TICKET_TEST' WHERE claim_id='C-002'")
        conn.commit()
    finally:
        conn.close()
    result = variant.run_claim('C-002', seed=55, store_path=str(public_db))
    assert 'CANARY_SECRET_B3_TICKET_TEST' not in artifact_blob(result.as_dict())


@pytest.mark.parametrize('cid,status', [('C-004', 'needs_info'), ('C-005', 'escalated'), ('NO-CLAIM', 'failed')])
def test_early_return_trace_contract(public_db, cid, status):
    result = variant.run_claim(cid, seed=11, store_path=str(public_db))
    from lab8.metrics import check_trace
    assert result.status == status
    assert check_trace(result.as_dict())[0]
    assert result.shape == 'swarm_verified'
