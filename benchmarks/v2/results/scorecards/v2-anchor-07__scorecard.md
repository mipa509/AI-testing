# Task Scorecard

- `task_id`: `v2-anchor-07`
- `task_title`: `Unchanged v1 EC3 planted-error trap test`
- `task_group`: `anchor`
- `judge_prompt_version`: `templates/judge_prompt_template.md`
- `manual_reviewer`: `Codex (anchor manual pass including qwen, minimax, and gpt5.4-xhigh extensions)`

## Scores

| Model | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Economics/practicality | Overall notes |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `gemma4:31b-cloud` | 4 | 5 | 3 | 4 | 4 | 4 | 4 | It caught the axis and unit trap, added a sensible buckling caution, and still landed on the correct `PASS` direction, though the chosen strong-axis modulus is not as good as the best section-property source. |
| `glm-5.1:cloud` | 3 | 5 | 3 | 4 | 5 | 5 | 4 | It fixes the planted axis and unit faults cleanly and adds an acceptable LTB caveat, but the chosen major-axis modulus drives the wrong final adequacy verdict. |
| `gpt5.4-xhigh` | 5 | 5 | 4 | 5 | 5 | 5 | 2 | Best revised anchor answer in the current set: it fixes axis and units, uses the best-matching major-axis modulus, reaches the right `PASS` result for the cross-section check, and adds a proportionate buckling warning. |
| `qwen-3.6plus` | 5 | 4 | 4 | 4 | 4 | 4 | 2 | Strong engineering correction: it fixes the axis and unit faults, uses a near-correct major-axis modulus, and reaches the right `PASS` outcome, but it loses auditability by narrating invented file/tool actions. |
| `minimax-m2.7-cloud` | 1 | 4 | 1 | 1 | 4 | 4 | 2 | Revised down sharply: it reaches `FAIL`, but via an implausibly low major-axis modulus and extra load-factor assumptions, so the logic is not trustworthy. |
| `kimi-k2-thinking` | 5 | 4 | 5 | 5 | 4 | 5 | 5 | Best all-round anchor answer on the revised standard: it fixes the axis and unit faults, uses a near-correct major-axis modulus, reaches the right `PASS` outcome, and adds a proportionate buckling warning. |
| `deepseek-v3.2` | 3 | 5 | 3 | 3 | 4 | 4 | 2 | It fixes the planted axis and unit faults, but like `glm` it uses a conservative major-axis modulus and therefore lands on the wrong final adequacy verdict. |
| `gpt5.6-sol-xhigh` | 5 | 5 | 5 | 5 | 4 | 5 | 2 | Finds both planted faults, cross-checks the corrected 97.08 kNm against the tabulated Mc,y,Rd, verifies the low-shear condition and shows the LTB interpolation, reaching the correct PASS at 0.916; the only blemish is an unused V_Ed in the corrected script. |
| `gpt5.6-luna-max` | 5 | 5 | 5 | 4 | 4 | 5 | 2 | Finds both planted faults, uses the correct tabulated Wpl,y = 353 cm3, reaches PASS at 0.916 and flags LTB, load factors and self-weight as caveats without replacing the objective, though its LTB figure is asserted without working. |
| `deepseek-v4.1-flash` | 3 | 2 | 4 | 3 | 4 | 3 | 2 | Reaches the correct corrected numbers (Wpl,y = 353 cm3, Mc,Rd = 97.08 kNm, utilisation 0.916) with a well-commented fix, but its headline verdict is not adequate on an LTB check the task did not pose, its narrative misdescribes the as-written code, and it asserts the planted 49.0 cm3 is the tabulated minor-axis value. |
| `glm-5.3-flash` | 4 | 4 | 4 | 4 | 4 | 4 | 2 | Finds both planted faults and reaches the correct cross-section PASS at utilisation 0.920 with restraint, shear and deflection stated as validity conditions, but uses Wpl,y = 351.5 cm3 instead of the tabulated 353, quotes a wrong minor-axis modulus of about 25.1 cm3, and repeats the prompt file's anchor header lines; no web lookup. |
| `tencent-hy4-preview` | 4 | 4 | 2 | 2 | 3 | 3 | 2 | Finds and explains both planted faults, uses the tabulated Wpl,y = 353 cm3 with a geometric cross-check and reaches the cross-section PASS, but headlines the verdict as not adequate on LTB and deflection checks the task did not pose, silently adds factored self-weight to the input load, and replaces the snippet with a full design script; web lookup appears to have been used. |
| `claude-fable-5.1-high` | 4.5 | 4.5 | 4 | 3.5 | 4 | 4 | 2 | Finds both planted faults, uses the tabulated Wpl,y = 353 cm3 with the full Blue Book property set, reaches the cross-section PASS at 0.92 and keeps the headline conditional on restraint (fails LTB at 2.83 if unrestrained over 6.2 m, with the working shown), but expands a snippet review into classification, shear, M_cr and an indicative deflection check built on assumed load factors that appears as Likely FAIL in the adequacy table, and the corrected script grows into a bending-plus-shear script. |
| `gemma4:26b-local` | 1 | 1 | 2 | 1 | 2 | 2 | 3 | Reaches PASS but by a wrong route: it never identifies the wrong-axis fault (keeps `Wpl_z` and calls the y/z notation interchangeable), replaces the planted value with a fabricated Wpl of about 440 cm3 attributed to the Blue Book (tabulated 353), so its 0.738 utilisation overstates capacity by a quarter; it misdescribes the original code as printing FAIL and as working because errors cancelled, treats the missing N.mm conversion as safer practice rather than a fault, and gives two different wrong values for M_Ed. |

