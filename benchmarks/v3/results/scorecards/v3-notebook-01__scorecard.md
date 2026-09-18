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
| `gpt5.6-sol-xhigh` | 5 | 5 | 4 | 4 | 4 | 4 | 4 | Correct, executable and self-verified notebook (3.0 m, LC2 governing, 2.9 m rejected at qmin = -0.41 kPa) with all six sections, but it quotes the compact 6|M|/B^3 formula without derivation, gives no justification for the rigid linear model and never defines eccentricities; the copy-time loss of formatting was not penalised. |
| `gpt5.6-luna-max` | 3 | 3 | 4 | 4 | 4 | 4 | 3 | Narrative, closed-form equations and final answers are right and derived from N/A +/- M*y/I, but the coded point-pressure function uses 6*M*x/B^3 instead of 12*M*x/B^4, so its own consistency assert fails at the first candidate and the notebook does not run past code cell 3 (verified by execution). |
| `deepseek-v4.1-flash` | 5 | 5 | 5 | 5 | 5 | 5 | 3 | Correct, unit-suffixed, guarded notebook that runs end to end (verified by execution), selects 3.0 m with LC2 governing, explains the 2.9 m rejection and cross-checks against the kern rule; deductions in the blind pack only for loose cell alternation, a section-modulus rather than second-moment derivation, and length. |

## Judge Output Summary

- Most models found the correct footing size of `3.0 m x 3.0 m`.
- The benchmark separated models on whether they clearly identified `LC2` as the governing selection case and explained why `2.9 m` fails due to `qmin = -0.410 kPa`.
- `gpt5.4-xhigh` was the strongest overall because it matched the reference mechanics closely, produced an executable notebook draft, and made the selection logic fully auditable.
- `glm-5.1:cloud` and `minimax-m2.7-cloud` were strong runner-ups.
- Main weaknesses observed across the field were wrong governing-case framing, unresolved placeholders in the final prose, weaker derivation, and slower-than-ideal response times.

### September 2026 refresh

- Blind pack judged twice: `gpt5.4-xhigh` 4.83 in both rounds, `gpt5.6-sol-xhigh` 3.67 in both rounds, `gpt5.6-luna-max` 3.17 and 2.83, `gemma4:31b-cloud` 2.50 and 2.33.
- Sol selected `3.0 m` with `LC2` governing and its code runs end to end (verified by execution), but it quotes the compact pressure formula without the requested derivation, gives no justification for the rigid linear model and never defines eccentricities.
- Luna's Markdown derivation and conclusions are correct, but its `pressure_at_point()` uses `6*M*x/B^3` instead of `12*M*x/B^4`, so its own consistency assert fails at the first candidate and the notebook does not run past code cell 3 (verified by execution). Neither new model chose `2.9 m`.

### DeepSeek V4.1 Flash addendum (2026-09-18)

- Blind pack (one judging round, 2026-09-18): `gpt5.4-xhigh` 4.83, `deepseek-v4.1-flash` 4.83, `gpt5.6-sol-xhigh` 3.67, `gemma4:31b-cloud` 2.83; the judge ranked `gpt5.4-xhigh` first and DeepSeek second on cell structure and derivation path, calling the gap presentational.
- DeepSeek V4.1 Flash selected `3.0 m` with `LC2` governing through no-uplift, explained the `2.9 m` rejection at `qmin = -0.41 kPa`, cross-checked the no-uplift criterion against the kern rule `e_x + e_y <= B/6`, and its six code cells run end to end (verified by execution).
- Deductions: cell alternation is loose (three Markdown cells then four code cells), the derivation goes through `S = B^3/6` rather than `I = B^4/12`, and the draft is long for a preliminary sizing note.

## Manual Override Notes

- Scores were locked by manual engineering review plus direct execution of the calculation cells.
- Per user instruction, `qwen-3.6plus` was scored mainly on the underlying notebook content rather than being heavily penalized for the VS Code cell-wrapper export format.
- Latency was treated as a light secondary factor only. It influenced practical-usability scoring but did not override technical correctness.

### September 2026 refresh

- Scoring: technical criteria for `gpt5.6-sol-xhigh` and `gpt5.6-luna-max` were scored blind by a new judge alongside two April anchor responses, then shifted onto the April scale with a per-task offset of +0.71 derived from those anchors (see `benchmarks/refresh_2026-09_calibration.md`). The April rows above are unchanged.
- Manual overrides: none. The judges' executability findings were verified by running each new model's code cells in order with standard-library Python: Sol runs end to end and selects `3.0 m` with `LC2` governing; Luna stops with `AssertionError` at code cell 4 because its point-pressure formula disagrees with its own closed form.
- Practicality `gpt5.6-sol-xhigh` = 4: latency not captured, about 23k tokens, notebook runs end to end; scored as the April `gpt5.4-xhigh` reference.
- Practicality `gpt5.6-luna-max` = 3: about 4 minutes, and the notebook needs a one-line formula fix before it runs; matches the April scores given for long think time alone.

### DeepSeek V4.1 Flash addendum (2026-09-18)

- Scoring: technical criteria for `deepseek-v4.1-flash` were scored blind on 2026-09-18 by the same judge family as the September refresh, in a pack with the same two April anchors plus `gpt5.6-sol-xhigh` as a consistency check, then shifted onto the April scale with the September per-task offset of +0.71 (user decision; see `benchmarks/addendum_2026-09-18_deepseek-v4.1-flash.md`). The April and September rows above are unchanged.
- Manual overrides: none. The judge's executability reading was verified by running the six fenced code cells in order with standard-library Python: the notebook runs end to end, selects `3.0 m`, names `LC2` and reports `2.9 m` rejected at `-0.410 kPa`.
- Practicality `deepseek-v4.1-flash` = 3: 4 min 15 s and about 59k tokens, inflated by reading the other task folders unasked, with a notebook that runs end to end (about $0.04 billed); matches the September score for `gpt5.6-luna-max` at similar latency.

## Winner

- Winner: `gpt5.4-xhigh`
- Difference size: `moderate`
- Why it matters in practice: Several models reached the correct `3.0 m` size, but the winner combined the best audit trail, the clearest explanation of the `2.9 m` no-uplift failure, correct governing-case framing, and clean executable notebook structure with the least manual rework.

September 2026 refresh: `gpt5.6-sol-xhigh` (overall mean 4.29) and `gpt5.6-luna-max` (3.57) do not beat the April result of `gpt5.4-xhigh` (4.86), so the winner line is unchanged.

DeepSeek V4.1 Flash addendum (2026-09-18): `deepseek-v4.1-flash` (overall mean 4.71) does not beat the April result of `gpt5.4-xhigh` (4.86), so the winner line is unchanged.
