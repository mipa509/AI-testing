# Structural Engineering AI Model Benchmark

This repository compares coding models on structural-engineering-focused tasks.

It now contains two benchmark rounds:
- `v1`: short prompt engineering coding and code-review tasks
- `v2`: larger-context cloud-model tasks with multi-file synthetic repo packs

## Benchmark Rounds

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

### V2 - Larger-context cloud benchmark

Fixed model slate:
- `gemma4:31b-cloud`
- `glm-5.1:cloud`
- `kimi-k2-thinking`
- `deepseek-v3.2`

Scope:
- `4` deep synthetic repo-context tasks
- `2` medium synthetic tasks
- `1` unchanged historical anchor copied from v1 Task 6
- hybrid scoring using structured judge prompts plus manual engineering review

The unchanged EC3 trap task is reported separately as an anchor comparison and is not part of the default v2 composite score.

## Start Here

If you are opening this repo for the first time, use this order:

1. `structural_engineering_benchmark_report.md`
2. `benchmark_presentation_report.html`
3. `benchmark_presentation_linkedin_3slides.html`
4. `structural_engineering_model_benchmark.md`
5. `benchmarks/v2/RUNBOOK.md`
6. `benchmarks/v2/README.md`
7. `benchmarks/v2/v2_benchmark_pack.md`

## Current Headline Results

These are the current v1 headline results from the latest 6-task report:

1. `gemma4:31b-cloud` — `3.93`
2. `Qwen3.5 27B` — `3.86`
3. `Qwen3-Coder-Next` — `3.18`

Task winners:

| Task | Winner | Difference size |
|---|---|---|
| Task 1 - Results cleanup | `Qwen3.5 27B` | Moderate |
| Task 2 - Slab check | `Qwen3.5 27B` | Large |
| Task 3 - Geometry assignment | `gemma4:31b-cloud` | Large |
| Task 4 - Rules engine | `Qwen3-Coder-Next` | Minor to Moderate |
| Task 5 - Summary and plotting | `gemma4:31b-cloud` | Minor |
| Task 6 - EC3 trap test | `gemma4:31b-cloud` | Moderate |

## Repository Structure

### V1 files

- `structural_engineering_model_benchmark.md`
  Benchmark pack, prompts, scoring framework, and original task structure.

- `Evaluation 1.md` to `Evaluation 6.md`
  Raw model outputs saved per task.

- `structural_engineering_benchmark_report.md`
  Full written benchmark report with scoring, commentary, summary tables, and conclusions.

- `benchmark_presentation_report.html`
  Technical-executive HTML presentation version.

- `benchmark_presentation_linkedin.html`
  Social-ready visual summary version.

- `benchmark_presentation_linkedin_3slides.html`
  3-slide square carousel version for LinkedIn-style sharing.

### V2 files

- `benchmarks/v2/v2_benchmark_pack.md`
  V2 benchmark instructions, fixed model slate, scoring protocol, and task list.

- `benchmarks/v2/models/fixed_model_slate.json`
  Fixed v2 model manifest.

- `benchmarks/v2/tasks/`
  Synthetic task folders with prompts, context files, and evaluator-only notes.

- `benchmarks/v2/templates/`
  Run record, judge prompt, and task scorecard templates.

- `benchmarks/v2/results/`
  Templates for per-task results, overall ranking, and anchor comparison outputs.

- `setup/01_setup.ipynb`
  Setup and replication notes for the original benchmark workflow.

## Replication Notes

Tests are intended to be run using `Ollama` in terminal sessions so the models are compared under the same interaction conditions.

For a fair rerun:
- use the exact same prompt for each model
- use a fresh session per model
- do not provide first-pass corrective guidance
- save raw outputs before evaluation
- record the exact model string used

## What This Repo Is Useful For

- comparing local or hosted coding models on realistic structural engineering tasks
- stress-testing unit handling, engineering judgement, and code reliability
- benchmarking larger cloud models on repo-context reading and multi-file reasoning
- sharing benchmark outcomes with a technical team
- creating presentation-ready summary outputs from the same benchmark data
