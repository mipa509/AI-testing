# Structural Engineering AI Model Benchmark

This repository compares coding models on structural-engineering-focused tasks across three benchmark rounds:
- `v1`: short prompt engineering coding and code-review tasks
- `v2`: larger-context repo-reading and engineering-review tasks
- `v3`: notebook-style structural engineering code-generation tasks

Artifacts include benchmark packs, written reports, per-task result summaries, presentation exports, and a generated dashboard.

## Benchmark Rounds At A Glance

| Round | Focus | Scope | Current leader | Main files |
|---|---|---|---|---|
| `v1` | Short coding and review prompts | `6` tasks, `3` models | `gemma4:31b-cloud` (`3.93`) | `benchmarks/v1/`, `structural_engineering_benchmark_report.md` |
| `v2` | Larger-context repo reading and change design | `6` primary tasks + `1` historical anchor, `7` models (April 2026) + `2` (September 2026 refresh) + `1` partial (2026-09-18 addendum, Task 2 and anchor only) | `gpt5.6-luna-max` (`4.48`), `gpt5.6-sol-xhigh` (`4.45`); April leader `gpt5.4-xhigh` (`4.14`) | `benchmarks/v2/`, `structural_engineering_benchmark_report_v2.md`, `benchmarks/refresh_2026-09_summary.md` |
| `v3` | Deterministic notebook-style code generation | `1` notebook task, `7` models (April 2026) + `2` (September 2026 refresh) + `1` (2026-09-18 addendum) | `gpt5.4-xhigh` (`4.86`) | `benchmarks/v3/`, `benchmarks/v3/results/`, `benchmarks/refresh_2026-09_summary.md` |

September 2026 refresh: `gpt5.6-sol-xhigh` (successor to `gpt5.4-xhigh`) and `gpt5.6-luna-max` (budget API tier) were run on the unchanged v2 and v3 tasks and scored blind with calibration against the April results. The then-vs-now comparison is in `benchmarks/refresh_2026-09_summary.md`; the calibration procedure and judge replies are in `benchmarks/refresh_2026-09_calibration.md`. The April full reports are unchanged. A 2026-09-18 addendum adds `deepseek-v4.1-flash` on three tasks (v2 Task 2, the anchor and the v3 notebook), scored the same way; see `benchmarks/addendum_2026-09-18_deepseek-v4.1-flash.md` and the addendum section of the summary.

## Start Here

If you are opening this repo for the first time, use this order:

1. `structural_engineering_benchmark_report_v2.md`
2. `benchmarks/v3/README.md`
3. `benchmarks/v3/v3_benchmark_pack.md`
4. `benchmarks/v3/results/v3_overall_ranking.md`
5. `benchmarks/v3/results/v3_per_task_results.md`
6. `benchmark_presentation_v2_report.html`
7. `benchmarks/v2/README.md`
8. `benchmarks/v2/v2_benchmark_pack.md`
9. `benchmarks/v2/results/v2_overall_ranking.md`
10. `benchmarks/v2/results/v2_per_task_results.md`
11. `benchmarks/v1/README.md`
12. `benchmarks/v1/structural_engineering_model_benchmark.md`
13. `structural_engineering_benchmark_report.md`
14. `dashboard.html`

The latest full written report in the repository is `structural_engineering_benchmark_report_v2.md`. This reading order starts with that report, then moves to the newest benchmark round (`v3`), then the underlying `v2` benchmark materials, then the original `v1` pack.

## Current Headline Results

### V1 - Original short-task benchmark

Models benchmarked:
- `Qwen3.5 27B`
- `Qwen3-Coder-Next`
- `gemma4:31b-cloud`

Scope:
- `6` benchmark tasks
- engineering coding and code-review style prompts
- scoring on correctness, robustness, readability, maintainability, engineering suitability, and clarity

Headline v1 ranking:
1. `gemma4:31b-cloud` - `3.93`
2. `Qwen3.5 27B` - `3.86`
3. `Qwen3-Coder-Next` - `3.18`

Task winners:

| Task | Winner | Difference size |
|---|---|---|
| Task 1 - Results cleanup | `Qwen3.5 27B` | Moderate |
| Task 2 - Slab check | `Qwen3.5 27B` | Large |
| Task 3 - Geometry assignment | `gemma4:31b-cloud` | Large |
| Task 4 - Rules engine | `Qwen3-Coder-Next` | Minor to Moderate |
| Task 5 - Summary and plotting | `gemma4:31b-cloud` | Minor |
| Task 6 - EC3 trap test | `gemma4:31b-cloud` | Moderate |

