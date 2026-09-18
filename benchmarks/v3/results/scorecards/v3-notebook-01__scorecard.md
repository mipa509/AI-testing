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
| `glm-5.3-flash` | 4 | 4 | 4 | 5 | 4 | 4 | 3 | Fullest written treatment among the addendum models (derivation via S = B^3/6, model justification, eccentricity directions, a full candidate sweep) and a Markdown conclusion of 3.0 m with LC2 governing, but its code prints LC3 as the governing case, contradicting the text (verified by execution), and its middle-third equivalence claim is wrong for biaxial loading. |
| `tencent-hy4-preview` | 5 | 5 | 5 | 5 | 5 | 5 | 3 | Fully correct and executable (3.0 m, LC2 governing through uplift, 2.9 m rejected at -0.410 kPa) with an explicit M*c/I derivation, exact-fraction arithmetic, all four corner pressures and closed-form minimum-width bounds; ranked first in its blind pack, with deductions only for defining e_x = Mx/N and e_y = My/N (the reverse of the reference convention), a swapped second-moment subscript in the stated field equation, and length. |
| `claude-fable-5.1-high` | 5 | 5 | 5 | 5 | 5 | 5 | 3 | Fully correct and executable (3.0 m, LC2 governing through uplift, 2.9 m rejected at -0.4 kPa; six code cells run end to end, verified by execution) with a Navier derivation from N/A + M*y/I, the kern validity limit, eccentricities defined as in the reference, a hand-check cell, a full pass/fail matrix with failure-type flags, a closed-form minimum-width cross-check (2.914 m) and reviewer commentary on the thin uplift margin and self-weight direction; ranked first in its blind pack, with only length, a SystemExit idiom and some loosely placed code citations noted against it. |
| `gemma4:26b-local` | 2 | 2 | 3 | 4 | 3 | 3 | 3 | Correct hand derivation of the corner pressure from N/A +/- M*c/I, but the delivered notebook does not run (a non-breaking space inside the LC1 load literal is a SyntaxError in cell 1) and, with that character removed, scales the candidate widths twice to 0.24 to 0.32 m so no size is ever selected; the written conclusion states 2.9 m with LC1 governing by highest q_max, the trap answer the task is built around, and sections 2 and 3 are missing. |

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

### GLM 5.3 Flash addendum (2026-09-18)

- Blind pack (one judging round, 2026-09-18): `gpt5.4-xhigh` 5.00, `gpt5.6-sol-xhigh` 4.33, `glm-5.3-flash` 4.17, `gemma4:31b-cloud` 2.67; the judge ranked GLM third, below Sol, on the grounds that an internally consistent notebook with omissions is preferable to one that contradicts itself.
- GLM 5.3 Flash met every analysis-note requirement (derivation via `S = B^3/6`, model justification, `e_x` and `e_y` directions, a full candidate sweep printing `qmax` and `qmin` for every case) and its Markdown selects `3.0 m` with `LC2` governing and explains the `2.9 m` rejection; the four code cells run end to end (verified by execution).
- Deductions: Code Cell 4 defines the governing case as the highest `qmax / q_allow` and prints `LC3`, contradicting the Markdown conclusion, and the claim that keeping each eccentricity within `B/6` is exactly equivalent to `qmin >= 0` is wrong for biaxial loading (the condition is `6e_x/B + 6e_y/B <= 1`), so the conclusion's middle-third explanation of the 2.9 m failure is incorrect.

### Tencent Hy4 Preview addendum (2026-09-18)

- Blind pack (one judging round, 2026-09-18): `tencent-hy4-preview` 4.83, `gpt5.4-xhigh` 4.50, `gpt5.6-sol-xhigh` 3.50, `gemma4:31b-cloud` 2.67; the judge ranked Hy4 first as the stronger audit document.
- Tencent Hy4 Preview derived the corner pressure from `M*c/I` with `I = B^4/12`, used exact-fraction arithmetic, evaluated all four corners, added closed-form minimum-width bounds per case, selected `3.0 m` with `LC2` governing through uplift and explained the `2.9 m` rejection at `-0.410 kPa`; the five code cells run end to end (verified by execution).
- Deductions: it defines `e_x = Mx/N` and `e_y = My/N`, the reverse of the reference convention, so its eccentricity columns are swapped relative to the reference table; the stated pressure field pairs each moment with the wrong second-moment subscript (harmless for a square); and the draft is long for the task.

### Claude Fable 5.1 addendum (2026-09-19)

