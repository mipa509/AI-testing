# Claude Fable 5.1 addendum (2026-09-19): blind scoring record

Scope: `claude-fable-5.1-high` (Anthropic `claude-fable-5-1`, reasoning effort high, run in Claude Code from the VS Code terminal on a subscription plan; the user withheld the model's identity until scoring was complete and disclosed it afterwards) on three tasks: `v2-deep-02`, `v2-anchor-07` and `v3-notebook-01`. The method is the September 2026 refresh procedure (`refresh_2026-09_calibration.md`) as applied to `deepseek-v4.1-flash`, `glm-5.3-flash` and `tencent-hy4-preview` on 2026-09-18. No April or September score, note or winner was changed.

## 1. Runs

All three runs were made by the user on 2026-09-19 from Claude Code (CLI in the VS Code terminal, subscription plan), one fresh session per task, in a sandbox folder holding the task folder (prompt and context files only). The responses were written as files in the task folder. Figures are from each session's own cost summary, which reports cost, API and wall-clock duration, lines changed and prompt-cache statistics but not token counts; the run records hold the detail.

| Task | API time | Wall clock | Session cost | Requests / cache | Protocol notes |
|---|---|---|---:|---|---|
| `v2-deep-02` | 4 min 14 s | 6 min 11 s | $1.29 | 7, 92% cached | Read the task folder; wrote `review_response.md` (104 lines). |
| `v2-anchor-07` | 6 min 17 s | 9 min 32 s | $1.48 | 11, 95% cached | Wrote `answer.md` (216 lines); full SCI P363 property set quoted, web lookup not reported. |
| `v3-notebook-01` | 6 min 20 s | 11 min 16 s | $2.65 | 12, 93% cached | Wrote `response.md` (486 lines); six code cells. |

## 2. Blind packs

One pack per task, four responses each: the new model, the April high anchor `gpt5.4-xhigh`, the same April low anchor as the September pack, and `gpt5.6-sol-xhigh` as a same-judge-family consistency check; same pack contents and judge instructions as the 2026-09-18 addenda, new seeds. Judges were Claude Fable 5.1 subagents, one per task, reading only the pack. An identity-word scan of the response sections found no hits; no redactions were needed. The orchestrator also did not know the model's identity.

| Task | Seed | A | B | C | D |
|---|---:|---|---|---|---|
| `v2-deep-02` | 20261303 | `gpt5.6-sol-xhigh` | `gpt5.4-xhigh` | `minimax-m2.7-cloud` | `claude-fable-5.1-high` |
| `v2-anchor-07` | 20261308 | `claude-fable-5.1-high` | `gpt5.6-sol-xhigh` | `minimax-m2.7-cloud` | `gpt5.4-xhigh` |
| `v3-notebook-01` | 20261309 | `gemma4:31b-cloud` | `gpt5.4-xhigh` | `claude-fable-5.1-high` | `gpt5.6-sol-xhigh` |

## 3. Calibration

| Task | Low anchor | High anchor MAD / signed | Low anchor MAD / signed | Anchor order preserved? | Sol vs Sept blind MAD / signed |
|---|---|---:|---:|---|---:|
| `v2-deep-02` | `minimax-m2.7-cloud` | 0.50 / -0.50 | 0.67 / -0.67 | yes (April 4.83 vs 3.00; blind 4.33 vs 2.33) | 0.00 / +0.00 |
| `v2-anchor-07` | `minimax-m2.7-cloud` | 0.50 / -0.17 | 0.67 / -0.67 | yes (April 4.83 vs 2.50; blind 4.67 vs 1.83) | 0.33 / +0.00 |
| `v3-notebook-01` | `gemma4:31b-cloud` | 0.33 / -0.33 | 1.17 / -1.17 | yes (April 5.00 vs 3.67; blind 4.67 vs 2.50) | 0.17 / -0.17 |

Overall anchor MAD 0.639 (six rows, 36 criterion pairs), signed -0.583, worst row 1.17 (the `gemma4:31b-cloud` low anchor on the notebook, whose April row is now also read as harsher for the LC3 governing-case slip). The gate (MAD at most 0.5, no row above 1.0) fails on both counts, in the same direction as the September refresh and the earlier addenda: this judge family sits about 0.6 below the April scale. Anchor order was preserved on every task, the high anchor never moved more than 0.5, and Sol reproduced its September blind scores to within a third of a point (identical on the repo review).

| Task | Offset from this pack | September offset | Raw blind (mean) | Adjusted with this pack | Adjusted with September offset |
|---|---:|---:|---:|---:|---:|
| `v2-deep-02` | +0.58 | +0.42 | [5, 5, 4, 5, 5, 4] (4.67) | [5, 5, 5, 5, 5, 5] (5.00) | [5, 5, 4, 5, 5, 4] (4.67) |
| `v2-anchor-07` | +0.42 | +0.08 | [5, 5, 4, 4, 4, 4] (4.33) | [5, 5, 4, 4, 4, 4] (4.33) | [5, 5, 4, 4, 4, 4] (4.33) |
| `v3-notebook-01` | +0.75 | +0.71 | [5, 5, 5, 5, 5, 5] (5.00) | [5, 5, 5, 5, 5, 5] (5.00) | [5, 5, 5, 5, 5, 5] (5.00) |

**Decision:** the September per-task offsets, the user's standing choice for packs that fail the gate (as for `deepseek-v4.1-flash` and `tencent-hy4-preview`). On the repo review the two offset sets differ: this pack's larger offset (+0.58) would round the two 4s up to a straight 5.00, while the September offset leaves the blind row unchanged at 4.67. The September offset is the conservative choice and keeps this row comparable with the other addenda; the anchor and the notebook are unaffected either way.

## 4. Manual review, execution and practicality

- `v3-notebook-01` execution (Python 3.13.2 standard library, six fenced code cells in order): runs end to end, selects `3.0 m`, prints `LC3` as governing for bearing utilisation and `LC2` for uplift, the hand-check assert and the closed-form assert both pass, and the printed matrix matches the expected-output blocks in the draft and the reference values (2.9 m fails LC2 at -0.4 kPa). Eccentricities are defined as `ex = My/N`, `ey = Mx/N`, the reference convention. No override.
- `v2-anchor-07`: both planted faults are found and the corrected numbers were re-checked by hand (`M_c,Rd` 97.1 kNm, utilisation 0.916; `A_v` 1781 mm2, `V_pl,Rd` 282.8 kN; `M_cr` 33.8 kNm from the quoted `I_z`, `I_T`, `I_w` and `C1` 1.132; `chi_LT` 0.32). The headline keeps the planted objective (0.92 PASS if restrained) and states the LTB failure as conditional on an unrestrained 6.2 m span, which is the proportionate framing; the deductions the judge made are for the indicative deflection row built on assumed load factors and for the answer's length and the enlarged corrected script, and they match the evaluator notes. No override.
- `v2-deep-02`: all three planted findings present and grounded; the worked table was re-checked (1470 x 355 / 1000 = 521.9 kNm; 25.5 x 6^2 / 8 = 114.8 kNm; 0.22 vs 185). No override.
- Practicality (unblinded, from the session summaries). The runs were made on a subscription plan, and the user decided on 2026-09-19 that from this addendum on cost is neglected for subscription runs and counted only for API-billed runs (April and September rows are frozen and keep the earlier reading, under which premium models were scored as expensive whatever the route; `gpt5.4-xhigh`, `gpt5.6-sol-xhigh` and `gpt5.6-luna-max` were also subscription captures). The session cost figures ($1.29, $1.48, $2.65; $5.42 in all) are therefore recorded but not scored; on an API-billed route they would have been the most expensive runs in the benchmark. Latency alone, on the reading given to the 2026-09-18 addendum models: `v2-deep-02` = 3 (4 min 14 s API, 6 min 11 s wall, the slowest run recorded on this task but usable; first scored 2 on the cost-inclusive reading, rescored the same day); `v2-anchor-07` = 2 (6 min 17 s API, 9 min 32 s wall, mid-pack; the September floor for slow but usable runs on the anchor, as for every other premium and addendum model); `v3-notebook-01` = 3 (6 min 20 s API, 11 min 16 s wall, the longest v3 run recorded, 24 s behind `glm-5.3-flash` on API time; the notebook runs end to end; as the addendum models and `gpt5.6-luna-max` at three to six minutes rather than the 4 given to the April premium reference, whose latency was not a factor).

| Task | Technical (April scale) | Practicality | Overall mean | April winner (overall) | Winner changed? |
|---|---|---:|---:|---|---|
| `v2-deep-02` | [5, 5, 4, 4, 4.5, 4] (4.42), two-judge mean; judge 1 alone [5, 5, 4, 5, 5, 4] (4.67) | 3 | 4.21 | `gemma4:31b-cloud` (4.71) | no |
| `v2-anchor-07` | [4.5, 4.5, 4, 3.5, 4, 4] (4.08), two-judge mean; judge 1 alone [5, 5, 4, 4, 4, 4] (4.33) | 2 | 3.79 | `gpt5.4-xhigh` (4.43) | no |
| `v3-notebook-01` | [5, 4.5, 4, 4.5, 4.5, 5] (4.58), two-judge mean; judge 1 alone [5, 5, 5, 5, 5, 5] (5.00) | 3 | 4.36 | `gpt5.4-xhigh` (4.86) | no |

On the six technical criteria alone the model ranked first in its blind pack on the repo review (4.67 against `gpt5.4-xhigh` 4.33 and `gpt5.6-sol-xhigh` 4.50) and on the notebook (5.00 against 4.67 and 3.50), and third of the three correct answers on the anchor (4.33 against 4.67 and 4.83) for scope drift. The overall means are pulled down by the practicality column, where latency puts it at the floor for usable runs on the anchor and one step above it on the other two tasks.

## 5. De-anonymised judge replies

Each reply is verbatim; the label key precedes it.

### `v2-deep-02` - Repo review with unit, combination, and reporting traps

Label key: A = `gpt5.6-sol-xhigh`, B = `gpt5.4-xhigh`, C = `minimax-m2.7-cloud`, D = `claude-fable-5.1-high`

### Blind judgement: v2-deep-02

#### 1. Task summary
Responders were asked to code-review (not rewrite) a three-file steel-beam ULS screening package (`load_factors.py`, `beam_capacity.py`, `reporting.py`), returning severity-ordered findings, why each matters in engineering use, the minimum fix direction, and anything deliberately not escalated, with the focus on correctness, units, load combinations and reporting integrity. The evaluator notes name three expected primary findings: the missing 1.50 factor on imposed load, the cm³-treated-as-mm³ error in the resistance (divisor should be 1e3 not 1e6), and `build_review_table()` returning only the lowest-utilisation row because it sorts ascending and slices `[:1]`; early rounding before the PASS/FAIL test is secondary.

#### 2. Score table

| Response | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Note |
|---|---|---|---|---|---|---|---|
| A | 5 | 4 | 5 | 4 | 4 | 5 | Finds all three primary defects with a correct unit derivation and worked check value, adds a well-hedged combination-label finding, and stays within the "short, high-signal" brief; only blemish is slightly off line references. |
| B | 5 | 4 | 5 | 4 | 4 | 4 | Finds all three primary defects with accurate line references and sensible test suggestions, but the "why it matters" text is thin, no numbers are worked, and the unused combination label is not noticed. |
| C | 2 | 2 | 2 | 2 | 3 | 3 | Misses the 1000x unit error outright and explicitly declares the `/1e6` conversion correct, misreads the truncation as returning the worst-case row when it returns the best-case row, and promotes a numerically inert gamma_M0 omission to Critical. |
| D | 5 | 5 | 4 | 5 | 5 | 4 | Finds all three primary defects, verifies them with a fully correct worked example, explains the conservative/unconservative interaction between them and how a partial fix would make the tool more dangerous; the review is longer than the brief asked for and findings 6-7 edge toward scope creep. |

#### 3. Top weaknesses per response

**A**
- Line references are wrong for `reporting.py` (cites 14-15; the sort/slice is at 17-18) and `load_factors.py` (cites 6-7; it is 5-6), which weakens auditability slightly.
- The combination-label finding (Medium) is inferential; it is appropriately hedged, but it rests on an assumption about what inputs the package might receive rather than on anything in the three files.
- No test or regression-check direction is given for any fix, unlike B and D.
- Ranks the 1000x unit error "High" rather than Critical; defensible because it is conservative and self-revealing, but it is still a release-blocking defect that makes every output wrong.

**B**
- The shortest review: each "why it matters" is one sentence, no worked numbers, so a reader cannot cross-check the 1000x claim or the magnitude of the gamma_Q shortfall from the review alone.
- Does not notice that `row["combination"]` is reported but never used in the calculation, which is a reporting-integrity point squarely within the stated focus.
- Not-escalated section is minimal (one item) and does not mention the KeyError lookup, zero-resistance, or documentation of the simply-supported/UDL precondition.
- Splits severities (two Critical, one High) without explaining why the 1000x resistance error is less severe than the others.

**C**
- Misses the cm³/mm³ unit error entirely, and in the not-escalated table affirmatively states "The `1e6` conversion is correct but opaque". This is the worst possible outcome for a review whose brief is units: it would ship a 1000x resistance error with the reviewer's blessing.
- Misreads `output[:1]` after an ascending sort as returning "the worst-case beam only" (repeated in the severity summary). It returns the least-utilised, i.e. safest, row, so the actual hazard (failures hidden behind a single PASS row) is described backwards.
- Escalates the absent gamma_M0 to Critical while conceding in the same finding that under the UK NA it changes nothing; contains the incoherent line "Design resistance is overstated by a factor of 1.0"; invents an EN 1993-1-1 compliance requirement not stated in the prompt.
- Rounding finding is muddled: says exact 1.00 fails "because Python float arithmetic rarely lands precisely on 1.0", then asserts "an exactly-at-limit beam should fail by most design philosophies anyway" (the usual convention is utilisation <= 1.0 passes).
- Shallow reading elsewhere: claims "No type hints on function signatures" when every function is annotated; calls wL²/8 a "fixed-end-moment formula".

**D**
- Length and breadth exceed the "short, high-signal review" constraint: seven findings, a worked example, an interaction section and a release-gate section. All content is defensible, but findings 6 (gamma_M0 and class guard) and 7 (provenance columns) go beyond minimum-fix review into design recommendations.
- Finding 4 (combination label) is graded HIGH on inference about inputs the files do not show; A graded the same point Medium, which is more proportionate.
- References "prompt.md" and assumes Eurocode 3 framing; both are stated as assumptions and are consistent with the 1.35/1.50 factors, but they are still assumptions the responder introduced.
- Option (a) of the finding-4 fix (dispatch on combination string with a factor table) is a larger change than the task's "minimum fix direction" implies, though option (b) is offered as the smaller alternative.

#### 4. Ranking (best to worst)
1. **D** — every primary defect found and numerically verified (all figures in its worked table check out: 25.5 vs 21.5 kN/m, 114.8 vs 96.8 kNm, 521.9 vs 0.522 kNm, 0.22 vs 185), plus the only response to reason about how the three bugs interact and why a partial fix is more dangerous than the current state.
2. **A** — all three primaries with a correct dimensional derivation and a check value, proportionate severities, a sensible combination-label observation and a tight not-escalated list; loses only on line-reference accuracy and absence of test guidance.
3. **B** — all three primaries, accurate citations, good test suggestions, but too terse to be self-auditing and blind to the unused combination label.
4. **C** — actively wrong on two of the three primaries (denies the unit error, inverts the truncation hazard) and inflates a no-op gamma_M0 point to Critical; formatting is tidy but the substance would mislead a release decision.

#### 5. Practical significance
D, A and B would all stop the release: each identifies the three defects that make every output row wrong, and each gives a correct minimum fix. The gap between them is in auditability and depth (D's worked example and interaction analysis, A's derivation, B's terseness), not in outcome; a team acting on any of the three would land in the same safe place. C is materially different: acting on C would fix the gamma_Q omission and remove the `[:1]` slice, but the 1000x resistance error would remain, with the review on record saying the conversion is correct, and the reporting fix would be motivated by a backwards description of the hazard. That is a release-blocking difference, not a stylistic one.

Manual-review watch-outs: verify D's numeric table independently if it is being used as evidence (I checked it and found no errors); note that A's line numbers do not match the supplied files; treat C's "1e6 is correct" statement as the decisive disqualifier rather than its otherwise polished structure.

### `v2-anchor-07` - EC3 planted-error trap (historical anchor)

Label key: A = `claude-fable-5.1-high`, B = `gpt5.6-sol-xhigh`, C = `minimax-m2.7-cloud`, D = `gpt5.4-xhigh`

## Blind judgement: v2-anchor-07

### 1. Task summary

The responders were asked to review a short Python snippet checking the EC3 bending resistance of a simply supported 254x102x28 UB under a 18.5 kN/m UDL over 6.2 m, find the errors, correct them, show working, cite section-property sources, and state adequacy. The planted faults are (1) the minor-axis modulus `Wpl_z` used where major-axis `Wpl_y` is needed, and (2) the missing N·mm to kN·m conversion (a 10^6 factor). The correct outcome is M_Ed = 88.9 kN·m, M_c,Rd = 353e3 x 275 / 1e6 = 97.1 kN·m, utilisation 0.92, cross-section bending PASS (with the caveat that this is not a member check unless the compression flange is restrained).

### 2. Score table

| Response | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Note |
|---|---|---|---|---|---|---|---|
| A | 5 | 5 | 4 | 4 | 4 | 4 | Both planted faults found and correctly fixed with verifiable hand working and Blue Book values, but the answer expands into shear, full LTB, classification and a speculative deflection check built on assumed load factors, well beyond the snippet review that was asked for. |
| B | 5 | 5 | 5 | 5 | 5 | 4 | Both faults identified and corrected, 0.916 PASS stated with explicit scope, minimal corrected script that stays close to the original, LTB flagged proportionately via tabulated values; only the unverifiable page-number citations and heavy LaTeX cost it. |
| C | 1 | 2 | 1 | 1 | 3 | 3 | Names the two planted faults conceptually but substitutes a fabricated Wpl,y = 106 cm³ (actual 353 cm³), invents load factoring, and arrives at the wrong adequacy verdict (FAIL at 3–4x) with a recommendation to upsize the section. |
| D | 5 | 5 | 5 | 4 | 4 | 5 | Concise, correct identification and fix of both faults, correct 0.916 PASS, minimal diff on the script, LTB caveat noted with tabulated values; thinner on working and the script still prints an unqualified PASS. |

### 3. Top weaknesses per response

**A**
- Scope drift: the deflection check invents SLS loads by dividing the ULS load by 1.35–1.5 and then reports "Likely FAIL" in the adequacy table; this is exactly the kind of extra assumption the anchor penalises, and it dilutes the headline.
- Length and structure are disproportionate to a snippet review; a reader must go through classification, shear, M_cr and deflection before reaching the two-line fix.
- Corrected script grows from a bending check into a bending-plus-shear script with additional hardcoded section geometry, increasing surface area for the colleague to maintain.
- Minor: "Chartered Engineer review required" boilerplate adds nothing to the technical content.

**B**
- Cites specific PDF page numbers (p.72, p.205, p.231, pp.35–36) that cannot be verified from the pack; if wrong, they are overconfident claims.
- Body is LaTeX-heavy, which reads poorly in plain-text review contexts.
- Shear and LTB are taken purely from tables rather than shown; acceptable for proportionality but less auditable than A.

**C**
- Wrong section property: Wpl,y = 106e3 mm³ is not the tabulated value (353e3 mm³); the resulting M_Rd = 29.15 kN·m is off by a factor of ~3.3 and the FAIL verdict is wrong.
- Adds an unrequested load-factor assumption (γG = 1.35 on the whole load), changing the design problem rather than reviewing the given one.
- Other quoted properties (Wel,y ≈ 69e3, Wpl,z ≈ 23e3) and classification ratios (c/t ≈ 6, d/t ≈ 39) are also wrong, indicating the source was not actually consulted.
- Recommends a larger section based on the incorrect result, which would cause a real design error if acted upon.

**D**
- Working is terse; no classification check, no shear check, and LTB is only described qualitatively with quoted table values.
- Corrected script prints an unconditional "STATUS: PASS" even though the prose says this is only valid for a restrained beam; B's script labels the scope explicitly.
- Assumptions are listed but not justified (e.g. why Class 1 holds).

### 4. Ranking (best to worst)

1. **B** — direct, correct, proportionate fix of both planted faults with a clearly scoped adequacy statement and a minimal-diff script.
2. **D** — equally correct on the planted objective and cleanest script diff, but thinner working and a less carefully scoped PASS print.
3. **A** — fully correct and the most auditable working, but marked down for drifting into a speculative deflection verdict and a three-page answer to a snippet review.
4. **C** — fails the anchor objective: fabricated section property and invented load factoring produce the wrong adequacy conclusion.

### 5. Practical significance

The gap between B, D and A is small in practice: all three find both planted faults, use the correct Wpl,y = 353 cm³, produce 97.1 kN·m and 0.92 utilisation, and give the same restrained/unrestrained caveat. A reviewer would accept any of them; the ordering reflects proportionality and scope discipline, not correctness. The gap to C is decisive: C would tell the colleague the beam fails by 3–4x and needs upsizing, which is a false result arising from an untraceable section property. For the anchor's purpose, C is the only response that materially fails.

### 6. Manual-review watch-outs

- B's page-number citations into SCI P363 should be spot-checked; correct values but wrong pages would still be an overconfidence issue.
- A's "Likely FAIL" deflection row in the adequacy table is built on assumed load factors and should not be read as a finding.
- D's corrected script still prints a bare PASS; if a reviewer weights script-level scoping heavily, D and B might swap on maintainability.
- C's wrong value (106 cm³) does not correspond to any property of this section that I can identify; treat all of C's numbers as unverified.

### `v3-notebook-01` - Square pad footing sizing notebook draft

Label key: A = `gemma4:31b-cloud`, B = `gpt5.4-xhigh`, C = `claude-fable-5.1-high`, D = `gpt5.6-sol-xhigh`

## Blind judgement: v3-notebook-01

### 1. Task summary

The responders had to produce an ordered Markdown/Python notebook draft (six mandated sections, standard-library Python only) that sizes the smallest square pad footing between 2.4 m and 3.2 m (0.1 m steps) for one column under three service load cases (N + biaxial M), checking only bearing pressure (qmax <= 220 kPa) and no-uplift (qmin >= 0) with a rigid-footing linear-pressure model, showing the derivation of the edge-pressure expression from axial plus bending stress, defining sign conventions and eccentricities, keeping units consistent, and stating the selected size and governing case. The expected answer is 3.0 m x 3.0 m governed by LC2 uplift (2.9 m fails with qmin = -0.41 kPa despite acceptable qmax).

### 2. Score table

| Response | Calculation correctness | Code quality/executability | Engineering judgement | Unit/assumption handling | Notebook traceability/clarity | Completeness of deliverable | Note |
|---|---|---|---|---|---|---|---|
| A | 3 | 3 | 2 | 3 | 2 | 2 | Correct formula and search logic reach 3.0 m, but the governing case is derived from qmax only (giving LC3, not LC2), the conclusion cell contains variable-name placeholders instead of numbers, and no candidate sweep or 2.9 m rejection is shown. |
| B | 5 | 4 | 4 | 5 | 5 | 5 | Full derivation from q = N/A + My*x/Iy + Mx*y/Ix with all four corners evaluated in code, correct 3.0 m / LC2 with the 2.9 m near-miss explained, clean six-section structure; slightly dense selection code and no discussion of the thin uplift margin. |
| C | 5 | 5 | 5 | 5 | 5 | 5 | Complete Navier derivation with kern validity limit, hand-check cell, full pass/fail matrix with failure-type flags, closed-form cross-check (B_min = 2.914 m), correct 3.0 m / LC2, and reviewer-grade commentary on margins and self-weight direction; long but well organised, with some loosely placed code citations. |
| D | 5 | 4 | 3 | 3 | 3 | 3 | Numerically correct throughout with correct 3.0 m / LC2 and explicit 2.9 m rejection, but quotes the compact 6|M|/B^3 formula without the required derivation, never defines ex/ey or moment directions, and gives no justification of why the model suits a preliminary check. |

### 3. Top weaknesses per response

**A**
- Governing case is chosen by the largest qmax in the results cell (`if q_max > max_q_found: governing_case = lc_name`), which returns LC3; the sizing is actually governed by LC2 uplift. This is the "qmax-only" reasoning pattern the evaluator is asked to flag, applied to governing-case identification rather than size selection.
- Final conclusion Markdown reports `selected_B`, `governing_case`, `max_q_found` as literal backticked variable names, so the notebook never states "3.0 m" or "LC2" in prose; the prompt explicitly required both to be stated.
- No per-candidate sweep output and no explanation of why 2.4-2.9 m fail; the search `break`s on first failure, so the reader cannot see which criterion or case rejected each width.
- Section order and labelling deviate from the brief (no "Input data" Markdown section, code cells not labelled, model section inserted between 1 and the search); the derivation stops at Z = B^3/6 rather than starting from N/A ± M*y/I.
- Sign convention is nominal ("positive moments about the x and y axes") without saying which corner is most compressed; units (kN/m^2 = kPa) never stated.

**B**
- `next(row for row in search_results if row["all_ok"])` and the nested `next` inside a comprehension are correct but dense and would raise an unhandled StopIteration if no candidate passed; no guard.
- Model justification is one sentence ("captures the first-order effect"); no mention of the kern/full-contact validity condition that makes the linear model self-consistent.
- Conclusion does not comment on the small LC2 uplift margin (2.2 kPa) or the direction of the self-weight effect, which a preliminary sizing note would normally flag.
- Search table shows only the worst qmax/qmin case per width, not all three cases (acceptable but less auditable than a full matrix).

**C**
- Length is well beyond what the brief needs (six code cells, expected-output blocks, closed-form bisection verification); still organised, but proportionality is marginal.
- Some code citations are loosely placed (e.g. describing a permissible-pressure check as an "EN 1997-1 §6.5.2 serviceability-type verification", and citing "Annex D commentary" for the linear-pressure model); decorative rather than wrong-answer-producing, but an overconfident touch.
- `raise SystemExit` in Code Cell 5 is an unusual notebook idiom (harmless in IPython, abrupt in a script).
- Uses absolute moments; justified for a doubly symmetric square, but it means the code cannot report which corner governs for signed inputs (B's four-corner evaluation is more general).

**D**
- Omits the required "show briefly how your edge-pressure expression is obtained from axial stress plus bending stress": the Markdown goes straight to q = N/B^2 ± 6|Mx|/B^3 ± 6|My|/B^3 with no A, I, Z or corner-coordinate step.
- Never defines eccentricities ex = My/N, ey = Mx/N or the direction each moment shifts the resultant; sign convention is limited to "N and q positive in compression" and "moments act about the centroidal axes". The prompt asked for eccentricity directions explicitly.
- No explanation of why the rigid linear model is appropriate for a preliminary check (only that it is assumed).
- Search summary prints pass/fail per width only, so a reader cannot see from the output which case/criterion rejects 2.4-2.9 m (the Markdown asserts the LC2 -0.41 kPa result but the code does not display it); Code Cell 6 hard-codes `assert selected_width_m == 3.0`, which is verification-by-answer rather than a generic check.
- Uses |Mx|, |My| without stating why absolute values are legitimate.

### 4. Ranking (best to worst)

1. **C** – fully correct, derivation from first principles with kern validity, independent hand and closed-form cross-checks, and the only response that discusses the thin uplift margin and self-weight direction; its only costs are length and some loose citations.
2. **B** – fully correct and unusually transparent (four-corner evaluation straight from the stress formula, governing case derived from first-passing width per case), with a clean six-section structure; just less depth of engineering commentary and slightly dense code.
3. **D** – numerically correct with the right answer and governing case, but misses three explicit prompt requirements (derivation, eccentricity/sign definitions, model justification) and shows only pass/fail in the sweep.
4. **A** – reaches 3.0 m by valid logic but reports the wrong governing case (LC3 via qmax), leaves the conclusion as unfilled placeholders, provides no candidate sweep or 2.9 m explanation, and deviates from the required section structure.

### 5. Practical significance

C and B are both usable as-is by a checking engineer; the gap between them is depth of verification and commentary, not correctness, and a reviewer would accept either. D would need light editing (add the derivation, define ex/ey and moment directions, justify the model) before it satisfies the brief, but its numbers and decision are trustworthy. A is materially weaker: a reviewer reading its conclusion would be told the wrong governing case and would have to run the code to learn the selected size, so it would be sent back for rework despite arriving at 3.0 m.

### Manual-review watch-outs

- None of the four responses selected 2.9 m by checking qmax only; all search loops apply both criteria. However, A's governing-case logic is qmax-only and yields LC3, which is the same failure mode shifted to reporting.
- C's expected-output blocks were spot-checked (LC1/LC3 at 2.4 m, LC2 kern ratio 0.1619, B_min uplift 2.914 m, bisection bearing widths) and match the reference model; no fabricated numbers found.
- D's Markdown table values (122.22/20.00/13.33 etc.) match the reference at 3.0 m.
- B and C use `list[...]`/`tuple[...]` style or `itertools`/`dataclasses`; all are standard library, C requires Python 3.9+ for built-in generic hints.

## 6. Second judge from a different model family (2026-09-19)

Because the first judge, the orchestrator and the model under test are all Claude models, the user ran the same three packs (unchanged, same A to D labels) through a judge from a different model family, one fresh chat per pack: pack only, no web, no code execution, no vendor guessing, six integer scores in the pack's column order. The judge was GPT-6 Astra at reasoning effort xhigh, run in the Codex VS Code extension (one fresh session per pack, agent mode, reading only the prompt and the named pack). The replies were de-anonymised with the recorded mapping. At first no score was changed on the strength of this comparison; the user then decided to record the two-judge mean (section 7), and the section 4 table shows both.

| Task | Response | April | Judge 1 (Claude) | Judge 2 (other family) | J2 - J1 |
|---|---|---:|---:|---:|---:|
| `v2-deep-02` | `claude-fable-5.1-high` | - | 4.67 | 3.17 [4, 4, 3, 2, 3, 3] | -1.50 |
| `v2-deep-02` | `gpt5.6-sol-xhigh` | - | 4.50 | 4.67 [5, 5, 5, 4, 5, 4] | +0.17 |
| `v2-deep-02` | `gpt5.4-xhigh` | 4.83 | 4.33 | 5.00 [5, 5, 5, 5, 5, 5] | +0.67 |
| `v2-deep-02` | `minimax-m2.7-cloud` | 3.00 | 2.33 | 1.50 [1, 2, 1, 1, 2, 2] | -0.83 |
| `v2-anchor-07` | `claude-fable-5.1-high` | - | 4.33 | 3.83 [4, 4, 4, 3, 4, 4] | -0.50 |
| `v2-anchor-07` | `gpt5.6-sol-xhigh` | - | 4.83 | 4.83 [5, 5, 5, 4, 5, 5] | +0.00 |
| `v2-anchor-07` | `gpt5.4-xhigh` | 4.83 | 4.67 | 4.67 [5, 5, 4, 4, 5, 5] | +0.00 |
| `v2-anchor-07` | `minimax-m2.7-cloud` | 2.50 | 1.83 | 1.83 [2, 2, 1, 1, 2, 3] | +0.00 |
| `v3-notebook-01` | `claude-fable-5.1-high` | - | 5.00 | 4.17 [5, 4, 3, 4, 4, 5] | -0.83 |
| `v3-notebook-01` | `gpt5.6-sol-xhigh` | - | 3.50 | 4.17 [5, 5, 4, 3, 4, 4] | +0.67 |
| `v3-notebook-01` | `gpt5.4-xhigh` | 5.00 | 4.67 | 5.00 [5, 5, 5, 5, 5, 5] | +0.33 |
| `v3-notebook-01` | `gemma4:31b-cloud` | 3.67 | 2.50 | 3.50 [4, 4, 3, 4, 3, 3] | +1.00 |

Judge 2 against the frozen April anchors: MAD 0.500, signed -0.389, worst row 1.50 (`minimax-m2.7-cloud` on the repo review, read 1.5 points below April). The gate fails on the worst row only; the high anchor is reproduced to within 0.17 on every task.

Judge 2 minus judge 1, mean of the six-criterion means: +0.22 over the nine rows that are not the model under test (level or more lenient), -0.94 over the three Fable rows (lower on every task: -1.50 on the repo review, -0.50 on the anchor, -0.83 on the notebook). Rankings: judge 2 keeps the anchor order on every task and agrees with judge 1 on the EC3 anchor (Fable third of the three correct answers), but moves Fable from first to third on the repo review (behind `gpt5.4-xhigh` and `gpt5.6-sol-xhigh`) and from first to second on the notebook (behind `gpt5.4-xhigh`).

Read of the disagreement, from the two judges' stated reasons:

- On the repo review, judge 2 scored the terse `gpt5.4-xhigh` review a straight 5.00 while noting it has no worked numbers, and marked the Fable review down to 2 on engineering judgement for categorical wording ("for every row", "accidentally safe state"), for treating the combination label as evidence of intended dispatch, for calling the rounding effect unpredictable when the only effect under the code's strict less-than test is a conservative false failure, and for findings 6 and 7 and the release gate turning unestablished requirements into required changes. The rounding point is correct and judge 1 missed it; the others are the proportionality and inference points judge 1 also made, weighed much more heavily. Judge 2 confirmed the worked table.
- On the anchor, judge 2's deductions are the ones judge 1 made (the assumed-load deflection row, the unsupported restraint-spacing remark, the enlarged script) plus a hand-working line in the shear check that omits the division by 1000 while the printed result is right. Half a point lower, same rank.
- On the notebook, judge 2 kept the 5 on calculation correctness and completeness and took points on engineering judgement for two assurances it found unsupported (that ignoring corner redistribution is conservative for `q_max`, and that the self-weight effects are modest without thickness data), for the EN 1997-1 6.5.2 inconsistency judge 1 noted without deducting, and for two consecutive code cells with no Markdown between them. It still ranked the draft second and usable.

What the pattern can and cannot show: judge 2 is at least as lenient as judge 1 on every response it could be compared on, and lower only on the Claude model's three responses. That is consistent with same-family favouritism in judge 1, and it is also consistent with judge 2 systematically preferring terse responses (its top-ranked response on each task is the shortest correct one, and its Fable deductions are mostly about scope, wording and assurances rather than errors). Two judges cannot separate those explanations. A third judge from a third family, or a pooled panel, would.

For reference only, the two-judge mean of the Fable technical rows would be 3.92 / 4.08 / 4.58 on the blind scale before any offset; the September offsets on the same three tasks are +0.42 / +0.08 / +0.71. The recorded scores remain judge 1's, under the standing rule that every other model in the repo was scored by a single judge of the same family.

### Judge 2 replies, de-anonymised (verbatim)

#### `v2-deep-02`

Label key: A = `gpt5.6-sol-xhigh`, B = `gpt5.4-xhigh`, C = `minimax-m2.7-cloud`, D = `claude-fable-5.1-high`

##### 1. Task summary

Review the three supplied Python modules for major-axis steel beam ULS screening, prioritising calculation, unit, combination and reporting defects, explaining their engineering consequences and minimum fixes, and identifying issues deliberately left outside the review scope without rewriting the package.

##### 2. Score table

| Response | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Note |
|---|---|---|---|---|---|---|---|
| A | 5 | 5 | 5 | 4 | 5 | 4 | Correctly identifies and safely addresses all three primary defects, but elevates a conditional combination-contract concern and gives inaccurate reporting line references. |
| B | 5 | 5 | 5 | 5 | 5 | 5 | Provides a focused, accurate review of all primary defects with proportionate fixes and sensible treatment of screening assumptions. |
| C | 1 | 2 | 1 | 1 | 2 | 2 | Misses the factor-of-1000 resistance error, reverses the reporting selection's meaning and proposes an unsafe acceptance fix while escalating an unsupported standards issue. |
| D | 4 | 4 | 3 | 2 | 3 | 3 | Explains all primary defects and their arithmetic well, but weakens the review with categorical overclaims, speculative release requirements and potentially disruptive interface changes. |

##### 3. Top weaknesses per response

**A**

- Finding 5 escalates the unused `combination` label to Medium without evidence that different labels require different factors: rows could already contain the appropriate action components under a single supported expression; its conditional wording and request to define the contract appropriately limit this concern.
- The reporting references are inaccurate: ascending sorting and truncation are at lines 17–18, not 14–15; the combination label is at line 12, not line 10; and the status comparison is at line 14, outside the cited 7–11 range.
- The governing-summary alternative, “globally or per member,” leaves the required coverage unresolved; returning all rows is sound, but a summary needs an explicit contract and a check that distinct members and combinations are represented as intended.

**B**

- Finding 4's wording, “uses `< 1.0` rather than the raw value,” does not cleanly distinguish the comparison operator from the rounded operand; the subsequent minimum fix is nevertheless correct.
- Regression tests are suggested for load factoring and resistance, but not for the ascending-sort/truncation defect; a mixed PASS/FAIL, multiple-member report case would strengthen protection of the most consequential reporting behaviour.
- The “Not Escalated” paragraph treats `wL²/8` and omitted stability checks as scope assumptions without explicitly recommending that the simple-support, full-span UDL and screening limitations be documented. These are minor improvement opportunities, not missing primary findings.

**C**

- It explicitly states that “the `1e6` conversion is correct” and leaves that divisor in its proposed resistance fix. This misses a primary finding: `cm³ × MPa` requires division by `1e3` to give kNm, so the supplied resistance is 1000 times too small.
- Finding 3 and the severity summary call the retained row the “worst-case beam.” Ascending sorting retains the lowest utilisation, potentially hiding governing failures; removing the slice is a valid fix, but the explanation reverses the engineering hazard.
- Changing the status expression to `util <= 1.0` while retaining rounding permits a raw utilisation of `1.004` to round to `1.00` and PASS. Increasing rounding precision also leaves classification dependent on presentation. Exact unity fails in the original code because of `<`, not because floating-point arithmetic rarely reaches unity.
- The Critical Eurocode partial-factor finding assumes an unspecified standard and national annex, conflates elastic analysis with the value of `γ_M0`, and claims a factor of 1.0 overstates resistance. The assertion that adding a factor requires changing every call site also ignores the centralised resistance function and its own proposed default argument.
- “No type hints on function signatures” contradicts the supplied annotations, while “simply supported fixed-end-moment formula” confuses the support model. These statements further undermine confidence in the repository reading.

**D**

- The opening assertion that all three blockers independently give wrong answers “for every row” is too broad: omitting the Q factor has no effect when Q is zero, and truncation need not affect a single-row input. “Every failing member is silently dropped” is also false when the minimum-utilisation row itself fails.
- “Today ... that row says FAIL” and “accidentally safe state” are not guaranteed: zero or sufficiently small demand can still pass despite the resistance error. The warning about correcting resistance while leaving other defects is valuable, but the claimed current safety is unsupported.
- Finding 4 treats a combination label as proof that dispatch among 6.10, 6.10a/b, accidental and SLS rules was intended. The supplied contract establishes none of this; dropping the `combination` column could remove traceability and break consumers, while adding dispatch could reinterpret existing rows.
- Finding 5 claims rounding moves the boundary “in an unpredictable direction.” With the existing rounded-value `< 1.0` rule, the demonstrated error is conservative false failure near unity; floating-point tie behaviour does not establish false passes in this code. Its proposed raw-value classification is correct.
- Findings 6–7 and the release gate turn unestablished Eurocode, section-class and output-schema requirements into required changes. Documentation and additional report values could help, but their necessity is not demonstrated; the further claim that LTB “will govern” for an unrestrained beam of the example span cannot be established from the supplied information.

##### 4. Ranking

1. **B** — Best balance of complete primary-defect detection, correct fixes, restraint and clear engineering consequences.
2. **A** — Equally strong on the primary calculations and reporting defect, with slightly weaker proportionality and source references.
3. **D** — Correct core diagnosis and useful numerical illustration, diminished by unsupported certainty and unnecessary expansion of the release scope.
4. **C** — Unreliable on the central unit and reporting checks, with a proposed change that can introduce false passes.

##### 5. Practical significance

A checking engineer could act on B's and A's primary findings as delivered, confirming the reporting contract and acceptance convention during implementation. D's first three fixes are also actionable, but its additional release requirements need independent justification. C requires substantial re-review before any changes are adopted. The decisive differences concern hidden governing failures, understated imposed-load demand and a resistance error of three orders of magnitude; A and B differ much less materially from each other.

##### 6. Manual-review watch-outs

- Numerical cross-checks support A's example: `1000 × 355 / 1000 = 355 kNm`, whereas the code gives `0.355 kNm`. D's example gives loads of 25.5 versus 21.5 kN/m, moments of 114.75 versus 96.75 kNm, and resistance of 521.85 versus 0.52185 kNm; its displayed utilisations of about 0.22 and 185 and 15.7% demand shortfall are consistent.
- The 1000-fold utilisation increase describes the resistance defect in isolation. The missing Q factor partly offsets it in the combined calculation; the defects do not cancel or justify treating the package as safe.
- Confirm the intended report coverage, characteristic versus already-combined input loads, and meaning of combination labels before accepting claims about additional combination logic or changing the output schema.
- Confirm the intended equality convention separately from the definite need to classify using unrounded utilisation; C's suggested rounded-value `<=` fix is unsafe regardless of whether equality itself should pass.
- No governing standard, national annex, section class or restraint data is supplied. D's approximate named-section properties and C/D's standards-specific assertions were not externally verified and receive no additional credit.
- This judgement uses only the supplied pack and manual arithmetic; no response code was executed. The repository context supplies the requested Python files, so answering despite the original prompt's instruction to wait for those files is not a defect.

#### `v2-anchor-07`

Label key: A = `claude-fable-5.1-high`, B = `gpt5.6-sol-xhigh`, C = `minimax-m2.7-cloud`, D = `gpt5.4-xhigh`

##### 1. Task summary

Review the EC3 beam-check snippet, correct the planted minor-axis property and N·mm-to-kN·m conversion faults, provide sourced section properties and corrected working, and state the resulting cross-section bending adequacy without inventing a different loading or restraint problem.

##### 2. Score table

| Response | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Note |
|---|---|---|---|---|---|---|---|
| A | 4 | 4 | 4 | 3 | 4 | 4 | Corrects both planted faults and obtains the cross-section PASS, but adds speculative serviceability and restraint advice and contains an omitted conversion in its shear working. |
| B | 5 | 5 | 5 | 4 | 5 | 5 | Provides a traceable, correct repair and explicitly scoped executable PASS, with some unnecessary extension into a conditional buckling calculation. |
| C | 2 | 2 | 1 | 1 | 2 | 3 | Identifies both planted faults but substitutes a conflicting modulus and invents load factoring, producing an unreliable FAIL and unsupported resizing advice. |
| D | 5 | 5 | 4 | 4 | 5 | 5 | Gives a concise, correct repair and cross-section verdict, but leaves the executable PASS unqualified and states an additional buckling verdict with limited supporting assumptions. |

##### 3. Top weaknesses per response

**A**

- Section 3.6 invents a characteristic load range of `18.5/1.35` to `18.5/1.5`, then uses the resulting 28–31 mm deflection to suggest failure against selected limits; neither the action split nor the serviceability criterion is supplied, so this moves beyond the planted-error objective.
- The claim that restraints at “roughly 1.5 m centres or closer” would suffice has no supporting calculation or restraint specification; it is actionable design advice that the supplied problem does not establish.
- “Adequate in bending only if the compression flange is fully laterally restrained” overstates a necessary condition: adequate discrete restraints and a satisfactory member check can also establish adequacy, as A itself subsequently acknowledges.
- Section 3.4 writes `1781 × 275 / 1.732 / 1.0 = 282.8 kN` without the required division by 1,000; the numerical result and subsequent Python conversion are consistent, but this hand-working line omits precisely the kind of unit conversion under review.

**B**

- The additional `M_b,Rd ≈ 31.46 kN·m` and utilisation `2.83` depend on the applicability of the cited buckling table and its boundary conditions, which the prompt does not establish; the final load-height caveat limits the claim but does not validate those assumptions.
- Linear interpolation between the quoted 6.0 m and 7.0 m resistances is labelled approximate, but its accuracy or conservatism is not demonstrated; it should remain an illustration rather than an established design resistance for this beam.
- The final wording “adequate for cross-sectional bending only if its compression flange is adequately restrained” conflates two checks: the calculated cross-section resistance is distinct from whether member stability permits that resistance to be developed.

**C**

- `Wpl_y = 106.0e3 mm³` conflicts with the `353e3 mm³` property consistently identified and sourced by A, B and D; it produces `29.15 kN·m` instead of `97.075 kN·m` and changes the unchanged-load verdict from PASS at approximately `0.916` to FAIL at approximately `3.05`.
- It declares `18.5 kN/m` characteristic and applies `gamma_G = 1.35`, changing the main design moment from `88.8925` to approximately `120.00 kN·m` without evidence that factoring is missing or that the load is wholly permanent; the later already-factored alternative does not repair this unjustified default.
- Its section-property account is internally inconsistent: the opening table calls `49.0e3 mm³` the minor-axis value, while the source section gives approximately `23e3 mm³`; the generic Blue Book attribution does not reconcile these claims or substantiate the major-axis value.
- The conclusion that the beam is “heavily over-stressed” and needs a `305×102×33 UB` or `305×165×46 UB` follows from the defective calculation, and neither suggested replacement is checked for the stated loading or member stability.

**D**

- The corrected code still prints a bare `STATUS: PASS`, without carrying the prose's “cross-section bending only” qualification into the executable result; the ULS-load and restraint assumptions are also absent from its code comments.
- The additional unrestrained-member FAIL relies on a stated `31 to 32 kN·m` resistance without showing the table entries or calculation and without specifying the end-restraint and load-height assumptions needed to apply it.
- “That is only enough if the compression flange is laterally restrained” is too absolute as a description of the cross-section check: adequacy may also be demonstrated through a separate satisfactory LTB check, rather than treating restraint as a prerequisite to the cross-section resistance itself.

##### 4. Ranking

1. **B** — Best combination of correct planted-error repair, explicit working, property attribution and a code output that clearly limits its PASS to cross-section bending.
2. **D** — Equally successful on the central calculation and closely focused on the snippet, but less safe when its standalone code or additional buckling verdict is reused.
3. **A** — Correct on the central calculation, but speculative serviceability and restraint advice reduces proportionality and introduces avoidable technical weaknesses.
4. **C** — Recognises the fault types but fails to deliver a trustworthy corrected result because its replacement property and default loading basis are defective.

##### 5. Practical significance

A checking engineer could use B and D as the basis for the intended snippet correction, and A's core bending correction is also usable after separating it from the speculative extensions. With `Wpl_y = 353e3 mm³` and the supplied load treated as the design load, the working gives `M_Ed = 88.8925 kN·m`, `M_Rd = 97.075 kN·m` and utilisation approximately `0.9157`: a cross-section bending PASS. B's scoped output reduces the chance of mistaking that result for complete member adequacy. C requires substantial correction and could prompt unnecessary rejection or resizing. None of the responses establishes unconditional whole-beam adequacy from the information supplied.

##### 6. Manual-review watch-outs

- The pack supplies no separate reference solution or authoritative numerical property table; its evaluator notes identify the two planted faults. The `353e3 mm³` value is supported by the mutually consistent, attributed claims in A, B and D, but their cited sources were not independently opened or verified.
- A human reviewer should confirm the exact section-table row, axis labels, property values and cited page references before relying on the resistance values; agreement between responses is not independent source verification.
- Check whether `18.5 kN/m` is already the complete ULS design load. Its status is unspecified, so clarification is appropriate, but automatically applying `1.35` is not justified by the prompt.
- Verify actual restraints, end conditions, load application height and the basis of any tabulated buckling resistance before adopting the additional `31–32 kN·m` member capacities or A's suggested restraint spacing.
- No response code was executed; the arithmetic and units were assessed from the supplied text. “Repo comprehension” here concerns the supplied snippet and task scope, since no wider repository context is included.
- The ranking prioritises correction of the two planted faults and the resulting adequacy statement; extra LTB or serviceability calculations are not requirements for a high score and were assessed for their accuracy, qualifications and proportionality.

#### `v3-notebook-01`

Label key: A = `gemma4:31b-cloud`, B = `gpt5.4-xhigh`, C = `claude-fable-5.1-high`, D = `gpt5.6-sol-xhigh`

##### 1. Task summary

Evaluate four notebook drafts for selecting the smallest square footing from 2.4–3.2 m that satisfies service-load bearing and no-uplift checks, with the reference requiring 3.0 m × 3.0 m governed by LC2 because its minimum pressure at 2.9 m is −0.410 kPa.

##### 2. Score table

| Response | Calculation correctness | Code quality and executability | Engineering judgement | Unit and assumption handling | Notebook traceability and clarity | Completeness of deliverable | Note |
|---|---|---|---|---|---|---|---|
| A | 4 | 4 | 3 | 4 | 3 | 3 | The search correctly checks both criteria, but the governing-case logic identifies LC3 and the conclusion leaves the selected size and case as variable names. |
| B | 5 | 5 | 5 | 5 | 5 | 5 | Correct mechanics, explicit directional conventions, an auditable four-corner calculation and candidate search support the correct size and LC2 governing conclusion. |
| C | 5 | 4 | 3 | 4 | 4 | 5 | Correct calculations and a thorough derivation support the selection, but unsupported engineering assurances, inconsistent general sign reporting and minor notebook/code issues weaken the draft. |
| D | 5 | 5 | 4 | 3 | 4 | 4 | Correct calculations and reported results establish the selection, but the required stress derivation, eccentricity directions and model justification are incomplete. |

##### 3. Top weaknesses per response

**A**

- The results cell sets `governing_case` solely through `if q_max > max_q_found`, so the final summary would name LC3; LC3 governs maximum bearing pressure, whereas LC2 governs size through uplift, with reference `qmin = −0.410 kPa` at 2.9 m and `+2.222 kPa` at 3.0 m.
- The conclusion gives literal placeholders `selected_B`, `governing_case` and `max_q_found`, rather than an explicit numerical footing size and named governing case; it also supplies no explanation of why the smaller candidates fail.
- The statement that `q = N/A ± Mx/Zx ± My/Zy` applies “at any point (x, y)” is incorrect: section-modulus terms represent extreme-fibre contributions, not arbitrary coordinates; the derivation never shows `Mx*y/Ix` and `My*x/Iy` or obtains `Z` from `I/(B/2)`.
- “Positive moments acting about” the axes does not identify which pressure edge becomes more compressed, and the unqualified `Mx + My` extrema formula assumes the supplied positive moments; opposite signs would require corner evaluation or absolute moment magnitudes.
- The outline has five numbered sections, places inputs in an unlabelled code cell instead of the requested Input data section, and does not clearly label alternating notebook cells; the calculation code also lacks a no-passing-candidate guard before using `selected_B`.

**B**

- `selected = next(row for row in search_results if row["all_ok"])` has no fallback, so an unsuccessful search would raise an unexplained `StopIteration`; the supplied data do contain a passing candidate, so this is a robustness limitation rather than an execution failure here.
- `max(first_passing_width_by_case, key=first_passing_width_by_case.get)` reports only one selection-governing case if several cases share the same first passing width; LC2 is uniquely governing for the given cases, so the reported result is correct.
- The model discussion does not explicitly distinguish a negative full-contact pressure prediction from physically admissible soil contact pressure or explain the need for a different contact model after separation; the implemented rejection and stated no-uplift criterion nevertheless handle this task correctly.

**C**

- Section 1.2 asserts that ignoring real pressure redistribution is “conservative for q_max,” and the conclusion says `q_min ≥ 0` “guarantees the model's validity”; nonnegative computed pressure establishes full contact within the assumed model, not actual footing rigidity, uniform soil stiffness or conservatism.
- Section 1.1 calls EN 1997-1 §6.5.2 a “serviceability-type verification,” while later sections identify the same clause with ULS bearing resistance; this internal inconsistency and the additional standards attributions are unsupported by the pack and should not increase confidence in the analysis.
- The self-weight discussion calls its bearing effect “slight” and both effects “modest at 0.81 utilisation,” despite having no footing thickness, weight or backfill data; extending the calculation also requires a consistent net-pressure basis rather than an unqualified addition to axial load.
- Section 1.4 defines signed eccentricities and then fixes the maximum at `(+B/2, +B/2)`, while `check_case` stores `abs(My)/N` and `abs(Mx)/N`; these statements coincide for the supplied positive moments but would misreport directions and corner locations for negative moments, although the pressure extrema remain correct.
- `round_up_to_increment` rounds `x / step` internally to nine decimal places despite the reporting-only rounding requirement, and Code Cells 2 and 3 are consecutive without an intervening Markdown cell; neither issue changes the supplied selection, but both depart from the requested notebook discipline.

**D**

- Markdown Cells 1 and 3 state `6|M|/B³` directly without deriving it from `q = N/A ± Mx*y/Ix ± My*x/Iy`, `I = B⁴/12` and corner coordinates; the explicit mechanics-derivation requirement is unmet.
- No cell defines `ex = My/N`, `ey = Mx/N`, their directions or the positive-moment compression edges; saying only that the moments act about centroidal axes does not fulfil the requested directional convention.
- The rigid, linear-pressure assumption is stated but not briefly justified for this preliminary check; the otherwise correct pressure decomposition does not supply that missing explanation.

##### 4. Ranking

1. **B** — Best overall: correct selection, preferred mechanics derivation, clear signs and units, and consistent identification of both selection-governing and bearing-governing cases.
2. **C** — Second on the strength of its mechanics derivation, full candidate matrix and independent sizing cross-check, although its engineering assurances require correction.
3. **D** — Correct and coherent computationally, but omission of the specifically requested derivation and eccentricity conventions places it narrowly behind C despite equal aggregate scores.
4. **A** — Its pressure calculation and search are sound for these inputs, but the wrong governing-case summary and unfinished numerical conclusion materially weaken the deliverable.

##### 5. Practical significance

A checking engineer could act on B as a complete preliminary sizing draft. C and D also establish the correct 3.0 m square selection: C needs qualification of its unsupported engineering claims, while D needs the missing mechanics and directional explanation. A needs its conclusion completed and governing-case logic corrected. The consequential distinction is LC2's uplift rejection at 2.9 m, rather than LC3's acceptable 178.889 kPa maximum pressure at 3.0 m; none of the responses selects 2.9 m by checking bearing alone.

##### 6. Manual-review watch-outs

- Assessment is based solely on the pack and static code inspection; no response code was executed, and no external standards or other files were consulted.
- Reference checks at 3.0 m are `(qmax, qmin)` in kPa: LC1 `(155.556, 88.889)`, LC2 `(153.333, 2.222)` and LC3 `(178.889, 98.889)`; LC2 at 2.9 m is `(166.879, −0.410)`, so a rounded display must not conceal uplift.
- Distinguish the size-governing LC2 uplift condition from the LC3 maximum-bearing condition; A's search itself includes uplift and should not be misclassified as a bearing-only search.
- D explicitly carries a copying-related formatting-loss notice; its scores assess the labelled cell content and do not penalise the enclosing text fence or damaged table/equation formatting.
- C's standards references and physical-model assurances need independent review before reliance; its Python type annotations also assume Python 3.9 or later, while its internal rounding helper does not affect this case's selected size.
- B's listed weaknesses concern extensions or explanatory refinements, not failures on the specified data; D's `1e-9 kPa` comparison tolerance likewise has no material effect on the supplied pass/fail decisions.

## 7. Two-judge mean (user decision, 2026-09-19)

The user read the section 6 pattern as the same-family judge favouring its own model and chose to record Fable's technical rows as the mean of the two judges. Method: each judge is first put on the April scale through its own anchors (judge 1 with the September per-task offsets; judge 2 with the offset implied by its own two anchor rows on that task, since its scale differs from judge 1's), then the two April-scale rows are averaged per criterion and recorded unrounded: a 4.5 marks a criterion where the two judges differ by one point after calibration, and rounding it either way would shift every such criterion in one direction. The dashboard parser and the ranking scripts read the cells as numbers, so half values are safe. Practicality is unchanged. Every other model in the repository keeps its single same-family judge, so this is a targeted correction for the one model whose judge shares its family.

| Task | Judge 1 blind | Sept offset | Judge 1 on April scale | Judge 2 blind | Judge 2 offset | Judge 2 on April scale | Recorded mean |
|---|---|---:|---|---|---:|---|---|
| `v2-deep-02` | [5, 5, 4, 5, 5, 4] | +0.42 | [5, 5, 4, 5, 5, 4] (4.67) | [4, 4, 3, 2, 3, 3] | +0.67 | [5, 5, 4, 3, 4, 4] (4.17) | [5, 5, 4, 4, 4.5, 4] (4.42) |
| `v2-anchor-07` | [5, 5, 4, 4, 4, 4] | +0.08 | [5, 5, 4, 4, 4, 4] (4.33) | [4, 4, 4, 3, 4, 4] | +0.42 | [4, 4, 4, 3, 4, 4] (3.83) | [4.5, 4.5, 4, 3.5, 4, 4] (4.08) |
| `v3-notebook-01` | [5, 5, 5, 5, 5, 5] | +0.71 | [5, 5, 5, 5, 5, 5] (5.00) | [5, 4, 3, 4, 4, 5] | +0.08 | [5, 4, 3, 4, 4, 5] (4.17) | [5, 4.5, 4, 4.5, 4.5, 5] (4.58) |

| Task | Technical (recorded) | Practicality | Overall | Was (judge 1 alone) | April winner (overall) | Winner changed? |
|---|---|---:|---:|---:|---|---|
| `v2-deep-02` | [5, 5, 4, 4, 4.5, 4] (4.42) | 3 | 4.21 | 4.43 | `gemma4:31b-cloud` (4.71) | no |
| `v2-anchor-07` | [4.5, 4.5, 4, 3.5, 4, 4] (4.08) | 2 | 3.79 | 4.00 | `gpt5.4-xhigh` (4.43) | no |
| `v3-notebook-01` | [5, 4.5, 4, 4.5, 4.5, 5] (4.58) | 3 | 4.36 | 4.71 | `gpt5.4-xhigh` (4.86) | no |

Provisional v2 average over Task 2 and the anchor: 4.00 (was 4.21). v3: 4.36 (was 4.71).
