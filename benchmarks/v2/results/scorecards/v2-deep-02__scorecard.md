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
| `gpt5.6-sol-xhigh` | 5 | 4 | 5 | 4 | 4 | 5 | 3 | Found all three planted blockers with a full dimensional derivation plus a well-argued extra finding on the unused combination label, but its line references do not match the supplied files and it rated the under-factored imposed load only High. |
| `gpt5.6-luna-max` | 5 | 5 | 5 | 4 | 4 | 4 | 3 | Found all three planted blockers with a correct worked numeric example and useful notes on the combination label and package imports, though its finding-1 fix direction (psi factors, combination as input) over-reaches the minimum fix. |
| `deepseek-v4.1-flash` | 4 | 5 | 4 | 3 | 4 | 4 | 3 | Found all three planted blockers with correct numeric examples and the strongest not-escalated section, but it over-escalates rounding to High, infers SLS rows from the combination label, wrongly claims the two numeric errors mask each other, and runs to three times the requested length. |
| `glm-5.3-flash` | 4 | 4 | 4 | 4 | 4 | 4 | 3 | Found all three planted blockers with good numeric examples, but it asserts an unconservative rounding path (1.004 rounding to PASS) that cannot occur under the code's strict less-than test and rates rounding High on that basis, offers reverse=True on a one-row return as the primary reporting fix, and is the longest of the responses judged. |
| `tencent-hy4-preview` | 5 | 5 | 3 | 4 | 4 | 4 | 3 | Found all three planted blockers with correct worked numbers and was the only response in its pack to explain that the two arithmetic errors act in opposite directions, but it runs far beyond the short high-signal brief, proposes minimum fixes that are not minimum (a mandatory section-class key, a new row schema, packaging rework) and rests some findings on assumptions the three supplied files cannot support. |
| `anon-2026-09-19` | 5 | 5 | 4 | 5 | 5 | 4 | 2 | Found all three planted blockers and verified them with a fully correct worked example (25.5 vs 21.5 kN/m, 521.9 vs 0.522 kNm), and was the only response in its pack to explain that the two arithmetic errors pull in opposite directions so a partial fix is more dangerous than the current state; ranked first in the pack, with deductions for running past the short high-signal brief, grading the unused combination label High on inference, and two later findings that drift from minimum fixes into design recommendations. |

## Judge Output Summary

Manual comparative pass completed for all seven models.

Task summary: Review a steel beam ULS screening package for unit conversion, load combination, and reporting integrity defects before release.

### September 2026 refresh

- Blind pack (one judging round): `gpt5.4-xhigh` 4.67, then `gpt5.6-sol-xhigh` and `gpt5.6-luna-max` tied at 4.50, with `minimax-m2.7-cloud` at 2.33.
- All three top responses found the missing 1.50 imposed-load factor, the cm3-as-mm3 resistance error and the review table that returns only the least-utilised row; the judge called the differences among them second-order.
- Sol lost points for line references that do not match the supplied files and for rating the under-factored load only High; Luna for a finding-1 fix direction (psi factors, combination as input) beyond the minimum fix.

### DeepSeek V4.1 Flash addendum (2026-09-18)

- Blind pack (one judging round, 2026-09-18): `gpt5.4-xhigh` 4.50, `gpt5.6-sol-xhigh` 4.33, `deepseek-v4.1-flash` 4.00, `minimax-m2.7-cloud` 2.33 on the six technical criteria.
- DeepSeek V4.1 Flash found all three planted blockers (unused `ULS_GAMMA_Q`, `1e6` instead of `1e3`, ascending sort plus `[:1]`) with correct numeric examples and the strongest deliberately-not-escalated section; the judge said any of the top three responses would lead a maintainer to the same fixes.
- Deductions: rounding-before-status escalated to High, an SLS-rows inference from the `combination` label presented as fact, a wrong claim that the two numeric errors mask each other, a float-equality test suggestion, and about three times the requested length.

### GLM 5.3 Flash addendum (2026-09-18)