## Judge Output Summary

Manual anchor pass completed for all seven models.

Task summary: Re-run the old EC3 beam-check trap unchanged and compare whether models correct the wrong-axis and wrong-units defects, use a defensible major-axis modulus, and reach the right adequacy conclusion.

### September 2026 refresh

- Blind pack (one judging round): `gpt5.6-sol-xhigh` 4.83, `gpt5.6-luna-max` 4.67, `gpt5.4-xhigh` 4.67, `minimax-m2.7-cloud` 2.50.
- Both new models fixed the axis and unit faults, used the tabulated `Wpl,y = 353 cm3`, reached the correct cross-section `PASS` at utilisation 0.916 and added a proportionate LTB caveat without replacing the planted objective, matching the April `gpt5.4-xhigh` result.
- Sol additionally cross-checked `Mc,y,Rd` against the tabulated value, verified the low-shear condition and showed the LTB interpolation; Luna asserted its LTB figure without working. Both used web lookup, as the April `gpt5.4-xhigh` run did.

### DeepSeek V4.1 Flash addendum (2026-09-18)

- Blind pack (one judging round, 2026-09-18): `gpt5.6-sol-xhigh` 5.00, `gpt5.4-xhigh` 4.33, `deepseek-v4.1-flash` 3.17, `minimax-m2.7-cloud` 2.17.
- DeepSeek V4.1 Flash reached the correct corrected numbers (`Wpl,y = 353 cm3`, `Mc,Rd = 97.08 kNm`, utilisation 0.916, Class 1 check, corrected script printing PASS) but led with the verdict that the section is not adequate because of an LTB check at about 2.9 utilisation that the task did not pose, which the judge treated as displacing the planted objective.
- Further deductions: the narrative misdescribes the as-written code (a phantom `1e6` divisor, 'prints FAIL' when it prints PASS at 6.6e-6, 'out by 10^3' against 10^6 in the body), it asserts the planted `49.0 cm3` is the tabulated minor-axis value (the tables give about 54.8), and the response carries the agent-mode tool trace plus unrequested workspace reads. Web lookups were attempted but blocked, so properties were quoted from memory.

### GLM 5.3 Flash addendum (2026-09-18)

- Blind pack (one judging round, 2026-09-18): `gpt5.6-sol-xhigh` 5.00, `gpt5.4-xhigh` 4.50, `glm-5.3-flash` 4.00, `minimax-m2.7-cloud` 2.00.
- GLM 5.3 Flash found both planted faults, corrected the axis and the N.mm to kN.m conversion, and reached the correct cross-section `PASS` at utilisation 0.920 with lateral restraint, shear and deflection stated as validity conditions rather than as a replacement problem.
- Deductions: `Wpl,y = 351.5 cm3` instead of the tabulated 353 (conservative, immaterial to the verdict), a wrong minor-axis modulus of about 25.1 cm3 (the tables give about 54.8), and a header that repeats the prompt file's historical-anchor framing lines; no web lookup was used.

