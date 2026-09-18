# Gemma 4 26B (local) addendum (2026-09-19): blind scoring record

Scope: `gemma4:26b-local` (Ollama `gemma4:26b`, run locally on the user's machine from a plain terminal, no harness, tools or skills) on two tasks, `v3-notebook-01` first and `v2-deep-02` later the same day (section 6), as a free-tier comparison point. The method is the September 2026 refresh procedure (`refresh_2026-09_calibration.md`) as applied to the 2026-09-18 and 2026-09-19 addenda. No earlier score, note or winner was changed. This is a different model from the April `gemma4:31b-cloud` row (Ollama cloud, 31B), which is the low anchor in this pack.

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
