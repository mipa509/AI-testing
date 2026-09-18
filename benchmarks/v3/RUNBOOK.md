# V3 Benchmark Runbook

This is the single working document for running the v3 notebook-style benchmark manually, saving outputs, and scoring the results.

## 1. What You Need Open

Open these files before starting:
1. `benchmarks/v3/v3_benchmark_pack.md`
2. `benchmarks/v3/models/fixed_model_slate.json`
3. `benchmarks/v3/tasks/task_manifest.json`
4. `benchmarks/v3/tasks/notebook_01_pad_footing_sizing/prompt.md`
5. `benchmarks/v3/tasks/notebook_01_pad_footing_sizing/reference_solution_review.md`
6. `benchmarks/v3/templates/run_record_template.md`
7. `benchmarks/v3/templates/task_scorecard_template.md`
8. `benchmarks/v3/templates/judge_prompt_template.md`
9. `benchmarks/v3/results/v3_per_task_results_template.md`
10. `benchmarks/v3/results/v3_overall_ranking_template.md`

Do not open or paste any `_evaluator_notes.md` file into the model.

## 2. Fixed Model Slate

Use these exact model IDs for the current scored slate:
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
- `glm-5.3-flash` (2026-09-18 addendum)
- `tencent-hy4-preview` (2026-09-18 addendum)

## 3. Folder Convention While Running

Use these folders during execution:
- raw outputs: `benchmarks/v3/runs/raw_outputs/`
- run records: `benchmarks/v3/runs/run_records/`

Pre-created raw output files:
- `v3-notebook-01__gemma4-31b-cloud__raw.md`
- `v3-notebook-01__glm-5.1-cloud__raw.md`
- `v3-notebook-01__gpt5.4-xhigh__raw.md`
- `v3-notebook-01__qwen-3.6plus__raw.md`
- `v3-notebook-01__minimax-m2.7-cloud__raw.md`
- `v3-notebook-01__kimi-k2-thinking__raw.md`
- `v3-notebook-01__deepseek-v3.2__raw.md`

Matching run-record files already exist in `benchmarks/v3/runs/run_records/`.

## 4. Execution Order

Run the benchmark in this order:
1. `v3-notebook-01`

This first v3 round contains one task only.

## 5. Exact Workflow For The Task

### Step A - Prepare the prompt

1. Open `tasks/notebook_01_pad_footing_sizing/prompt.md`.
2. Copy the full prompt text exactly as written.
3. Do not share `_evaluator_notes.md` or `reference_solution_review.md` with the model.

### Step B - Run one model

For each model:
1. Start a fresh terminal session.
2. Confirm the exact model ID you are about to use.
3. Paste the task prompt from `prompt.md`.
4. Do not add clarifying hints unless you are deliberately recording a second-pass rerun outside the main benchmark.
5. Wait for the first-pass output to finish.
6. Paste the full output into the matching placeholder file under `benchmarks/v3/runs/raw_outputs/`.

Recommended raw output file structure:

```md
# Raw Output

- task_id: `v3-notebook-01`
- model_id_used: `gemma4:31b-cloud`
- run_date: `YYYY-MM-DD`
- thinking_mode_used: `[yes/no or short note]`

## Prompt Used

[paste the exact prompt text]

## Raw Model Output

[paste the full first-pass output here]
```

### Step C - Fill the run record

For the same model, open the matching placeholder under `benchmarks/v3/runs/run_records/` and fill:
- `run_date`
- `thinking_mode_used`
- `prompt_version`
- `raw_output_path`
- `rate_limit_or_refusal_notes`
- `latency_notes`
- `manual_observations`

### Step D - Repeat for the full current model slate

Do not score the task until all seven model raw outputs are captured.

## 6. Scoring Workflow

After all seven model runs are captured:

1. Open `results/scorecards/v3-notebook-01__scorecard.md`.
2. Use `templates/judge_prompt_template.md` as the evaluator prompt.
3. Paste:
   - the task prompt
   - all seven first-pass outputs
   - any operational observations needed for practicality scoring
4. Save the judge response inside the scorecard under `Judge Output Summary`.
5. Compare model outputs against `reference_solution_review.md`.
6. Apply manual engineering review before locking the winner.

Primary scoring criteria:
- Calculation correctness
- Code quality and executability
- Engineering judgement
- Unit and assumption handling
- Notebook traceability and clarity
- Completeness of deliverable
- Practical usability

## 7. Publishing The Result Documents

After the task is scored:

### A. Per-task results

Fill:
- `benchmarks/v3/results/v3_per_task_results.md`

### B. Overall v3 ranking

Fill:
- `benchmarks/v3/results/v3_overall_ranking.md`

For this first round, the overall ranking is based on `v3-notebook-01` only.

## 8. Minimum Quality Checks Before You Call The Round Finished

Before treating the benchmark as complete, check:
1. the raw output folder contains one completed file per model
2. the run record folder contains one completed file per model
3. the scorecard is filled
4. the per-task results file is filled
5. the overall ranking file is filled
6. the exact model IDs used are recorded
7. the selected footing size in reviewed outputs is checked against the reference solution