- Blind pack (one judging round, 2026-09-18): `gpt5.4-xhigh` 4.83, `gpt5.6-sol-xhigh` 4.33, `glm-5.3-flash` 4.00, `minimax-m2.7-cloud` 2.50 on the six technical criteria.
- GLM 5.3 Flash found all three planted blockers (`1e6` instead of `1e3`, unused `ULS_GAMMA_Q`, ascending sort plus `[:1]`) with good numeric examples; the judge said none of the top three responses would lead to an unsafe merge.
- Deductions: it asserts an unconservative rounding path (1.004 rounding to PASS) that cannot occur under the code's strict `< 1.0` test and rates rounding High on that basis, offers `reverse=True` on a one-row return as the primary reporting fix, and is the longest of the four responses.

### Tencent Hy4 Preview addendum (2026-09-18)

- Blind pack (one judging round, 2026-09-18): `gpt5.6-sol-xhigh` 4.83, `gpt5.4-xhigh` 4.33, `tencent-hy4-preview` 4.17, `minimax-m2.7-cloud` 2.50 on the six technical criteria.
- Tencent Hy4 Preview found all three planted blockers with correct worked numbers and was the only response in the pack to explain that the two arithmetic errors act in opposite directions; the judge called it technically the deepest review.
- Deductions, mainly on change safety: far longer than the short high-signal brief, minimum fixes that are not minimum (a mandatory section-class key that would break callers, a new row schema, packaging rework), and assumptions about tests and import layout that the three supplied files cannot support.

### Anonymous model addendum (2026-09-19)

- Blind pack (one judging round, 2026-09-19): `anon-2026-09-19` 4.67, `gpt5.6-sol-xhigh` 4.50, `gpt5.4-xhigh` 4.33, `minimax-m2.7-cloud` 2.33 on the six technical criteria; the judge ranked the new model first.
- The anonymous model found all three planted blockers, verified them with a worked example the judge re-computed without finding an error (25.5 vs 21.5 kN/m, 114.8 vs 96.8 kNm, 521.9 vs 0.522 kNm), and was the only response in its pack to explain that the two arithmetic errors act in opposite directions, so fixing only the loud unit error would ship a PASS on the safest member computed with an unconservative load.
- Deductions on change safety and clarity: seven findings plus an interaction section and a release gate exceed the short high-signal brief, the unused combination label is graded High on inference about inputs the files do not show, and findings 6 (gamma_M0 and class guard) and 7 (provenance columns) drift from minimum fixes into design recommendations.

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

### September 2026 refresh

- Scoring: technical criteria for `gpt5.6-sol-xhigh` and `gpt5.6-luna-max` were scored blind by a new judge alongside two April anchor responses, then shifted onto the April scale with a per-task offset of +0.42 derived from those anchors (see `benchmarks/refresh_2026-09_calibration.md`). The April rows above are unchanged.
- Manual overrides: none. The de-anonymised judgements were checked against the evaluator notes and no score was changed.
- Practicality `gpt5.6-sol-xhigh` = 3: same premium Codex route as `gpt5.4-xhigh`, faster on every task with a recorded time, no refusal or truncation, waited for context; scored as the April premium reference.
- Practicality `gpt5.6-luna-max` = 3: same Codex route on the budget API tier ($0.20 / $1.20 per 1M tokens list price), about 3 to 4 minutes per v2 task, no refusal or truncation, waited for context; low price offset by the slowest latency in the set.

### DeepSeek V4.1 Flash addendum (2026-09-18)

- Scoring: technical criteria for `deepseek-v4.1-flash` were scored blind on 2026-09-18 by the same judge family as the September refresh, in a pack with the same two April anchors plus `gpt5.6-sol-xhigh` as a consistency check, then shifted onto the April scale with the September per-task offset of +0.42 (user decision; see `benchmarks/addendum_2026-09-18_deepseek-v4.1-flash.md`). The April and September rows above are unchanged.
- Manual overrides: none. The de-anonymised judgement was checked against the evaluator notes; all three planted findings are present and no score was changed.
- Practicality `deepseek-v4.1-flash` = 3: 2 min 45 s and about 35k tokens on a cheap paid API route (about $0.0135 billed through OpenRouter), no refusal or truncation, followed the instruction to read only the task folder; scored as `gpt5.6-luna-max` on this task.

### GLM 5.3 Flash addendum (2026-09-18)

