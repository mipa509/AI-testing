# September 2026 Refresh: Scoring Session Prompt

Use this in a fresh Claude Code session started in `C:\Users\mikol\Python_script_test\04-Apps\AI-testing`. It is written to be followed as-is.

---

## Your task

Score two newly benchmarked models against the April 2026 results in this repo, then publish the results. The user wants to know how current models compare with the April 2026 slate on the same structural-engineering tasks.

New models:
- `gpt5.6-sol-xhigh`: API `gpt-5.6-sol`, reasoning effort xhigh; like-for-like successor to April's `gpt5.4-xhigh`.
- `gpt5.6-luna-max`: API `gpt-5.6-luna`, reasoning effort max; low-cost tier.

All 16 first-pass runs are already captured. Do not rerun models and do not edit raw outputs.

## Ground rules

1. **Git.** Follow the workspace `CLAUDE.md`. Work on the existing branch: `git checkout feat/sept-2026-model-refresh && git pull --ff-only`. Make one commit per step below, push after every commit, and finish with a PR via `gh pr create`. Do not merge it.
2. **Python.** `python` is usually not on PATH. Use `C:\Users\mikol\Python_script_test\.venv\Scripts\python.exe` (3.13.2, has pytest and jinja2).
3. **April rows are frozen.** Never change the April 2026 scores, notes, or winners for the seven original models. You only add rows and columns for the two new models, and a winner changes only if a new model beats the April winner.
4. **Blind technical scoring.** The six technical criteria per task are scored by judge subagents that never see model names, run records, scorecards, or result files. You (the orchestrator) will see model names while preparing packs; do not form or record scores yourself before the blind judgements come back.
5. **Checkpoint.** Stop after Step 3 (calibration) and show the user the calibration table. Do not write any scores into the repo until the user approves.

## Where things are

| What | Path |
|---|---|
| v2 task definitions (6 primary + anchor) | `benchmarks/v2/tasks/task_manifest.json`, `benchmarks/v2/tasks/*/prompt.md`, `context_combined.md`, `_evaluator_notes.md` |
| v3 task definition | `benchmarks/v3/tasks/notebook_01_pad_footing_sizing/` (`prompt.md`, `_evaluator_notes.md`, `reference_solution_review.md`) |
| Raw outputs | `benchmarks/v2/runs/raw_outputs/`, `benchmarks/v3/runs/raw_outputs/`; files named `<task_id>__<model_id>__raw.md` (`:` in model IDs becomes `-`) |
| Run records (latency, tokens, route, capture notes) | `benchmarks/v2/runs/run_records/`, `benchmarks/v3/runs/run_records/` |
| Judge templates | `benchmarks/v2/templates/judge_prompt_template.md`, `benchmarks/v3/templates/judge_prompt_template.md` |
| April scorecards (7 models each) | `benchmarks/v2/results/scorecards/*.md`, `benchmarks/v3/results/scorecards/v3-notebook-01__scorecard.md` |
| April summaries | `benchmarks/v2/results/v2_overall_ranking.md`, `v2_per_task_results.md`, `anchor_task6_comparison.md`; `benchmarks/v3/results/v3_overall_ranking.md`, `v3_per_task_results.md` |
| Model slates | `benchmarks/v2/models/fixed_model_slate.json`, `benchmarks/v3/models/fixed_model_slate.json` (new models already added) |
| Dashboard | `dashboard/parser.py`, `dashboard/build.py`, `tests/test_parser.py`, output `dashboard.html` |

Criteria:
- v2 (all 7 tasks, including the anchor): technical = `Correctness`, `Repo comprehension`, `Change safety`, `Engineering judgement`, `Maintainability`, `Clarity`; practicality = `Economics/practicality`.
- v3: technical = `Calculation correctness`, `Code quality/executability`, `Engineering judgement`, `Unit/assumption handling`, `Notebook traceability/clarity`, `Completeness of deliverable`; practicality = `Practical usability`.

