# Gemma 4 26B (local) addendum (2026-09-19): blind scoring record

Scope: `gemma4:26b-local` (Ollama `gemma4:26b`, run locally on the user's machine from a plain terminal, no harness, tools or skills) on all eight tasks, run in the order `v3-notebook-01`, `v2-deep-02` (section 6), `v2-anchor-07` (section 7) and the remaining five v2 tasks (section 8), as a free-tier comparison point. Section 8 revises the calibration decision and the practicality scores of the first three tasks; the figures in sections 3 to 7 are as first recorded. The method is the September 2026 refresh procedure (`refresh_2026-09_calibration.md`) as applied to the 2026-09-18 and 2026-09-19 addenda. No earlier score, note or winner was changed. This is a different model from the April `gemma4:31b-cloud` row (Ollama cloud, 31B), which is the low anchor in this pack.

## 1. Run

One run on 2026-09-19, `ollama run gemma4:26b` in a terminal, prompt pasted as one message, response copied from the terminal. The terminal wrapped long lines and rendered a non-breaking space inside the LC1 load literal as `<0xA0>`; the raw output keeps the wrapping and restores the U+00A0 character. Latency, token counts and cost were not captured (free local inference). For future local runs `ollama run <model> --verbose` prints duration and token counts after each reply.

## 2. Blind pack

Four responses: the new model, the April high anchor `gpt5.4-xhigh`, the April low anchor `gemma4:31b-cloud` and `gpt5.6-sol-xhigh` as a same-judge-family consistency check; same pack contents and judge instructions as the other addenda, new seed. A neutral line above the new response says line wrapping was introduced by the terminal copy. Judge: a Claude Fable 5.1 subagent reading only the pack. Identity-word scan: no hits.

| Task | Seed | A | B | C | D |
|---|---:|---|---|---|---|
| `v3-notebook-01` | 20261409 | `gemma4:26b-local` | `gemma4:31b-cloud` | `gpt5.4-xhigh` | `gpt5.6-sol-xhigh` |

## 3. Calibration

| Task | Low anchor | High anchor MAD / signed | Low anchor MAD / signed | Anchor order preserved? | Sol vs Sept blind MAD / signed |
|---|---|---:|---:|---|---:|
| `v3-notebook-01` | `gemma4:31b-cloud` | 0.00 / +0.00 | 0.33 / -0.33 | yes (April 5.00 vs 3.67; blind 5.00 vs 3.33) | 0.67 / +0.67 |

Anchor MAD 0.167 (two rows, 12 criterion pairs), signed -0.167, worst row 0.33. The gate (MAD at most 0.5, no row above 1.0) passes: this judge reproduced the April `gpt5.4-xhigh` row exactly and read `gemma4:31b-cloud` a third of a point below April. It read `gpt5.6-sol-xhigh` two thirds of a point above its September blind score (4.33 against 3.50), the largest Sol movement seen in any pack, on the same criteria the September judge marked down (derivation, eccentricity definitions, model justification); Sol's frozen scores are not affected. **Decision:** blind scores used as-is, no offset, as for `glm-5.3-flash` whose anchors also met the gate. The September offset (+0.71) would have lifted the row to 2.83; it was not applied.

## 4. Manual review, execution and practicality

- Execution (Python 3.13.2 standard library, three fenced code cells in order): cell 1 fails with `SyntaxError: invalid non-printable character U+00A0` (the LC1 axial load is written `1 100.0` with a non-breaking space). With that character removed the cells run and print `No suitable size found in range`: `B_candidates` is scaled twice (`round(x * 0.1, 1)` over a list that is already 2.4 to 3.2) and holds 0.24 to 0.32 m. Both faults are the judge's; confirmed.
- The conclusion states `2.9 m` with `LC1` governing by highest `q_max` and both criteria passed, hedged as depending on execution. 2.9 m is the value the evaluator notes single out as the trap (bearing passes, LC2 uplift fails at -0.41 kPa). No override.
- Practicality = 3: free local route, no API cost, no refusal; but the notebook needs two code fixes before it runs, so it is scored as `gpt5.6-luna-max` was for a notebook that stops on its own code, not the 4 to 5 April gave the free cloud route for runnable deliverables. Latency not captured. Cost is not a factor on this route under the rule adopted with the Claude Fable 5.1 addendum.

| Task | Technical (April scale) | Practicality | Overall mean | April winner (overall) | Winner changed? |
|---|---|---:|---:|---|---|
| `v3-notebook-01` | [1, 1, 2, 3, 2, 2] (1.83) | 3 | 2.00 | `gpt5.4-xhigh` (4.86) | no |

Context for the free tier: the April `gemma4:31b-cloud` row scored 3.71 overall on this task with a runnable notebook and the same LC3 governing-case slip; the 26B local model at 2.00 is the lowest score in the v3 table, below `gpt5.6-luna-max` (3.57).

## 5. De-anonymised judge reply

Label key: A = `gemma4:26b-local`, B = `gemma4:31b-cloud`, C = `gpt5.4-xhigh`, D = `gpt5.6-sol-xhigh`

## Blind judgement: v3-notebook-01

### 1. Task summary

The responders had to produce a notebook-style draft (alternating Markdown and standard-library Python cells, six sections in a fixed order) for preliminary sizing of a square pad footing under three service load cases with axial load plus biaxial moment, using a rigid-footing linear-pressure model, deriving the corner-pressure expression from axial plus bending stress, searching B = 2.4 to 3.2 m in 0.1 m steps, and selecting the smallest B with qmax <= 220 kPa and qmin >= 0 for every case. The reference answer is 3.0 m governed by LC2 through the no-uplift check (2.9 m fails only because LC2 gives qmin = -0.41 kPa, while its qmax is fine).

### 2. Score table

| Response | Calculation correctness | Code quality/executability | Engineering judgement | Unit/assumption handling | Notebook traceability/clarity | Completeness of deliverable | Note |
|---|---|---|---|---|---|---|---|
| A | 1 | 1 | 2 | 3 | 2 | 2 | Good hand derivation, but the code has a syntax error and a candidate-width bug that makes every size fail, and the prose concludes 2.9 m governed by LC1, which is the benchmark trap answer. |
| B | 4 | 4 | 3 | 3 | 3 | 3 | Code runs and would select 3.0 m, but "governing case" is defined as the max-qmax case (LC3, not LC2), the conclusion is left as placeholders rather than a stated size, sections are misnumbered and the near-miss at 2.9 m is never explained. |
| C | 5 | 5 | 5 | 5 | 5 | 5 | Full derivation from q = N/A + My x/Iy + Mx y/Ix, four-corner evaluation, a per-candidate sweep table showing why 2.4 to 2.9 m fail, correct 3.0 m / LC2 with the 2.9 m qmin = -0.4 kPa reason stated. |
| D | 5 | 5 | 4 | 4 | 4 | 4 | Correct 3.0 m / LC2 with correct hand-typed table and runnable, well-structured code, but the edge-pressure formula is quoted with absolute moments rather than derived from axial plus bending stress, and eccentricities/moment directions are never defined. |

### 3. Top weaknesses per response

**A**
- Code Cell 1, line `{"id": "LC1", "N": 1 100.0, ...}`: `1 100.0` is a SyntaxError in Python; the cell will not execute. (Possibly a copy artefact, but it is what was delivered.)
- Code Cell 1, `B_candidates = [round(x * 0.1, 1) for x in [i/10 for i in range(24, 33)]]`: the inner list is already 2.4 to 3.2 m, so multiplying by 0.1 again gives widths of about 0.2 to 0.3 m. Every load case then fails (e.g. B = 0.2 m gives q_axial = 1100/0.04 = 27 500 kPa), `selected_B` becomes the string "No suitable size found in range", and Code Cell 3 prints only that message. Even with the syntax error fixed, the notebook selects nothing.
- Code Cell 2 tracks `governing_case_id` by the largest q_max over every candidate width including failing ones, so it would report LC3 at 2.4 m, not the case that actually controls selection.
- Section 6 states "Selected Footing Size: 2.9 m" and "Governing Load Case: LC1 (the case producing the highest qmax)", both wrong, with a hedge that "actual value depends on execution". This is exactly the qmax-only trap flagged in the rules (rule 9), even though the loop itself does test q_min.
- Required sections 2 (Input data) and 3 (Python calculation cells) have no Markdown cells; the outline jumps from section 1 to section 4 and there is no explanation of why smaller candidates fail.

**B**
- The conclusion cell states `selected_B` metres and `governing_case` as literal placeholders; the deliverable never states the selected size in metres or the governing case in prose, contrary to the "must" requirements.
- Governing case is computed as the case with the largest qmax at the selected size (LC3). The selection is actually controlled by the LC2 no-uplift check, and B never reports or explains that 2.9 m fails on qmin.
- Derivation is by section modulus Z = B^3/6 stated as a fact; the path from N/A ± M y/I is not shown as the brief required.
- Sign convention is vague ("positive moments acting about the x and y axes") with no statement of which corner is compressed; eccentricities are defined but never used.
- Section numbering does not match the brief (Input data has no heading; "2. Analysis Model" is inserted; final sections are 3, 4, 5 instead of 4, 5, 6).

**C**
- Justification of why the rigid linear model is appropriate is a single sentence (adequate but brief).
- The `print_markdown_table` helper is placed as Code Cell 1 under the Assumptions section, which slightly blurs the section boundary.
- Governing-case logic (`max(first_passing_width_by_case, ...)`) silently picks the first case on a tie; harmless here but not documented.
- Some nested `next(...)` generator expressions in Code Cell 4 are dense for a reader auditing by hand.

**D**
- Edge-pressure expression is stated as a compact memorised formula with |Mx| and |My|; the brief's requirement to show how it comes from axial stress plus bending stress (N/A ± M y/I, I = B^4/12, y = B/2) is not met.
- Eccentricities ex, ey and the direction of positive moments/compressed corner are never defined, so "define your sign convention and eccentricity directions clearly" is only partly satisfied.
- Code Cell 6 hard-codes `assert selected_width_m == 3.0` and `candidate["B_m"] == 2.9`; the asserts pass here (29/10.0 and 30/10.0 compare exactly), but a notebook whose verification is the expected answer is brittle if inputs change.
- The candidate search summary prints only PASS/FAIL per width; the numerical reason for the 2.9 m rejection lives in prose and asserts rather than in a printed sweep table.

### 4. Ranking (best to worst)

1. **C** - correct answer, correct governing case, full mechanics derivation, four-corner evaluation, transparent sweep showing every rejection, runnable standard-library code.
2. **D** - equally correct numerically and cleanly coded, but quotes the pressure formula instead of deriving it and omits eccentricity definitions.
3. **B** - runnable and selects 3.0 m, but misreports the governing case as LC3, leaves the conclusion as placeholders and never explains the 2.9 m near-miss.
4. **A** - not executable (syntax error), candidate widths wrong by a factor of 10 so no size is ever selected, and the written conclusion is the trap answer of 2.9 m with LC1 governing.

### 5. Practical significance

C and D are both engineering-usable as written; the gap between them is one paragraph of derivation and an eccentricity definition that a reviewer would ask D to add. B needs its conclusion rewritten and its governing-case logic changed from "largest qmax" to "controls the no-uplift check" before it could be issued, though its numbers are right. A is unusable and actively misleading: it cannot run, and its stated 2.9 m / LC1 result would, if trusted, deliver an undersized footing with soil-contact loss under LC2.

### 6. Manual-review watch-outs

- A's `1 100.0` may be a copy artefact, but the `B_candidates` double-scaling bug is independent of it and is fatal on its own.
- B's LC3 "governing case" is defensible only as "governs peak bearing"; it is not the case that governs selection.
- D's use of |Mx|, |My| is numerically equivalent to the reference for the all-positive inputs given, and is a coherent worst-corner convention, but it is not the derivation the brief asked for.
- Only C and D flag the 2.9 m rejection value (-0.41 kPa) explicitly; B's notebook would show it only if a reader added a sweep printout.

## 6. Task 2 (`v2-deep-02`), run later the same day

Same route (`ollama run gemma4:26b`, plain terminal, prompt then the pasted `context_combined.md`), response copied from the terminal with its line wrapping. Latency, tokens and cost not captured.

| Task | Seed | A | B | C | D |
|---|---:|---|---|---|---|
| `v2-deep-02` | 20261403 | `gpt5.6-sol-xhigh` | `gemma4:26b-local` | `gpt5.4-xhigh` | `minimax-m2.7-cloud` |

| Task | Low anchor | High anchor MAD / signed | Low anchor MAD / signed | Anchor order preserved? | Sol vs Sept blind MAD / signed |
|---|---|---:|---:|---|---:|
| `v2-deep-02` | `minimax-m2.7-cloud` | 0.50 / -0.17 | 0.33 / -0.33 | yes (April 4.83 vs 3.00; blind 4.67 vs 2.67) | 0.17 / +0.17 |

Across both packs the anchor MAD is 0.292 (signed -0.208, worst row 0.50), so the gate passes and the blind scores stand without an offset (the September offset would have added +0.42 and rounded the row to the same integers anyway).

- Manual review: all three planted findings present with the correct fix directions; the dimensional argument (cm3 x MPa = N.m, divide by 1000 for kNm) is right; the rounding note gives the correct, conservative direction. The judge's deductions (no line references, no worked numbers or tests, combination column unexamined, rounding waved through) match the response. No override.
- Practicality = 4: free local route, complete answer in the brief's structure, no refusal; latency not captured, so the 5 April gave the free cloud route here is not claimed.

| Task | Technical (April scale) | Practicality | Overall mean | April winner (overall) | Winner changed? |
|---|---|---:|---:|---|---|
| `v2-deep-02` | [5, 4, 5, 4, 3, 4] (4.17) | 4 | 4.14 | `gemma4:31b-cloud` (4.71) | no |

Context for the free tier: on this task the 26B local model is a competent short review, level with `qwen-3.6plus` (4.14) and above the three 2026-09-18 addendum models, while its April cloud sibling won the task at 4.71. The notebook task, not this one, is where the smaller weights fell over.

### De-anonymised judge reply

Label key: A = `gpt5.6-sol-xhigh`, B = `gemma4:26b-local`, C = `gpt5.4-xhigh`, D = `minimax-m2.7-cloud`

#### Judgement: v2-deep-02

##### 1. Task summary
The responders were asked to code-review a three-file package (`load_factors.py`, `beam_capacity.py`, `reporting.py`) intended for major-axis steel beam ULS screening, returning severity-ordered findings, engineering significance, minimum fix direction, and deliberately non-escalated items, with focus on correctness, units, combinations and reporting integrity. The three seeded defects are: the imposed-load factor `ULS_GAMMA_Q = 1.50` is defined but never applied; `major_axis_resistance_kNm()` divides `Wpl_y_cm3 * fy_MPa` by `1e6` instead of `1e3` (cm³ × N/mm² = 1000 Nmm = 1 Nm, so the result is 1000× too small); and `build_review_table()` sorts ascending and returns `[:1]`, i.e. only the least-utilised row. Secondary: rounding before pass/fail classification.

##### 2. Score table

| Response | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Note |
|---|---|---|---|---|---|---|---|
| A | 5 | 4 | 5 | 5 | 4 | 5 | Finds all three seeded bugs with a correct worked unit example (1000 cm³ × 355 MPa = 355 kNm vs 0.355 from the code), adds a valid combination-label integrity finding, but several cited line numbers are off. |
| B | 5 | 4 | 5 | 4 | 3 | 4 | All three primary bugs found with a correct dimensional argument and minimal correct fixes, but shallow beyond that: no line references, no test guidance, and the combination column is never examined. |
| C | 5 | 5 | 5 | 4 | 5 | 4 | All three primary bugs found with accurate line references, regression-test recommendations and a proportionate API-rename suggestion; misses the combination-label point and reads densely. |
| D | 2 | 2 | 3 | 2 | 3 | 4 | Well formatted, but explicitly asserts the `1e6` divisor is correct, invents a γ_M0 "Critical" that is numerically vacuous, and misdescribes the truncation as returning the worst-case beam. |

##### 3. Top weaknesses per response

**A**
- Line references are inaccurate against the supplied files (e.g. cites `reporting.py:14–15` for the sort/slice, which is at lines 17–18; `load_factors.py:6–7` for the return at line 6). Minor, but it is a repo-reading slip in an otherwise precise review.
- Ranks the missing `γ_Q` as "High" below the truncation "Critical"; both are flagged, but an unconservative load factor arguably deserves parity with the reporting bug.
- Finding 5 (combination label) is valid but partly speculative about input semantics ("if the input can represent alternative ULS combinations") — it is framed as a contract question rather than a proven defect, which is the right framing but adds length.

**B**
- No file line references and no proposed tests; the fixes are stated as bare edits ("change `1e6` to `1000`") with nothing to lock the conversion down.
- Does not examine the `combination` column at all despite the prompt's explicit "combinations" focus.
- Leaves rounding-before-status as non-escalated "assuming the user accepts the rounding margin" — a soft assumption; it is a reporting-integrity defect at the acceptance limit and should at least be a Low/Medium finding.
- Minimal fix for reporting keeps ascending sort, so failures land at the bottom of the table; acceptable but not the best direction.

**C**
- Misses the combination-label integrity point (the `combination` string is passed through unvalidated and unused).
- Findings are single dense paragraphs; harder to scan than A or D, though nothing is omitted.
- No worked numeric example for the unit error, although the dimensional reasoning stated is correct.

**D**
- Misses the seeded unit error outright and states in the non-escalated table that "The `1e6` conversion is correct but opaque" — a confident, false claim on the exact category the task told it to focus on.
- Finding 2 (γ_M0) is invented and self-refuting: "overstated by a factor of 1.0" is no overstatement; the recommended fix is a signature change that also carries the wrong `/1e6` forward.
- Finding 3 mischaracterises the truncation as returning "the worst-case beam only" — the ascending sort with `[:1]` returns the *least* utilised row, which is the unsafe direction. Both the risk description and the severity narrative are therefore wrong.
- Rounding fix (`util <= 1.0` on the already-rounded value) does not address the root cause; the "Python float arithmetic rarely lands precisely on 1.0" explanation is muddled, and "an exactly-at-limit beam should fail by most design philosophies" is contrary to the usual `≤ 1.0` acceptance.
- Claims "No type hints on function signatures" — every function in the supplied code is type-hinted, indicating shallow reading.

##### 4. Ranking (best to worst)
1. **A** — all three seeded defects correct with a checkable numeric example, plus the most task-relevant extra finding (combination label vs actual calculation); only line-number slips detract.
2. **C** — equally correct on the seeded defects, most accurate repo referencing, and the best maintainability guidance (regression tests, API rename); loses narrowly for missing the combination point and denser presentation.
3. **B** — correct and safe on the three primaries but shallow: no line refs, no tests, rounding waved through, combination column ignored.
4. **D** — misses and explicitly denies the 1000× unit bug, fabricates a γ_M0 critical, and inverts the direction of the truncation defect.

##### 5. Practical significance
A, C and B would each let a maintainer fix the three real defects correctly; the gap between them is depth and auditability (worked numbers, line refs, tests, the combination-label contract), not correctness. D is materially different in kind: applying D's review would ship the package with the 1000× resistance error intact and with a misleading understanding of what the truncated report shows, while adding a γ_M0 parameter that changes nothing at the default. The A–C gap is marginal; the B–D gap is a release-blocking difference.

##### 6. Manual-review watch-outs
- Confirm the intended kNm conversion: `Wpl_y_cm3 * fy_MPa / 1e3` (A, B and C agree; D's assertion that `/1e6` is correct should be disregarded).
- Decide the acceptance rule (`<= 1.0` vs `< 1.0`) and whether status is computed on raw or rounded utilisation before adopting any of the rounding fixes.
- Decide whether `build_review_table` should return the full table (A/B/C/D) or a governing row per member; A and D both note a per-member `max`/`groupby` would be needed if the latter.
- A's finding 5 (combination string unused by the calculation) is a genuine reporting-integrity gap not listed in the evaluator notes; worth carrying into the fix scope.

## 7. Anchor (`v2-anchor-07`), run last

Same route (`ollama run gemma4:26b`, PowerShell terminal, prompt pasted; no web access, so section properties come from the model's weights), response copied from the terminal with its line wrapping. The user's note: it started answering at once and did not loop. Latency, tokens and cost not captured.

| Task | Seed | A | B | C | D |
|---|---:|---|---|---|---|
| `v2-anchor-07` | 20261408 | `gpt5.4-xhigh` | `gpt5.6-sol-xhigh` | `gemma4:26b-local` | `minimax-m2.7-cloud` |

| Task | Low anchor | High anchor MAD / signed | Low anchor MAD / signed | Anchor order preserved? | Sol vs Sept blind MAD / signed |
|---|---|---:|---:|---|---:|
| `v2-anchor-07` | `minimax-m2.7-cloud` | 0.50 / -0.17 | 1.00 / +0.00 | yes (April 4.83 vs 2.50; blind 4.67 vs 2.50) | 0.33 / +0.00 |

Across the three gemma packs the anchor MAD is 0.444 (signed -0.167, worst row 1.00); the gate passes and the blind scores stand without an offset.

- Manual review: the planted wrong-axis fault is not identified (the corrected code keeps `Wpl_z`, and the text calls the y/z notation interchangeable); the replacement property of about 440 cm3 is not the tabulated 353 cm3 and is cited to the SCI Blue Book, which the model could not consult; the response says the original code prints FAIL at 13.5 kN.m and that it worked because the errors cancelled, neither of which is what the snippet does (it prints PASS at a utilisation of about 6.6e-6 because N.mm is compared with kN.m); `M_Ed` is given as 88.76 and then 89.31 for 18.5 x 6.2^2 / 8 = 88.89. The PASS headline is right by coincidence with a capacity overstated by a quarter, which the judge called the more dangerous failure mode. No override.
- Practicality = 4: free local route, prompt answer, no refusal; the fabricated property is a technical failure and is scored under correctness, so the free route keeps the April practicality given to `gemma4:31b-cloud` on this task. Latency not captured.

| Task | Technical (April scale) | Practicality | Overall mean | April winner (overall) | Winner changed? |
|---|---|---:|---:|---|---|
| `v2-anchor-07` | [1, 1, 2, 1, 2, 2] (1.50) | 4 | 1.86 | `gpt5.4-xhigh` (4.43) | no |

Context: 1.86 is the lowest anchor score in the table, below `minimax-m2.7-cloud` (2.43). The April `gemma4:31b-cloud` row reached 4.00 on the same task with the correct axis and a usable modulus. With Task 2 at 4.14 and the anchor at 1.86, the provisional v2 average over the two tasks is 3.00.

### De-anonymised judge reply

Label key: A = `gpt5.4-xhigh`, B = `gpt5.6-sol-xhigh`, C = `gemma4:26b-local`, D = `minimax-m2.7-cloud`

#### Judgement: v2-anchor-07

##### 1. Task summary
Responders were asked to review a short Python EC3 bending check for a 254x102x28 UB (simply supported, 6.2 m, 18.5 kN/m UDL), find errors in engineering logic, units or section properties, correct them, show working and state adequacy. The planted faults (evaluator notes) are (1) the minor-axis plastic modulus `Wpl_z` used instead of the major-axis `Wpl_y`, and (2) `M_Rd` computed in N·mm but labelled/compared as kN·m (missing /1e6). Reference values against which I checked every response: Wpl,y = 353 cm³, Wpl,z = 54.8 cm³, M_Ed = 18.5 × 6.2² / 8 = 88.89 kN·m, M_c,y,Rd = 353e3 × 275 / 1e6 = 97.075 kN·m, utilisation 0.916, PASS for the cross-section check. The original code as written computes `M_Rd = 13,475,000` (N·mm, printed as kN·m) and therefore prints PASS with a utilisation of ~6.6e-6; it does not print FAIL.

##### 2. Score table

| Response | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Note |
|---|---|---|---|---|---|---|---|
| A | 5 | 5 | 5 | 4 | 4 | 5 | Finds both planted faults, correct properties and arithmetic, correct conditional adequacy statement, minimal safe diff. |
| B | 5 | 5 | 5 | 5 | 5 | 4 | Same correct core as A plus a tabulated cross-check, a low-shear check and a worked LTB interpolation; opening sentence is slightly muddled. |
| C | 1 | 1 | 2 | 1 | 2 | 2 | Misses the axis fault, invents Wpl = 440 cm³ (non-conservative), misdescribes what the original code prints, and its own M_Ed arithmetic contradicts itself. |
| D | 2 | 3 | 2 | 2 | 3 | 3 | Names both planted faults but uses Wpl,y = 106 cm³ (wrong by ~3.3x), bolts on unrequested load factors and reaches the wrong conclusion (FAIL). |

##### 3. Top weaknesses per response

**A**
- Quotes Mb,Rd "about 31 to 32 kN·m" and C1 = 1.13 without showing the table values or the interpolation; the LTB conclusion is an assertion rather than working (though consistent with B's numbers).
- Says LTB "governs" for an unrestrained beam without stating that restraint is unknown from the prompt beyond the assumption list; minor.
- Corrected code carries no in-code source comment for the 353e3 value (source is only in the prose).
- Every quoted property and arithmetic step checked: 353 cm³, 54.8-55 cm³, 88.89, 97,075,000 N·mm, 97.1, 0.916 all match.

**B**
- Opening line "The code's unconditional PASS is incorrect ... the section passes" reads as self-contradictory on first pass; it is defensible (the original PASS is an artefact of the 10^6 error) but could be worded better.
- PDF page references (p.72, p.205, p.231, pp.35-36) and the tabulated Mb,Rd values (32.3 at 6 m, 28.1 at 7 m) cannot be verified from the pack; the interpolation arithmetic itself (31.46) and the ratio (2.83) are correct.
- Printed output line "M_c,y,Rd = 97.08" vs exact 97.075: a 2-dp rounding of a binary float may show 97.07 or 97.08; immaterial.
- Everything else checked: 353e3, 54.8e3, 88.8925, 97,075,000 N·mm, 0.9157, V_Ed = 57.35 kN, V_c,Rd = 283 kN (consistent with Av ≈ 1780 mm² × 275/√3), ratio 0.203; all match.

**C**
- Does not identify planted fault 1 at all: keeps `Wpl_z` in the corrected code and treats the y/z notation as interchangeable ("W_pl,y or W_pl,z depending on notation").
- Wrong section property: claims Wpl = 440 × 10³ mm³ "from the SCI Blue Book"; the tabulated Wpl,y is 353 cm³. This overstates capacity by 25% and gives a false utilisation of 0.738 instead of 0.916 - a non-conservative planted error attributed to a source.
- Misstates the original code's behaviour twice: says it "would calculate a resistance of ≈13.5 kN.m and report a FAIL" (it computes 13,475,000 and reports PASS), and says "your original code worked because the error cancelled out" (nothing cancels; the missing /1e6 is a 10^6 error).
- Arithmetic is internally inconsistent: 18.5 × 38.44 / 8 is quoted as 88.7625 and then as 89.3125 "using the exact values"; the correct product is 88.8925. Neither figure is right.
- Frames the unit conversion (planted fault 2) as merely "safer practice" rather than a substantive error.
- Typo "2rub 254x102x28 UB"; contradictory numbers reduce clarity.

**D**
- Wrong section properties throughout: Wpl,y ≈ 106 × 10³ mm³ (actual 353 × 10³), Wel,y ≈ 69 × 10³ (actual ~308 × 10³), Wpl,z ≈ 23 × 10³ (actual 54.8 × 10³). Also asserts the snippet's 49.0e3 is "the minor-axis value" - it matches neither tabulated axis.
- Wrong adequacy conclusion (FAIL, utilisation 3.05 to 4.12) and recommends larger sections, purely as a consequence of the wrong Wpl,y. The internal arithmetic (29.15 kN·m, 24.98 kN/m, 120.0 kN·m, 4.12) is consistent with its wrong inputs.
- Drifts from the planted objective: introduces the unrequested assumption that 18.5 kN/m is characteristic and applies γG = 1.35 in the primary code path (exactly the "replace the objective with a different design problem" behaviour the notes penalise); leaves an unused `gamma_Q`.
- Class 1 verification quotes flange c/t ≈ 6 and web d/t ≈ 39; actual values are about 4.0 and 35.7. Conclusion (Class 1) is right, the numbers are not.
- "γ_M0 = 1.0 – EC3-1-1 Table 5" is not where γ_M0 is given (Cl. 6.1(1)); minor.
- Uses "the beam fails anyway" to dismiss LTB - circular reasoning from wrong data.
- Correctly describes the original code's unit fault ("10⁶ times too large when printed"), which is why repo comprehension is scored above C.

##### 4. Ranking (best to worst)
1. **B** - both planted faults identified and correctly fixed, every property and arithmetic step checks out, plus a tabulated cross-check, shear-interaction check and worked LTB estimate that do not displace the core objective.
2. **A** - the same correct core answer with a tighter, minimal diff; marginally less supporting working than B.
3. **D** - names both planted faults and reads the original code's behaviour correctly, but wrong section properties, an invented load-factor step and a wrong FAIL conclusion make the corrected result unusable.
4. **C** - misses the axis fault entirely, plants a wrong non-conservative property, misdescribes what the original code does, and its working contradicts itself; the PASS conclusion is right only by coincidence.

##### 5. Practical significance
A and B are both reviews a checking engineer could accept as-is; the gap between them is small (B's extra checks vs A's brevity) and would not change any decision. The gap between A/B and C/D is large and decision-changing: D would reject an adequate beam and specify a heavier section on the strength of a property wrong by a factor of 3.3, while C would sign off the beam with a 25% overstated capacity and no awareness of the axis error - the more dangerous failure mode even though its headline answer happens to be PASS. D edges C because it at least identified the two planted faults and described the original code accurately.

##### 6. Manual-review watch-outs
- Confirm Blue Book values used as reference here: Wpl,y = 353 cm³, Wpl,z = 54.8 cm³, Mc,y,Rd (S275) = 97.1 kN·m, Vc,Rd = 283 kN, C1 = 1.13 for UDL, and B's Mb,Rd table values (32.3 at 6 m, 28.1 at 7 m). None could be verified from the pack; A and B agree with each other and with my recollection.
- B's PDF page anchors are unverified and should not be treated as evidence of correctness.
- C's "440 × 10³ mm³ from the SCI Blue Book" and D's "106 × 10³ mm³ from the Blue Book" are both attributed to a real source but do not match it; treat as fabricated citations.
- Response C's line wrapping note is a formatting caveat only; the substantive errors are independent of formatting.
- D's wide markdown table wraps badly but its content was assessed in full.

## 8. Remaining v2 tasks, eight-pack calibration and revision

The user ran the remaining five v2 tasks later on 2026-09-19 on the same route, this time with `ollama run --verbose`, which prints duration and token counts. Every task followed the two-message protocol and the model waited for the pasted context each time. Hardware: Intel Core i7-9700K, 64 GB RAM, RTX 2070 SUPER 8 GB; llama-server held about 4 GB and about half the CPU while generating, so the 26B weights run mostly on CPU with partial GPU offload.

| Task | Prompt-only reply | Answer | Generated tokens (answer, thinking included) | Rate |
|---|---|---|---:|---:|
| `v2-deep-01` | 43.7 s | 7 min 32 s | 3436 | 7.65 tok/s |
| `v2-deep-03` | 31.3 s | 5 min 31 s | 2995 | 9.09 tok/s |
| `v2-deep-04` | 43.2 s | 3 min 35 s | 2290 | 10.78 tok/s |
| `v2-medium-05` | 31.1 s | 5 min 50 s | 2699 | 7.76 tok/s |
| `v2-medium-06` | 36.4 s | 4 min 21 s | 2687 | 10.38 tok/s |

The prompt-only replies each generated 330 to 510 tokens for a one-line answer, so the counts include hidden thinking. Ollama counts only the last turn's prompt, so these token figures are not comparable with the harness totals of the other routes and are not charted.

### Blind packs

| Task | Seed | A | B | C | D |
|---|---:|---|---|---|---|
| `v2-deep-01` | 20261402 | `gpt5.4-xhigh` | `gpt5.6-sol-xhigh` | `qwen-3.6plus` | `gemma4:26b-local` |
| `v2-deep-03` | 20261404 | `gemma4:26b-local` | `qwen-3.6plus` | `gpt5.4-xhigh` | `gpt5.6-sol-xhigh` |
| `v2-deep-04` | 20261405 | `gemma4:26b-local` | `gpt5.6-sol-xhigh` | `gpt5.4-xhigh` | `gemma4:31b-cloud` |
| `v2-medium-05` | 20261406 | `gemma4:26b-local` | `gemma4:31b-cloud` | `gpt5.4-xhigh` | `gpt5.6-sol-xhigh` |
| `v2-medium-06` | 20261407 | `gemma4:26b-local` | `gpt5.6-sol-xhigh` | `gpt5.4-xhigh` | `deepseek-v3.2` |

### Calibration over all eight packs

| Task | Low anchor | High anchor MAD / signed | Low anchor MAD / signed | Anchor order preserved? | Sol vs Sept blind MAD / signed |
|---|---|---:|---:|---|---:|
| `v2-deep-01` | `qwen-3.6plus` | 0.33 / -0.33 | 0.67 / -0.67 | yes (April 4.17 vs 3.67; blind 3.83 vs 3.00) | 0.00 / +0.00 |
| `v2-deep-02` | `minimax-m2.7-cloud` | 0.50 / -0.17 | 0.33 / -0.33 | yes (April 4.83 vs 3.00; blind 4.67 vs 2.67) | 0.17 / +0.17 |
| `v2-deep-03` | `qwen-3.6plus` | 1.17 / -1.17 | 0.83 / -0.83 | yes (April 4.83 vs 3.83; blind 3.67 vs 3.00) | 0.00 / +0.00 |
| `v2-deep-04` | `gemma4:31b-cloud` | 0.67 / -0.67 | 0.83 / -0.83 | NO (April 4.83 vs 4.83; blind 4.17 vs 4.00) | 0.00 / +0.00 |
| `v2-medium-05` | `gemma4:31b-cloud` | 0.17 / -0.17 | 1.17 / -1.17 | yes (April 4.00 vs 3.83; blind 3.83 vs 2.67) | 0.58 / -0.58 |
| `v2-medium-06` | `deepseek-v3.2` | 0.83 / +0.50 | 0.17 / +0.17 | yes (April 3.50 vs 2.33; blind 4.00 vs 2.50) | 0.17 / +0.17 |
| `v2-anchor-07` | `minimax-m2.7-cloud` | 0.50 / -0.17 | 1.00 / +0.00 | yes (April 4.83 vs 2.50; blind 4.67 vs 2.50) | 0.33 / +0.00 |
| `v3-notebook-01` | `gemma4:31b-cloud` | 0.00 / +0.00 | 0.33 / -0.33 | yes (April 5.00 vs 3.67; blind 5.00 vs 3.33) | 0.67 / +0.67 |

Overall anchor MAD 0.594 (sixteen rows, 96 criterion pairs), signed -0.385, worst row 1.17 (`gpt5.4-xhigh` on deep-03 and `gemma4:31b-cloud` on medium-05, both read 1.17 below April). The gate fails on both counts, in the usual direction for this judge family. The deep-04 anchor order flag reflects an April tie (4.83 each) that the blind pass broke by a sixth of a point, not a reversal. Sol reproduced its September blind scores to within 0.67 everywhere and exactly on three tasks.

**Decision (revision):** the first three packs (notebook, Task 2, anchor) met the gate on their own and were recorded as-is in sections 3, 6 and 7. With eight packs the model's calibration fails, so the standing rule (September per-task offsets, as for `deepseek-v4.1-flash`, `tencent-hy4-preview` and `claude-fable-5.1-high`) is applied to every task of this model for consistency. The Task 2 and anchor integers do not change under their offsets (+0.42 and +0.08); the notebook row moves from [1, 1, 2, 3, 2, 2] (1.83) to [2, 2, 3, 4, 3, 3] (2.83) under +0.71.

| Task | Raw blind (mean) | September offset | On April scale (mean) |
|---|---:|---:|---:|
| `v2-deep-01` | [2, 2, 2, 2, 2, 3] (2.17) | +0.67 | [3, 3, 3, 3, 3, 4] (3.17) |
| `v2-deep-02` | [5, 4, 5, 4, 3, 4] (4.17) | +0.42 | [5, 4, 5, 4, 3, 4] (4.17) |
| `v2-deep-03` | [3, 3, 4, 3, 3, 3] (3.17) | +1.42 | [4, 4, 5, 4, 4, 4] (4.17) |
| `v2-deep-04` | [3, 4, 4, 4, 3, 3] (3.50) | +0.96 | [4, 5, 5, 5, 4, 4] (4.50) |
| `v2-medium-05` | [2, 3, 2, 2, 3, 3] (2.50) | +0.42 | [2, 3, 2, 2, 3, 3] (2.50) |
| `v2-medium-06` | [3, 3, 2, 3, 3, 4] (3.00) | +0.17 | [3, 3, 2, 3, 3, 4] (3.00) |
| `v2-anchor-07` | [1, 1, 2, 1, 2, 2] (1.50) | +0.08 | [1, 1, 2, 1, 2, 2] (1.50) |
| `v3-notebook-01` | [1, 1, 2, 3, 2, 2] (1.83) | +0.71 | [2, 2, 3, 4, 3, 3] (2.83) |

### Manual review

- `v2-deep-01`: Root cause correct and unknown-section guard sensible, but the proposed patch contains `SEIONS[name]`, which would raise `NameError` on every call, and it misses every other defect in the pipeline and reporting files. Checked against the response text; no override.
- `v2-deep-03`: Sound additive skeleton (default `columns=RESULT_COLUMNS` keeps the legacy slice) but never decides the per-group aggregation rule, ignores divide-by-zero, and is sloppy (`build_slli_summary`, `all(cols in df.columns)`). Checked against the response text; no override.
- `v2-deep-04`: Spots the trap and rightly prefers leaving the code alone, but its regression tests are mis-specified (expects `"PASS"`/`"FAIL"` from `concrete_utilisation`, which returns floats) and omit negative denominators. Checked against the response text; no override.
- `v2-medium-05`: Sound review and vectorised outline, but the code contains a stray walrus-in-subscript (`df[REQUIRED_column_subset := REQUIRED_COLUMNS]`, a SyntaxError below Python 3.10 and meaningless above it), silently drops unparseable rows, and still counts zero-length members while excluding their ratio. Checked against the response text; no override.
- `v2-medium-06`: Finds the false-PASS and the multi-point spacing ambiguity, but its own fix reintroduces the same silent-zero anti-pattern for invalid spacing and one test's expected value (5.0) matches neither the original nor the fixed code (both give 10.0). Checked against the response text; no override.

### Practicality (revision)

- Every task = 3. Free local inference on the user's own hardware, no API cost, no refusal, the two-message protocol followed; on the timed tasks the answer took 3 min 35 s to 7 min 32 s after a 30 to 45 s prompt-only reply (7.7 to 10.8 generated tokens per second, CPU-bound on an 8 GB card), so on the latency-only reading that applies to routes where cost is not counted it is scored as the 3 to 6 minute runs of `gpt5.6-luna-max` and the 2026-09-18 addendum models, not the 4 to 5 April gave the free cloud route for one-to-two-minute answers.
- Task 2 and the anchor were first scored 4 with latency uncaptured (sections 6 and 7); the timed runs showed the route takes 4 to 8 minutes per task, so they are revised to 3 the same day for consistency with the rule applied to every other model. The notebook stays at 3.

### Results, all eight tasks

| Task | Technical (April scale) | Practicality | Overall mean | April winner (overall) | Winner changed? |
|---|---|---:|---:|---|---|
| `v2-deep-01` | [3, 3, 3, 3, 3, 4] (3.17) | 3 | 3.14 | `gpt5.6-sol-xhigh` (4.71) | no |
| `v2-deep-02` | [5, 4, 5, 4, 3, 4] (4.17) | 3 | 4.00 | `gemma4:31b-cloud` (4.71) | no |
| `v2-deep-03` | [4, 4, 5, 4, 4, 4] (4.17) | 3 | 4.00 | `gpt5.6-sol-xhigh` (4.71) | no |
| `v2-deep-04` | [4, 5, 5, 5, 4, 4] (4.50) | 3 | 4.29 | `kimi-k2-thinking` (5.00) | no |
| `v2-medium-05` | [2, 3, 2, 2, 3, 3] (2.50) | 3 | 2.57 | `gpt5.6-sol-xhigh` (4.57) | no |
| `v2-medium-06` | [3, 3, 2, 3, 3, 4] (3.00) | 3 | 3.00 | `gpt5.6-luna-max` (4.00) | no |
| `v2-anchor-07` | [1, 1, 2, 1, 2, 2] (1.50) | 3 | 1.71 | `gpt5.4-xhigh` (4.43) | no |
| `v3-notebook-01` | [2, 2, 3, 4, 3, 3] (2.83) | 3 | 2.86 | `gpt5.4-xhigh` (4.86) | no |

v2 cross-task average over the six primary tasks (the composite every full model is ranked on): 3.50. The anchor (1.71) is reported separately as for every model. v3: 2.86.

### De-anonymised judge replies, five new tasks

#### `v2-deep-01` - Multi-file bug hunt in a member check pipeline

Label key: A = `gpt5.4-xhigh`, B = `gpt5.6-sol-xhigh`, C = `qwen-3.6plus`, D = `gemma4:26b-local`

##### Judgement: v2-deep-01

###### 1. Task summary
The responders were asked to review a three-file pandas-based beam bending check pipeline (section library, analysis pipeline, reporting), identify the root cause of inflated major-axis utilisation ratios after a refactor, order any secondary risks by severity, propose the smallest safe multi-file fix with explicit units and section-property conventions, and list tests to add before merging. The planted root cause is a `cm³ → mm³` conversion using `1e2` instead of `1e3` in `section_library.get_section_properties()`; key secondary risks are the signed `max` moment envelope (misses governing hogging moments), the missing guard for unknown sections, and (also legitimately present in the code) pass/fail being decided after rounding and `"Section": "first"` pairing demand with an unrelated section.

###### 2. Score table

| Response | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Note |
|---|---|---|---|---|---|---|---|
| A | 4 | 4 | 4 | 3 | 4 | 4 | Correct root cause with a clean minimal patch and good unit-explicit tests, but it never notices the signed-max envelope defect, which is the structurally important secondary risk. |
| B | 5 | 5 | 4 | 5 | 4 | 4 | Finds the root cause, the envelope defect, the rounding-before-status defect, the section-pairing risk and the NaN drop, all verified against the code with exact line references and correct arithmetic; patch is correct but slightly wider than strictly minimal. |
| C | 3 | 3 | 3 | 2 | 3 | 4 | Root cause and unknown-section guard are right, but it invents a zero-capacity risk, misses the envelope and rounding defects, and its test 6 locks in the very NaN behaviour it flagged as a risk. |
| D | 2 | 2 | 2 | 2 | 2 | 3 | Root cause correct and unknown-section guard sensible, but the proposed patch contains `SEIONS[name]`, which would raise `NameError` on every call, and it misses every other defect in the pipeline and reporting files. |

###### 3. Top weaknesses per response

**A**
- Misses the signed `"Mz_kNm": "max"` envelope defect entirely; for `[-120, +80]` the pipeline checks 80 kN·m and would mark a failing member as passing, so this is a real safety gap left in the "smallest safe fix".
- No guard for unknown section names (raw `KeyError`), which the task's refactor context makes a plausible risk.
- Line references are off by one (`section_library.py:10` is the `fy_MPa` line, the bug is on line 11; `analysis_pipeline.py:15` is the props lookup, the resistance line is 16). Minor, but a precision lapse in a code-review deliverable.
- The `build_member_summary` consistency check is described only as "example intent", not shown as code.

**B**
- "Reject invalid or missing `Mz_kNm`" is a behaviour change beyond the reported bug: any existing input with blank moment cells (e.g. members with no bending results) would start raising. Defensible, but not the *smallest* patch and not called out as a possible compatibility break.
- No explicit unknown-section guard; the "validate one section per member" check does not cover a section name absent from `SECTIONS`.
- Reproduced local file-system links are noise in the write-up (does not affect technical content).
- The Mz/My axis-convention discussion is correct and appropriately cautious, but lengthens the answer for a task that asked for the smallest safe fix.

**C**
- Misses both the envelope defect and the rounding-before-status defect, so the "two lines changed, one guard added" patch leaves two real correctness problems in place.
- The zero/negative capacity guard is an invented risk: `SECTIONS` contains only positive moduli and yield strengths, and returning `float("inf")` silently is worse than raising; it also makes the code harder to reason about.
- Internal contradiction on NaN handling: section 2c flags silent coercion as a risk, then test 6 asserts that NaN "propagates, not crash", entrenching that behaviour. The explanation of how `decorate_status` treats NaN is muddled ("neither PASS nor FAIL ... they'd be marked FAIL").
- Minor arithmetic slop: 50/10.065 = 4.968, presented as 4.96.

**D**
- The proposed `section_library.py` contains `section = SEIONS[name]`, a typo that would raise `NameError` on every lookup. Applying the patch as written breaks the pipeline completely; the task explicitly asked for a safe fix.
- Misses the envelope defect, the rounding-before-status defect, and the `"Section": "first"` pairing risk; only one file is touched despite the "multi-file fix" instruction.
- "`NaN <= 1.0` evaluates to `False` in some pandas versions" is hedged and misleading; it is always `False`, so all NaN rows are labelled FAIL with an empty utilisation, which is the actual issue to state.
- Test 2 proposes inputs without stating the expected result (100/100.65 ≈ 0.9935), so it is not a concrete test; the whole `SECTIONS` dict is reproduced unnecessarily.

###### 4. Ranking (best to worst)
1. **B** — only response that finds and correctly fixes the unit bug *and* the governing-moment envelope, with verified numbers, exact line references, explicit unit and convention statements, and tests that would catch each defect.
2. **A** — correct, minimal and safe, with good unit-explicit tests and the rounding/section-pairing catches, but blind to the envelope defect.
3. **C** — right root cause and a sensible unknown-section guard, undermined by a speculative guard, a self-contradictory NaN position, and no engagement with the aggregation or reporting defects.
4. **D** — right root cause but the patch as written is broken (`SEIONS`), coverage is the shallowest of the four, and the NaN claim is inaccurate.

###### 5. Practical significance
The gap between B and A is material for a structural check: A's patch would ship a pipeline that still silently under-reports hogging-governed members, a safety-relevant miss, while B's would not. The gap between A and C is moderate: both fix the headline bug, but C leaves the rounding boundary bug and the envelope bug and adds a dubious guard. D is separated from the others by a hard-stop defect: a reviewer applying its patch verbatim would get a `NameError`, so it is not usable without correction, and its remaining analysis adds little beyond the root cause.

###### 6. Manual-review watch-outs
- Confirm that the project's solver really maps major-axis moment to the `Mz_kNm` column; B is the only response that flags this convention question instead of assuming it.
- B's "reject missing moments" change should be checked against real input files before adoption; blank moment cells may be legitimate.
- C's `float("inf")` return and D's `SEIONS` typo must not be copied into any patch.
- Any adopted patch should include the envelope test (`[-120, +80]` → governing 120 kN·m) and the rounding-boundary test (`1.0004` → FAIL); only B proposes both, and only A and B propose the rounding one.

#### `v2-deep-03` - Scoped feature design on an existing package

Label key: A = `gemma4:26b-local`, B = `qwen-3.6plus`, C = `gpt5.4-xhigh`, D = `gpt5.6-sol-xhigh`

##### Blind judgement: v2-deep-03

###### 1. Task summary
The responders were given a three-file structural design package (`design_engine.build_uls_summary` grouping by `Member`/`Section` and taking max `Utilisation_ULS` with a PASS/FAIL `Status`; `io_contract.RESULT_COLUMNS` fixing the four-column report contract plus `normalise_columns`; `report_writer.report_rows` projecting exactly `RESULT_COLUMNS` via `.loc[:, RESULT_COLUMNS]`) and asked for a decision-complete plan, not code, to add an optional serviceability summary computing `DeflectionRatio = Deflection_mm / AllowableDeflection_mm`, while leaving ULS-only callers untouched and keeping `report_rows()` output stable; the deliverable had to cover files changed, interface/schema changes, data flow, backward-compatibility risks, and tests/acceptance criteria.

###### 2. Score table

| Response | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Note |
|---|---|---|---|---|---|---|---|
| A | 3 | 3 | 4 | 3 | 3 | 3 | Sound additive skeleton (default `columns=RESULT_COLUMNS` keeps the legacy slice) but never decides the per-group aggregation rule, ignores divide-by-zero, and is sloppy (`build_slli_summary`, `all(cols in df.columns)`). |
| B | 3 | 3 | 3 | 2 | 3 | 4 | Most concrete, but its `report_rows` rewrite silently drops missing columns (a real semantic change it then claims is "no existing logic modified"), its zero-guard (`pd.NA` into the PASS/FAIL lambda) would raise, and it aggregates numerator and denominator independently (`max`/`first`). |
| C | 4 | 4 | 5 | 3 | 3 | 3 | Nothing it says about the code is wrong and it is the most conservative, but it hedges nearly every decision the task asked it to make and explicitly leaves the aggregation rule open. |
| D | 5 | 5 | 5 | 4 | 5 | 5 | Fully additive, decision-complete, and engineering-coherent (row-level ratio, governing row carried intact, deterministic ties, empty schema-correct frame for absence, opt-in `report_sections`); only its validation rules are debatable. |

###### 3. Top weaknesses per response

**A**
- Names the new function `build_slli_summary` in section 1 and `build_sls_summary` everywhere else; guard written as `if all(cols in df.columns)` which is not valid pseudo-Python. Small, but signals carelessness.
- No aggregation rule: `build_uls_summary` groups by `Member`/`Section`, so the SLS builder must too, yet A never says how `Deflection_mm`/`AllowableDeflection_mm` collapse per group or whether the ratio is taken before or after grouping.
- No handling of `AllowableDeflection_mm == 0` or nulls; after the left merge, ULS-only members carry `NaN` in `Status_SLS`, which is not addressed.
- Invents `Status_SLS` (not requested) and its "ratio calculated correctly" test actually checks status, not the ratio.
- Does not mention `normalise_columns` in the flow.

**B**
- `report_rows` change filters `cols` to those present, so a summary missing `Status` would no longer raise `KeyError` but silently emit short records to downstream consumers. This is a hidden contract weakening, and the closing claim "No existing logic is modified" is false.
- Division guard is buggy as written: `.replace(0, pd.NA)` then `ratio <= 1.0` yields `NA`, and `"PASS" if NA else "FAIL"` raises `TypeError`; the test expecting "inf or NaN with FAIL" is inconsistent with the mitigation.
- `Deflection_mm=max`, `AllowableDeflection_mm=first` aggregates numerator and denominator from potentially different rows; `first` is order-dependent.
- `SLS_COLUMNS` includes `Member`/`Section`, forcing the `SLS_COLUMNS[2:]` slicing hack in every caller.
- Mentions helpers (`report_rows_combined`, `has_sls_data`) that never appear in the plan; offers "alternatively, add `include_sls` to `build_uls_summary`" instead of deciding.

**C**
- Not decision-complete: "ideally ... or a small wrapper", "or a combined writer with an explicit flag", "optionally `ServiceabilityStatus`", "decide whether such rows are excluded, set to null, or flagged", "depending on chosen API". The task explicitly asked for decisions.
- Explicitly defers the aggregation rule to "before implementation" rather than fixing it, and its lean ("after aggregation, not per raw row") is the weaker engineering choice.
- No concrete schema, signatures, or code; tests are generic statements rather than executable specifications.
- No discussion of what "absent" looks like at the API level (None vs empty frame) or how a combined report is shaped.

**D**
- Rejecting negative `Deflection_mm` is an invented constraint; sign conventions differ (hogging/upward deflection is legitimate) and an absolute-value or sign-agnostic rule may be more appropriate. Raising on one-sided nulls is also strict, though correctly scoped to the SLS path only.
- Deliberately omits a serviceability pass/fail field; defensible given the literal request but many consumers will want it, and the point is asserted rather than left as an option.
- No code sketch of `build_serviceability_summary` itself; the rules are precise enough to implement, but an implementer must translate the idxmax-per-group logic themselves.

###### 4. Ranking (best to worst)
1. **D** — the only plan that is additive, decision-complete, and engineering-coherent (governing row selected on row-level ratio; existing contract literally untouched; absence represented consistently).
2. **C** — zero errors and maximally safe, correctly flags the aggregation and divide-by-zero issues, but hands most decisions back to the implementer.
3. **A** — workable and safe default-argument design, but shallow on the engineering (no aggregation or zero handling) and careless in naming.
4. **B** — most concrete, yet the concreteness exposes a silent `report_rows` semantics change, a guard that would raise, and incoherent independent aggregation.

###### 5. Practical significance
The gap between D and the rest is material: D could be handed to an implementer as-is, whereas C needs a design decision round first, A needs the aggregation and zero-division rules added before coding, and B needs its `report_rows` change reverted and its guard/aggregation fixed. C, A and B are within a few points of each other and the ordering among them is arguable; none would break existing ULS-only callers on the default path, so the differences there are about engineering coherence and rigour rather than immediate breakage.

###### Manual-review watch-outs
- Verify B's `report_rows` "available columns" filter is not merged; it converts a loud `KeyError` into silent partial records.
- If D's validation is adopted, confirm the project's deflection sign convention before rejecting negatives.
- All four responses (except D, which reasons about it) leave unspecified what happens to `Status_SLS`/ratio for ULS-only members after a left merge; check NaN handling in any combined-frame approach.

#### `v2-deep-04` - Safe refactor with behaviour preservation constraints

Label key: A = `gemma4:26b-local`, B = `gpt5.6-sol-xhigh`, C = `gpt5.4-xhigh`, D = `gemma4:31b-cloud`

#### Judgement: v2-deep-04

##### 1. Task summary

The responders were asked to review a proposed "deduplicate shared utilisation helpers" refactor across `concrete_checks.py` and `steel_checks.py`, both of which call `common_formatting.format_status`, and to say whether it is safe, what may be shared versus what must stay distinct, give a minimal behaviour-preserving approach, and list regression checks, under constraints that downstream spreadsheets depend on the current status text, that broad rewrites are not wanted, and that any silent change to zero-denominator behaviour is penalised. The hidden trap is that `concrete_utilisation` returns `None` for `v_rd <= 0` (giving `"CHECK INPUT"`) whereas `steel_utilisation` returns `0.0` (giving `"PASS"` via `format_status(0.0)`), so a naive unified helper silently changes one module's status text.

##### 2. Score table

| Response | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Note |
|---|---|---|---|---|---|---|---|
| A | 3 | 4 | 4 | 4 | 3 | 3 | Spots the trap and rightly prefers leaving the code alone, but its regression tests are mis-specified (expects `"PASS"`/`"FAIL"` from `concrete_utilisation`, which returns floats) and omit negative denominators. |
| B | 5 | 5 | 5 | 5 | 4 | 5 | Every claim checks out against the code (including that `format_status(None)` raises `TypeError`), the refactor is exact, the policy is kept visible in each module, and the pytest suite tests exact return values, exact strings, the inclusive boundary and negative denominators. |
| C | 5 | 4 | 4 | 4 | 4 | 4 | Correct and tight; a parameterised helper with a required sentinel plus a complete test checklist (return values, status text, negatives, boundary), but no full code, no home named for the helper, and no mention of the `None`/`format_status` interaction. |
| D | 4 | 4 | 4 | 4 | 4 | 4 | Full, behaviour-preserving code with a required `fallback` argument, but the test list only checks status strings (never the `None` vs `0.0` return values) and omits the inclusive `1.0` boundary. |

##### 3. Top weaknesses per response

**A**
- Regression checks 3 and 4 call `concrete_utilisation(1.0, 1.0)` / `concrete_utilisation(1.1, 1.0)` and expect `"PASS"` / `"FAIL"`; those functions return `1.0` and `1.1`. The tests as written would fail or would be quietly rewritten by whoever implements them; for a task that is explicitly about exactness of status text, that is a real defect.
- No negative-denominator test even though its own table says "Zero/Negative Denominator" and the code uses `<= 0`.
- The optional helper gives `fallback_value` a default of `None`; a default makes it easier for a call site to silently pick up the wrong semantics (here a missed argument in steel would propagate `None` into `format_status` and raise, which is at least loud, but a default on a semantics-selecting parameter is still poor design).
- Table has a redundant row ("Error String Output" repeats "Zero/Negative Denominator"); the analysis is a little padded relative to its content.

**B**
- The helper `utilisation_or_none` lives in `common_formatting.py`, which is a formatting module; a small naming/placement smell (shared by A and D).
- `steel_utilisation` becomes an indirection through `None` and back to `0.0`; behaviour-identical, but arguably no simpler than the original two-liner. B does say the lowest-risk option is to leave the functions alone, which mitigates this.
- The opening "Yes, but only if..." is slightly softer than the rest of the answer, which then effectively says "no to any unified default".

**C**
- No full modified module code and no stated file location for `utilisation_or`, so the reviewer has to fill in the diff; acceptable for "minimal approach" but less auditable than B or D.
- Does not note that `format_status(None)` would raise `TypeError`, i.e. why the concrete `None` branch must sit before the formatter.
- Does not explicitly say that not refactoring at all is a valid outcome; it goes straight to "a small refactor is acceptable".
- Tests are a checklist rather than runnable code (fine, but less rigorous about exact float values).

**D**
- Regression tests only exercise `concrete_status` / `steel_status`; they never assert `concrete_utilisation(10, 0) is None` or `steel_utilisation(10, 0) == 0.0`, even though those functions are public and are the layer actually being refactored.
- No test of the inclusive `util == 1.0 -> "PASS"` boundary, which is the one line of shared logic being touched.
- Does not consider the "leave it as is" option; presents the helper as what "you should implement".
- Does not mention the `format_status(None)` hazard.

##### 4. Ranking (best to worst)

1. **B** - only response whose analysis, code and tests are all exact against the supplied code, and it both offers the no-change option and explicitly guards against the configurable-default failure mode.
2. **C** - fully correct analysis with a required-sentinel helper and the most complete test checklist after B; loses only on depth of code detail and the unstated `None` hazard.
3. **D** - correct, complete code, but the merge gate it proposes is weaker (status-only tests, no boundary test), which matters for a task about regression protection.
4. **A** - reaches the right conclusion and the right recommendation, but the mis-specified tests and defaulted helper parameter are errors of exactly the kind the task is probing.

##### 5. Practical significance

Small to moderate. All four responses identify the `None`/`"CHECK INPUT"` versus `0.0`/`"PASS"` split, all preserve status text, and none proposes an unsafe unified helper, so none would cause the spreadsheet regression the task is designed to catch. The separation is in rigour of the merge gate: B and C would catch a regression in either the return values or the status strings; D would miss a change in the utilisation return values or the `1.0` boundary; A's test list would need correcting before it could be run. A reviewer using B could merge with confidence; a reviewer using A would have to redo the tests.

##### 6. Manual-review watch-outs

- Confirm A's regression tests are read as errors, not typos: `concrete_utilisation` returns a float, never a status string.
- B's float equality assertions (`0.5`, `1.0`, `1.01`) are exact in IEEE double for those inputs; if a reviewer generalises them to other values, `pytest.approx` should be used.
- All three code-proposing responses (A, B, D) put arithmetic into `common_formatting.py`; if the repo has a stricter module layout, that placement may need adjusting, but it is not a correctness issue.
- None of the responses questions whether `steel_utilisation` returning `0.0` (and therefore `"PASS"`) for zero capacity is itself a latent engineering bug; the task forbids changing it silently, but a human reviewer may want to flag it for explicit sign-off separately.

#### `v2-medium-05` - Large dataset engineering summary pipeline

Label key: A = `gemma4:26b-local`, B = `gemma4:31b-cloud`, C = `gpt5.4-xhigh`, D = `gpt5.6-sol-xhigh`

##### Blind judgement: v2-medium-05

###### 1. Task summary
The responders were given a 25-line pandas module that computes an L/250 deflection utilisation ratio per row via an `iterrows()` loop with bare `float()` casts, then groups by Storey/Material to produce MemberCount, MaxRatio, MeanRatio and a PASS/FAIL Status; they were asked to review it or propose a revised implementation addressing performance at several hundred thousand rows, data cleaning/validation, correctness of the utilisation summary, and maintainability. The evaluator notes flag `iterrows()`, unsafe `float()` casts, and unhandled zero/missing lengths as the expected issues, with a preference for solutions that are not over-complicated.

###### 2. Score table

| Response | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Note |
|---|---|---|---|---|---|---|---|
| A | 2 | 3 | 2 | 2 | 3 | 3 | Sound review and vectorised outline, but the code contains a stray walrus-in-subscript (`df[REQUIRED_column_subset := REQUIRED_COLUMNS]`, a SyntaxError below Python 3.10 and meaningless above it), silently drops unparseable rows, and still counts zero-length members while excluding their ratio. |
| B | 3 | 3 | 2 | 2 | 3 | 3 | Simplest correct vectorisation for clean data, but it mutates the caller's DataFrame in place (coerces columns and adds `DeflectionRatio`), does no schema validation, and leaves NaN-ratio rows counted in MemberCount while they vanish from Max/Mean. |
| C | 4 | 4 | 3 | 4 | 4 | 4 | Tight, line-referenced findings and a clean staged implementation with schema check, fail-fast validation, absolute deflection and a member envelope; the unflagged cost is that `_clean_text` casts numeric group keys (e.g. integer Storey) to string dtype in the output. |
| D | 5 | 4 | 4 | 4 | 4 | 4 | Most complete and careful revision: dtype-aware identifier cleaning, finiteness and positivity checks with reason counts and example indices, raise/drop policy, parameterised span limit, backward-compatible signature and numerically correct test cases. |

###### 3. Top weaknesses per response

**A**
- `work_df = df[REQUIRED_column_subset := REQUIRED_COLUMNS].copy()` is an unparenthesised assignment expression inside a subscript: SyntaxError on Python < 3.10, and a pointless throwaway variable on 3.10+. Signals unverified code.
- `dropna` silently discards rows with non-numeric Length/Deflection, so a storey can report PASS with members missing and no warning; MemberCount still includes zero-length members whose ratio became NaN, so count and ratio populations disagree.
- Negative lengths and signed (negative) deflections are unhandled, so a large negative deflection yields a negative ratio and a PASS; the claim that `inf` "might bypass the PASS logic" is backwards (inf fails; -inf passes).
- Empty-frame early return happens before the column check, so an empty frame with the wrong schema passes silently.
- Overconfident performance claims ("milliseconds", "SIMD") without qualification.

**B**
- Mutates the input DataFrame (`df[col] = ...`, `df["DeflectionRatio"] = ...`), a side effect the original did not have; will also raise SettingWithCopyWarning on slices.
- No required-column validation, no handling of negative lengths, signed deflection, or empty input beyond incidental behaviour.
- Rows with NaN Length/Deflection are retained and counted in MemberCount but excluded from MaxRatio/MeanRatio, so the summary is internally inconsistent with no warning.
- `1000.0` and the `1.0` threshold remain magic numbers despite the "constants" claim.
- Review is shallow: does not notice its own in-place mutation or the missing schema check.

**C**
- `_clean_text` does `astype("string")` unconditionally, so integer or float Storey/Material/Member keys come back as StringDtype in the summary; downstream `summary.Storey == 1` would silently return nothing. Not mentioned.
- `sort=False` changes the output row order relative to the original sorted groupby; not mentioned.
- Fail-fast on any invalid row with no drop/report option means a dataset that previously produced a (NaN-tolerant) summary now raises; the alternative is only mentioned in prose.
- The member-envelope step changes MemberCount/MeanRatio semantics when a member has multiple rows; stated, but it is an assumption about the export format.

**D**
- Most complex of the four (raise/drop policy, span-limit validation, reason counts); proportionate for a production pipeline but somewhat beyond the stated scope, given the evaluator preference for not over-complicating.
- `sort=False` changes output row order relative to the original; not mentioned.
- Default `errors="raise"` makes any NaN in the numeric columns fatal, which is stricter than the original's implicit NaN tolerance; stated, but pipelines relying on the old behaviour will break.
- Uses a tuple for `df.loc[:, _REQUIRED_COLUMNS]`; this works on flat column indexes in modern pandas but a list would be the unambiguous idiom (the code itself converts to `list(...)` for groupby).

###### 4. Ranking (best to worst)
1. **D** — correct, vectorised, validates everything the notes ask for and more, preserves key dtypes, and documents every semantic change with a numerically verified test case.
2. **C** — nearly as strong and more concise, but the silent string-casting of numeric group keys is an unflagged output change.
3. **B** — runs and gives correct numbers on clean data, but in-place mutation of the caller's frame and zero validation make it unsafe to drop in.
4. **A** — the better review of the bottom pair, but the code carries a possible syntax error and silently drops rows in a pass/fail summary.

###### 5. Practical significance
The gap between the top pair (C, D) and the bottom pair (A, B) is material: C and D could be merged after small fixes (C: guard the string cast on non-object keys; D: optionally mention ordering), whereas A needs the walrus artefact removed and a decision on drop-vs-raise before it can even be imported reliably, and B must stop mutating its input and add a schema check. Within pairs the differences are modest: D beats C mainly on dtype safety and diagnostics; B edges A only because B's code runs everywhere while A's may not. All four fix the headline `iterrows()` and `float()` problems; only C and D address signed deflection, negative lengths and the count/ratio population mismatch.

Manual-review watch-outs: confirm the target Python version before judging A's walrus line; check whether Storey/Member are numeric in real exports (affects C); confirm whether exports contain multiple rows per member (affects the envelope semantics in C and D); and note that C and D both change group row ordering via `sort=False`.

#### `v2-medium-06` - Review plus targeted test design

Label key: A = `gemma4:26b-local`, B = `gpt5.6-sol-xhigh`, C = `gpt5.4-xhigh`, D = `deepseek-v3.2`

##### Judgement: v2-medium-06

###### 1. Task summary
The responders were given a 14-line Python helper (`settlement_ratio`, `differential_slope`, `status_from_ratio`) for early-stage foundation assessment and asked to identify the key bugs/risks, propose minimum fixes, and design a small, high-value test set, being explicit about sign conventions and units. The planted failures are: `settlement_ratio()` returning `0.0` for `allowable_mm == 0` (which yields a false PASS), `differential_slope()` dividing mm by m without conversion or documentation, and the unguarded `spacing_m == 0` / borderline-threshold behaviour that good tests should pin down.

###### 2. Score table

| Response | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Note |
|---|---|---|---|---|---|---|---|
| A | 3 | 3 | 2 | 3 | 3 | 4 | Finds the false-PASS and the multi-point spacing ambiguity, but its own fix reintroduces the same silent-zero anti-pattern for invalid spacing and one test's expected value (5.0) matches neither the original nor the fixed code (both give 10.0). |
| B | 4 | 4 | 3 | 4 | 4 | 5 | Most complete finding list with explicit sign/unit assumptions and a fully self-consistent test set that directly catches the zero-allowable and mm-to-m failures, marred by an incorrect NaN claim and several breaking API changes labelled "minimum". |
| C | 4 | 4 | 4 | 4 | 4 | 4 | Proportionate, well-documented fixes that keep mm/m but make it explicit, with consistent tests; misses the multi-point ambiguity, cites wrong line numbers, and flips the equality boundary to the less conservative side. |
| D | 2 | 3 | 2 | 2 | 3 | 3 | Adds a default 5 % "engineering tolerance" that silently makes ratios up to 1.049 PASS for every caller, its own boundary tests then fail against its own code, and the integration test contains an mm-vs-mm/m unit error (L/300 over 5 m is 3.33 mm/m, not 16.7 mm/m). |

###### 3. Top weaknesses per response

**A**
- `differential_slope` fix returns `0.0` when `spacing_m <= 0` — a silent benign default for invalid input, exactly the failure class it called "catastrophic" in `settlement_ratio`; a downstream check would see zero distortion and pass.
- Test "Sequence Expansion" expects `differential_slope([10, 5, 0], 1) == 5.0`; both the original and A's fixed code return `10.0` (max−min = 10, /1). The test would fail against A's own fix, and the "validates if user is aware" wording is not a test.
- Does not flag the mm/m unit mixing as a bug; it only appears as a footnote. No unit-conversion test, no negative-allowable guard, and the sign convention for heave is never stated despite the prompt asking for it.
- `float('inf')` sentinel forces FAIL (correct direction) but propagates silently into any downstream arithmetic instead of failing loudly.

**B**
- Claim that "NaN can silently produce a PASS" is wrong for the supplied code: `nan < 1.0` is `False`, so `status_from_ratio(nan)` returns `"FAIL"` (and would under B's `<=` too). Overconfident misread of the code's actual behaviour.
- "Minimum code fixes" are actually four contract-breaking changes: raising instead of returning `0.0` for <2 points, rejecting anything other than exactly two points, dividing by 1000 (a 1000× change in output magnitude for any existing caller comparing against a mm/m limit), and flipping `<` to `<=`. All are flagged, but the scaling change and the equality flip could silently alter downstream results.
- Equality flip makes ratio = 1.0 PASS where the original code failed it — a change in the less conservative direction, adopted on the basis of "normally" with only a "confirm this" caveat.

**C**
- Misses the multi-point ambiguity (`max − min` over a single `spacing_m` when the extreme points may not be adjacent) and keeps the `return 0.0` for <2 points, even writing a test that locks that behaviour in.
- Line references are wrong (`:10` for `status_from_ratio` is actually the slope return; `:8` for the unit-inconsistent return is the `return 0.0` line; the division is line 10). Substantive reading is right, but citations are sloppy.
- Flips equality to `<= 1.0` PASS (less conservative) on "usually acceptable", and applies `abs()` so heave is assessed by magnitude — a defensible choice but a silent semantic change to results for negative inputs.
- Unit test `differential_slope([10, 16], 3) == 2.0` passes against the original code as well, so it documents the mm/m convention rather than catching a hidden failure.

**D**
- `status_from_ratio(ratio, tolerance=0.05)` changes the default outcome for all callers: ratio 1.00–1.049 becomes PASS. An invented, non-conservative relaxation of a serviceability check with no basis in the supplied code.
- Its own tests contradict its own code: `status_from_ratio(1.00) == "FAIL"` and `status_from_ratio(1.01) == "FAIL"` both fail, because with the default tolerance `1.00 < 1.05` → `"PASS"`.
- Hidden unit error in the integration test: "5000 mm / 300 = 16.7 mm/m" conflates an allowable differential settlement (16.7 mm over 5 m) with a gradient (3.33 mm/m). The assertion still passes only because 1.4 < 16.7, so the wrong limit would never be caught.
- Empty list raises but a single point returns `0.0` — inconsistent validation. The test set is the largest of the four and includes a demo-style integration test, against the "no huge test matrix" constraint. Multi-point ambiguity not mentioned, yet the integration test relies on it.

###### 4. Ranking (best to worst)
1. **B** — most complete identification of the planted and adjacent issues, explicit sign/unit assumptions, and the only test set that would actually fail against the original code on both the zero-allowable and the mm-to-m conversion; held back by the wrong NaN claim and over-broad "minimum" changes.
2. **C** — near-tie with B; more proportionate and safer to apply (keeps mm/m, documents it, raises on bad denominators), but misses the multi-point ambiguity, cites wrong lines, and its unit test does not discriminate original from fixed code.
3. **A** — correct headline findings, but the fix reintroduces a silent-zero default and one test's expected value is inconsistent with its own code; no sign convention, unit issue not treated as a bug.
4. **D** — the tolerance change is the single most unsafe proposal in the set, its boundary tests fail against its own implementation, and the integration test embeds a unit error.

###### 5. Practical significance
B and C are both acceptable review outputs and the gap between them is small: B is the better bug report and test design, C is the safer patch. Either would need a reviewer to decide the equality-boundary convention before merging. A is a step below — its findings are usable but its patch and one test would need correction before use. D is materially worse: applying its `status_from_ratio` change as written would loosen a pass/fail safety check for every caller, and its test file would not run green, so it is not a mergeable contribution without rework.

###### 6. Manual-review watch-outs
- Confirm the project's intended threshold convention (`<` vs `<=` at ratio 1.0) before accepting B, C or D; three of four responses flipped it without evidence from the code.
- Confirm whether `differential_slope` is meant to return mm/m or a dimensionless gradient; B's ×1/1000 change is only correct if callers expect dimensionless.
- Verify D's tolerance change is rejected; check that no reviewer treats "engineering tolerance" as a legitimate default.
- A's `spacing_m <= 0 → 0.0` and D's single-point `0.0` both preserve a silent-benign-default path that should be flagged regardless of which patch is chosen.
