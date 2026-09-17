"""Tests for dashboard/parser.py"""
import sys
from pathlib import Path

# Add repo root to path so `dashboard` is importable
sys.path.insert(0, str(Path(__file__).parent.parent))

from dashboard.parser import parse_md_table, parse_ranking_table, parse_scorecard, discover_rounds

REPO_ROOT = Path(__file__).parent.parent


# ---------------------------------------------------------------------------
# parse_md_table tests
# ---------------------------------------------------------------------------

def test_parse_md_table_basic():
    md = """\
## Scores

| Model | Correctness | Clarity |
|---|---:|---:|
| `gemma4:31b-cloud` | 4 | 5 |
| `gpt5.4-xhigh` | 5 | 5 |
"""
    header, rows = parse_md_table(md, start_marker="## Scores")
    assert header == ["Model", "Correctness", "Clarity"]
    assert rows[0] == ["gemma4:31b-cloud", "4", "5"]
    assert rows[1] == ["gpt5.4-xhigh", "5", "5"]


def test_parse_md_table_no_marker():
    md = """\
| Criterion | m1 | m2 |
|---|---:|---:|
| Correctness | 4.00 | 3.83 |
"""
    header, rows = parse_md_table(md)
    assert header == ["Criterion", "m1", "m2"]
    assert rows[0] == ["Correctness", "4.00", "3.83"]


def test_parse_md_table_missing_section():
    header, rows = parse_md_table("no table here", start_marker="## Missing")
    assert header is None
    assert rows == []


# ---------------------------------------------------------------------------
# parse_ranking_table tests
# ---------------------------------------------------------------------------

def test_parse_ranking_table_real():
    ranking_path = REPO_ROOT / "benchmarks/v2/results/v2_overall_ranking.md"
    ranking, criteria, model_ids = parse_ranking_table(ranking_path)

    assert "gemma4:31b-cloud" in model_ids
    assert "gpt5.4-xhigh" in model_ids
    assert "Correctness" in criteria
    assert "Overall average" in criteria
    assert ranking["gpt5.4-xhigh"]["Overall average"] == 4.14
    assert ranking["gemma4:31b-cloud"]["Correctness"] == 4.00


def test_parse_ranking_table_v3():
    ranking_path = REPO_ROOT / "benchmarks/v3/results/v3_overall_ranking.md"
    ranking, criteria, model_ids = parse_ranking_table(ranking_path)

    assert "gpt5.4-xhigh" in model_ids
    assert "Calculation correctness" in criteria
    assert ranking["gpt5.4-xhigh"]["Overall average"] == 4.86


# ---------------------------------------------------------------------------
# parse_scorecard tests
# ---------------------------------------------------------------------------

def test_parse_scorecard_v2_deep01():
    sc_path = REPO_ROOT / "benchmarks/v2/results/scorecards/v2-deep-01__scorecard.md"
    task = parse_scorecard(sc_path)

    assert task["task_id"] == "v2-deep-01"
    assert task["task_title"] == "Multi-file bug hunt in a member check pipeline"
    assert task["winner"] == "gemma4:31b-cloud"
    assert task["difference_size"].lower() == "small"
    assert task["scores"]["gpt5.4-xhigh"]["Correctness"] == 4.0
    assert task["scores"]["kimi-k2-thinking"]["Correctness"] == 1.0
    assert "gemma4:31b-cloud" in task["notes"]
    assert len(task["commentary"]) > 50


def test_parse_scorecard_v3():
    sc_path = REPO_ROOT / "benchmarks/v3/results/scorecards/v3-notebook-01__scorecard.md"
    task = parse_scorecard(sc_path)

    assert task["task_id"] == "v3-notebook-01"
    assert task["winner"] == "gpt5.4-xhigh"
    assert task["scores"]["gpt5.4-xhigh"]["Calculation correctness"] == 5.0
    assert task["scores"]["gemma4:31b-cloud"]["Engineering judgement"] == 3.0


# ---------------------------------------------------------------------------
# discover_rounds tests
# ---------------------------------------------------------------------------

def test_discover_rounds():
    rounds = discover_rounds(REPO_ROOT)

    round_ids = [r["round_id"] for r in rounds]
    assert "v2" in round_ids
    assert "v3" in round_ids
    # v1 has no fixed_model_slate.json — must be excluded
    assert "v1" not in round_ids

    v2 = next(r for r in rounds if r["round_id"] == "v2")
    assert len(v2["models"]) == 9
    assert v2["models"][0]["model_id"] == "gemma4:31b-cloud"
    v2_model_ids = {m["model_id"] for m in v2["models"]}
    assert {"gpt5.6-sol-xhigh", "gpt5.6-luna-max"} <= v2_model_ids
    assert len(v2["tasks"]) >= 6
    assert len(v2["criteria"]) >= 7
    assert v2["ranking"]["gpt5.4-xhigh"]["Overall average"] == 4.14

    # Cost tier mapping
    gpt_model = next(m for m in v2["models"] if m["model_id"] == "gpt5.4-xhigh")
    assert gpt_model["cost_tier"] == 3
    assert gpt_model["cost_label"] == "Premium"

    gemma_model = next(m for m in v2["models"] if m["model_id"] == "gemma4:31b-cloud")
    assert gemma_model["cost_tier"] == 1

    qwen_model = next(m for m in v2["models"] if m["model_id"] == "qwen-3.6plus")
    assert qwen_model["cost_tier"] == 2
