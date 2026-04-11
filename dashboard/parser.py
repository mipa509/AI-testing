import json
import re
from pathlib import Path


def parse_md_table(md_text: str, start_marker: str = None):
    """
    Parse the first pipe-delimited Markdown table found in md_text,
    optionally starting the search after start_marker.

    Returns (header_list, rows_list) where each row is a list of strings.
    Returns (None, []) if no table is found.
    Skips separator rows (|---|).
    Strips backtick wrappers from cell values.
    """
    lines = md_text.splitlines()

    if start_marker:
        start = next(
            (i for i, l in enumerate(lines) if start_marker in l), None
        )
        if start is None:
            return None, []
        lines = lines[start:]

    table_lines = []
    in_table = False
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|"):
            if in_table and table_lines:
                break
            continue
        # Skip separator rows: |---|  |---:|  |:---:|
        if re.match(r"^\|[\s\-:|]+\|", stripped):
            continue
        in_table = True
        table_lines.append(stripped)

    if not table_lines:
        return None, []

    def parse_row(line):
        cells = [c.strip() for c in line.strip("|").split("|")]
        # Strip backtick wrappers: `value` -> value
        return [re.sub(r"^`(.+)`$", r"\1", c) for c in cells]

    header = parse_row(table_lines[0])
    rows = [parse_row(ln) for ln in table_lines[1:]]
    return header, rows


def parse_ranking_table(md_path: Path):
    """
    Parse a *_overall_ranking.md file.

    The table has criterion names in the first column and model IDs as
    subsequent column headers (e.g. | Criterion | gemma4:31b-cloud | ... |).

    Returns:
        ranking  : dict[model_id, dict[criterion, float]]
        criteria : list[str]  — in order, including 'Overall average'
        model_ids: list[str]
    """
    text = Path(md_path).read_text(encoding="utf-8")
    header, rows = parse_md_table(text, start_marker="Cross-Task Average Scores")
    if not header:
        return {}, [], []

    model_ids = header[1:]  # first col is "Criterion"
    criteria = []
    ranking = {m: {} for m in model_ids}

    for row in rows:
        if len(row) < 2:
            continue
        criterion = row[0]
        if not criterion:
            continue
        criteria.append(criterion)
        for i, model_id in enumerate(model_ids):
            try:
                ranking[model_id][criterion] = float(row[i + 1])
            except (ValueError, IndexError):
                ranking[model_id][criterion] = None

    return ranking, criteria, model_ids


def parse_scorecard(md_path: Path):
    """
    Parse a scorecard MD file.

    Score table format:
      | Model | Criterion1 | ... | CriterionN | Overall notes |
      |---|---:|...|---|
      | `model-id` | score | ... | score | commentary text |

    Returns a dict with keys:
      task_id, task_title, criteria, scores, notes, winner,
      difference_size, commentary
    """
    text = Path(md_path).read_text(encoding="utf-8")

    # --- Metadata ---
    task_id = re.search(r"`task_id`:\s*`(.+?)`", text)
    task_title = re.search(r"`task_title`:\s*`(.+?)`", text)
    task_id = task_id.group(1) if task_id else md_path.stem
    task_title = task_title.group(1) if task_title else ""

    # --- Scores table ---
    header, rows = parse_md_table(text, start_marker="## Scores")
    # header = ["Model", "Criterion1", ..., "CriterionN", "Overall notes"]
    criteria = header[1:-1] if header and len(header) > 2 else []

    scores: dict = {}
    notes: dict = {}
    for row in rows:
        if not row:
            continue
        model_id = row[0]
        if not model_id:
            continue
        scores[model_id] = {}
        for i, criterion in enumerate(criteria):
            try:
                scores[model_id][criterion] = float(row[i + 1])
            except (ValueError, IndexError):
                scores[model_id][criterion] = None
        # Last cell = Overall notes
        notes[model_id] = row[len(criteria) + 1] if len(row) > len(criteria) + 1 else ""

    # --- Winner block ---
    winner_m = re.search(r"Winner:\s*`(.+?)`", text)
    diff_m = re.search(r"Difference size:\s*`(.+?)`", text)
    winner = winner_m.group(1) if winner_m else ""
    difference_size = diff_m.group(1) if diff_m else ""

    # --- Commentary (Judge Output Summary section) ---
    commentary_m = re.search(
        r"##\s+Judge Output Summary\s*\n+(.*?)(?=\n##|\Z)", text, re.DOTALL
    )
    commentary = commentary_m.group(1).strip() if commentary_m else ""

    return {
        "task_id": task_id,
        "task_title": task_title,
        "criteria": criteria,
        "scores": scores,
        "notes": notes,
        "winner": winner,
        "difference_size": difference_size,
        "commentary": commentary,
    }


