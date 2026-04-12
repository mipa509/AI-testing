# Task Scorecard

- `task_id`: `v3-notebook-01`
- `task_title`: `Square pad footing sizing notebook draft`
- `task_group`: `primary`
- `judge_prompt_version`: `judge_prompt_template.md + manual engineering review`
- `manual_reviewer`: `Codex`

## Scores

| Model | Calculation correctness | Code quality/executability | Engineering judgement | Unit/assumption handling | Notebook traceability/clarity | Completeness of deliverable | Practical usability | Overall notes |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `gemma4:31b-cloud` | 4 | 4 | 3 | 4 | 3 | 4 | 4 | Correct `3.0 m` selection and runnable code, but the final prose leaves placeholders unresolved and misidentifies the governing case as `LC3` instead of `LC2`. |
| `glm-5.1:cloud` | 5 | 5 | 5 | 5 | 4 | 5 | 4 | Strong reference-aligned derivation, correct `3.0 m` selection, and correct overall governing case `LC2`; slightly plainer notebook flow than the winner. |
| `gpt5.4-xhigh` | 5 | 5 | 5 | 5 | 5 | 5 | 4 | Best overall submission: exact handling of the `2.9 m` uplift trap, strongest derivation, clean executable notebook, and minimal cleanup needed. |
| `qwen-3.6plus` | 4 | 4 | 3 | 5 | 4 | 4 | 4 | Strong derivation and correct size search, but the final governing case is reported as `LC3` and the exported notebook contains wrapper and placeholder cleanup issues. |
| `minimax-m2.7-cloud` | 5 | 5 | 4 | 4 | 4 | 5 | 4 | Clear, correct, and well presented; minor penalty because the `abs(Mx) + abs(My)` framing is less rigorous than the stated sign-convention model. |
| `kimi-k2-thinking` | 5 | 5 | 4 | 4 | 4 | 5 | 3 | Correct result and usable notebook, but the pressure model is presented mostly as a section-modulus shortcut and the governing-case logic is more heuristic than explicit. |
| `deepseek-v3.2` | 5 | 5 | 4 | 3 | 4 | 5 | 3 | Correct size and solid executable code, but the written eccentricity definitions are swapped and the narrative is less precise than the stronger entries. |

## Judge Output Summary

- Most models found the correct footing size of `3.0 m x 3.0 m`.
- The benchmark separated models on whether they clearly identified `LC2` as the governing selection case and explained why `2.9 m` fails due to `qmin = -0.410 kPa`.
- `gpt5.4-xhigh` was the strongest overall because it matched the reference mechanics closely, produced an executable notebook draft, and made the selection logic fully auditable.
- `glm-5.1:cloud` and `minimax-m2.7-cloud` were strong runner-ups.
- Main weaknesses observed across the field were wrong governing-case framing, unresolved placeholders in the final prose, weaker derivation, and slower-than-ideal response times.

## Manual Override Notes

- Scores were locked by manual engineering review plus direct execution of the calculation cells.
- Per user instruction, `qwen-3.6plus` was scored mainly on the underlying notebook content rather than being heavily penalized for the VS Code cell-wrapper export format.
- Latency was treated as a light secondary factor only. It influenced practical-usability scoring but did not override technical correctness.

## Winner

- Winner: `gpt5.4-xhigh`
- Difference size: `moderate`
- Why it matters in practice: Several models reached the correct `3.0 m` size, but the winner combined the best audit trail, the clearest explanation of the `2.9 m` no-uplift failure, correct governing-case framing, and clean executable notebook structure with the least manual rework.