### Tencent Hy4 Preview addendum (2026-09-18)

- Blind pack (one judging round, 2026-09-18): `gpt5.6-sol-xhigh` 5.00, `gpt5.4-xhigh` 4.67, `tencent-hy4-preview` 3.00, `minimax-m2.7-cloud` 2.00.
- Tencent Hy4 Preview found and explained both planted faults, including why they cancel, used the tabulated `Wpl,y = 353 cm3` with a geometric cross-check and reached the cross-section `PASS` at 0.933 after adding self-weight.
- Deductions: the headline verdict is NOT adequate on LTB and deflection checks the task did not pose, the input load is silently altered by adding factored self-weight (`M_Ed` 90.69 instead of 88.89 kNm) while treating 18.5 kN/m as a full ULS load, and the corrected code is a wholesale rewrite with a no-op shear-interaction line; the judge treated this as replacing the planted objective with a design study.

### Claude Fable 5.1 addendum (2026-09-19)

- Blind pack (one judging round, 2026-09-19): `gpt5.6-sol-xhigh` 4.83, `gpt5.4-xhigh` 4.67, `claude-fable-5.1-high` 4.33, `minimax-m2.7-cloud` 1.83.
- Claude Fable 5.1 found and corrected both planted faults with the tabulated `Wpl,y = 353 cm3` and the full Blue Book property set, reached the cross-section PASS at 0.92, and kept the headline conditional: adequate if the compression flange is fully restrained, failing LTB at 2.83 if unrestrained over 6.2 m, with `M_cr`, `chi_LT` and `M_b,Rd` worked and cross-checked against tabulated values.
- Deductions: the snippet review expands into classification, shear, a full LTB calculation and an indicative deflection check built on assumed load factors that appears as Likely FAIL in the adequacy table, the answer runs to three pages before the two-line fix, and the corrected script grows into a bending-plus-shear script with extra hard-coded geometry.

### Gemma 4 26B local addendum (2026-09-19)

- Blind pack (one judging round, 2026-09-19): `gpt5.6-sol-xhigh` 4.83, `gpt5.4-xhigh` 4.67, `minimax-m2.7-cloud` 2.50, `gemma4:26b-local` 1.50 on the six technical criteria; the judge ranked the local model last, below minimax, because minimax at least named both planted faults and described the original code correctly.
- Gemma 4 26B (local) saw that 49.0 cm3 is far too small for a 254x102x28 UB, added an explicit N.mm to kN.m conversion, and concluded PASS.
- Deductions: the wrong-axis fault is never identified (the corrected code keeps `Wpl_z`), the replacement Wpl of about 440 cm3 is not the tabulated 353 and is attributed to the SCI Blue Book without web access, so the 0.738 utilisation overstates capacity by 25 percent; the response says the original code prints FAIL at 13.5 kN.m (it prints PASS at 6.6e-6) and that it worked because the errors cancelled (nothing cancels); M_Ed is given as 88.76 and then 89.31 (it is 88.89); the unit fault is framed as safer practice.

## Manual Override Notes

Provisional `gemma4:31b-cloud` review:
- It correctly identified the wrong-axis and missing `1e6` conversion issues, so the core trap categories were recognised.
- It also adds a sensible LTB warning, which is good assistant behaviour rather than harmful drift.
- The main deduction is that the chosen strong-axis modulus (`324e3 mm3`) is still materially off the better section-property source, so it is not top-tier on corrected engineering fidelity.

Provisional `glm-5.1:cloud` review:
- It corrected both the use of `Wpl_z` and the missing `1e6` conversion, cited a plausible source, and presented the working clearly.
- The added LTB caveat is good judgement because it stays subordinate to the direct prompt objective.
- The main deduction is now correctness: with a better major-axis modulus the corrected answer should be about `M_Rd ≈ 97 kN.m` and therefore `PASS`, so `glm` reaches the wrong final adequacy verdict.