def discover_rounds(repo_root: Path):
    """
    Walk benchmarks/ for structured rounds (those with models/fixed_model_slate.json).
    Returns a list of round dicts sorted by round_id.

    Each round dict:
      round_id    : str          e.g. "v2"
      label       : str          e.g. "V2"
      models      : list[dict]   from fixed_model_slate.json, augmented with
                                 cost_tier (1/2/3) and cost_label
      task_manifest: list[dict]  from task_manifest.json (empty list if absent)
      criteria    : list[str]    from overall ranking table
      ranking     : dict[model_id, dict[criterion, float]]
      tasks       : list[dict]   from scorecard files
    """
    repo_root = Path(repo_root)
    benchmarks_dir = repo_root / "benchmarks"
    rounds = []

    for item in sorted(benchmarks_dir.iterdir()):
        if not item.is_dir():
            continue
        slate_path = item / "models" / "fixed_model_slate.json"
        if not slate_path.exists():
            continue  # unstructured round (v1), skip

        with open(slate_path, encoding="utf-8") as f:
            models = json.load(f)

        # Augment models with cost tier
        for model in models:
            provider = model.get("provider", "").lower()
            if "openai" in provider or "subscription" in provider:
                model["cost_tier"] = 3
                model["cost_label"] = "Premium"
            elif "api" in provider and "ollama" not in provider:
                model["cost_tier"] = 2
                model["cost_label"] = "Paid API"
            else:
                model["cost_tier"] = 1
                model["cost_label"] = "Free/Cloud"

        # Task manifest (optional)
        manifest_path = item / "tasks" / "task_manifest.json"
        task_manifest = []
        if manifest_path.exists():
            with open(manifest_path, encoding="utf-8") as f:
                task_manifest = json.load(f)
        manifest_by_id = {t["task_id"]: t for t in task_manifest}

        # Overall ranking
        results_dir = item / "results"
        ranking, criteria, model_ids = {}, [], []
        if results_dir.exists():
            ranking_files = sorted(results_dir.glob("*_overall_ranking.md"))
            if ranking_files:
                ranking, criteria, model_ids = parse_ranking_table(ranking_files[0])

        # Scorecards
        tasks = []
        scorecards_dir = results_dir / "scorecards" if results_dir.exists() else None
        if scorecards_dir and scorecards_dir.exists():
            for sc_file in sorted(scorecards_dir.glob("*.md")):
                task_data = parse_scorecard(sc_file)
                # Merge group/depth from manifest
                if task_data["task_id"] in manifest_by_id:
                    m = manifest_by_id[task_data["task_id"]]
                    task_data["group"] = m.get("group", "")
                    task_data["depth"] = m.get("depth", "")
                else:
                    task_data.setdefault("group", "")
                    task_data.setdefault("depth", "")
                tasks.append(task_data)

        rounds.append({
            "round_id": item.name,
            "label": item.name.upper(),
            "models": models,
            "task_manifest": task_manifest,
            "criteria": criteria,
            "ranking": ranking,
            "tasks": tasks,
        })

    return rounds
