# V2 Larger-Context Cloud Benchmark Pack

This benchmark extends the repository from short prompt coding tasks to larger-context repo reading, review, and scoped-change work.

## Current Scored Model Slate

- `gemma4:31b-cloud` - continuity baseline from v1
- `glm-5.1:cloud`
- `gpt5.4-xhigh` - premium reference model
- `qwen-3.6plus` - paid API middle-tier comparator
- `minimax-m2.7-cloud`
- `kimi-k2-thinking`
- `deepseek-v3.2`

Record the exact model string used in every run, even though execution is manual.

Access note:
- `gemma4`, `glm`, `minimax`, and `kimi` fit the free/cloud route used in this benchmark.
- `qwen-3.6plus` requires paid API access.
- `gpt5.4-xhigh` should be interpreted separately as the premium reference path.

## Execution Protocol

For every task and model:
1. Start a fresh session.
2. Paste the task prompt exactly as written in the task folder.
3. Provide the matching context files from the task folder.
4. Do not provide corrective hints on the first pass.
5. Save the raw output before any follow-up.
6. Fill in a run record from `templates/run_record_template.md`.

Manual execution is expected. This folder is a lightweight benchmark harness, not an automation framework.

## Scoring Protocol

Use hybrid scoring:
- first-pass structured judge scoring using `templates/judge_prompt_template.md`
- final manual engineering review to confirm rankings, override weak judge calls, and capture practical commentary

Score the `6` primary v2 tasks on:
1. Correctness
2. Repo comprehension
3. Change safety
4. Engineering judgement
5. Maintainability
6. Clarity
7. Economics and practical usability

Economics and practical usability should explicitly consider:
- free-use viability
- usable context size in practice
- latency burden
- refusal, truncation, or instability risk

## Reporting Structure

Produce three outputs:
1. Per-task results for the `6` new v2 tasks
2. Overall v2 ranking across those `6` tasks
3. Separate anchor comparison for Task 7 against v1 Task 6

Do not include the anchor task in the default v2 composite average.

## Task List

### Deep Tasks

#### Task 1 - Multi-file bug hunt in a member check pipeline
- Folder: `tasks/deep_01_multifile_bug_hunt`
- Primary skill under test: tracing a real defect across multiple files
- Expected output shape: prioritised bug report plus minimal safe fix proposal

#### Task 2 - Repo review with unit, combination, and reporting traps
- Folder: `tasks/deep_02_repo_review_traps`
- Primary skill under test: code review judgement across multiple modules
- Expected output shape: review findings ordered by severity

#### Task 3 - Scoped feature design on an existing package
- Folder: `tasks/deep_03_scoped_feature_design`
- Primary skill under test: understanding interfaces before proposing changes
- Expected output shape: decision-complete implementation plan and interface changes

#### Task 4 - Safe refactor with behaviour preservation constraints
- Folder: `tasks/deep_04_safe_refactor`
- Primary skill under test: resisting over-refactor and preserving hidden semantics
- Expected output shape: refactor proposal with explicit compatibility notes

### Medium Tasks

#### Task 5 - Large dataset engineering summary pipeline
- Folder: `tasks/medium_05_large_dataset_pipeline`
- Primary skill under test: robust data-processing design under scale constraints
- Expected output shape: improved code or review with performance and validation notes

#### Task 6 - Review plus targeted test design
- Folder: `tasks/medium_06_review_plus_tests`
- Primary skill under test: finding likely numerical failure modes and designing tests
- Expected output shape: concise review plus targeted high-value tests

### Historical Anchor

#### Task 7 - Unchanged v1 EC3 planted-error trap test
- Folder: `tasks/anchor_07_v1_task6_ec3`
- Purpose: direct continuity comparison with the v1 benchmark
- Reporting: separate from the new v2 composite

## Files To Fill During Benchmarking

- Copy `templates/run_record_template.md` once per model-task pair.
- Copy `templates/task_scorecard_template.md` once per task after all candidate outputs are collected.
- Copy the three files in `results/` when publishing the round.
