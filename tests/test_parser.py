"""Tests for dashboard/parser.py"""
import sys
from pathlib import Path

# Add repo root to path so `dashboard` is importable
sys.path.insert(0, str(Path(__file__).parent.parent))

from dashboard.parser import (
    parse_md_table, parse_ranking_table, parse_scorecard, discover_rounds,
    blended_price_usd_per_1m, parse_run_record_usage,
)

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
    # September 2026 refresh: gpt5.6-sol-xhigh overtook the April winner gemma4:31b-cloud
    assert task["winner"] == "gpt5.6-sol-xhigh"
    assert task["difference_size"].lower() == "very small"
    # April rows are frozen
    assert task["scores"]["gpt5.4-xhigh"]["Correctness"] == 4.0
    assert task["scores"]["kimi-k2-thinking"]["Correctness"] == 1.0
    assert "gemma4:31b-cloud" in task["notes"]
    # refresh rows are appended, not substituted
    assert task["scores"]["gpt5.6-sol-xhigh"]["Correctness"] == 5.0
    assert task["scores"]["gpt5.6-luna-max"]["Economics/practicality"] == 3.0
    assert len(task["scores"]) == 9
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
    assert len(v2["models"]) == 10
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

    # gpt5.6-luna-max is an OpenAI budget-tier API model; the slate sets its tier explicitly
    luna_model = next(m for m in v2["models"] if m["model_id"] == "gpt5.6-luna-max")
    assert luna_model["cost_tier"] == 2
    assert luna_model["cost_label"] == "Paid API"

    # every model in both slates carries sourced list pricing for the cost chart
    for r in rounds:
        for model in r["models"]:
            assert model["blended_price_usd_per_1m"] is not None, model["model_id"]
            assert model["pricing"]["as_of"] == "2026-09-17"
            assert model["pricing"]["source"].startswith("https://")
    assert luna_model["blended_price_usd_per_1m"] == 0.45          # 0.75*0.20 + 0.25*1.20
    sol_model = next(m for m in v2["models"] if m["model_id"] == "gpt5.6-sol-xhigh")
    assert sol_model["blended_price_usd_per_1m"] == 11.25          # 0.75*5.00 + 0.25*30.00
    # deepseek-v4.1-flash (2026-09-18 addendum, three tasks only) is an OpenRouter API model
    ds_model = next(m for m in v2["models"] if m["model_id"] == "deepseek-v4.1-flash")
    assert ds_model["cost_tier"] == 2
    assert ds_model["blended_price_usd_per_1m"] == 0.2625         # 0.75*0.15 + 0.25*0.60
    assert "deepseek-v4.1-flash" not in v2["ranking"]              # no v2 cross-task average


def test_discover_rounds_explicit_cost_tier_overrides_provider_keyword(tmp_path):
    """A slate entry may carry cost_tier / cost_label; they take precedence over the provider keyword mapping."""
    import json
    models_dir = tmp_path / "benchmarks" / "vx" / "models"
    models_dir.mkdir(parents=True)
    slate = [
        {"model_id": "premium-by-keyword", "display_name": "P", "role": "r", "provider": "OpenAI API", "notes": ""},
        {"model_id": "budget-explicit", "display_name": "B", "role": "r", "provider": "OpenAI API", "notes": "",
         "cost_tier": 2, "cost_label": "Paid API"},
        {"model_id": "free-explicit-label-only", "display_name": "F", "role": "r", "provider": "Ollama cloud", "notes": "",
         "cost_label": "Free/Local"},
    ]
    (models_dir / "fixed_model_slate.json").write_text(json.dumps(slate), encoding="utf-8")

    rounds = discover_rounds(tmp_path)
    assert [r["round_id"] for r in rounds] == ["vx"]
    by_id = {m["model_id"]: m for m in rounds[0]["models"]}

    # keyword mapping still applies when nothing explicit is given
    assert by_id["premium-by-keyword"]["cost_tier"] == 3
    assert by_id["premium-by-keyword"]["cost_label"] == "Premium"
    # explicit values win over the keyword mapping
    assert by_id["budget-explicit"]["cost_tier"] == 2
    assert by_id["budget-explicit"]["cost_label"] == "Paid API"
    # a partial override keeps the keyword-derived value for the missing field
    assert by_id["free-explicit-label-only"]["cost_tier"] == 1
    assert by_id["free-explicit-label-only"]["cost_label"] == "Free/Local"


