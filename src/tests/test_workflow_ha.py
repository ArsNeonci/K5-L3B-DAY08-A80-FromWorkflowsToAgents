"""Test của Hà: workflow từ chối đúng khi đơn đã được hoàn đủ trước đó (T13)."""

from lab8.db import connect, init_store
from lab8.shapes.workflow import run_claim
from tests.conftest import CLAIMS, WORLD


def test_workflow_denies_order_already_refunded(tmp_path):
    # C-013 (T13): đơn O-505 đã được hoàn 35.000 ship từ claim trước.
    # Ticket nói "chưa nhận được tiền" -> vẫn phải denied, proposal 35.000, không ghi ledger, có audit policy_denied.
    store = tmp_path / "t13.sqlite"
    init_store(store, WORLD, CLAIMS).close()
    result = run_claim("C-013", seed=11, store_path=str(store))
    conn = connect(store)
    try:
        rows = conn.execute("SELECT COUNT(*) AS n FROM refund_ledger WHERE claim_id = 'C-013'").fetchone()["n"]
        denied = conn.execute(
            "SELECT COUNT(*) AS n FROM audit_events WHERE claim_id = 'C-013' AND event_type = 'policy_denied'"
        ).fetchone()["n"]
    finally:
        conn.close()
    assert result.status == "denied"
    assert result.proposal_amount == 35000
    assert rows == 0
    assert denied == 1