Provisional `qwen-3.6plus` review:
- It correctly identified the wrong-axis and missing `1e6` conversion faults, and its chosen `Wpl,y = 358e3 mm3` is close to the later Blue Book check (`~353 cm3`), so the underlying engineering path is much better than first scored.
- On the revised standard that is a strength, not a weakness: this property path leads to the right corrected adequacy conclusion of `PASS`.
- It also drifts operationally by narrating invented file creation and terminal execution, which hurts auditability and practicality.

Provisional `gpt5.4-xhigh` review:
- This is the strongest revised anchor answer in the set: it fixes the axis and unit issues, uses `Wpl,y = 353e3 mm3`, shows the corrected `M_Rd ≈ 97.1 kN.m`, and reaches the right cross-section verdict of `PASS`.
- It also adds the right kind of assistant behaviour beyond pure calculation: the LTB note is explicit, well-bounded, and does not replace the requested corrected cross-section check.
- Main deduction is only practical: this run was slower and more expensive than the best free/cloud anchor answers.

Provisional `minimax-m2.7-cloud` review:
- It correctly identified the wrong-axis and missing `1e6` conversion faults, but the corrected resistance path is not defensible: `Wpl_y = 106e3 mm3` is far away from the later Blue Book check (`~353 cm3`).
- That means the `FAIL` outcome is not strong evidence of a good anchor answer, because it is reached through a materially wrong section-property path plus added load-factor assumptions that were not requested.
- Operationally it was also one of the least practical anchor runs because the observed thinking/latency was unusually long.

Provisional `kimi-k2-thinking` review:
- It correctly identified the wrong-axis and wrong-units issues, and its chosen major-axis property value (`354e3 mm3`) is close to the later Blue Book check (`~353 cm3`).
- It also adds the most proportionate “real assistant” caveat in the set by warning about lateral-torsional buckling without replacing the task with a different design problem.
- On the revised standard this remains one of the best anchor answers: it fixes the two planted faults, uses a near-correct modulus, and reaches the right corrected `PASS` conclusion.

Provisional `deepseek-v3.2` review:
- Strong planted-error answer: it corrected the axis and unit issue, used the same major-axis modulus as `glm`, and concluded the section fails.
- The main revision is now stronger than that: with the better section-property source, this modulus drives the wrong final adequacy verdict, so the answer is no longer top-tier on correctness.
- Compared with `glm`, it is slightly less explicit on why the original property line is itself misleading, and the observed latency was worse.

### September 2026 refresh

- Scoring: technical criteria for `gpt5.6-sol-xhigh` and `gpt5.6-luna-max` were scored blind by a new judge alongside two April anchor responses, then shifted onto the April scale with a per-task offset of +0.08 derived from those anchors (see `benchmarks/refresh_2026-09_calibration.md`). The April rows above are unchanged.
- Manual overrides: none. The de-anonymised judgements were checked against the evaluator notes and no score was changed.
- Practicality `gpt5.6-sol-xhigh` = 2: 3 min 30 s with web lookup and about 85k tokens on the premium route, faster than April's `gpt5.4-xhigh` (4 min 38 s) but still the slowest and most expensive class of anchor answer, so scored as the April reference.
- Practicality `gpt5.6-luna-max` = 2: over 6 min 30 s and about 131k tokens, the slowest run in the whole refresh, despite the low list price.

### DeepSeek V4.1 Flash addendum (2026-09-18)

- Scoring: technical criteria for `deepseek-v4.1-flash` were scored blind on 2026-09-18 by the same judge family as the September refresh, in a pack with the same two April anchors plus `gpt5.6-sol-xhigh` as a consistency check, then shifted onto the April scale with the September per-task offset of +0.08 (user decision; see `benchmarks/addendum_2026-09-18_deepseek-v4.1-flash.md`). The April and September rows above are unchanged.
- Manual overrides: none. The judge's watch-out on the minor-axis modulus was checked: SCI P363 tabulates about 54.8 cm3 for `Wpl,z`, so the response's claim that the planted 49.0 value matches the tables is wrong and the deduction stands. The agent-mode tool trace was flagged to the judge as a capture feature and was not penalised as invented narration.
- Practicality `deepseek-v4.1-flash` = 2: about 15 min and 55k tokens, the slowest run in any round, with unrequested reads of the other task folders and blocked web lookups; the floor used in September for slow but usable runs, despite the near-zero cost (about $0.05).

