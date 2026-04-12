# Structural Engineering AI Model Benchmark

## What Is This?

This repository compares how well AI coding models perform on structural engineering tasks.

It is intended as a practical stress test for engineering use, not a general chatbot ranking. The benchmark asks models to do work such as:
- reviewing engineering code and calculations
- handling units, combinations, and standards correctly
- reading larger repo-style context without drifting
- producing usable notebook-style engineering drafts

Why this matters:
- engineering mistakes are not harmless formatting errors
- a model can sound confident while still getting the governing case wrong
- this repo shows which models stayed reliable enough to be useful and which ones broke down under realistic engineering pressure

Quick answer:
- Best overall model in the current structured rounds (`v2` and `v3`): `gpt5.4-xhigh`
- Strongest value option under free-use constraints: `gemma4:31b-cloud`

## 5-Minute Summary

What was tested:
- `3` benchmark rounds
- `v1`: `6` short tasks across `3` models
- `v2`: `6` primary larger-context tasks plus `1` historical anchor across `7` models
- `v3`: `1` deterministic notebook-style task across the same `7`-model slate
- all reported scores are out of `5.0`

Top performers:

| Round | Best Overall | Best Value Under Free-Use Constraints |
|---|---|---|
| `v1` | `gemma4:31b-cloud` (`3.93/5`) | `gemma4:31b-cloud` |
| `v2` | `gpt5.4-xhigh` (`4.14/5`) | `gemma4:31b-cloud` (`4.10/5`) |
| `v3` | `gpt5.4-xhigh` (`4.86/5`) | `gemma4:31b-cloud` (`3.71/5`) |

Reading notes:
- raw scores are most meaningful within a round, not across rounds, because task shape and difficulty change
- the latest full written report is `structural_engineering_benchmark_report_v2.md`
- the current `v3` round reports through the structured result files in `benchmarks/v3/results/`

## Getting Started

If you are new to the repo, use this order:

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

If you just want the latest results:
1. `structural_engineering_benchmark_report_v2.md`
2. `benchmarks/v3/results/v3_overall_ranking.md`
3. `benchmarks/v3/results/v3_per_task_results.md`
4. `benchmark_presentation_v2_report.html`

If you want the latest methodology:
1. `benchmarks/v3/README.md`
2. `benchmarks/v3/v3_benchmark_pack.md`
3. `benchmarks/v3/RUNBOOK.md`
4. `benchmarks/v2/README.md`

If you want to rerun the benchmark:
- start with `benchmarks/v3/RUNBOOK.md`
- then use the `Replication Guide` section below

## Glossary

| Term | Meaning |
|---|---|
| Model | An AI coding assistant or coding-capable model being benchmarked |
| `v1` / `v2` / `v3` | Benchmark rounds; each round changes the task style and difficulty |
| Anchor task | The same historical task rerun in a later round to compare change over time |
| EC3 | Eurocode 3, the European structural steel design standard referenced in the benchmark |
| Notebook-style | Output that mixes explanation and Python code in an ordered notebook-like draft |
| Context-fidelity | How well a model uses the files and repo context it was actually given |

## Benchmark Rounds At A Glance

| Round | Focus | Scope | Current leader | Main files |
|---|---|---|---|---|
| `v1` | Short coding and review prompts | `6` tasks, `3` models | `gemma4:31b-cloud` (`3.93`) | `benchmarks/v1/`, `structural_engineering_benchmark_report.md` |
| `v2` | Larger-context repo reading and change design | `6` primary tasks + `1` historical anchor, `7` models | `gpt5.4-xhigh` (`4.14`) | `benchmarks/v2/`, `structural_engineering_benchmark_report_v2.md` |
| `v3` | Deterministic notebook-style code generation | `1` notebook task, `7` models | `gpt5.4-xhigh` (`4.86`) | `benchmarks/v3/`, `benchmarks/v3/results/` |

## Current Headline Results

Score reading guide:
- `5` = engineering-grade output with little or no cleanup needed
- `4` = strong result, but still needs minor edits or checks
- `3` = usable only with moderate review and correction
- `2` = significant issues
- `1` = not suitable for engineering use without major rework

### V1 - Original Short-Task Benchmark

Models benchmarked:
- `Qwen3.5 27B`
- `Qwen3-Coder-Next`
- `gemma4:31b-cloud`

Scope:
- `6` short engineering coding and code-review tasks
- scoring on correctness, robustness, readability, maintainability, engineering suitability, and clarity

Headline ranking:
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

### V2 - Larger-Context Repo Benchmark

Scope:
- `6` primary tasks: `4` deep repo-context tasks and `2` medium tasks
- `1` historical anchor task copied unchanged from `v1` Task 6
- hybrid scoring using structured judge prompts plus manual engineering review

The historical anchor is reported separately and is not part of the default `v2` composite score.

Headline ranking:
1. `gpt5.4-xhigh` - `4.14`
2. `gemma4:31b-cloud` - `4.10`
3. `glm-5.1:cloud` - `3.88`
4. `qwen-3.6plus` - `3.74`
5. `minimax-m2.7-cloud` - `3.72`
6. `kimi-k2-thinking` - `3.67`
7. `deepseek-v3.2` - `2.65`

Primary task winners:

