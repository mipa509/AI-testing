# V2 Overall Ranking

This ranking covers the six new v2 tasks for `gemma4:31b-cloud`, `glm-5.1:cloud`, `gpt5.4-xhigh`, `qwen-3.6plus`, `minimax-m2.7-cloud`, `kimi-k2-thinking`, `deepseek-v3.2`, and, from the September 2026 refresh, `gpt5.6-sol-xhigh` and `gpt5.6-luna-max`.

## Cross-Task Average Scores

| Criterion | gemma4:31b-cloud | glm-5.1:cloud | gpt5.4-xhigh | qwen-3.6plus | minimax-m2.7-cloud | kimi-k2-thinking | deepseek-v3.2 | gpt5.6-sol-xhigh | gpt5.6-luna-max | deepseek-v4.1-flash | glm-5.3-flash | tencent-hy4-preview | claude-fable-5.1-high | gemma4:26b-local |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---: |---: |---: |---: |---: |---:|
| Correctness | 4.00 | 3.83 | 4.33 | 4.00 | 3.67 | 3.50 | 2.67 | 4.83 | 4.83 | 3.50 | 4.00 | 4.50 | 5.00 | 3.00 |
| Repo comprehension | 4.00 | 3.83 | 4.50 | 4.17 | 4.00 | 3.50 | 2.83 | 4.67 | 5.00 | 3.50 | 4.00 | 4.50 | 5.00 | 2.50 |
| Change safety | 3.83 | 3.50 | 4.00 | 3.33 | 3.50 | 3.33 | 2.33 | 4.50 | 4.67 | 4.00 | 4.00 | 2.50 | 4.00 | 3.50 |
| Engineering judgement | 4.00 | 3.67 | 4.33 | 3.67 | 3.50 | 3.33 | 2.50 | 4.67 | 4.67 | 3.00 | 4.00 | 3.00 | 4.50 | 2.50 |
| Maintainability | 4.00 | 4.00 | 4.17 | 4.00 | 4.17 | 3.50 | 2.86 | 4.67 | 4.50 | 4.00 | 4.00 | 3.50 | 4.50 | 2.50 |
| Clarity | 4.17 | 4.50 | 4.83 | 4.00 | 4.17 | 4.17 | 3.17 | 4.83 | 4.67 | 3.50 | 4.00 | 3.50 | 4.00 | 3.00 |
| Economics/practicality | 4.67 | 3.83 | 2.83 | 3.00 | 3.00 | 4.33 | 2.17 | 3.00 | 3.00 | 2.50 | 2.50 | 2.50 | 2.50 | 4.00 |
| Overall average | 4.10 | 3.88 | 4.14 | 3.74 | 3.72 | 3.67 | 2.65 | 4.45 | 4.48 | 3.43 | 3.79 | 3.43 | 4.21 | 3.00 |

Provisional columns: `deepseek-v4.1-flash` (Task 2 and the anchor only), `glm-5.3-flash` (Task 2 and the anchor only), `tencent-hy4-preview` (Task 2 and the anchor only), `claude-fable-5.1-high` (Task 2 and the anchor only), `gemma4:26b-local` (Task 2 and the anchor only) were run on a subset of the v2 tasks (2026-09-18 and 2026-09-19 addenda), so their averages cover only those tasks, include the anchor where it was run, and are provisional until the remaining primary tasks are run; they are not comparable with the six-task composite of the other columns.

## Overall Ranking

1. `gpt5.6-luna-max` - `4.48`
2. `gpt5.6-sol-xhigh` - `4.45`
3. `claude-fable-5.1-high` - `4.21` (provisional: Task 2 and the anchor only)
4. `gpt5.4-xhigh` - `4.14`
5. `gemma4:31b-cloud` - `4.10`
6. `glm-5.1:cloud` - `3.88`
7. `glm-5.3-flash` - `3.79` (provisional: Task 2 and the anchor only)
8. `qwen-3.6plus` - `3.74`
9. `minimax-m2.7-cloud` - `3.72`
10. `kimi-k2-thinking` - `3.67`
11. `deepseek-v4.1-flash` - `3.43` (provisional: Task 2 and the anchor only)
12. `tencent-hy4-preview` - `3.43` (provisional: Task 2 and the anchor only)
13. `gemma4:26b-local` - `3.00` (provisional: Task 2 and the anchor only)
14. `deepseek-v3.2` - `2.65`

September 2026 note: the `gpt5.6-sol-xhigh` and `gpt5.6-luna-max` rows were scored blind by a new judge alongside April anchor responses and shifted onto the April scale with per-task calibration offsets (see `benchmarks/refresh_2026-09_calibration.md`). On three tasks the shift saturates at the 5 cap, so Sol's blind margin over Luna on deep-03 and deep-04 is not visible in these averages. April rows are unchanged.

## Recommended Use Cases

- Best premium reference model: `gpt5.6-sol-xhigh` (September 2026; like-for-like successor to `gpt5.4-xhigh`, 4.45 against 4.14)
- Best primary coder: `gpt5.6-sol-xhigh` (blind winner on the scoped feature design, safe refactor and dataset pipeline tasks)
- Best reviewer: `gpt5.6-luna-max` (winner on review plus tests; tied with Sol on the bug hunt and repo review tasks)
- Best value under free-use constraints: `gemma4:31b-cloud`
- Best value paid API: `gpt5.6-luna-max` (4.48 overall at the lowest list price in the slate; replaces `qwen-3.6plus` as the paid middle option)
- Biggest operational weakness observed: Severe context-fidelity failures before or without the supplied files, especially on `kimi-k2-thinking` and `deepseek-v3.2`; among the September models, slower responses from `gpt5.6-luna-max` (about 3 to 4 minutes per task)
