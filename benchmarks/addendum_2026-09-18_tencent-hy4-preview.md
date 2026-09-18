# Tencent Hy4 Preview addendum (2026-09-18): blind scoring record

Scope: `tencent-hy4-preview` (OpenRouter `tencent/hy4-preview`, reasoning effort high) on three tasks: `v2-deep-02`, `v2-anchor-07` and `v3-notebook-01`. The method is the September 2026 refresh procedure (`refresh_2026-09_calibration.md`) as applied to `deepseek-v4.1-flash` and `glm-5.3-flash` the same day. No April or September score, note or winner was changed.

## 1. Runs

All three runs were made by the user on 2026-09-18 from a VS Code agent chat routed through OpenRouter, one fresh chat per task, in a separate sandbox folder holding the three task folders (prompt and context files only). Figures are from the user's run note; the run records hold the detail.

| Task | Order | Latency | Tokens (chat) | Billed (OpenRouter) | Protocol notes |
|---|---:|---|---:|---:|---|
| `v2-deep-02` | 1 | 1 min 59 s | ~37k | $0.094 | Read the task folder; wrote `code_review.md` as asked. |
| `v3-notebook-01` | 2 | 3 min 18 s | ~43k | $0.128 | Deliverable written as `pad_footing_sizing_notebook.md`. |
| `v2-anchor-07` | 3 | 12 min 50 s | ~65k | $0.115 | Read the full `prompt.md`; cites two web property tables, so web lookup appears to have been used. |

## 2. Blind packs

One pack per task, four responses each: the new model, the April high anchor `gpt5.4-xhigh`, the same April low anchor as the September pack, and `gpt5.6-sol-xhigh` as a same-judge-family consistency check; same pack contents and judge instructions as the other addenda, new seeds. Judges were Claude Fable 5.1 subagents, one per task, reading only the pack. An identity-word scan of the response sections found no hits; no redactions were needed.

| Task | Seed | A | B | C | D |
|---|---:|---|---|---|---|
| `v2-deep-02` | 20261203 | `gpt5.6-sol-xhigh` | `minimax-m2.7-cloud` | `tencent-hy4-preview` | `gpt5.4-xhigh` |
| `v2-anchor-07` | 20261208 | `gpt5.6-sol-xhigh` | `tencent-hy4-preview` | `minimax-m2.7-cloud` | `gpt5.4-xhigh` |
| `v3-notebook-01` | 20261209 | `tencent-hy4-preview` | `gpt5.4-xhigh` | `gpt5.6-sol-xhigh` | `gemma4:31b-cloud` |

## 3. Calibration

| Task | Low anchor | High anchor MAD / signed | Low anchor MAD / signed | Anchor order preserved? | Sol vs Sept blind MAD / signed |
|---|---|---:|---:|---|---:|
| `v2-deep-02` | `minimax-m2.7-cloud` | 0.50 / -0.50 | 0.50 / -0.50 | yes (April 4.83 vs 3.00; blind 4.33 vs 2.50) | 0.33 / +0.33 |
| `v2-anchor-07` | `minimax-m2.7-cloud` | 0.50 / -0.17 | 0.83 / -0.50 | yes (April 4.83 vs 2.50; blind 4.67 vs 2.00) | 0.17 / +0.17 |
| `v3-notebook-01` | `gemma4:31b-cloud` | 0.50 / -0.50 | 1.00 / -1.00 | yes (April 5.00 vs 3.67; blind 4.50 vs 2.67) | 0.17 / -0.17 |

Overall anchor MAD 0.639 (six rows, 36 criterion pairs), signed -0.528, worst row 1.00. The gate (MAD at most 0.5, no row above 1.0) fails on the MAD, as it did for the September refresh and the DeepSeek addendum, in the same direction. Anchor order was preserved on every task and Sol stayed within a third of a point of its September blind scores.