- Blind pack (one judging round, 2026-09-19): `claude-fable-5.1-high` 5.00, `gpt5.4-xhigh` 4.67, `gpt5.6-sol-xhigh` 3.50, `gemma4:31b-cloud` 2.50; the judge ranked the new model first as the stronger audit document.
- Claude Fable 5.1 derived the corner pressure from `q = N/A + Mx*y/Ix + My*x/Iy` with the kern validity limit, defined `ex = My/N` and `ey = Mx/N` as in the reference, added a hand-check cell, printed a full pass/fail matrix with failure-type flags for every width and case, cross-checked the search against a closed-form minimum width (2.914 m for LC2), selected `3.0 m` with `LC2` governing through uplift and `LC3` for bearing, and discussed the thin 2.2 kPa uplift margin and the direction of the self-weight effect; the six code cells run end to end (verified by execution).
- Noted against it, without a score deduction: length well beyond what the brief needs, some loosely placed code citations (EN 1997-1 6.5.2, Annex D commentary), a `raise SystemExit` idiom in a notebook cell, and absolute moments that cannot report which corner governs for signed inputs.

### Gemma 4 26B local addendum (2026-09-19)

- Blind pack (one judging round, 2026-09-19): `gpt5.4-xhigh` 5.00, `gpt5.6-sol-xhigh` 4.33, `gemma4:31b-cloud` 3.33, `gemma4:26b-local` 1.83 on the six technical criteria; the judge ranked the local model last.
- Gemma 4 26B (local) derived the corner pressure correctly from axial plus bending stress with I = B^4/12 and c = B/2, stated a compression-positive sign convention and an exclusions list, and its search loop tests both criteria.
- Deductions: the delivered code does not run (a non-breaking space in the LC1 load literal is a SyntaxError), the candidate list is scaled twice to 0.24 to 0.32 m so even a repaired cell 1 selects nothing, the governing case is tracked by the largest q_max over every width, the conclusion states 2.9 m with LC1 governing, the trap answer, hedged as depending on execution, and the Input data and calculation-cell sections are missing; no sweep output, no explanation of any rejected width, no eccentricity definitions.

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

### GLM 5.3 Flash addendum (2026-09-18)

- Scoring: technical criteria for `glm-5.3-flash` were scored blind on 2026-09-18 by the same judge family as the September refresh, in a pack with the same two April anchors plus `gpt5.6-sol-xhigh` as a consistency check. The anchors met the calibration gate (overall MAD 0.50, no row above 1.0), so the blind scores are used as-is with no offset (see `benchmarks/addendum_2026-09-18_glm-5.3-flash.md`). Earlier rows above are unchanged.
- Manual overrides: none. The judge's reading was verified by running the four fenced code cells in order with standard-library Python: the notebook runs end to end, selects `3.0 m`, and prints `Governing case (highest qmax/q_allow): LC3`, contradicting the Markdown's `LC2`. No score was changed.
- Practicality `glm-5.3-flash` = 3: 5 min 56 s and about 35k tokens (about $0.0094 billed) with a notebook that runs end to end but prints a governing case that contradicts its own conclusion; matches the September score for `gpt5.6-luna-max`.

### Tencent Hy4 Preview addendum (2026-09-18)

- Scoring: technical criteria for `tencent-hy4-preview` were scored blind on 2026-09-18 by the same judge family as the September refresh, in a pack with the same two April anchors plus `gpt5.6-sol-xhigh` as a consistency check, then shifted onto the April scale with the September per-task offset of +0.71 (the standing user decision for packs that fail the calibration gate, as for `deepseek-v4.1-flash`; see `benchmarks/addendum_2026-09-18_tencent-hy4-preview.md`). Earlier rows above are unchanged.
- Manual overrides: none. The judge's reading was verified by running the five fenced code cells in order with standard-library Python: the notebook runs end to end, selects `3.0 m`, and prints `LC2` for no-uplift and `LC3` for bearing utilisation. The reversed eccentricity naming is stated and applied consistently, so it stays a unit-and-assumption deduction. No score was changed.
- Practicality `tencent-hy4-preview` = 3: 3 min 18 s and about 43k tokens (about $0.128 billed) with a notebook that runs end to end; scored as the other addendum models on this task.

### Claude Fable 5.1 addendum (2026-09-19)