- Scoring: technical criteria for `glm-5.3-flash` were scored blind on 2026-09-18 by the same judge family as the September refresh, in a pack with the same two April anchors plus `gpt5.6-sol-xhigh` as a consistency check. The anchors met the calibration gate (overall MAD 0.50, no row above 1.0), so the blind scores are used as-is with no offset (see `benchmarks/addendum_2026-09-18_glm-5.3-flash.md`). Earlier rows above are unchanged.
- Manual overrides: none. The de-anonymised judgement was checked against the evaluator notes and the supplied code: `round(1.004, 2) < 1.0` is False, so the judge's point stands; all three planted findings are present and no score was changed.
- Practicality `glm-5.3-flash` = 3: 4 min 30 s and about 33k tokens on a cheap paid API route (about $0.012 billed through OpenRouter), no refusal or truncation, followed the instruction to read only the task folder and wrote the review file as asked; as `gpt5.6-luna-max` and `deepseek-v4.1-flash` on this task.

### Tencent Hy4 Preview addendum (2026-09-18)

- Scoring: technical criteria for `tencent-hy4-preview` were scored blind on 2026-09-18 by the same judge family as the September refresh, in a pack with the same two April anchors plus `gpt5.6-sol-xhigh` as a consistency check, then shifted onto the April scale with the September per-task offset of +0.42 (the standing user decision for packs that fail the calibration gate, as for `deepseek-v4.1-flash`; see `benchmarks/addendum_2026-09-18_tencent-hy4-preview.md`). Earlier rows above are unchanged.
- Manual overrides: none. The de-anonymised judgement was checked against the evaluator notes; all three planted findings are present and the worked numbers are right. No score was changed.
- Practicality `tencent-hy4-preview` = 3: 1 min 59 s and about 37k tokens (about $0.094 billed through OpenRouter) on a mid-tier paid route about seven times the flash models' list price, no refusal or truncation; the fastest addendum run on this task, scored as the other paid-API models.

### Anonymous model addendum (2026-09-19)

- Scoring: technical criteria for `anon-2026-09-19` (a placeholder id; the model's identity was withheld from the orchestrator and the judge until scoring was complete) were scored blind on 2026-09-19 by the same judge family as the September refresh, in a pack with the same two April anchors plus `gpt5.6-sol-xhigh` as a consistency check, then shifted onto the April scale with the September per-task offset of +0.42 (the standing user decision for packs that fail the calibration gate, as for `deepseek-v4.1-flash` and `tencent-hy4-preview`; see `benchmarks/addendum_2026-09-19_anon-2026-09-19.md`). Earlier rows above are unchanged.
- Manual overrides: none. The de-anonymised judgement was checked against the evaluator notes; all three planted findings are present and the worked table was re-computed. No score was changed.
- Practicality `anon-2026-09-19` = 2: 4 min 14 s API time, 6 min 11 s wall clock and $1.29 session cost on a premium agentic CLI route, no refusal or truncation; slower than every other premium run on this task and the most expensive recorded, so scored as April scored `gpt5.4-xhigh` here (slower and less economical than the best free or cloud answers).

## Winner

- Winner: `gemma4:31b-cloud`
- Difference size: `Very small over gpt5.4-xhigh`
- Why it matters in practice: `Gemma and gpt5.4 both produced top-tier task-2 reviews, but gemma still has the stronger practicality/economics profile for repeated use on this kind of repo review.`

September 2026 refresh: `gpt5.6-sol-xhigh` (overall mean 4.29) and `gpt5.6-luna-max` (4.29) do not beat the April result of `gemma4:31b-cloud` (4.71), so the winner line is unchanged.

DeepSeek V4.1 Flash addendum (2026-09-18): `deepseek-v4.1-flash` (overall mean 3.86) does not beat the April result of `gemma4:31b-cloud` (4.71), so the winner line is unchanged.

GLM 5.3 Flash addendum (2026-09-18): `glm-5.3-flash` (overall mean 3.86) does not beat the April result of `gemma4:31b-cloud` (4.71), so the winner line is unchanged.

Tencent Hy4 Preview addendum (2026-09-18): `tencent-hy4-preview` (overall mean 4.00) does not beat the April result of `gemma4:31b-cloud` (4.71), so the winner line is unchanged.

Anonymous model addendum (2026-09-19): `anon-2026-09-19` (overall mean 4.29) does not beat the April result of `gemma4:31b-cloud` (4.71), so the winner line is unchanged.
