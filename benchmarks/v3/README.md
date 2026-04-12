# V3 Notebook-Style Code-Generation Benchmark

This folder contains the third benchmark round for notebook-style structural engineering code-generation tasks.

Current scored model slate:
- `gpt5.4-xhigh`
- `gemma4:31b-cloud`
- `glm-5.1:cloud`
- `qwen-3.6plus`
- `minimax-m2.7-cloud`
- `kimi-k2-thinking`
- `deepseek-v3.2`

Benchmark shape:
- `1` deterministic notebook-style task
- output is an ordered Markdown notebook draft with Markdown and Python code cells
- no repository context files are shared for the task

Start here:
1. `RUNBOOK.md`
2. `v3_benchmark_pack.md`
3. `models/fixed_model_slate.json`
4. `tasks/task_manifest.json`
5. `tasks/notebook_01_pad_footing_sizing/prompt.md`
6. `tasks/notebook_01_pad_footing_sizing/reference_solution_review.md`
7. `templates/run_record_template.md`
8. `templates/task_scorecard_template.md`
9. `templates/judge_prompt_template.md`
10. `results/v3_per_task_results.md`
11. `results/v3_overall_ranking.md`

Rules:
- Run each model in a fresh terminal session.
- Use the exact same prompt text for every model.
- Save raw first-pass outputs before any corrective follow-up.
- Do not show `_evaluator_notes.md` to the model.
- Keep the task deterministic and score against the provided engineering brief only.
