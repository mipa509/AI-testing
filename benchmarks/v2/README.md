# V2 Larger-Context Cloud Benchmark

This folder contains the second benchmark round for larger-context repo-reading and engineering-review tasks.

Current scored model slate:
- `gpt5.4-xhigh`
- `gemma4:31b-cloud`
- `glm-5.1:cloud`
- `qwen-3.6plus`
- `minimax-m2.7-cloud`
- `kimi-k2-thinking`
- `deepseek-v3.2`
- `gpt5.6-sol-xhigh` (September 2026 refresh; successor to `gpt5.4-xhigh`)
- `gpt5.6-luna-max` (September 2026 refresh; budget API tier)
- `deepseek-v4.1-flash` (2026-09-18 addendum; OpenRouter API; Task 2 and anchor only)
- `glm-5.3-flash` (2026-09-18 addendum; OpenRouter API; Task 2 and anchor only)
- `tencent-hy4-preview` (2026-09-18 addendum; OpenRouter API; Task 2 and anchor only)
- `claude-fable-5.1-high` (2026-09-19 addendum; Anthropic, Claude Code subscription; Task 2 and anchor only)

Practical access note:
- `gemma4:31b-cloud`, `glm-5.1:cloud`, `minimax-m2.7-cloud`, and `kimi-k2-thinking` were runnable via the free Ollama cloud route.
- `qwen-3.6plus` used a paid API/OpenRouter route.
- `gpt5.4-xhigh` is treated as a premium reference model and should be interpreted separately from the free/cloud value story.
- `gpt5.6-sol-xhigh` and `gpt5.6-luna-max` were run in September 2026 through the Codex VS Code extension (the same route as `gpt5.4-xhigh`) and scored blind with calibration against the April results; see `benchmarks/refresh_2026-09_summary.md` and `benchmarks/refresh_2026-09_calibration.md`.
- `deepseek-v4.1-flash` was run on 2026-09-18 from a VS Code agent chat via OpenRouter on Task 2 and the anchor only, and scored with the same blind procedure; see `benchmarks/addendum_2026-09-18_deepseek-v4.1-flash.md`.
- `glm-5.3-flash` followed on the same route and tasks the same day; see `benchmarks/addendum_2026-09-18_glm-5.3-flash.md`. `tencent-hy4-preview` followed on the same route and tasks; see `benchmarks/addendum_2026-09-18_tencent-hy4-preview.md`. `claude-fable-5.1-high` (2026-09-19; Claude Fable 5.1 run in Claude Code, identity withheld from the judges until scoring was complete) followed on the same tasks; see `benchmarks/addendum_2026-09-19_claude-fable-5.1-high.md`. All four partial models carry provisional v2 averages over Task 2 and the anchor.

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
7. `results/v2_per_task_results.md`
8. `results/v2_overall_ranking.md`
9. `results/anchor_task6_comparison.md`

Rules:
- Run each model in a fresh terminal session.
- Use the exact same task prompt text for every model.
- Save raw first-pass outputs before any corrective follow-up.
- Do not show files named `_evaluator_notes.md` to the model.
- Keep the anchor task separate from the v2 composite by default.

Reporting outputs:
- `results/v2_per_task_results.md`
- `results/v2_overall_ranking.md`
- `results/anchor_task6_comparison.md`
