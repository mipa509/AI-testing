# V3 Overall Ranking

## Cross-Task Average Scores

| Criterion | gemma4:31b-cloud | glm-5.1:cloud | gpt5.4-xhigh | qwen-3.6plus | minimax-m2.7-cloud | kimi-k2-thinking | deepseek-v3.2 | gpt5.6-sol-xhigh | gpt5.6-luna-max | deepseek-v4.1-flash | glm-5.3-flash | tencent-hy4-preview | anon-2026-09-19 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---: |---: |---: |---: |---:|
| Calculation correctness | 4 | 5 | 5 | 4 | 5 | 5 | 5 | 5 | 3 | 5 | 4 | 5 | 5 |
| Code quality/executability | 4 | 5 | 5 | 4 | 5 | 5 | 5 | 5 | 3 | 5 | 4 | 5 | 5 |
| Engineering judgement | 3 | 5 | 5 | 3 | 4 | 4 | 4 | 4 | 4 | 5 | 4 | 5 | 5 |
| Unit/assumption handling | 4 | 5 | 5 | 5 | 4 | 4 | 3 | 4 | 4 | 5 | 5 | 5 | 5 |
| Notebook traceability/clarity | 3 | 4 | 5 | 4 | 4 | 4 | 4 | 4 | 4 | 5 | 4 | 5 | 5 |
| Completeness of deliverable | 4 | 5 | 5 | 4 | 5 | 5 | 5 | 4 | 4 | 5 | 4 | 5 | 5 |
| Practical usability | 4 | 4 | 4 | 4 | 4 | 3 | 3 | 4 | 3 | 3 | 3 | 3 | 3 |
| Overall average | 3.71 | 4.71 | 4.86 | 4.00 | 4.43 | 4.29 | 4.14 | 4.29 | 3.57 | 4.71 | 4.00 | 4.71 | 4.71 |

## Overall Ranking

1. `gpt5.4-xhigh` - `4.86`
2. `deepseek-v4.1-flash` - `4.71`
3. `tencent-hy4-preview` - `4.71`
4. `anon-2026-09-19` - `4.71`
5. `glm-5.1:cloud` - `4.71`
6. `minimax-m2.7-cloud` - `4.43`
7. `kimi-k2-thinking` - `4.29`
8. `gpt5.6-sol-xhigh` - `4.29`
9. `deepseek-v3.2` - `4.14`
10. `glm-5.3-flash` - `4.00`
11. `qwen-3.6plus` - `4.00`
12. `gemma4:31b-cloud` - `3.71`
13. `gpt5.6-luna-max` - `3.57`

September 2026 note: `gpt5.6-sol-xhigh` and `gpt5.6-luna-max` were scored blind by a new judge alongside April anchor responses and shifted onto the April scale with a per-task calibration offset (see `benchmarks/refresh_2026-09_calibration.md`). Ties on the overall average are ordered by the six-criterion technical mean. April rows are unchanged.
DeepSeek V4.1 Flash addendum (2026-09-18): `deepseek-v4.1-flash` was scored blind on this task with the same procedure and the September calibration offset (see `benchmarks/addendum_2026-09-18_deepseek-v4.1-flash.md`); it was run on three tasks only. Its tie with `glm-5.1:cloud` on the overall average is ordered by the six-criterion technical mean.
GLM 5.3 Flash addendum (2026-09-18): `glm-5.3-flash` was scored blind on this task with the same procedure; its anchors met the calibration gate, so no offset was applied (see `benchmarks/addendum_2026-09-18_glm-5.3-flash.md`). It was run on three tasks only. Its tie with `qwen-3.6plus` on the overall average is ordered by the six-criterion technical mean.
Tencent Hy4 Preview addendum (2026-09-18): `tencent-hy4-preview` was scored blind on this task with the same procedure and the September calibration offset (see `benchmarks/addendum_2026-09-18_tencent-hy4-preview.md`); it was run on three tasks only. Its tie with `deepseek-v4.1-flash` and `glm-5.1:cloud` on the overall average is ordered by the six-criterion technical mean, then by table order.

Anonymous model addendum (2026-09-19): `anon-2026-09-19` (a placeholder id until the user discloses the model) was scored blind on this task with the same procedure and the September calibration offset (see `benchmarks/addendum_2026-09-19_anon-2026-09-19.md`); it was run on three tasks only. Its tie with `deepseek-v4.1-flash`, `tencent-hy4-preview` and `glm-5.1:cloud` on the overall average is ordered by the six-criterion technical mean, then by table order.

## Recommended Use Cases

- Best notebook drafter: `gpt5.4-xhigh`
- Best technically reliable result: `gpt5.4-xhigh`
- Best value under free-use constraints: `gemma4:31b-cloud` if local or no-cost access is available; fastest usable draft in this run, but it still needs manual QC on the governing-case conclusion.
- Biggest operational weakness observed: Long think time on several otherwise strong models, plus conclusion-level governing-case mistakes in some outputs that would need human review before use.
- September 2026 note: `gpt5.6-sol-xhigh` (4.29) did not match its predecessor on this task because it quoted the compact pressure formula without the requested derivation or eccentricity definitions; `gpt5.6-luna-max` (3.57) stated the correct answer but its notebook stops on its own consistency assert until a one-line formula fix is applied.
- DeepSeek V4.1 Flash addendum (2026-09-18): `deepseek-v4.1-flash` (4.71) matches `glm-5.1:cloud` on this task at the second-lowest list price in the slate ($0.15 / $0.60 per 1M tokens), with a working notebook and a kern-rule cross-check; single task, 4 min 15 s run.
- GLM 5.3 Flash addendum (2026-09-18): `glm-5.3-flash` (4.00) reaches `3.0 m` and `LC2` in its conclusion with the fullest written derivation among the addendum models, but its code prints `LC3` as the governing case and its middle-third explanation is wrong for biaxial loading; single task, 5 min 56 s run.
- Tencent Hy4 Preview addendum (2026-09-18): `tencent-hy4-preview` (4.71) ties `deepseek-v4.1-flash` and `glm-5.1:cloud` on this task with the richest audit document of the addendum models (exact fractions, corner pressures, closed-form width bounds) at a mid-tier price ($0.83 / $2.50 per 1M tokens); single task, 3 min 18 s run.
- Anonymous model addendum (2026-09-19): `anon-2026-09-19` (4.71) ties the 4.71 group on this task with a straight 5.00 on the six technical criteria (Navier derivation with the kern limit, hand-check cell, full pass/fail matrix, closed-form width cross-check, margin commentary) and ranked first in its blind pack above `gpt5.4-xhigh`; held below the winner only by practicality (6 min 20 s API, 11 min 16 s wall, $2.65 session cost on a premium route); single task.
