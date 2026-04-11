"""
Generate dashboard.html from benchmark data.

Usage:
    python dashboard/build.py

Output: dashboard.html at the repo root.
"""
import json
import sys
from pathlib import Path

import jinja2

sys.path.insert(0, str(Path(__file__).parent.parent))
from dashboard.parser import discover_rounds


def build(repo_root: Path = None):
    if repo_root is None:
        repo_root = Path(__file__).parent.parent

    print(f"Discovering benchmark rounds in {repo_root / 'benchmarks'} ...")
    rounds = discover_rounds(repo_root)
    print(f"  Found {len(rounds)} structured round(s): {[r['round_id'] for r in rounds]}")

    # Build template context
    context = _build_context(rounds)

    # Load Chart.js source for inline embedding
    chartjs_path = Path(__file__).parent / "chartjs.min.js"
    chartjs_source = chartjs_path.read_text(encoding="utf-8") if chartjs_path.exists() else \
        'console.warn("chartjs.min.js not found — charts will not render");'

    # Render template
    template_dir = Path(__file__).parent
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(template_dir)),
        autoescape=False,
    )
    template = env.get_template("template.html")

    output_path = repo_root / "dashboard.html"
    output_path.write_text(
        template.render(**context, chartjs_source=chartjs_source),
        encoding="utf-8"
    )
    print(f"Dashboard written to {output_path}")


def _build_context(rounds):
    """
    Build the template context dict from parsed rounds.

    Returns a dict with:
      data_json  : JSON string embedded in the <script> tag
      kpis       : dict with summary stats for the KPI row
      rounds     : the raw rounds list (for Jinja2 iteration)
    """
    # Compute KPIs
    total_models = max(
        (len(set(m["model_id"] for m in r["models"])) for r in rounds),
        default=0,
    )
    total_tasks = sum(len(r["tasks"]) for r in rounds)
    total_rounds = len(rounds)

    # Overall leader: model with highest average across all rounds they appear in
    model_scores: dict = {}
    model_counts: dict = {}
    for r in rounds:
        for model_id, scores in r["ranking"].items():
            avg = scores.get("Overall average")
            if avg is not None:
                model_scores[model_id] = model_scores.get(model_id, 0) + avg
                model_counts[model_id] = model_counts.get(model_id, 0) + 1
    overall_leader = ""
    if model_scores:
        best_id = max(model_scores, key=lambda m: model_scores[m] / model_counts[m])
        # Get display name
        for r in rounds:
            for m in r["models"]:
                if m["model_id"] == best_id:
                    overall_leader = m["display_name"]
                    break
            if overall_leader:
                break

    kpis = {
        "total_models": total_models,
        "total_tasks": total_tasks,
        "total_rounds": total_rounds,
        "overall_leader": overall_leader,
    }

    # Serialize rounds for JSON embedding
    data_json = json.dumps({"rounds": rounds}, ensure_ascii=False, default=str)

    return {
        "data_json": data_json,
        "kpis": kpis,
        "rounds": rounds,
    }


if __name__ == "__main__":
    build()
