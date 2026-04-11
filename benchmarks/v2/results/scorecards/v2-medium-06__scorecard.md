# Task Scorecard

- `task_id`: `v2-medium-06`
- `task_title`: `Review plus targeted test design`
- `task_group`: `primary`
- `judge_prompt_version`: `templates/judge_prompt_template.md`
- `manual_reviewer`: `Codex (full seven-model manual pass including gpt5.4-xhigh)`

## Scores

| Model | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Economics/practicality | Overall notes |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `gemma4:31b-cloud` | 2 | 2 | 2 | 2 | 3 | 4 | 4 | It catches the zero-allowable issue clearly, but it also rewrites `differential_slope()` around an adjacent-point assumption and changes the unit/semantic contract. |
| `glm-5.1:cloud` | 3 | 3 | 2 | 2 | 3 | 4 | 3 | Caught real hidden failures, but overreached with new `WARNING` logic, extra validation assumptions, and a broader test set than needed. |
| `gpt5.4-xhigh` | 3 | 4 | 2 | 3 | 4 | 5 | 3 | Grounded and clear: it catches the zero-allowable flaw, the sign-convention trap, and the hidden unit issue, but its minimum fix still stops short of a fully convincing unit-normalisation path for `differential_slope()`. |
| `qwen-3.6plus` | 2 | 3 | 2 | 2 | 3 | 4 | 3 | It catches the zero-allowable and zero-spacing failures, but misses the hidden unit-consistency bug in `differential_slope()` and broadens behaviour with new validation rules. |
| `minimax-m2.7-cloud` | 3 | 4 | 3 | 3 | 4 | 4 | 3 | Grounded and better aligned with the real helper than most task-6 answers, but it still broadens behaviour by turning several quiet returns into exceptions and adding extra sign/validation policy. |
| `kimi-k2-thinking` | 2 | 2 | 2 | 2 | 3 | 4 | 5 | Fast and well structured, but it invents a new adjacent-point interpretation for `differential_slope()` that is not grounded by the supplied helper. |
| `deepseek-v3.2` | 2 | 3 | 2 | 2 | 2 | 3 | 2 | It finds some real bugs, but the proposed `status_from_ratio()` fix is internally inconsistent with its own tests and adds an unjustified tolerance policy. |

## Judge Output Summary

Manual comparative pass completed for all seven models.

Task summary: Review a foundation-settlement helper for hidden numerical failures and specify the minimum fixes plus the highest-value tests.

## Manual Override Notes

Provisional `glm-5.1:cloud` review:
- Correctly spotted the zero-allowable, zero-spacing, and insufficient-data failure modes.
- The proposed fix drifts away from minimum change by inventing a new `WARNING` status band and enforcing validation rules that are not clearly justified by the supplied repo.
- The test set is useful but not especially focused for a prompt that explicitly asked to avoid a large matrix.

Provisional `qwen-3.6plus` review:
- It correctly catches the zero-allowable silent pass and the zero-spacing crash, and it keeps the core max-minus-min helper shape.
- The main miss is important: it does not identify the hidden unit-consistency bug in `differential_slope()`, and instead codifies the existing `mm/m` interpretation in its docstring.
- It also broadens behaviour with new negative-input validation, so this is a weaker engineering answer than the more grounded task-6 responses.

Provisional `gpt5.4-xhigh` review:
- It correctly catches the zero-allowable silent pass, the hidden sign-convention trap, the exact-limit boundary issue, and the mixed `mm` versus `m` problem in `differential_slope()`.
- The answer is clearer than most on units and test targeting, and it avoids the adjacent-point semantic rewrite seen in weaker runs.
- Main deductions are for the minimum-fix path: the proposed code keeps the `mm/m` interpretation rather than fully normalising the quantity, so it is strong but not decisive enough to overturn the current task winner.

Provisional `minimax-m2.7-cloud` review:
- This is one of the more grounded task-6 responses: it catches the zero-allowable flaw, the mixed `mm` versus `m` slope issue, and the lack of a spacing guard.
- It preserves the core max-minus-min slope logic, which is a better fit to the supplied helper than the adjacent-point rewrites seen in some other answers.
- Main deductions are for proportionality: the proposed fix still broadens behaviour with new exceptions and extra negative-input validation that the helper did not clearly require.

Provisional `kimi-k2-thinking` review:
- It correctly identified the zero-allowable silent pass and the `< 1.0` versus `<= 1.0` boundary issue.
- The main problem is a repo-unsupported semantic rewrite: it changes `differential_slope()` from a max-minus-min helper into an adjacent-point slope routine based on outside engineering assumptions not present in the task context.
- Additional sign/unit commentary is partly sensible, but the answer is no longer a minimum safe fix once it changes the meaning of the core helper.

Provisional `deepseek-v3.2` review:
- It correctly spotted the zero-allowable silent pass, the zero-spacing crash, and the mixed-units communication risk.
- The answer then drifts: it invents a tolerance-based pass/fail policy, changes the function signature, and its own proposed code contradicts its tests on the exact `ratio == 1.0` boundary.
- Because the fix and test set are not internally consistent, this is a materially weaker engineering answer than the better grounded task-6 responses.

Provisional `gemma4:31b-cloud` review:
- It clearly identifies the zero-allowable flaw and the unit-communication risk around `mm/m`.
- The main problem is the same kind of drift seen in some other task-6 answers: it redefines `differential_slope()` around adjacent-point behaviour and converts the returned quantity to a different semantic contract.
- That makes it better than a hallucinated answer, but still not a minimum safe fix for the supplied helper.

## Winner

- Winner: `glm-5.1:cloud`
- Difference size: `Small`
- Why it matters in practice: `No model was ideal on task 6, but glm still stayed slightly closer to the real helper semantics than minimax, qwen, kimi, deepseek, or gemma.`