### GLM 5.3 Flash addendum (2026-09-18)

- Scoring: technical criteria for `glm-5.3-flash` were scored blind on 2026-09-18 by the same judge family as the September refresh, in a pack with the same two April anchors plus `gpt5.6-sol-xhigh` as a consistency check. The anchors met the calibration gate (overall MAD 0.50, no row above 1.0), so the blind scores are used as-is with no offset (see `benchmarks/addendum_2026-09-18_glm-5.3-flash.md`). Earlier rows above are unchanged.
- Manual overrides: none. Checked against the evaluator notes: both planted faults are corrected and the verdict is the corrected `PASS`; the property slips (351.5 and about 25.1 cm3) are as the judge describes. The repeated header lines come from the task's `prompt.md`, which the agent read from the folder, not from evaluator material, and were not treated as contamination. No score was changed.
- Practicality `glm-5.3-flash` = 2: 10 min 34 s, the second-slowest anchor run after `deepseek-v4.1-flash`, no web lookup; the September floor for slow but usable runs, despite the near-zero cost (about $0.0065).

### Tencent Hy4 Preview addendum (2026-09-18)

- Scoring: technical criteria for `tencent-hy4-preview` were scored blind on 2026-09-18 by the same judge family as the September refresh, in a pack with the same two April anchors plus `gpt5.6-sol-xhigh` as a consistency check, then shifted onto the April scale with the September per-task offset of +0.08 (the standing user decision for packs that fail the calibration gate, as for `deepseek-v4.1-flash`; see `benchmarks/addendum_2026-09-18_tencent-hy4-preview.md`). Earlier rows above are unchanged.
- Manual overrides: none. Checked against the evaluator notes: both planted faults are corrected and the cross-section numbers are right; the verdict drift and the altered input load are as the judge describes and are exactly what the notes penalise. No score was changed.
- Practicality `tencent-hy4-preview` = 2: 12 min 50 s and about 65k tokens (about $0.115 billed), with web lookup; the September floor for slow but usable runs.

### Claude Fable 5.1 addendum (2026-09-19)

- Scoring: technical criteria for `claude-fable-5.1-high` (identity withheld from the orchestrator and the judge until scoring was complete, then disclosed) were scored blind on 2026-09-19 by the same judge family as the September refresh, in a pack with the same two April anchors plus `gpt5.6-sol-xhigh` as a consistency check, then shifted onto the April scale with the September per-task offset of +0.08 (the standing user decision for packs that fail the calibration gate, as for `deepseek-v4.1-flash` and `tencent-hy4-preview`; see `benchmarks/addendum_2026-09-19_claude-fable-5.1-high.md`). Earlier rows above are unchanged.
- Manual overrides: none. Checked against the evaluator notes: both planted faults are corrected, the cross-section and shear numbers and the `M_cr` chain were re-checked by hand, and the headline keeps the planted objective with the LTB failure stated as conditional on restraint; the deductions are for the assumed-load deflection row and the answer's scope, as the notes penalise. No score was changed.
- Practicality `claude-fable-5.1-high` = 2: 6 min 17 s API time, 9 min 32 s wall clock; the September floor for slow but usable runs on the anchor, as for every other premium and addendum model. Subscription run, so the $1.48 session figure is not counted. Practicality rule from this addendum on (user decision, 2026-09-19): cost is neglected for runs made on a subscription plan and counted only for API-billed runs; April and September rows are frozen and keep the earlier reading, under which premium models were scored as expensive whatever the route.

### Gemma 4 26B local addendum (2026-09-19)