Known capture facts, all recorded in the run records:
- Every new run used the Codex VS Code extension in an empty sandbox folder, one fresh chat per run. Inputs came from a neutral copy with no evaluator or reference files. April's `gpt5.4-xhigh` used the same Codex route.
- `v2-deep-01`: Sol received the three `.py` files as attachments, so its output has absolute file links. Luna and all other v2 runs received pasted `context_combined.md`. The code content is identical.
- `v3-notebook-01` Sol output lost its Markdown fences and table pipes in the copy. It is wrapped in a `text` block and must be judged on content, not formatting, as April did for `qwen-3.6plus`.
- `v2-anchor-07`: both new models used web lookups, as April's `gpt5.4-xhigh` did.
- Some run records contain a capture-time "First-Pass Output Summary" written without blinding. Do not pass run records to judges.

## Step 1: Build blind judge packs (no commit)

For each of the 8 tasks (`v2-deep-01` … `v2-medium-06`, `v2-anchor-07`, `v3-notebook-01`):

1. Choose 4 responses:
   - `gpt5.6-sol-xhigh`
   - `gpt5.6-luna-max`
   - `gpt5.4-xhigh`, the April high calibration anchor
   - a low calibration anchor: the April model with the lowest mean of the six technical scores on that task's scorecard. Exclude rows where all six technical scores are ≤ 2; break ties by table order.
2. From each raw output file, take only the text under `## Raw Model Output`. Strip every metadata line. For the Sol v3 response, add one neutral line above it: "Formatting was lost when this response was copied; judge content, not formatting."
3. Shuffle the four responses with a recorded random seed and label them `Response A`–`D`.
4. Write the pack into the session scratchpad, outside the repo: `packs/<task_id>.md`. Include:
   - the task prompt (for the anchor, only the text inside its `text` block)
   - `context_combined.md` (v2 primary tasks only)
   - `_evaluator_notes.md`, plus `reference_solution_review.md` for v3
   - the relevant judge template, amended to score **only the six technical criteria** (no economics/practicality)
   - the four labelled responses
5. Write the label-to-model mapping and seeds to `mapping/mapping.json` in a separate scratchpad folder. Judges must never be given this path.

## Step 2: Blind judging (no commit)

Dispatch one fresh subagent per task (8 total; they can run in parallel). Give each subagent only its pack path and these instructions:
- Read only that file. Do not open any other file on disk, and do not browse the web.
- Act as the strict evaluator described in the pack.
- Score each response 1–5 on the six technical criteria, as integers.
- Return a Markdown table (`Response | criterion columns | one-sentence note`), the top weaknesses per response, a ranking A–D, and practical significance.
- Do not guess which model wrote a response.

Save each judge's full reply to the scratchpad. After all 8 return, de-anonymise using the mapping.

For `v3-notebook-01`, also execute each new model's code cells in order with the venv Python (standard library only). For Sol, rebuild the cells from the fence-less text. Record whether the notebook runs end to end, the selected width, and the governing case. The run records contain a capture-time execution note; re-verify it rather than trusting it.

## Step 3: Calibration checkpoint (stop here)

For the two April anchor models on each task, compare blind scores with the frozen April scores on the six technical criteria:
- per task and per model: mean absolute difference (MAD) and signed mean difference
- overall MAD across all 16 anchor rows, and whether the blind ranking of the two anchors matches April's order

Show the user one table: task | high anchor MAD / signed diff | low anchor MAD / signed diff | anchor order preserved?
Then give the overall figures and a one-paragraph read: is this judge harsher or more lenient than April, and on which tasks?

Proposed gate: overall MAD ≤ 0.5 and no single task MAD > 1.0 means the blind scores for the new models are used as-is, subject to Step 4 review. Otherwise, propose how to handle the drift, for example re-anchoring a task by manual comparison against the April anchor responses and notes. **Wait for the user's decision before Step 4.**

## Step 4: Manual engineering review and practicality scores (commit when done)