### V2 - Larger-context cloud benchmark

Current scored model set:
- `gpt5.4-xhigh`
- `gemma4:31b-cloud`
- `glm-5.1:cloud`
- `qwen-3.6plus`
- `minimax-m2.7-cloud`
- `kimi-k2-thinking`
- `deepseek-v3.2`
- `gpt5.6-sol-xhigh` (September 2026 refresh)
- `gpt5.6-luna-max` (September 2026 refresh)
- `deepseek-v4.1-flash` (2026-09-18 addendum; Task 2 and anchor only, no cross-task average)

Scope:
- `6` new v2 tasks
- `4` deep synthetic repo-context tasks
- `2` medium synthetic tasks
- `1` historical anchor task copied unchanged from v1 Task 6
- hybrid scoring using structured judge prompts plus manual engineering review

The unchanged EC3 trap task is reported separately as an anchor comparison and is not part of the default v2 composite score.

Headline v2 ranking (September 2026 refresh rows scored blind with calibration against April anchors; April rows unchanged):
1. `gpt5.6-luna-max` - `4.48`
2. `gpt5.6-sol-xhigh` - `4.45`
3. `gpt5.4-xhigh` - `4.14`
4. `gemma4:31b-cloud` - `4.10`
5. `glm-5.1:cloud` - `3.88`
6. `qwen-3.6plus` - `3.74`
7. `minimax-m2.7-cloud` - `3.72`
8. `kimi-k2-thinking` - `3.67`
9. `deepseek-v3.2` - `2.65`

Current v2 primary task winners:

| Task | Winner | Difference size | April 2026 winner |
|---|---|---|---|
| Task 1 - Multi-file bug hunt | `gpt5.6-sol-xhigh` | Very small (tie with `gpt5.6-luna-max`) | `gemma4:31b-cloud` |
| Task 2 - Repo review traps | `gemma4:31b-cloud` | Small | unchanged |
| Task 3 - Scoped feature design | `gpt5.6-sol-xhigh` | Small | `gpt5.4-xhigh` |
| Task 4 - Safe refactor | `kimi-k2-thinking` | Very small | unchanged |
| Task 5 - Large dataset pipeline | `gpt5.6-sol-xhigh` | Small | `kimi-k2-thinking` |
| Task 6 - Review plus tests | `gpt5.6-luna-max` | Small | `glm-5.1:cloud` |

Latest report-aligned takeaways:
- Best premium reference model: `gpt5.6-sol-xhigh` (like-for-like successor to `gpt5.4-xhigh`; 4.45 against 4.14)
- Best primary coder: `gpt5.6-sol-xhigh`
- Best reviewer: `gpt5.6-luna-max`
- Best value under free-use constraints: `gemma4:31b-cloud`
- Best value paid API: `gpt5.6-luna-max`
- Biggest operational weakness observed: severe context-fidelity failures before or without the supplied files on weaker models; slower responses (about 3 to 4 minutes per task) from `gpt5.6-luna-max`

Historical anchor:
- winner on corrected engineering standard: `gpt5.4-xhigh` (September 2026: `gpt5.6-sol-xhigh` ties it at 4.43 overall with the same corrected answer; `gpt5.6-luna-max` 4.29; `deepseek-v4.1-flash` 3.00 on the 2026-09-18 addendum)
- strongest free/cloud value result on the primary six-task set: `gemma4:31b-cloud`

### V3 - Notebook-style code-generation benchmark

Current scored model set:
- `gpt5.4-xhigh`
- `gemma4:31b-cloud`
- `glm-5.1:cloud`
- `qwen-3.6plus`
- `minimax-m2.7-cloud`
- `kimi-k2-thinking`
- `deepseek-v3.2`
- `gpt5.6-sol-xhigh` (September 2026 refresh)
- `gpt5.6-luna-max` (September 2026 refresh)
- `deepseek-v4.1-flash` (2026-09-18 addendum)

Benchmark shape:
- `1` deterministic notebook-style task
- output is an ordered Markdown notebook draft with Markdown and Python code cells
- no repository context files are shared for the task
- scoring combines structured judge prompts with final manual engineering review