| Task | Offset from this pack | September offset | Raw blind (mean) | Adjusted with this pack | Adjusted with September offset |
|---|---:|---:|---:|---:|---:|
| `v2-deep-02` | +0.50 | +0.42 | [5, 5, 3, 4, 4, 4] (4.17) | [5, 5, 4, 4, 4, 4] (4.33) | [5, 5, 3, 4, 4, 4] (4.17) |
| `v2-anchor-07` | +0.33 | +0.08 | [4, 4, 2, 2, 3, 3] (3.00) | [4, 4, 2, 2, 3, 3] (3.00) | [4, 4, 2, 2, 3, 3] (3.00) |
| `v3-notebook-01` | +0.75 | +0.71 | [5, 5, 5, 4, 5, 5] (4.83) | [5, 5, 5, 5, 5, 5] (5.00) | [5, 5, 5, 5, 5, 5] (5.00) |

**Decision:** the September per-task offsets, the user's standing choice for packs that fail the gate (as for `deepseek-v4.1-flash`). The two offset sets agree on the anchor and the notebook and differ by one Change safety point on the repo review, so the choice is immaterial here.

## 4. Manual review, execution and practicality

- `v3-notebook-01` execution (Python 3.13.2 standard library, five fenced code cells in order): runs end to end, selects `3.0 m`, prints `LC2` as governing for no-uplift and `LC3` for bearing utilisation, and the printed search trace matches the reference values. The reversed `e_x`/`e_y` naming is stated explicitly and applied consistently, so it was left as the judge scored it (a unit-and-assumption deduction, not a correctness error).
- `v2-anchor-07`: both planted faults are found and the corrected numbers are right; the verdict drift (LTB and deflection headlining a NOT adequate answer, factored self-weight added to the load) is as the judge describes and matches the evaluator notes' penalty for replacing the planted objective. No override.
- `v2-deep-02`: all three planted findings present and grounded; the judge's checks of the worked numbers were confirmed. No override.
- Practicality (unblinded, from the run note): `v2-deep-02` = 3 (1 min 59 s, the fastest addendum run on this task, about $0.094 on a mid-tier paid route about seven times the flash models' price); `v2-anchor-07` = 2 (12 min 50 s and about 65k tokens; the September floor for slow-but-usable runs); `v3-notebook-01` = 3 (3 min 18 s, notebook runs end to end; as the other addendum models).

| Task | Technical (April scale) | Practicality | Overall mean | April winner (overall) | Winner changed? |
|---|---|---:|---:|---|---|
| `v2-deep-02` | [5, 5, 3, 4, 4, 4] (4.17) | 3 | 4.00 | `gemma4:31b-cloud` (4.71) | no |
| `v2-anchor-07` | [4, 4, 2, 2, 3, 3] (3.00) | 2 | 2.86 | `gpt5.4-xhigh` (4.43) | no |
| `v3-notebook-01` | [5, 5, 5, 5, 5, 5] (5.00) | 3 | 4.71 | `gpt5.4-xhigh` (4.86) | no |

## 5. De-anonymised judge replies

Each reply is verbatim; the label key precedes it.

### `v2-deep-02` - Repo review with unit, combination, and reporting traps

Label key: A = `gpt5.6-sol-xhigh`, B = `minimax-m2.7-cloud`, C = `tencent-hy4-preview`, D = `gpt5.4-xhigh`

## Judgement: v2-deep-02

### 1. Task summary

Code-review (no rewrite) of a three-file steel-beam ULS screening package containing three planted defects: the imposed-load factor 1.50 is never applied, the plastic-modulus/yield product divides by 1e6 instead of 1e3 (cm3 treated as mm3, resistance 1000x too small), and the report sorts ascending then returns only `output[:1]` so only the least-utilised row survives.

### 2. Score table

| Response | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Note |
|---|---|---|---|---|---|---|---|
| A | 5 | 5 | 5 | 5 | 4 | 5 | Finds all three planted defects with correct unit arithmetic and direction-of-error, adds a sound rounding-before-status point and a well-framed combination-label caveat, and stays proportionate to the "short, high-signal" brief. |
| B | 2 | 2 | 3 | 2 | 3 | 3 | Misses the 1000x unit error outright and explicitly asserts the `1e6` conversion is correct, misreads the `[:1]` truncation as keeping the worst case, and elevates a non-issue (gamma_M0 = 1.0) to Critical. |
| C | 5 | 5 | 3 | 4 | 4 | 4 | Technically the deepest review (correct worked numbers, F1/F2 opposite-sign interaction note, section-class validity), but it is far longer than the brief asked for and its "minimum fixes" include schema redesign, breaking signature changes and packaging rework built on invented assumptions. |
| D | 5 | 4 | 5 | 4 | 4 | 4 | Finds all three defects and the rounding issue with correct fix directions and regression-test suggestions, but the "why it matters" is thin, the F1/F2 interaction is not noted and several quoted line numbers do not match the supplied files. |

### 3. Top weaknesses per response

**A**
- Ranks the report truncation above the unconservative Q-factor omission and rates the 1000x unit error only "High"; defensible but arguable, since the unit error makes every result unusable.
- Does not suggest regression tests to pin the two one-token arithmetic fixes, which is the cheapest way to stop them recurring.
- Finding 5 (combination label never validated) is somewhat speculative about what the input schema might represent, though it is correctly kept at Medium and framed as a contract question.
- Line references are off by one in places (`load_factors.py:6-7`, `reporting.py:7-11`); trivial.

**B**
- Misses the cm3-to-mm3 unit error entirely and states in the not-escalated table that "the `1e6` conversion is correct but opaque" — a false assurance that would mislead a maintainer.
- Describes `output[:1]` after an ascending sort as returning "the worst-case beam only"; it returns the best-case (lowest-utilisation) row, so the safety implication is reversed.
- Elevates the absence of an explicit gamma_M0 to Critical while conceding it produces correct numbers ("overstated by a factor of 1.0" is incoherent), and calls the package "structurally non-compliant with EN 1993-1-1" on that basis.
- Rounding finding is internally contradictory: proposes `<= 1.0` on the already-rounded value (which would pass raw 0.995-0.999 as 1.00, non-conservative) while stating an at-limit beam "should fail by most design philosophies anyway"; the float-arithmetic explanation is muddled.
- Claims "no type hints on function signatures" when every function has them — evidence of shallow reading.

**C**
- Disproportionate to the brief ("prefer a short, high-signal review"): eight findings, a release gate, CI lint rules, pint/pydantic/dataclass suggestions and packaging changes for a three-function screening tool.
- Several "minimum fixes" are not minimum: F5 makes a `class` key mandatory and raises on its absence (breaks every existing caller), F4 proposes a new row schema with psi0 and favourable-G flags, F8 rewrites imports and adds package markers.
- Invented assumptions: "no tests at all" and "works only when the CWD happens to be `context/`" cannot be known from the three files supplied; F4 assumes the tool is meant to handle multiple variable actions, accidental and seismic combinations.
- Minor over-statement that sorting on rounded values makes the governing member "non-deterministic" (Python's sort is stable; ties are merely engineering-arbitrary).
- Includes a fair amount of code despite the "do not rewrite" instruction.

**D**
- Line references do not match the supplied files (`reporting.py:17-18` in a 15-line file; `load_factors.py:5-6` given as where `ULS_GAMMA_Q` is defined, when it is at lines 1-2).
- "Why it matters" explanations are one clause each; no worked example or magnitude estimate for the unit or Q-factor errors.
- Does not note that F1 (unconservative) and F2 (conservative by 1000x) act in opposite directions, so a partial fix of only the loud bug would leave the silent one live.
- Rounding finding is phrased confusingly ("uses `< 1.0` rather than the raw value") though the fix direction is correct.
- Not-escalated section is minimal; no mention of the combination label being unvalidated.

### 4. Ranking (best to worst)

1. **A** — complete, correct, proportionate, safe fix directions, clean reasoning.
2. **D** — complete and correct with safe, test-backed fix directions, but thin explanations and inaccurate line references.
3. **C** — deepest engineering content and the only response to explain the F1/F2 interaction, but penalised for disproportion, invented assumptions and non-minimal, caller-breaking fix proposals.
4. **B** — misses one of the three planted defects, asserts it correct, and reverses the meaning of another.

D and C are close; the order flips if explanatory depth is weighed above proportion and change safety.

### 5. Practical significance of the differences

- A, C and D would all lead a maintainer to fix the three real bugs correctly, with correct direction-of-error and a correct `/1e3` conversion. In practice any of them is an acceptable pre-release review; the differences are about reading effort, precision of references and how much unrelated work they would trigger.
- C's extra findings (section classification, combination envelope, input validation) are legitimate engineering concerns for a real tool, but treating F4/F5 as "required before release" would likely delay a screening tool for scope it was never intended to cover.
- B is materially different: a maintainer following B would fix the Q factor, remove `[:1]`, add a gamma_M0 argument, and ship with the resistance still 1000x too small — and B's text would actively discourage anyone from looking at the divisor. B's reversed description of the truncation also understates its safety consequence.

### 6. Manual-review watch-outs

- Verify C's worked numbers before trusting the depth: 625 cm3 x 355 MPa / 1000 = 221.9 kNm is correct; for G = Q = 10 kN/m on 6 m, w = 28.5 kN/m, M = 128.25 kNm, utilisation = 0.578 (as coded: w = 23.5, M = 105.75, R = 0.222 kNm, utilisation about 477). These check out.
- B's statement that the `1e6` conversion is correct is false; do not let its confident formatting and severity table mask the missed defect.
- A proposes `<= 1.0` as the acceptance rule; C argues `< 1.0` is correct and conservative. EN 1993-1-1 writes the check as M_Ed / M_c,Rd <= 1.0, so A is closer to the code, but this is a convention disagreement, not a correctness error in either.
- D's line numbers are wrong for the files as supplied; check whether the responder was working from a differently formatted copy before treating this as a comprehension failure.
- C's "no tests exist" and CWD-import claims are unverifiable from the pack; do not credit or penalise them beyond noting they are assumptions.
- Severity ordering differs across A, C and D (truncation vs Q factor vs unit error at the top). All three orderings are defensible; the evaluator notes list all three as primary and do not rank them.

### `v2-anchor-07` - EC3 planted-error trap (historical anchor)

Label key: A = `gpt5.6-sol-xhigh`, B = `tencent-hy4-preview`, C = `minimax-m2.7-cloud`, D = `gpt5.4-xhigh`

## Judgement: v2-anchor-07

### 1. Task summary

Review a short EC3 bending-check snippet for a 254x102x28 UB and find/correct the two planted faults (minor-axis `Wpl_z` used instead of major-axis `Wpl_y`, and the missing N.mm to kN.m conversion), then state clearly whether the section is adequate.

### 2. Score table

| Response | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Note |
|---|---|---|---|---|---|---|---|
| A | 5 | 5 | 5 | 5 | 5 | 5 | Nails both planted faults with the correct Wpl,y = 353 cm3 and a sourced, auditable 88.89 / 97.08 kN.m = 0.916 PASS, keeping the LTB caveat as a clearly-flagged conditional rather than replacing the task. |
| B | 4 | 4 | 2 | 2 | 3 | 3 | Both planted faults are found and explained well (including why they cancel), but the response then rebuilds the problem with self-weight, LTB, deflection and section swaps so the headline "NOT adequate" answers a different design question on assumptions the prompt never gave. |
| C | 1 | 2 | 2 | 1 | 3 | 3 | Recognises the two fault types but substitutes a fabricated Wpl,y = 106 cm3 (real value 353 cm3) attributed to the Blue Book, adds an unrequested 1.35 load factor as an "error", and therefore reaches the wrong adequacy conclusion (FAIL at 3-4x). |
| D | 5 | 5 | 5 | 5 | 4 | 4 | Compact, correct and proportionate: both faults identified, Wpl,y = 353 cm3 with sources, 88.89 / 97.1 = 0.916 PASS for cross-section bending, LTB flagged as a caveat; slightly thinner working than A and the code still prints an unqualified PASS. |

### 3. Top weaknesses per response

**A**
- Mentions C1 = 1.13 for the UDL case but then interpolates the Blue Book Mb,Rd table directly without applying it; harmless (conservative) but a small internal inconsistency in the optional LTB aside.
- Shear reserve check and LTB section are beyond the brief; they are short and clearly labelled, so the drift is minor.

**B**
- Headline verdict ("NOT adequate", LTB fail by 2.9x, deflection fail by 2.5x) depends on assumptions not in the prompt (unrestrained over 6.2 m, 18.5 kN/m also the SLS load, L/360 limit) and buries the planted-objective answer (cross-section PASS) beneath a redesign; this is exactly the drift the evaluator notes penalise.
- Silently changes the task input: adds 1.35 x self-weight so M_Ed becomes 90.69 kN.m rather than the snippet's 88.89 kN.m, while simultaneously assuming 18.5 kN/m is already a full ULS combination.
- Corrected code is a wholesale rewrite (classification, shear, LTB, deflection) rather than a fix; contains a no-op line (`M_Rd = Mpl_Rd if VEd <= 0.5*Vpl_Rd else Mpl_Rd`) and a classification routine that lumps Class 3 and 4 together.
- Very long; the section-alternatives table and lessons list are unverifiable extras for this task.

**C**
- Wrong section property: Wpl,y = 106e3 mm3 (and Wel,y = 69e3, Wpl,z = 23e3) are not the tabulated values (353 / 308 / 54.8 cm3); the "Blue Book" citation is therefore false, and the statement that correcting the axis "roughly doubles" resistance is wrong (it is about 7x).
- Wrong adequacy conclusion (FAIL at 3-4x utilisation) that flows directly from the invented modulus.
- Treats the absence of a partial factor as an "error" and hard-codes gamma_G = 1.35 on a load whose basis is unknown, reframing the planted objective.
- Classification numbers are approximate and unsourced; text is partly mangled by line wrapping inside the table.

**D**
- Working is minimal; no explicit unit trace for M_Ed and no statement that the Class 1 assumption was checked.
- Corrected code prints an unqualified "PASS" although the prose says LTB governs if unrestrained; a one-word label change would have closed that gap.
- LTB caveat cites a table value (31-32 kN.m) without stating its basis (C1, load height).

### 4. Ranking (best to worst)

1. A
2. D
3. B
4. C

### 5. Practical significance of the differences

- A and D are both fully acceptable answers to the planted objective: both identify the axis and unit faults directly, use the correct Wpl,y = 353 cm3, arrive at 0.916 utilisation and PASS for cross-section bending, and flag LTB as a conditional caveat. The gap between them is auditability (A shows more working, cites page-level sources, qualifies the PASS label in code); it is not a difference in correctness.
- B is technically competent on the two planted faults and its extra calculations check out numerically, but it fails the anchor's proportionality test: the answer to "is the section adequate?" is inverted by assumptions the prompt did not supply, the input load is altered, and the corrected code is an unsafe-to-drop-in rewrite. Materially worse than A/D for this task even though it contains more engineering.
- C is disqualifying: a fabricated section property attributed to a real source leads to the wrong conclusion. The distance between C and the rest is large and would matter in practice (a reviewer trusting C would reject a section that actually passes the check asked about).

### 6. Manual-review watch-outs

- Verify Wpl,y for 254x102x28 UB against the Blue Book (353 cm3); C's 106 cm3 looks plausible to a non-specialist and is the single most consequential error in the pack.
- Do not let B's length or its correct LTB/deflection arithmetic pull its score up; the anchor rewards direct comparability to the two planted faults and penalises replacing the objective with a design study.
- Check that reviewers notice B's self-weight addition changes M_Ed (90.69 vs 88.89 kN.m) and the no-op M-V interaction line in its code.
- A's LTB aside mentions C1 but does not apply it; confirm reviewers treat this as a minor inconsistency in optional content, not as a core error.
- D's code prints an unqualified PASS; decide whether that counts against change safety or only maintainability (scored here as maintainability/clarity).
- All four responses assume S275; the snippet only gives fy = 275, so this is a fair shared assumption rather than a differentiator.

### `v3-notebook-01` - Square pad footing sizing notebook draft

Label key: A = `tencent-hy4-preview`, B = `gpt5.4-xhigh`, C = `gpt5.6-sol-xhigh`, D = `gemma4:31b-cloud`

## Judgement: v3-notebook-01

### 1. Task summary

Produce a notebook-style draft (alternating Markdown and standard-library Python cells) that sizes the smallest square pad footing from 2.4 m to 3.2 m under three service load cases with axial load plus biaxial moment, using a rigid-footing linear-pressure model, checking only qmax <= 220 kPa and qmin >= 0, and stating the selected size, governing case and omitted checks.

### 2. Score table

| Response | Calculation correctness | Code quality and executability | Engineering judgement | Unit and assumption handling | Notebook traceability and clarity | Completeness of deliverable | Note |
|---|---|---|---|---|---|---|---|
| A | 5 | 5 | 5 | 4 | 5 | 5 | Fully correct (3.0 m, LC2 by uplift, 2.9 m rejected at qmin = -0.410 kPa) with an explicit Mc/I derivation, exact-fraction arithmetic, corner pressures and closed-form diagnostic bounds, marred only by a non-standard e_x = Mx/N naming and a mixed-up Ix/Iy subscript in the field equation. |
| B | 5 | 5 | 4 | 5 | 4 | 4 | Correct and lean: derives q = N/A + My x/Iy + Mx y/Ix at the corners, evaluates all four corners in code, picks 3.0 m with LC2 as the last case to clear uplift, but keeps the model justification and margins discussion thin and shows no executed output. |
| C | 5 | 4 | 3 | 3 | 3 | 3 | Numerically correct and explains the 2.9 m rejection, but quotes only the compact absolute-value formula with no derivation from N/A +/- M y/I, defines no eccentricities or moment sign convention, gives no model justification, prints only PASS/FAIL per size, and hard-codes `assert selected_width_m == 3.0`. |
| D | 3 | 4 | 2 | 3 | 2 | 2 | Pressure functions and search loop would select 3.0 m, but the conclusion leaves the size and governing case as code placeholders, the code identifies the governing case by largest qmax (LC3, not LC2), and there is no search trace, no explanation of why 2.9 m fails and only a Z = B^3/6 assertion instead of a derivation. |

### 3. Top weaknesses per response

**A**
- Defines e_x = Mx/N and e_y = My/N (the reverse of the conventional and reference e_x = My/N, e_y = Mx/N). It is stated and applied consistently, so no numbers are wrong, but the results table's e_x/e_y columns are swapped relative to the reference and could mislead a checker.
- The stated pressure field q(x,y) = N/A + (My/Ix) x + (Mx/Iy) y pairs each moment with the wrong second moment of area; harmless for a square (Ix = Iy) but notationally sloppy in a cell that is meant to show the mechanics.
- Longer than the task needs (Fraction arithmetic, bisection for a continuous bearing bound, eight omitted-check items, caveats). Not wrong, but proportionality is an evaluation criterion.
- "Search output (from execution)" is a hand-condensed trace whose format does not match the print statements in Code Cell 3; the claim of execution cannot be verified from the draft.

**B**
- Justification of the rigid linear model is a single sentence; no discussion of the tight uplift margin at 3.0 m (2.2 kPa) or sensitivity.
- No executed output is shown anywhere; the reader has to trust the numbers quoted in the conclusion.
- Reported values rounded to 1 dp (qmin = -0.4 kPa), which is adequate but coarse for a near-miss of -0.41 kPa.
- Code Cell 1 is a table-printing helper placed before the input data, which slightly muddles the "input data then calculation cells" order.

**C**
- No derivation of the edge-pressure expression from axial plus bending stress; the 6|M|/B^3 term is simply asserted. This was an explicit prompt requirement and the pack's reward item.
- Uses abs(Mx), abs(My) and never defines eccentricities, eccentricity directions or a moment sign convention, so the "define your sign convention and eccentricity directions clearly" requirement is not met and the method cannot tell the reader which corner is critical.
- No justification of why the rigid linear model is appropriate for this preliminary check.
- Search output prints only PASS/FAIL per width without qmax/qmin, so the trap at 2.9 m is visible only in the prose, not in the code output.
- Code Cell 6 asserts the expected answer (`== 3.0`) and the 2.9 m failure, which is circular as a verification step.
- Formatting was lost in transit; content is judged on its merits, but the cell boundaries are harder to audit.

**D**
- Final conclusion never states the selected size in metres or the governing case; it uses literal placeholders `selected_B` and `governing_case`, violating two explicit "must" requirements.
- Governing case is computed as the case with the largest qmax at the selected size (LC3), whereas the selection is governed by LC2 through the uplift check. If executed, the notebook would report LC3 as governing, which is wrong for the selection rule.
- No search trace and no explanation of why 2.4 m to 2.9 m fail; the search loop breaks on the first failing case and discards results.
- Edge-pressure expression is quoted as N/A +/- M/Z with Z = B^3/6 stated, not derived from I; e_x and e_y are defined but never used, and the moment sign convention is vague.
- Section structure does not follow the required six-section order (input data has no heading; "Python calculation cells" is folded into "Analysis Model").
- Omitted-check statement in the conclusion drops sliding and settlement (they appear only in the exclusions list) and the self-weight remark is loose.

### 4. Ranking (best to worst)

1. A
2. B
3. C
4. D

### 5. Practical significance of the differences

- A and B are both technically correct, executable, and land on 3.0 m with LC2 governing via uplift, and both show the derivation from N/A +/- M y/I. A is the stronger audit document (corner pressures, closed-form bounds, margins), but B is closer to a proportionate deliverable with the conventional e_x = My/N naming. The gap between them is one of depth and polish, not correctness; a checker would accept either after a quick read.
- C would give a checker the right answer and the right reason for rejecting 2.9 m, but it fails several explicit prompt requirements (derivation, eccentricity/sign convention, model justification) and hides the sign logic behind abs(). It would need a rewrite of the Markdown before it could be issued, even though the numbers are right.
- D is materially deficient: as written it does not state the footing size or governing case, and its governing-case logic would name LC3. The gap between D and the other three is a correctness-of-deliverable gap, not a style gap.
- None of the four selects 2.9 m by checking qmax only; all four implement the qmin >= 0 check in code.

### 6. Manual-review watch-outs

- A: confirm the reviewer is not confused by the swapped e_x/e_y column labels when comparing to the reference table (A's e_x column equals the reference e_y and vice versa). Check the Ix/Iy subscript slip in Markdown Cell 3. Verify the "from execution" trace by running Code Cells 1 to 5; the Fraction-based code should run, but the bisection in Code Cell 4 mixes Fraction and float.
- B: run the notebook to confirm the search table and governing_selection_case logic (largest first-passing width) prints LC2; no output is shown in the draft.
- C: the pasted response lost cell formatting; confirm the Markdown/code alternation is genuine and not reconstructed. The hard-coded `assert selected_width_m == 3.0` should be read as a test of the expected answer, not evidence of independent derivation. Float equality `candidate["B_m"] == 2.9` works here because both are parsed from the same literal, but it is fragile.
- D: confirm on execution that `governing_case` prints LC3, which contradicts the reference governing case LC2. Check whether the reviewer accepts placeholders in the conclusion as "stating" the size; under the prompt's wording they should not.
- All: the qmin margin at 3.0 m for LC2 is only 2.222 kPa, so any response that rounds to 0 dp or uses a loose tolerance could misreport a pass/fail; only C introduces an explicit tolerance (1e-9 kPa), which is benign.
