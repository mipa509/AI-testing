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

## Judge Output Summary

Manual anchor pass completed for all seven models.

Task summary: Re-run the old EC3 beam-check trap unchanged and compare whether models correct the wrong-axis and wrong-units defects, use a defensible major-axis modulus, and reach the right adequacy conclusion.

### September 2026 refresh

- Blind pack (one judging round): `gpt5.6-sol-xhigh` 4.83, `gpt5.6-luna-max` 4.67, `gpt5.4-xhigh` 4.67, `minimax-m2.7-cloud` 2.50.
- Both new models fixed the axis and unit faults, used the tabulated `Wpl,y = 353 cm3`, reached the correct cross-section `PASS` at utilisation 0.916 and added a proportionate LTB caveat without replacing the planted objective, matching the April `gpt5.4-xhigh` result.
- Sol additionally cross-checked `Mc,y,Rd` against the tabulated value, verified the low-shear condition and showed the LTB interpolation; Luna asserted its LTB figure without working. Both used web lookup, as the April `gpt5.4-xhigh` run did.

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

## Winner

- Winner: `gpt5.4-xhigh`
- Difference size: `Small over kimi-k2-thinking; moderate over qwen-3.6plus and gemma4:31b-cloud; large over glm-5.1:cloud, deepseek-v3.2, and minimax-m2.7-cloud.`
- Why it matters in practice: `On the corrected-engineering standard, GPT-5.4 is the cleanest anchor answer: it fixes the planted faults, uses the best section-property value, reaches the correct `PASS` result, and adds a well-scoped buckling caveat without drifting away from the task.`

September 2026 refresh: `gpt5.6-sol-xhigh` (overall mean 4.43) and `gpt5.6-luna-max` (4.29) do not beat the April result of `gpt5.4-xhigh` (4.43), so the winner line is unchanged.
