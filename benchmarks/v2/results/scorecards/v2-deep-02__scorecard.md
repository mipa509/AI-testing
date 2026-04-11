# Task Scorecard

- `task_id`: `v2-deep-02`
- `task_title`: `Repo review with unit, combination, and reporting traps`
- `task_group`: `primary`
- `judge_prompt_version`: `templates/judge_prompt_template.md`
- `manual_reviewer`: `Codex (full seven-model manual pass including gpt5.4-xhigh)`

## Scores

| Model | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Economics/practicality | Overall notes |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `gemma4:31b-cloud` | 5 | 5 | 5 | 5 | 4 | 4 | 5 | High-signal and fully grounded: it found the three real release blockers and kept the fix directions concise and proportionate. |
| `glm-5.1:cloud` | 3 | 3 | 3 | 3 | 4 | 4 | 4 | Found the two main release blockers, but misread the reporting path and added some unsupported assumptions. |
| `gpt5.4-xhigh` | 5 | 5 | 5 | 5 | 4 | 5 | 2 | Excellent grounded review: it found the three real release blockers, de-prioritised the non-core rounding issue correctly, and kept the findings tightly tied to engineering correctness. |
| `qwen-3.6plus` | 5 | 5 | 4 | 4 | 4 | 4 | 3 | Strong grounded review: it caught the three real release blockers, but broadened into extra standards and reporting-policy issues beyond the core release pass. |
| `minimax-m2.7-cloud` | 2 | 3 | 3 | 2 | 4 | 4 | 3 | It stayed on the real codebase and found the load-factor and reporting bugs, but it missed the actual resistance unit defect and replaced it with a weaker `gamma_M0` standards point. |
| `kimi-k2-thinking` | 5 | 5 | 5 | 4 | 4 | 5 | 5 | Strong task fit: it found the three key release blockers, including the reporting trap that `glm` missed; minor overreach on configurability/compliance extras. |
| `deepseek-v3.2` | 1 | 1 | 1 | 1 | 1 | 2 | 1 | Severe context failure: the final review targets an invented package with nonexistent functions and misses the actual supplied defects. |

## Judge Output Summary

Manual comparative pass completed for all seven models.

Task summary: Review a steel beam ULS screening package for unit conversion, load combination, and reporting integrity defects before release.

## Manual Override Notes

Provisional `glm-5.1:cloud` review:
- Correctly flagged the `1e6` resistance divisor issue and the missing `ULS_GAMMA_Q` factor on variable load.
- Reporting review is incomplete: the code sorts ascending and returns the lowest-utilisation row, but the response describes it as returning the highest-utilisation case.
- Boundary-condition concerns are sensible general engineering cautions, but they are not the strongest repo-grounded release finding in the supplied code.

Provisional `qwen-3.6plus` review:
- This is a grounded, technically strong task-2 response: it found the missing `ULS_GAMMA_Q` factor, the resistance unit-conversion error, and the reporting slice bug.
- Main deductions are for proportion and safety: the answer expands into extra boundary, rounding, combination, and self-weight issues beyond the core release blockers.
- That still leaves it clearly stronger than the incomplete task-2 reviews, but a step behind the most concise and proportionate answers.

Provisional `gpt5.4-xhigh` review:
- This is one of the strongest task-2 responses in the set: it found the missing `ULS_GAMMA_Q` factor, the resistance unit-conversion error, and the reporting slice bug.
- It also correctly treated early rounding as secondary rather than mistaking it for a primary release blocker.
- Main deductions are operational rather than technical: this run was slower and less economical than the best free/cloud answers.

Provisional `minimax-m2.7-cloud` review:
- The answer stayed grounded in the supplied three-file package and correctly found the missing `ULS_GAMMA_Q` factor plus the reporting slice bug.
- Its main miss is important: it did not identify the actual `cm3` versus `mm3` resistance-unit defect, and instead escalated a mostly unsupported `gamma_M0` compliance concern.
- That makes the review incomplete for a pre-release blocker pass, even though the structure and fix directions are otherwise clear.

Provisional `kimi-k2-thinking` review:
- Correctly identified all three core release blockers in the supplied repo: the missing `ULS_GAMMA_Q` factor, the resistance unit conversion error, and the reporting bug that returns the least critical case.
- The minimum fix directions are mostly safe and proportionate, even if the reporting fix could equally be framed as returning the full review set depending on intended product behaviour.
- Main deductions are for extra compliance/configurability recommendations that are reasonable but not necessary to satisfy the task.

Provisional `deepseek-v3.2` review:
- This run is a hard hallucination: it discusses nonexistent functions such as `apply_load_factors()`, `moment_capacity()`, `shear_capacity()`, and `generate_report()` instead of the actual three small supplied files.
- Because it reviewed an invented codebase, it missed the real release blockers in the repo and is unsafe to trust for engineering review.
- The structured presentation does not rescue it; the core problem is that the technical basis is fabricated.

Provisional `gemma4:31b-cloud` review:
- Correctly identified all three core release blockers in the supplied repo: missing `ULS_GAMMA_Q`, the resistance unit-conversion error, and the reporting path that hides the critical case.
- The answer stayed concise and proportionate, with less unnecessary standards/configurability drift than `kimi`.
- This is one of the cleanest task-2 reviews in the set.

## Winner

- Winner: `gemma4:31b-cloud`
- Difference size: `Very small over gpt5.4-xhigh`
- Why it matters in practice: `Gemma and gpt5.4 both produced top-tier task-2 reviews, but gemma still has the stronger practicality/economics profile for repeated use on this kind of repo review.`
