# Gemma 4 26B (local) addendum (2026-09-19): blind scoring record

Scope: `gemma4:26b-local` (Ollama `gemma4:26b`, run locally on the user's machine from a plain terminal, no harness, tools or skills) on one task, `v3-notebook-01`, as a free-tier comparison point. The method is the September 2026 refresh procedure (`refresh_2026-09_calibration.md`) as applied to the 2026-09-18 and 2026-09-19 addenda. No earlier score, note or winner was changed. This is a different model from the April `gemma4:31b-cloud` row (Ollama cloud, 31B), which is the low anchor in this pack.

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