# ---------------------------------------------------------------------------
# list pricing (cost vs performance chart)
# ---------------------------------------------------------------------------

def test_blended_price_is_three_to_one_input_to_output():
    # 3 parts input : 1 part output per 1M tokens
    assert blended_price_usd_per_1m({"input_usd_per_1m": 0.20, "output_usd_per_1m": 1.20}) == 0.45
    assert blended_price_usd_per_1m({"input_usd_per_1m": 4.0, "output_usd_per_1m": 4.0}) == 4.0


def test_blended_price_missing_or_partial_pricing_is_none():
    assert blended_price_usd_per_1m(None) is None
    assert blended_price_usd_per_1m({}) is None
    assert blended_price_usd_per_1m({"input_usd_per_1m": 1.0}) is None
    assert blended_price_usd_per_1m({"input_usd_per_1m": None, "output_usd_per_1m": 2.0}) is None


def test_discover_rounds_adds_blended_price_from_slate_pricing(tmp_path):
    import json
    models_dir = tmp_path / "benchmarks" / "vx" / "models"
    models_dir.mkdir(parents=True)
    slate = [
        {"model_id": "priced", "display_name": "P", "role": "r", "provider": "OpenAI API", "notes": "",
         "pricing": {"input_usd_per_1m": 0.20, "output_usd_per_1m": 1.20,
                     "as_of": "2026-09-17", "source": "https://example.com"}},
        {"model_id": "unpriced", "display_name": "U", "role": "r", "provider": "Ollama cloud", "notes": ""},
    ]
    (models_dir / "fixed_model_slate.json").write_text(json.dumps(slate), encoding="utf-8")

    rounds = discover_rounds(tmp_path)
    by_id = {m["model_id"]: m for m in rounds[0]["models"]}
    assert by_id["priced"]["blended_price_usd_per_1m"] == 0.45
    assert by_id["priced"]["pricing"]["as_of"] == "2026-09-17"   # pricing block passes through untouched
    assert by_id["unpriced"]["blended_price_usd_per_1m"] is None
    assert "pricing" not in by_id["unpriced"]


# ---------------------------------------------------------------------------
# run-record usage (measured tokens / latency for the usage chart)
# ---------------------------------------------------------------------------

def test_parse_run_record_usage_real_september_record():
    rec = REPO_ROOT / "benchmarks/v2/runs/run_records/v2-deep-01__gpt5.6-sol-xhigh__run_record.md"
    usage = parse_run_record_usage(rec)
    assert usage["task_id"] == "v2-deep-01"
    assert usage["model_id"] == "gpt5.6-sol-xhigh"
    assert usage["tokens_k"] == 24
    assert "56 s" in usage["latency"]


def test_parse_run_record_usage_april_record_has_no_tokens():
    rec = REPO_ROOT / "benchmarks/v2/runs/run_records/v2-deep-01__gpt5.4-xhigh__run_record.md"
    usage = parse_run_record_usage(rec)
    assert usage["model_id"] == "gpt5.4-xhigh"
    assert usage["tokens_k"] is None
    assert usage["latency"] is None


def test_discover_rounds_collects_usage_only_where_tokens_were_recorded():
    rounds = discover_rounds(REPO_ROOT)
    v2 = next(r for r in rounds if r["round_id"] == "v2")
    usage = v2["usage"]
    assert usage["v2-anchor-07"]["gpt5.6-luna-max"]["tokens_k"] == 131
    assert usage["v2-anchor-07"]["gpt5.6-sol-xhigh"]["tokens_k"] == 85
    assert "gpt5.4-xhigh" not in usage["v2-anchor-07"]          # April records carry no token figure
    assert set(usage["v2-deep-01"]) == {"gpt5.6-sol-xhigh", "gpt5.6-luna-max"}
    # 2026-09-18 addendum records carry token figures too
    assert usage["v2-deep-02"]["deepseek-v4.1-flash"]["tokens_k"] == 35
    assert usage["v2-anchor-07"]["deepseek-v4.1-flash"]["tokens_k"] == 55
    v3 = next(r for r in rounds if r["round_id"] == "v3")
    assert v3["usage"]["v3-notebook-01"]["gpt5.6-sol-xhigh"]["tokens_k"] == 23
    assert v3["usage"]["v3-notebook-01"]["deepseek-v4.1-flash"]["tokens_k"] == 59
