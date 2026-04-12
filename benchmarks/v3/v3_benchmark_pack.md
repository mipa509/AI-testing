# V3 Notebook-Style Code-Generation Benchmark Pack

This benchmark extends the structural engineering test suite into deterministic notebook-style code generation.

## Current Scored Model Slate

- `gemma4:31b-cloud` - continuity baseline from v1 and v2
- `glm-5.1:cloud`
- `gpt5.4-xhigh` - premium reference model
- `qwen-3.6plus` - paid API middle-tier comparator
- `minimax-m2.7-cloud`
- `kimi-k2-thinking`
- `deepseek-v3.2`

Record the exact model string used in every run, even though execution is manual.

## Execution Protocol

For every task and model:
1. Start a fresh session.
2. Paste the task prompt exactly as written.
3. Do not provide corrective hints on the first pass.
4. Save the raw output before any follow-up.
5. Fill in the matching run record from `templates/run_record_template.md`.

Manual execution is expected. This folder is a lightweight benchmark harness, not an automation framework.

## Scoring Protocol

Use hybrid scoring:
- first-pass structured judge scoring using `templates/judge_prompt_template.md`
- final manual engineering review against `tasks/notebook_01_pad_footing_sizing/reference_solution_review.md`

Score the primary v3 task on:
1. Calculation correctness
2. Code quality and executability
3. Engineering judgement
4. Unit and assumption handling
5. Notebook traceability and clarity
6. Completeness of deliverable
7. Practical usability

Practical usability should explicitly consider:
- free-use viability
- latency burden
- refusal, truncation, or instability risk
- whether the output is usable as an assistant-engineer style notebook draft without major rework

## Reporting Structure

Produce two outputs:
1. Per-task results for the current v3 task set
2. Overall v3 ranking across the scored task set

## Task List

### Notebook Task

#### Task 1 - Square pad footing sizing notebook draft
- Folder: `tasks/notebook_01_pad_footing_sizing`
- Primary skill under test: converting a deterministic engineering brief into readable Markdown plus working Python
- Expected output shape: notebook-style Markdown/code draft with a final selected footing size and governing case

## Files To Fill During Benchmarking

- Fill one raw output placeholder per model-task pair in `runs/raw_outputs/`.
- Fill one run record placeholder per model-task pair in `runs/run_records/`.
- Fill the task scorecard in `results/scorecards/`.
- Fill the summary files in `results/`.
