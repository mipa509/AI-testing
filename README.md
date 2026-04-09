# Structural Engineering AI Model Benchmark

This repository compares multiple coding models on structural-engineering-focused tasks.

Current models benchmarked:
- `Qwen3.5 27B`
- `Qwen3-Coder-Next`
- `gemma4:31b-cloud`

Current scope:
- 6 benchmark tasks
- engineering coding and code-review style prompts
- scoring on correctness, robustness, readability, maintainability, engineering suitability, and clarity

## Start Here

If you are opening this repo on GitHub for the first time, use this order:

1. `structural_engineering_benchmark_report.md`
2. `benchmark_presentation_report.html`
3. `benchmark_presentation_linkedin_3slides.html`
4. `structural_engineering_model_benchmark.md`

## Current Headline Results

Overall ranking from the latest 6-task report:

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

- `setup/01_setup.ipynb`
  Setup and replication notes.

## Replication Notes

Tests were run using `Ollama` in terminal sessions so the models were compared under the same interaction conditions.

For a fair rerun:
- use the exact same prompt for each model
- use a fresh session per model
- do not provide first-pass corrective guidance
- save raw outputs before evaluation

## What This Repo Is Useful For

- comparing local or hosted coding models on realistic structural engineering tasks
- stress-testing unit handling, engineering judgement, and code reliability
- sharing benchmark outcomes with a technical team
- creating presentation-ready summary outputs from the same benchmark data