Headline v3 ranking (September 2026 refresh rows scored blind with calibration against April anchors; April rows unchanged):
1. `gpt5.4-xhigh` - `4.86`
2. `deepseek-v4.1-flash` - `4.71` (2026-09-18 addendum; tie with `glm-5.1:cloud` ordered by technical mean)
3. `glm-5.1:cloud` - `4.71`
4. `minimax-m2.7-cloud` - `4.43`
5. `kimi-k2-thinking` - `4.29`
6. `gpt5.6-sol-xhigh` - `4.29`
7. `deepseek-v3.2` - `4.14`
8. `qwen-3.6plus` - `4.00`
9. `gemma4:31b-cloud` - `3.71`
10. `gpt5.6-luna-max` - `3.57`

Current v3 task result:

| Task | Winner | Difference size | Notes |
|---|---|---|---|
| Task 1 - Square pad footing sizing notebook draft | `gpt5.4-xhigh` | `moderate` | Several models found `3.0 m`, but `gpt5.4-xhigh` gave the cleanest derivation, clearest explanation of why `2.9 m` fails on uplift in `LC2`, and the strongest notebook traceability with minimal cleanup. |

Current v3 takeaways:
- Best notebook drafter: `gpt5.4-xhigh`
- Best technically reliable result: `gpt5.4-xhigh`
- Best value under free-use constraints: `gemma4:31b-cloud` if local or no-cost access is available
- Biggest operational weakness observed: long think time on several otherwise strong models, plus conclusion-level governing-case mistakes that still need human review
- September 2026 note: `gpt5.6-sol-xhigh` did not match its predecessor here (correct and executable, but no derivation or eccentricity definitions); `gpt5.6-luna-max` states the right answer but its notebook fails its own consistency assert until a one-line formula fix is applied
- 2026-09-18 addendum: `deepseek-v4.1-flash` scores 4.71, level with `glm-5.1:cloud`, with a notebook that runs end to end and a kern-rule cross-check; weakest on the EC3 anchor (3.00), where it headlined an unrequested LTB verdict

## Repository Structure

Root reports and presentations:
- `structural_engineering_benchmark_report.md` - full written report for the original v1 benchmark
- `structural_engineering_benchmark_report_v2.md` - latest full written report for the larger-context v2 benchmark
- `benchmark_presentation_report.html` - technical-executive HTML presentation for v1
- `benchmark_presentation_linkedin.html` - social summary version for v1
- `benchmark_presentation_linkedin_3slides.html` - 3-slide square carousel for v1
- `benchmark_presentation_v2_report.html` - presentation version of the v2 report
- `dashboard.html` - generated interactive dashboard artifact

Benchmark folders:
- `benchmarks/v1/` - original benchmark definition, prompts, and saved raw evaluation outputs for the six v1 tasks
- `benchmarks/v2/` - larger-context pack with `RUNBOOK.md`, task folders, templates, run records, scorecards, and ranking summaries
- `benchmarks/v3/` - notebook-style pack with `RUNBOOK.md`, task brief, templates, run records, scorecards, and ranking summaries

Supporting code and setup:
- `dashboard/` - parser, build script, template, and requirements for generating `dashboard.html`
- `tests/` - parser coverage for the structured benchmark dashboard inputs
- `setup/01_setup.ipynb` - original setup and replication notes

## Replication Notes

For a fair rerun:
- use the exact same prompt text for each model
- start a fresh session for every model-task run
- do not provide first-pass corrective guidance
- save raw outputs before evaluation
- record the exact model string used
- do not show `_evaluator_notes.md` files to the model
- keep the v2 historical anchor separate from the v2 composite by default

The v2 and v3 folders are lightweight manual benchmark harnesses, not automated execution frameworks.

## What This Repo Is Useful For

- comparing local or hosted coding models on realistic structural engineering tasks
- stress-testing unit handling, engineering judgement, and code reliability
- benchmarking larger cloud models on repo-context reading and multi-file reasoning
- benchmarking notebook-style assistant outputs that mix engineering narrative with executable Python
- sharing benchmark outcomes with a technical team
- creating presentation-ready and dashboard-ready summary outputs from the same benchmark data

## Dashboard

Generate the interactive benchmark dashboard:

```bash
pip install -r dashboard/requirements.txt
python dashboard/build.py
```

This writes `dashboard.html` at the repository root.

The dashboard auto-discovers structured rounds in `benchmarks/` that include `models/fixed_model_slate.json`. At the moment that means `v2` and `v3`; `v1` remains documented in Markdown and the root reports but is intentionally excluded from the generated dashboard.

To deploy to GitHub Pages, commit `dashboard.html` and enable Pages on `main`.