| Task | Winner | Difference size |
|---|---|---|
| Task 1 - Multi-file bug hunt | `gemma4:31b-cloud` | Small |
| Task 2 - Repo review traps | `gemma4:31b-cloud` | Small |
| Task 3 - Scoped feature design | `gpt5.4-xhigh` | Small |
| Task 4 - Safe refactor | `kimi-k2-thinking` | Very small |
| Task 5 - Large dataset pipeline | `kimi-k2-thinking` | Small |
| Task 6 - Review plus tests | `glm-5.1:cloud` | Small |

Main takeaways:
- Best premium reference model: `gpt5.4-xhigh`
- Best primary coder: `gpt5.4-xhigh`
- Best reviewer: `gpt5.4-xhigh`
- Best value under free-use constraints: `gemma4:31b-cloud`
- Biggest operational weakness observed: context-fidelity failures on weaker models when repo files had to be read and used correctly

Historical anchor:
- winner on corrected engineering standard: `gpt5.4-xhigh`
- strongest free/cloud value result on the primary six-task set: `gemma4:31b-cloud`

### V3 - Notebook-Style Code-Generation Benchmark

Scope:
- `1` deterministic notebook-style task
- expected output is an ordered Markdown notebook draft with Markdown and Python code cells
- no repository context files are shared for the task
- scoring combines structured judge prompts with final manual engineering review

Headline ranking:
1. `gpt5.4-xhigh` - `4.86`
2. `glm-5.1:cloud` - `4.71`
3. `minimax-m2.7-cloud` - `4.43`
4. `kimi-k2-thinking` - `4.29`
5. `deepseek-v3.2` - `4.14`
6. `qwen-3.6plus` - `4.00`
7. `gemma4:31b-cloud` - `3.71`

Current task result:

| Task | Winner | Difference size | Notes |
|---|---|---|---|
| Task 1 - Square pad footing sizing notebook draft | `gpt5.4-xhigh` | `moderate` | Several models found `3.0 m`, but `gpt5.4-xhigh` gave the cleanest derivation, clearest explanation of why `2.9 m` fails on uplift in `LC2`, and the strongest notebook traceability with minimal cleanup. |

Main takeaways:
- Best notebook drafter: `gpt5.4-xhigh`
- Best technically reliable result: `gpt5.4-xhigh`
- Best value under free-use constraints: `gemma4:31b-cloud` if local or no-cost access is available
- Biggest operational weakness observed: long think time on several otherwise strong models, plus conclusion-level governing-case mistakes that still need human review

## Replication Guide

If you want to rerun the benchmark, start with `v3`. It is the smallest current round and the cleanest entry point.

Before you start:
- use the runbook for the round you want to run
- make sure you have access to the model routes you plan to test
- use Python only if you also want to rebuild `dashboard.html`

Recommended entry files:
- `benchmarks/v3/RUNBOOK.md`
- `benchmarks/v3/v3_benchmark_pack.md`
- `benchmarks/v2/RUNBOOK.md`
- `benchmarks/v2/v2_benchmark_pack.md`

### Step-By-Step For Running `v3`

1. Open `benchmarks/v3/RUNBOOK.md` and `benchmarks/v3/v3_benchmark_pack.md`.
2. Open `benchmarks/v3/tasks/notebook_01_pad_footing_sizing/prompt.md`.
3. Start a fresh session for the model you are testing.
4. Paste the prompt exactly as written. Do not modify it.
5. Save the full first-pass output into the matching file under `benchmarks/v3/runs/raw_outputs/`.
6. Fill the matching run record under `benchmarks/v3/runs/run_records/`.
7. Repeat until all seven model outputs are captured.
8. Score the round using `benchmarks/v3/results/scorecards/v3-notebook-01__scorecard.md`, `benchmarks/v3/templates/judge_prompt_template.md`, and `reference_solution_review.md`.

Important fairness rules:
- use a fresh session for every model-task run
- do not provide corrective hints on the first pass
- record the exact model string used
- do not show `_evaluator_notes.md` files to the model
- for `v3`, do not share `reference_solution_review.md` with the model
- keep the `v2` historical anchor separate from the `v2` composite by default

## Repository Structure

Root reports and presentations:
- `structural_engineering_benchmark_report.md` - full written report for the original `v1` benchmark
- `structural_engineering_benchmark_report_v2.md` - latest full written report for the larger-context `v2` benchmark
- `benchmark_presentation_report.html` - technical-executive HTML presentation for `v1`
- `benchmark_presentation_linkedin.html` - social summary version for `v1`
- `benchmark_presentation_linkedin_3slides.html` - three-slide square carousel for `v1`
- `benchmark_presentation_v2_report.html` - presentation version of the `v2` report
- `dashboard.html` - generated interactive dashboard artifact

Benchmark folders:
- `benchmarks/v1/` - original benchmark definition, prompts, and saved raw evaluation outputs for the six `v1` tasks
- `benchmarks/v2/` - larger-context benchmark pack with runbook, task folders, templates, run records, scorecards, and ranking summaries
- `benchmarks/v3/` - notebook-style benchmark pack with runbook, task brief, templates, run records, scorecards, and ranking summaries

Supporting code and setup:
- `dashboard/` - parser, build script, template, and requirements for generating `dashboard.html`
- `tests/` - parser coverage for the structured benchmark dashboard inputs
- `setup/01_setup.ipynb` - original setup and replication notes

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
