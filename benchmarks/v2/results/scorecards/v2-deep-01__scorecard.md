# Task Scorecard

- `task_id`: `v2-deep-01`
- `task_title`: `Multi-file bug hunt in a member check pipeline`
- `task_group`: `primary`
- `judge_prompt_version`: `templates/judge_prompt_template.md`
- `manual_reviewer`: `Codex (full seven-model manual pass including gpt5.4-xhigh)`

## Scores

| Model | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Economics/practicality | Overall notes |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `gemma4:31b-cloud` | 4 | 4 | 4 | 4 | 4 | 5 | 5 | Strong grounded review: it found the real conversion bug and raised a plausible signed-moment aggregation risk without drifting away from the supplied repo. |
| `glm-5.1:cloud` | 4 | 4 | 4 | 4 | 4 | 5 | 4 | Correctly found the cm3 to mm3 conversion defect and proposed strong tests, but the fix scope drifted beyond the minimum. |
| `gpt5.4-xhigh` | 4 | 4 | 4 | 4 | 4 | 5 | 3 | High-quality grounded review: it found the real conversion bug and proposed safe targeted hardening, but it missed the stronger signed-moment envelope risk called out by the evaluator notes. |
| `qwen-3.6plus` | 4 | 4 | 3 | 3 | 4 | 4 | 3 | Grounded and correct on the root conversion bug, but like minimax it missed the stronger signed-moment envelope risk and expanded the patch with weaker defensive changes. |
| `minimax-m2.7-cloud` | 4 | 4 | 3 | 3 | 4 | 4 | 3 | Grounded and correct on the root unit bug, but it missed the stronger signed-moment envelope risk and expanded the patch with weaker secondary issues. |
| `kimi-k2-thinking` | 1 | 1 | 1 | 1 | 1 | 2 | 1 | Final answer is clearly written, but it evaluates an invented codebase with nonexistent APIs, types, and tests rather than the supplied files. |
| `deepseek-v3.2` | 4 | 4 | 3 | 3 | 4 | 4 | 3 | Correctly found the unit-conversion defect, but the proposed fix widens behaviour by swallowing errors and introducing `ERROR` status handling. |

## Judge Output Summary

Manual comparative pass completed for all seven models.

Task summary: Diagnose why major-axis beam utilisation ratios became too high after a refactor and define the smallest safe multi-file fix.

## Manual Override Notes

Provisional `glm-5.1:cloud` review:
- Correctly identified the core cm3 to mm3 conversion defect as the most likely root cause.
- Secondary risks on axis conventions and `gamma_M0` are reasonable to mention but not fully grounded by the supplied repo alone.
- Proposed tests are high value, but the code change is broader than the minimum safe patch requested.

Provisional `qwen-3.6plus` review:
- Correctly identified the core cm3 to mm3 conversion defect and explained the inflated utilisation effect clearly.
- The answer stayed grounded in the supplied files, but it missed the more important signed-moment envelope risk called out by the evaluator notes.
- Main deductions are for proportionality: the extra section lookup and zero-capacity hardening are weaker secondary issues than the real governing-moment trap.

Provisional `gpt5.4-xhigh` review:
- Correctly identified the core cm3 to mm3 conversion defect as the root cause and kept the main fix direction tight.
- Its additional hardening on inconsistent section labels and unrounded status logic is grounded, but it still misses the more important signed-moment envelope risk called out in the evaluator notes.
- So this is a strong review, but not stronger than `gemma`, which found the better repo-grounded secondary defect.

Provisional `minimax-m2.7-cloud` review:
- Correctly identified the core cm3 to mm3 conversion defect and explained the 10x utilisation inflation clearly.
- The response stayed grounded in the supplied files, but it missed the more important signed-moment envelope risk called out by the task notes.
- Main deductions are for proportionality: the added NaN and lookup hardening are weaker secondary issues than the real governing-moment trap.

Provisional `kimi-k2-thinking` review:
- This run is a severe context-fidelity failure: the final answer discusses nonexistent objects such as `AnalysisResult`, `Section`, `calculate_utilisation()`, `load_sections()`, `SECTION_LIBRARY`, and `Zx`/`Sx` fields instead of the supplied pandas-based files.
- Because it diagnoses and patches an invented repository, the response is unsafe to apply and fails the core repo-comprehension requirement of the task.
- Clarity is the only relative strength here: the write-up is structured and confident, but that confidence is misplaced because the technical basis is fabricated.

Provisional `deepseek-v3.2` review:
- Correctly identified the cm3 to mm3 conversion bug as the primary root cause and explained the 10x utilisation inflation clearly.
- The answer stayed on the real codebase, but the fix is less proportionate than `glm`: it changes error handling to return `NaN`, adds a new `ERROR` status path, and broadens behaviour beyond the minimum patch.
- Secondary points on `gamma_M0` and robustness are reasonable, though weaker than the core unit-conversion finding.

Provisional `gemma4:31b-cloud` review:
- Correctly identified the cm3 to mm3 conversion defect as the root cause and explained the 10x utilisation inflation clearly.
- Its secondary risk on `.max()` missing a governing negative moment is grounded in the supplied code and stronger than the more speculative side-notes in some other answers.
- The proposed sign-handling change is still a behaviour change, so this is strong rather than perfect, but it remains well within the task brief.

## Winner

- Winner: `gemma4:31b-cloud`
- Difference size: `Small`
- Why it matters in practice: `Gemma found the core unit bug and paired it with the most repo-grounded secondary risk, giving the strongest overall review without hallucinating a different codebase.`