- Scoring: technical criteria for `claude-fable-5.1-high` (identity withheld from the orchestrator and the judge until scoring was complete, then disclosed) were scored blind on 2026-09-19 by the same judge family as the September refresh, in a pack with the same two April anchors plus `gpt5.6-sol-xhigh` as a consistency check, then shifted onto the April scale with the September per-task offset of +0.71 (the standing user decision for packs that fail the calibration gate, as for `deepseek-v4.1-flash` and `tencent-hy4-preview`; see `benchmarks/addendum_2026-09-19_claude-fable-5.1-high.md`). Earlier rows above are unchanged.
- Manual overrides: none. The judge's reading was verified by running the six fenced code cells in order with standard-library Python: the notebook runs end to end, selects `3.0 m`, prints `LC2` for uplift and `LC3` for bearing, and both internal asserts pass. No score was changed.
- Practicality `claude-fable-5.1-high` = 3: 6 min 20 s API time, 11 min 16 s wall clock (the longest v3 run recorded) with a notebook that runs end to end; scored on latency alone as the 2026-09-18 addendum models and `gpt5.6-luna-max` at three to six minutes, rather than the 4 given to the April premium reference, whose latency was not a factor. Subscription run, so the $2.65 session figure is not counted. Practicality rule from this addendum on (user decision, 2026-09-19): cost is neglected for runs made on a subscription plan and counted only for API-billed runs; April and September rows are frozen and keep the earlier reading, under which premium models were scored as expensive whatever the route.

### Gemma 4 26B local addendum (2026-09-19)

- Scoring: technical criteria for `gemma4:26b-local` were scored blind on 2026-09-19 by the same judge family as the September refresh, in a pack with the two April anchors (`gpt5.4-xhigh`, `gemma4:31b-cloud`) plus `gpt5.6-sol-xhigh` as a consistency check. The anchors met the gate on this pack alone (MAD 0.17), but over the model's eight packs the gate failed (MAD 0.59, worst row 1.17), so the blind scores [1, 1, 2, 3, 2, 2] are shifted with the September offset of +0.71 to [2, 2, 3, 4, 3, 3], the standing rule; revised the same day from the as-is row first recorded (see `benchmarks/addendum_2026-09-19_gemma4-26b-local.md`). Earlier rows above are unchanged.
- Manual overrides: none. The judge's reading was verified by execution with standard-library Python: cell 1 fails with `SyntaxError: invalid non-printable character U+00A0`; with that character removed, the three cells run and print `No suitable size found in range` because the widths are 0.24 to 0.32 m. The judge's numbers (q_axial at 0.2 m, LC3 as the tracked case) were confirmed.
- Practicality `gemma4:26b-local` = 3: free local inference on the user's own hardware, no API cost, run from a plain terminal with no tools; latency and token counts not captured. The free route would score 4 to 5 under April's principle, but the delivered notebook needs two code fixes before it runs at all, so it is scored as `gpt5.6-luna-max` was for a notebook that stops on its own code (3). Cost is not a factor on this route under the rule adopted with the Claude Fable 5.1 addendum. Revised 2026-09-19 (batch): after the remaining tasks were judged, the model's eight-pack calibration failed the gate (MAD 0.59, worst row 1.17), so the standing September-offset rule now applies to every task, and the `ollama --verbose` timings on the later tasks (3 min 35 s to 7 min 32 s per answer) showed the route's latency, so practicality is 3 on every task on the latency-only reading.

## Winner

- Winner: `gpt5.4-xhigh`
- Difference size: `moderate`
- Why it matters in practice: Several models reached the correct `3.0 m` size, but the winner combined the best audit trail, the clearest explanation of the `2.9 m` no-uplift failure, correct governing-case framing, and clean executable notebook structure with the least manual rework.

September 2026 refresh: `gpt5.6-sol-xhigh` (overall mean 4.29) and `gpt5.6-luna-max` (3.57) do not beat the April result of `gpt5.4-xhigh` (4.86), so the winner line is unchanged.

DeepSeek V4.1 Flash addendum (2026-09-18): `deepseek-v4.1-flash` (overall mean 4.71) does not beat the April result of `gpt5.4-xhigh` (4.86), so the winner line is unchanged.

GLM 5.3 Flash addendum (2026-09-18): `glm-5.3-flash` (overall mean 4.00) does not beat the April result of `gpt5.4-xhigh` (4.86), so the winner line is unchanged.

Tencent Hy4 Preview addendum (2026-09-18): `tencent-hy4-preview` (overall mean 4.71) does not beat the April result of `gpt5.4-xhigh` (4.86), so the winner line is unchanged.

Claude Fable 5.1 addendum (2026-09-19): `claude-fable-5.1-high` (overall mean 4.71) does not beat the April result of `gpt5.4-xhigh` (4.86), so the winner line is unchanged.

Gemma 4 26B local addendum (2026-09-19): `gemma4:26b-local` (overall mean 2.86, revised the same day from 2.00) does not beat the April result of `gpt5.4-xhigh` (4.86), so the winner line is unchanged.
