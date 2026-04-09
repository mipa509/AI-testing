# V2 Larger-Context Cloud Benchmark

This folder contains the second benchmark round for larger-context cloud-hosted models run manually through Ollama terminal sessions.

Fixed model slate:
- `gemma4:31b-cloud`
- `glm-5.1:cloud`
- `kimi-k2-thinking`
- `deepseek-v3.2`

Benchmark split:
- `6` new v2 tasks
  - `4` deep synthetic repo-context tasks
  - `2` medium synthetic tasks
- `1` historical anchor task copied unchanged from v1 Task 6

Start here:
1. `RUNBOOK.md`
2. `v2_benchmark_pack.md`
3. `models/fixed_model_slate.json`
4. `tasks/task_manifest.json`
5. `templates/run_record_template.md`
6. `templates/task_scorecard_template.md`
7. `results/v2_per_task_results_template.md`

Rules:
- Run each model in a fresh terminal session.
- Use the exact same task prompt text for every model.
- Save raw first-pass outputs before any corrective follow-up.
- Do not show files named `_evaluator_notes.md` to the model.
- Keep the anchor task separate from the v2 composite by default.

Reporting outputs:
- `results/v2_per_task_results_template.md`
- `results/v2_overall_ranking_template.md`
- `results/anchor_task6_comparison_template.md`
