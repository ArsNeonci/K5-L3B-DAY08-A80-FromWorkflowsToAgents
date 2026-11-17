"""Member 5: the hand-in documents agree with the generated evidence.

Numbers in the ADR must come from src/reports/*.json, not be typed from memory.
Run the strict pre-submit check (no TODO left) with:

    LAB8_PRESUBMIT=1 python -m pytest -q tests/test_submission_docs.py      (bash)
    $env:LAB8_PRESUBMIT=1; python -m pytest -q tests/test_submission_docs.py (PowerShell)
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

import pytest

from lab8.check_submission import ALL_SHAPES, PUBLIC_SEEDS, _contribution_rows, _field

SRC = Path(__file__).resolve().parents[1]
REPO = SRC.parent
ADR = (REPO / "report" / "team" / "decision_adr.md").read_text(encoding="utf-8")
CARD = (REPO / "report" / "team" / "research_card.md").read_text(encoding="utf-8")
TEAM = (REPO / "TEAM.md").read_text(encoding="utf-8")
ADR_LABELS = (
    "Shape chọn",
    "Commit hash",
    "Run id dẫn chứng",
    "Pass rate / pass^5 / seed min-max / variance",
    "Cost per success (mô phỏng, VND)",
    "Crash safety",
    "Secret leak / approval bypass",
)


def _report(name: str) -> dict:
    return json.loads((SRC / "reports" / name).read_text(encoding="utf-8"))


def _chosen() -> str:
    return (_field(ADR, "Shape chọn") or "").strip("`").lower()


def test_adr_labels_are_filled_and_shape_is_valid():
    assert _chosen() in ALL_SHAPES
    for label in ADR_LABELS:
        assert _field(ADR, label), f"ADR line '- {label}:' is empty"


def test_benchmark_report_has_four_shapes_public_seeds_and_enough_claims():
    bench = _report("benchmark.json")
    assert set(ALL_SHAPES) <= set(bench["by_shape"])
    assert bench["controlled_variables"]["seeds"] == PUBLIC_SEEDS
    assert len(bench["controlled_variables"]["claim_ids"]) >= 10


def test_adr_numbers_match_the_benchmark_file():
    stats = _report("benchmark.json")["by_shape"][_chosen()]
    rates = re.findall(r"\d+\.\d{3}", _field(ADR, "Pass rate / pass^5 / seed min-max / variance"))
    assert rates[0] == f"{stats['pass_rate']:.3f}"
    assert rates[1] == f"{stats['pass_5']:.3f}"
    cost = re.search(r"\d+\.\d{2}", _field(ADR, "Cost per success (mô phỏng, VND)")).group(0)
    assert cost == f"{stats['cost_per_success_vnd']:.2f}"


def test_adr_run_ids_exist_in_the_benchmark_file():
    run_ids = {trial["run_id"] for trial in _report("benchmark.json")["trials"]}
    cited = re.findall(r"R-[a-z_0-9]+-C-\d{3}-s\d+", _field(ADR, "Run id dẫn chứng"))
    assert cited
    assert set(cited) <= run_ids


def test_adr_crash_line_matches_crash_report():
    crash = _report("crash.json")["crash_safety"]
    assert crash == "20/20"
    assert crash in _field(ADR, "Crash safety")


def test_research_card_rows_are_filled():
    filled = {}
    for line in CARD.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) == 3 and cells[0] in ("CÂU", "SOURCE", "CLAIM", "BOUNDARY", "HYPOTHESIS", "METHOD", "FAILURE / METRIC"):
            filled[cells[0]] = cells[2]
    assert len(filled) == 7
    assert all(filled.values()), [k for k, v in filled.items() if not v]


def test_contribution_table_names_a_test_file_that_exists_for_every_member():
    rows = [row for row in _contribution_rows(TEAM) if row.strip("| ").replace("|", "").strip()]
    assert len(rows) >= 2
    for row in rows:
        tests = re.findall(r"src/tests/[\w/]+\.py", row)
        assert tests, f"no test file in row: {row}"
        for test in tests:
            assert (REPO / test).is_file(), test


@pytest.mark.skipif(os.environ.get("LAB8_PRESUBMIT") != "1", reason="strict pre-submit check: set LAB8_PRESUBMIT=1")
def test_no_todo_left_before_submitting():
    for name, text in {"decision_adr.md": ADR, "TEAM.md": TEAM, "research_card.md": CARD}.items():
        assert "TODO" not in text, f"{name} still has TODO"
    commit = _field(ADR, "Commit hash") or ""
    assert re.fullmatch(r"`?[0-9a-f]{7,40}`?", commit.strip()), f"commit hash looks wrong: {commit!r}"
