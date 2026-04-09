# V2 Benchmark Runbook

This is the single working document for running the v2 benchmark manually, saving outputs, scoring results, and keeping the work in git without publishing it yet.

## 1. What You Need Open

Open these files before starting:
1. `benchmarks/v2/v2_benchmark_pack.md`
2. `benchmarks/v2/models/fixed_model_slate.json`
3. `benchmarks/v2/tasks/task_manifest.json`
4. `benchmarks/v2/templates/run_record_template.md`
5. `benchmarks/v2/templates/task_scorecard_template.md`
6. `benchmarks/v2/templates/judge_prompt_template.md`
7. `benchmarks/v2/results/v2_per_task_results_template.md`
8. `benchmarks/v2/results/v2_overall_ranking_template.md`
9. `benchmarks/v2/results/anchor_task6_comparison_template.md`

Do not open or paste any `_evaluator_notes.md` file into the model.

## 2. Fixed Model Slate

Use these exact model IDs:
- `gemma4:31b-cloud`
- `glm-5.1:cloud`
- `kimi-k2-thinking`
- `deepseek-v3.2`

## 3. Folder Convention While Running

Use these folders during execution:
- raw outputs: `benchmarks/v2/runs/raw_outputs/`
- run records: `benchmarks/v2/runs/run_records/`

Recommended filename pattern for raw outputs:
- `v2-deep-01__gemma4-31b-cloud__raw.md`
- `v2-deep-01__glm-5.1-cloud__raw.md`

Recommended filename pattern for run records:
- `v2-deep-01__gemma4-31b-cloud__run_record.md`
- `v2-deep-01__glm-5.1-cloud__run_record.md`

Recommended filename pattern for completed scorecards:
- `v2-deep-01__scorecard.md`

## 4. Execution Order

Run the benchmark in this order:
1. `v2-deep-01`
2. `v2-deep-02`
3. `v2-deep-03`
4. `v2-deep-04`
5. `v2-medium-05`
6. `v2-medium-06`
7. `v2-anchor-07`

The first six tasks form the v2 composite.

The seventh task is the historical anchor only.

## 5. Exact Workflow For One Task

Use the same steps for every task.

### Step A - Prepare the prompt pack

1. Open the task folder listed in `tasks/task_manifest.json`.
2. Open `prompt.md`.
3. Open the files inside the task `context/` folder.
4. Do not open `_evaluator_notes.md` for the model.

### Step B - Run one model

For each model:
1. Start a fresh Ollama terminal session.
2. Confirm the exact model ID you are about to use.
3. Paste the task prompt from `prompt.md`.
4. Paste the relevant context files in a consistent order.
5. Do not give corrective hints.
6. Wait for the first-pass output to finish.
7. Copy the full raw output into a new file under `benchmarks/v2/runs/raw_outputs/`.

Recommended raw output file structure:

```md
# Raw Output

- task_id: `v2-deep-01`
- model_id_used: `gemma4:31b-cloud`
- run_date: `YYYY-MM-DD`
- thinking_mode_used: `[yes/no or short note]`

## Prompt Used

[paste the exact prompt text]

## Context Files Shared

- `context/file_a.py`
- `context/file_b.py`

## Raw Model Output

[paste the full first-pass output here]
```

### Step C - Fill the run record

Copy `templates/run_record_template.md` to `benchmarks/v2/runs/run_records/` and fill:
- `task_id`
- `task_title`
- `model_id_used`
- `run_date`
- `thinking_mode_used`
- `prompt_version`
- `context_files_shared`
- `raw_output_path`
- `rate_limit_or_refusal_notes`
- `latency_notes`
- `manual_observations`

### Step D - Repeat for all four models

Do not score the task until all four raw outputs are captured.

## 6. Scoring Workflow For One Task

After all four model runs are captured:

1. Copy `templates/task_scorecard_template.md` to a task-specific scorecard file.
2. Use `templates/judge_prompt_template.md` as the evaluator prompt.
3. Paste:
   - the task prompt
   - the relevant context
   - all four first-pass outputs
   - any operational observations needed for economics scoring
4. Save the judge response inside the scorecard under `Judge Output Summary`.
5. Apply manual engineering review.
6. Fill the final winner and difference size.

Economics and practicality should consider:
- whether the route stayed usable without payment
- whether the model truncated
- whether it slowed down materially
- whether it refused or drifted
- whether it handled the amount of context cleanly

## 7. Publishing The Three Result Documents

After the six primary v2 tasks are scored:

### A. Per-task results

Fill:
- `benchmarks/v2/results/v2_per_task_results_template.md`

### B. Overall v2 ranking

Fill:
- `benchmarks/v2/results/v2_overall_ranking_template.md`

Only include:
- `v2-deep-01`
- `v2-deep-02`
- `v2-deep-03`
- `v2-deep-04`
- `v2-medium-05`
- `v2-medium-06`

Do not include the anchor task in the default average.

### C. Anchor comparison

Fill:
- `benchmarks/v2/results/anchor_task6_comparison_template.md`

Use:
- the old v1 Task 6 result for `gemma4:31b-cloud`
- the new v2 anchor outputs for all four models

## 8. Task-Specific Notes

### For deep tasks

Prefer full-file context sharing in the order listed in the prompt.

### For medium tasks

Still use a fresh session per model. Do not carry learning forward from the previous task.

### For the anchor task

Keep it verbatim. Do not simplify, modernise, or “improve” the prompt before running it.

## 9. Minimum Quality Checks Before You Call The Round Finished

Before treating the benchmark as complete, check:
1. every task has four raw output files
2. every task has four run records
3. every task has one completed scorecard
4. the six primary tasks are present in the per-task and overall ranking files
5. the anchor task is present only in the anchor comparison file
6. the exact model IDs used are recorded

## 10. Safe Git Workflow Before Anything Goes Public

Because this repo is on your work machine and you do not want to publish yet, use git locally only.

Safe options:

### Option A - Local branch only

Run locally:

```powershell
git checkout -b v2-benchmark-work
git add README.md benchmarks/v2
git commit -m "Add v2 larger-context benchmark scaffold and runbook"
```

This keeps the work in git history on the machine without pushing anywhere.

### Option B - Local commit on current branch, no push

Run locally:

```powershell
git add README.md benchmarks/v2
git commit -m "Add v2 larger-context benchmark scaffold and runbook"
```

Only use this if you are comfortable carrying the unpublished work on `main` locally.

### Option C - Transfer to your local PC without publishing

If you want the changes on your home machine before any remote push, use one of these:
- copy the repo folder directly
- zip the repo and move it
- create a git bundle or patch set

If you want the simplest workflow, use:
1. create the local branch
2. commit locally
3. copy the repo folder or zip to your local PC
4. continue testing there
5. push later only when ready

## 11. Recommended Practical Routine

Use this exact pattern:
1. commit the scaffold locally but do not push
2. transfer or sync the repo to your local PC
3. run all benchmark sessions on the local PC
4. paste outputs into the raw output files and run records
5. complete scorecards
6. fill the three result documents
7. review the final write-up
8. push only when you are happy with the benchmark state