- Scoring: technical criteria for `gemma4:26b-local` were scored blind on 2026-09-19 by the same judge family as the September refresh, in a pack with the two April anchors plus `gpt5.6-sol-xhigh` as a consistency check. Over the model's eight packs the anchors failed the calibration gate (MAD 0.59, worst row 1.17), so the blind scores are shifted with the September offset of +0.08, which leaves this row's integers unchanged (see `benchmarks/addendum_2026-09-19_gemma4-26b-local.md`). Earlier rows above are unchanged.
- Manual overrides: none. Checked against the evaluator notes and the snippet: the 440 cm3 value is not tabulated (353 cm3), the axis fault is unaddressed, and the claims about the original code's output are wrong; the judge's arithmetic checks were confirmed (18.5 x 6.2^2 / 8 = 88.89).
- Practicality `gemma4:26b-local` = 3: free local inference, no API cost, PowerShell terminal with no tools or web access; the user reports it answered promptly without looping. Latency and tokens not captured. The wrong property is a technical failure, not an operational one, so the free route keeps the April score given to `gemma4:31b-cloud` on this task. Cost is not a factor on this route under the rule adopted with the Claude Fable 5.1 addendum. Revised 2026-09-19 (batch): after the remaining tasks were judged, the model's eight-pack calibration failed the gate (MAD 0.59, worst row 1.17), so the standing September-offset rule now applies to every task, and the `ollama --verbose` timings on the later tasks (3 min 35 s to 7 min 32 s per answer) showed the route's latency, so practicality is 3 on every task on the latency-only reading.

### Claude Fable 5.1 addendum, two-judge mean (2026-09-19)

- Two-judge mean (user decision, 2026-09-19): after a judge from another family (GPT-6 Astra, xhigh, Codex) scored the same packs level or more lenient on every other response and lower on all three Fable responses, the user chose to record Fable's technical rows as the mean of the two judges. Each judge is first put on the April scale through its own anchors (judge 1: September per-task offset; judge 2: the offset from its own anchor rows), the two rows are averaged per criterion and recorded unrounded, so a 4.5 marks a criterion where the two judges differ by one point. Every other model keeps its single same-family judge. Full working in section 7 of the record.
- This task: judge 1 blind [5, 5, 4, 4, 4, 4] +0.08 -> [5, 5, 4, 4, 4, 4] (4.33); judge 2 blind [4, 4, 4, 3, 4, 4] +0.42 -> [4, 4, 4, 3, 4, 4] (3.83); recorded mean [4.5, 4.5, 4, 3.5, 4, 4] (4.08). Practicality unchanged at 2; overall 3.79 (was 4.00).

## Winner

- Winner: `gpt5.4-xhigh`
- Difference size: `Small over kimi-k2-thinking; moderate over qwen-3.6plus and gemma4:31b-cloud; large over glm-5.1:cloud, deepseek-v3.2, and minimax-m2.7-cloud.`
- Why it matters in practice: `On the corrected-engineering standard, GPT-5.4 is the cleanest anchor answer: it fixes the planted faults, uses the best section-property value, reaches the correct `PASS` result, and adds a well-scoped buckling caveat without drifting away from the task.`

September 2026 refresh: `gpt5.6-sol-xhigh` (overall mean 4.43) and `gpt5.6-luna-max` (4.29) do not beat the April result of `gpt5.4-xhigh` (4.43), so the winner line is unchanged.

DeepSeek V4.1 Flash addendum (2026-09-18): `deepseek-v4.1-flash` (overall mean 3.00) does not beat the April result of `gpt5.4-xhigh` (4.43), so the winner line is unchanged.

GLM 5.3 Flash addendum (2026-09-18): `glm-5.3-flash` (overall mean 3.71) does not beat the April result of `gpt5.4-xhigh` (4.43), so the winner line is unchanged.

Tencent Hy4 Preview addendum (2026-09-18): `tencent-hy4-preview` (overall mean 2.86) does not beat the April result of `gpt5.4-xhigh` (4.43), so the winner line is unchanged.

Claude Fable 5.1 addendum (2026-09-19): `claude-fable-5.1-high` (overall mean 3.79, two-judge mean; 4.00 on judge 1 alone)) does not beat the April result of `gpt5.4-xhigh` (4.43), so the winner line is unchanged.

Gemma 4 26B local addendum (2026-09-19): `gemma4:26b-local` (overall mean 1.71, revised the same day from 1.86) does not beat the April result of `gpt5.4-xhigh` (4.43), so the winner line is unchanged.