1. Review the de-anonymised judgements for the two new models against the evaluator notes, the reference solution, and your execution results. Override a technical score only with a concrete, stated reason, recorded under `## Manual Override Notes`.
2. Score the practicality criterion for the new models unblinded, from the run records: route, latency, token counts, refusals, truncation, whether it waited for context, and cost tier. Apply the same principles April used; April's `gpt5.4-xhigh` on the same premium route is the reference point. Briefly state the reasoning per model.
3. Save `benchmarks/refresh_2026-09_calibration.md` with the calibration table, gate outcome, user decision, seeds, label mapping per task, and the de-anonymised judge replies (or faithful summaries) for all 32 responses.
4. Commit: `docs: add Sept 2026 refresh calibration record`.

## Step 5: Scorecards (commit)

In each of the 8 scorecards:
- Append rows for `gpt5.6-sol-xhigh` and `gpt5.6-luna-max` to the `## Scores` table, using the same column order and integer scores, with a one-sentence `Overall notes` cell. Do not modify existing rows.
- Under `## Judge Output Summary`, append a `September 2026 refresh` sub-block summarising the blind judgement for the new models.
- Under `## Manual Override Notes`, append a `September 2026 refresh` sub-block covering overrides, calibration outcome, and practicality reasoning.
- In `## Winner`, keep exactly one line matching `- Winner: \`<model_id>\`` because `dashboard/parser.py` reads the first match. Change it only if a new model's overall mean beats the April winner. Add refresh commentary on separate lines that do not contain the capitalised `Winner:` pattern.

Commit: `chore: score gpt5.6 sol and luna in v2 and v3 scorecards`.

## Step 6: Rankings and per-task results (commit)

- `v2_overall_ranking.md`: add two columns to `Cross-Task Average Scores`. The averages use the six primary tasks only, not the anchor, and 2-decimal means per criterion including `Overall average`. Re-rank the list and update `Recommended Use Cases` (for example, best value). Add one line noting that the September rows were scored blind with calibration against April anchors.
- `v2_per_task_results.md`: update the slate line and any changed winners.
- `anchor_task6_comparison.md`: add rows for both new models and update the anchor result block if warranted.
- `v3_overall_ranking.md` and `v3_per_task_results.md`: the same updates for v3.
- Check every recomputed average by script, not by hand.

Commit: `chore: update v2 and v3 rankings for Sept 2026 refresh`.

## Step 7: Dashboard cost tier (TDD, commit)

`dashboard/parser.py` labels any provider containing "openai" as `Premium`, which misrepresents Luna.
1. Write a failing test in `tests/test_parser.py`: an explicit `cost_tier` / `cost_label` in a slate entry overrides the provider keyword mapping.
2. Implement the override in `discover_rounds`.
3. In both slate JSON files, set `"cost_tier": 2, "cost_label": "Paid API"` on `gpt5.6-luna-max`.
4. Run the full test suite, then `python dashboard/build.py` to regenerate `dashboard.html`. Check the new models appear in the rendered dashboard data.

Commit: `feat: allow explicit cost tier in model slate` (test and code), then `chore: rebuild dashboard for Sept 2026 refresh`.

## Step 8: Then-vs-now summary and docs (commit)

1. Create `benchmarks/refresh_2026-09_summary.md` containing:
   - the headline answer: how Sol and Luna compare with April's models, especially `gpt5.4-xhigh`, on v2 primary, the anchor, and v3
   - per-task and overall score tables including April models
   - a practicality table with latency, tokens and cost from the run records; mark cost figures as list-price estimates
   - the calibration result and caveats: different judge from April, one run per model per task, Codex route with web lookup, capture artefacts
2. Update the root `README.md`: the rounds table, the v2/v3 model lists, headline rankings, and a link to the summary. Also update the slate lists in `benchmarks/v2/README.md`, `benchmarks/v2/RUNBOOK.md`, `benchmarks/v3/README.md` and `benchmarks/v3/RUNBOOK.md`. Leave the April full reports (`structural_engineering_benchmark_report*.md`) unchanged.

Commit: `docs: add Sept 2026 refresh summary and update READMEs`.

## Step 9: PR

Run the tests one final time, then `gh pr create` against `main`, with a body summarising results, the calibration outcome, and caveats. Report the PR URL to the user with a short then-vs-now headline. Do not merge.
