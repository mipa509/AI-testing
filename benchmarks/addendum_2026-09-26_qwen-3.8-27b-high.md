# Qwen 3.8 27B (high) addendum (2026-09-26): blind scoring record

Scope: `qwen-3.8-27b-high` (OpenRouter `qwen/qwen3.8-27b`, reasoning effort high, run by the user from the GitHub Copilot agent chat in VS Code) on all eight tasks: the six v2 primary tasks, the v2 anchor and `v3-notebook-01`. The method is the September 2026 refresh procedure (`refresh_2026-09_calibration.md`) as applied to the 2026-09-18 and 2026-09-19 addenda. No earlier score, note or winner was changed. This is a different model from the April `qwen-3.6plus` row, which is the low anchor in two of the packs.

## 1. Run

The user ran each task in a fresh Copilot agent chat with the model supplied through OpenRouter, in a local sandbox folder (`D:\codex-sandbox`) holding one subfolder per task with only its prompt and context files (no evaluator or reference files). Task 2 had the three `context/*.py` files instead of `context_combined.md`; Task 6's folder held only the prompt and the code was supplied separately. On Task 2 and the anchor the agent wrote its answer to a file in the task folder (`review.md`, `findings.md`); the other deliverables are `response.md`. Latency and token counts are Copilot's per-run figures (the token totals include Copilot's own system prompt and tool definitions, so they sit at 37k to 49k for every task). Costs are differences of the user's cumulative OpenRouter spend, in run order.

| Order | Task | Latency | Tokens (Copilot) | Cost | Cumulative spend |
|---:|---|---|---:|---:|---:|
| 1 | `v2-deep-02` | 1 min 56 s | 40.3k | $0.033 | $0.033 |
| 2 | `v2-anchor-07` | 2 min 5 s | 36.9k | $0.0337 | $0.0667 |
| 3 | `v3-notebook-01` | 8 min 18 s | 48.9k | $0.182 | $0.249 |
| 4 | `v2-deep-01` | 53 s | 37.2k | $0.022 | $0.271 |
| 5 | `v2-deep-03` | 1 min 16 s | 39.1k | $0.037 | $0.308 |
| 6 | `v2-deep-04` | 39 s | 37.2k | $0.021 | $0.329 |
| 7 | `v2-medium-05` | 2 min 59 s | 40k | $0.073 | $0.402 |
| 8 | `v2-medium-06` | 1 min 56 s | 37.9k | $0.039 | $0.441 |

User notes folded into the run records: on `v3-notebook-01` the task "proves tricky for the model again": during the run it calculated sizes wrongly, had B values off and found several of its own errors before finishing; on `v2-medium-05` the agent tried to create a virtual environment and install pandas to evaluate its code, then cleaned up and removed the temporary folder. List price on 2026-09-26: $0.42 input / $3.00 output per 1M tokens (OpenRouter `qwen/qwen3.8-27b`; a rate-limited `:free` variant is also listed).

## 2. Blind packs

Four responses per pack: the new model, the April high anchor `gpt5.4-xhigh`, the April low anchor (the same choice as the Gemma 4 26B addendum) and `gpt5.6-sol-xhigh` as a same-judge-family consistency check; same pack contents and judge instructions as the other addenda, new seeds. The capture note inside Sol's v3 raw output (which names its harness) was stripped from the pack; the neutral formatting line was kept. Judges: one Claude Fable 5.1 subagent per pack, reading only the pack. Identity-word scan of the final packs: no hits.

| Task | Seed | A | B | C | D |
|---|---:|---|---|---|---|
| `v2-deep-01` | 20262601 | `qwen-3.6plus` | `gpt5.4-xhigh` | `gpt5.6-sol-xhigh` | `qwen-3.8-27b-high` |
| `v2-deep-02` | 20262602 | `qwen-3.8-27b-high` | `gpt5.4-xhigh` | `minimax-m2.7-cloud` | `gpt5.6-sol-xhigh` |
| `v2-deep-03` | 20262603 | `gpt5.4-xhigh` | `qwen-3.8-27b-high` | `gpt5.6-sol-xhigh` | `qwen-3.6plus` |
| `v2-deep-04` | 20262604 | `qwen-3.8-27b-high` | `gemma4:31b-cloud` | `gpt5.4-xhigh` | `gpt5.6-sol-xhigh` |
| `v2-medium-05` | 20262605 | `gpt5.6-sol-xhigh` | `gemma4:31b-cloud` | `gpt5.4-xhigh` | `qwen-3.8-27b-high` |
| `v2-medium-06` | 20262606 | `qwen-3.8-27b-high` | `gpt5.6-sol-xhigh` | `gpt5.4-xhigh` | `deepseek-v3.2` |
| `v2-anchor-07` | 20262607 | `gpt5.6-sol-xhigh` | `qwen-3.8-27b-high` | `gpt5.4-xhigh` | `minimax-m2.7-cloud` |
| `v3-notebook-01` | 20262608 | `gemma4:31b-cloud` | `gpt5.6-sol-xhigh` | `gpt5.4-xhigh` | `qwen-3.8-27b-high` |

## 3. Calibration

| Task | Low anchor | High anchor MAD / signed | Low anchor MAD / signed | Anchor order preserved? | Sol vs Sept blind MAD / signed |
|---|---|---:|---:|---|---:|
| `v2-deep-01` | `qwen-3.6plus` | 0.67 / -0.67 | 0.33 / +0.00 | NO (April 4.17 vs 3.67; blind 3.50 vs 3.67) | 0.00 / +0.00 |
| `v2-deep-02` | `minimax-m2.7-cloud` | 0.33 / -0.33 | 0.67 / -0.67 | yes (April 4.83 vs 3.00; blind 4.50 vs 2.33) | 0.00 / +0.00 |
| `v2-deep-03` | `qwen-3.6plus` | 1.00 / -1.00 | 1.17 / -1.17 | yes (April 4.83 vs 3.83; blind 3.83 vs 2.67) | 0.50 / -0.17 |
| `v2-deep-04` | `gemma4:31b-cloud` | 0.67 / -0.67 | 1.17 / -1.17 | tie in April (April 4.83 vs 4.83; blind 4.17 vs 3.67) | 0.00 / +0.00 |
| `v2-medium-05` | `gemma4:31b-cloud` | 0.50 / +0.17 | 1.00 / -1.00 | yes (April 4.00 vs 3.83; blind 4.17 vs 2.83) | 0.08 / -0.08 |
| `v2-medium-06` | `deepseek-v3.2` | 1.00 / -0.33 | 0.67 / -0.67 | yes (April 3.50 vs 2.33; blind 3.17 vs 1.67) | 0.00 / +0.00 |
| `v2-anchor-07` | `minimax-m2.7-cloud` | 0.50 / -0.17 | 0.83 / -0.50 | yes (April 4.83 vs 2.50; blind 4.67 vs 2.00) | 0.33 / -0.33 |
| `v3-notebook-01` | `gemma4:31b-cloud` | 0.00 / +0.00 | 1.00 / -1.00 | yes (April 5.00 vs 3.67; blind 5.00 vs 2.67) | 0.67 / +0.67 |

Overall anchor MAD 0.719 (sixteen rows, 96 criterion pairs), signed -0.573, worst row 1.17 (`qwen-3.6plus` on deep-03 and `gemma4:31b-cloud` on deep-04, both read 1.17 below April). The gate (MAD at most 0.5, no row above 1.0) fails, in the usual direction for this judge family. The deep-01 order flag is a narrow reversal (April 4.17 vs 3.67 for `gpt5.4-xhigh` over `qwen-3.6plus`; blind 3.50 vs 3.67); the deep-04 flag is an April tie. Sol reproduced its September blind scores exactly on five tasks and to within 0.67 everywhere.

**Decision:** the standing rule for a failed gate (September per-task offsets, as for `deepseek-v4.1-flash`, `tencent-hy4-preview`, `claude-fable-5.1-high` and `gemma4:26b-local`) is applied to every task. Adjusted score per criterion = round(blind score + per-task offset), clamped to 1 to 5. On deep-03, deep-04 and v3 the shift saturates at 5 on every criterion.

| Task | Raw blind (mean) | September offset | On April scale (mean) |
|---|---:|---:|---:|
| `v2-deep-01` | [4, 4, 3, 3, 4, 4] (3.67) | +0.67 | [5, 5, 4, 4, 5, 5] (4.67) |
| `v2-deep-02` | [5, 5, 5, 5, 4, 4] (4.67) | +0.42 | [5, 5, 5, 5, 4, 4] (4.67) |
| `v2-deep-03` | [4, 5, 4, 4, 4, 5] (4.33) | +1.42 | [5, 5, 5, 5, 5, 5] (5.00) |
| `v2-deep-04` | [5, 5, 5, 5, 5, 5] (5.00) | +0.96 | [5, 5, 5, 5, 5, 5] (5.00) |
| `v2-medium-05` | [3, 4, 3, 3, 3, 4] (3.33) | +0.42 | [3, 4, 3, 3, 3, 4] (3.33) |
| `v2-medium-06` | [4, 4, 4, 4, 4, 5] (4.17) | +0.17 | [4, 4, 4, 4, 4, 5] (4.17) |
| `v2-anchor-07` | [2, 3, 2, 2, 4, 4] (2.83) | +0.08 | [2, 3, 2, 2, 4, 4] (2.83) |
| `v3-notebook-01` | [5, 4, 5, 5, 5, 5] (4.83) | +0.71 | [5, 5, 5, 5, 5, 5] (5.00) |

## 4. Manual review, execution and practicality

- `v2-deep-01`: Checked against the response text: the signed `max` aggregation is never questioned and `test_build_member_summary_takes_max_moment` asserts the max is used, as the judge says. No override.
- `v2-deep-02`: Checked against the response text: all three planted findings present with the correct fix directions (factor Q, divide by 1000, return the full table). No override.
- `v2-deep-03`: Checked against the response text: the `report_rows` signature has no `*`, as the judge says, and `build_uls_summary` and `RESULT_COLUMNS` are untouched. No override.
- `v2-deep-04`: Checked against the response text: the zero and negative capacity split is preserved for both modules and the status strings are left alone. No override.
- `v2-medium-05`: Execution (2026-09-26, pandas 2.2.3): the revised function runs on a dirty frame; a group whose rows are all invalid disappears instead of reaching the `N/A` branch, and `pd.DataFrame` built from `iterrows` rows keeps the original index labels, confirming both judge points. The run note says the agent created a temporary virtual environment and installed pandas to time its code, then removed it. No override.
- `v2-medium-06`: Execution (2026-09-26, pytest): with the response's own fixed functions, 9 of its 10 tests pass and `test_status_negative_ratio_fails` fails, as the judge says. No override.
- `v2-anchor-07`: Checked against the evaluator notes: the tabulated Wpl,y for 254x102x28 UB is 353 cm3 (M_c,Rd 97.1 kN.m, utilisation about 0.92); the response's 588 cm3 is wrong and unconservative. No web lookup was reported for this run. No override.
- `v3-notebook-01`: Execution (2026-09-26, Python 3.13.2 standard library, the five fenced code cells in order): runs end to end, prints `Selected footing size B = 3.0 m` (the float-accumulated candidate prints as 3.0), and a sweep table matching the hand-typed one with 2.9 m failing LC2 at -0.41 kPa. The governing case is stated in prose only. The user's run note says the model miscalculated sizes and B values during the run and corrected several of its own errors before finishing; the delivered notebook is judged as delivered. No override.

Practicality = 3 on every task. This run was billed through OpenRouter, so cost counts under the rule adopted with the Claude Fable 5.1 addendum. The model was fast (39 s to 2 min on most v2 tasks, 2 min 59 s on medium-05, 2 min 5 s on the anchor, 8 min 18 s on v3) and cheap ($0.021 to $0.073 per v2 task, $0.441 for all eight). A 4 on the six fastest tasks was considered and declined: no paid-API run has scored above 3 on a v2 task (April `qwen-3.6plus`, `gpt5.6-luna-max`, and the three 2026-09-18 addendum models on this same route), and `tencent-hy4-preview`'s near-identical deep-02 run (1 min 59 s, about $0.094) got 3. **User decision (2026-09-26):** score this route consistently, 3 everywhere, including the anchor, where the 2 used for the 6 to 15 minute anchor runs does not apply to a 2 minute run. With 4s, Qwen would have taken the deep-03 and medium-06 wins; with 3s it ties those winners without beating them.

## 5. Results

| Task | Technical (April scale) | Practicality | Overall mean | Winner (overall) | Winner changed? |
|---|---|---:|---:|---|---|
| `v2-deep-01` | [5, 5, 4, 4, 5, 5] (4.67) | 3 | 4.43 | `gpt5.6-sol-xhigh` (4.71) | no |
| `v2-deep-02` | [5, 5, 5, 5, 4, 4] (4.67) | 3 | 4.43 | `gemma4:31b-cloud` (4.71) | no |
| `v2-deep-03` | [5, 5, 5, 5, 5, 5] (5.00) | 3 | 4.71 | `gpt5.6-sol-xhigh` (4.71) | no (tie, not beaten) |
| `v2-deep-04` | [5, 5, 5, 5, 5, 5] (5.00) | 3 | 4.71 | `kimi-k2-thinking` (5.00) | no |
| `v2-medium-05` | [3, 4, 3, 3, 3, 4] (3.33) | 3 | 3.29 | `gpt5.6-sol-xhigh` (4.57) | no |
| `v2-medium-06` | [4, 4, 4, 4, 4, 5] (4.17) | 3 | 4.00 | `gpt5.6-luna-max` (4.00) | no (tie, not beaten) |
| `v2-anchor-07` | [2, 3, 2, 2, 4, 4] (2.83) | 3 | 2.86 | `gpt5.4-xhigh` (4.43) | no |
| `v3-notebook-01` | [5, 5, 5, 5, 5, 5] (5.00) | 3 | 4.71 | `gpt5.4-xhigh` (4.86) | no |

v2 cross-task average over the six primary tasks: 4.26 (criterion means 4.50, 4.67, 4.33, 4.33, 4.33, 4.67, practicality 3.00), third of fifteen behind `gpt5.6-luna-max` (4.48) and `gpt5.6-sol-xhigh` (4.45), ahead of April's `gpt5.4-xhigh` (4.14) and `qwen-3.6plus` (3.74). Anchor 2.86, reported separately. v3 4.71, level with `glm-5.1:cloud` and `deepseek-v4.1-flash` behind `gpt5.4-xhigh` (4.86).

Blind-pack reading: the judge placed `qwen-3.8-27b-high` first in three packs (deep-02, deep-04, medium-06), ahead of both `gpt5.6-sol-xhigh` and `gpt5.4-xhigh`, second in three (deep-01, deep-03, v3) and third in two (medium-05, anchor). Its weak spots are the anchor, where it named both planted errors but invented a major-axis modulus (588 cm3 against the tabulated 353 cm3) and so reported an unconservative 0.55 utilisation, and medium-05, where its rewrite silently drops invalid rows from a pass/fail summary. The run cost $0.441 for all eight tasks.

## 6. De-anonymised judge replies

### `v2-deep-01` - Multi-file bug hunt in a member check pipeline

Label key: A = `qwen-3.6plus`, B = `gpt5.4-xhigh`, C = `gpt5.6-sol-xhigh`, D = `qwen-3.8-27b-high`

#### Blind judgement: v2-deep-01

##### 1. Task summary
Review a three-file pandas beam-check package, find why major-axis utilisations are ~10x too high after a refactor, list secondary risks by severity, design the smallest safe multi-file fix, and name the pre-merge tests.

##### 2. Score table

| Response | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Note |
|---|---|---|---|---|---|---|---|
| A | 4 | 3 | 4 | 3 | 4 | 4 | Nails the 1e2→1e3 root cause with a correct worked table and keeps the patch small, but misses the signed-max envelope and the round-before-status bug, padding instead with a dead zero-capacity guard. |
| B | 4 | 3 | 4 | 3 | 3 | 4 | Correct root cause with a clean dimensional argument and a real catch on rounding-before-status, but misses the envelope/sign issue and the unknown-section guard, and leaves the consistency check as prose only. |
| C | 5 | 5 | 4 | 5 | 4 | 4 | Only response to find the signed-max envelope defect; also catches rounding, mixed sections, NaN loss and the Mz/Wpl_y axis-convention question, with correct hand numbers throughout; patch is somewhat broader than "smallest". |
| D | 4 | 4 | 3 | 3 | 4 | 4 | Broadest secondary sweep (NaN status, unknown section, mixed sections, sort order, γM0, axis naming) but misses the envelope entirely, proposes a test that would lock in the signed-max behaviour, and defers the rounding bug rather than fixing it. |

##### 3. Top weaknesses per response

**Response A**
- Misses the governing-moment envelope: `"Mz_kNm": "max"` is never questioned, so a member with hogging `-120` and sagging `+80` is still checked at 80 kNm.
- Misses that `decorate_status` rounds to 3 dp before assigning PASS/FAIL (1.0004 → PASS).
- Secondary (b) is invented risk: "If `m_rd_kNm` were ever zero (e.g., missing properties)" cannot happen with the supplied library (a missing key raises before the division), so the `return float("inf")` guard is dead code that quietly turns a data error into a FAIL row instead of raising.
- Claims "two lines changed, one guard added" while the diff actually adds two guards; small, but an overconfident summary of its own patch.
- Test list has no envelope/sign case; test 7 (`1.001 → FAIL`) would pass even with the rounding bug present, so it does not probe the boundary it names.

**Response B**
- Misses the signed-max envelope issue; the aggregation is only critiqued for section/row mixing, not for sign.
- Misses the unknown-section guard (raw `KeyError` on any typo or new size).
- The consistency-check and reporting changes are described ("add a consistency check before aggregation", "Round only after status classification") but never shown, so the "smallest safe fix" cannot be audited as written.
- Raising on inconsistent sections per member is a hard behaviour change (spliced members would abort the run) presented without discussing a softer alternative.
- Line references are off by one (`section_library.py:10`, `analysis_pipeline.py:15`) against the supplied files; cosmetic but a sign of loose reading.

**Response C**
- The "smallest safe patch" is not the smallest: rejecting invalid/missing `Mz_kNm` and rejecting multi-section members are both new hard failures added to a pipeline that currently tolerates them; a warning or a flag column would be the safer first step.
- Does not explicitly list the unknown-section `KeyError` guard, one of the two obvious hardening items.
- The proposed aggregation overwrites `Mz_kNm` with `abs()` values while keeping the same column name; the text says to "retain the governing row's sign separately if reports need it" but the snippet does not, so sign information is silently lost in the summary.
- The in-text file references are absolute local paths rendered as links, which clutter an otherwise clean review.

**Response D**
- Misses the envelope defect and actively proposes `test_build_member_summary_takes_max_moment` ("assert the max is used"), which would pin the signed-max behaviour and make the future envelope fix a test failure.
- Sees the rounding-before-status problem but defers it: "1.0004 (rounds to 1.0) → document and assert the intended behaviour ... decide if that's acceptable and pin it in a test". Classifying pass/fail from a rounded value is a defect, not a design choice.
- Introducing a third status value `"DATA"` changes the reporting contract (any consumer that partitions on PASS/FAIL now sees an unexpected label, and it also perturbs the `sort_values(["Status", ...])` order it discusses in 2.4); this is not a "smallest safe" change.
- The γM0 paragraph is garbled: "Fine for S235/S275 ... so it isn't silently applied to S355 where γM0 = 1.0 also holds but fy differs — the library already carries per-section fy, so that part is OK" says nothing actionable.
- Describes the apply as a "`groupby().apply()` pipeline"; it is a plain `DataFrame.apply` on the aggregated summary.

##### 4. Ranking (best to worst)
1. **C** — the only response that finds both planted secondary risks that matter structurally (envelope/sign) plus the rounding bug, with correct numbers (100.65, 178.475, 0.4968) and a sensible refusal to touch the Mz/Wpl_y mapping without a documented convention; docked slightly for a patch broader than asked.
2. **D** — correct root cause and the widest, mostly accurate secondary survey including the unknown-section guard and the axis-naming concern, but it misses the envelope, would enshrine signed max in a test, and treats the rounding bug as optional.
3. **B** — correct root cause with a good dimensional explanation and the rounding catch, but misses envelope and unknown-section guard and leaves half its patch unspecified.
4. **A** — correct root cause and a genuinely minimal patch, but the thinnest secondary analysis, padded by a non-existent zero-capacity risk, with no envelope or rounding coverage.

##### 5. Practical significance
All four responses would fix the reported 10x inflation, so on the headline symptom they are interchangeable. The real difference is in what ships alongside: C is the only one whose patch would stop a hogging-governed member from being under-checked, which is an unconservative (unsafe) error rather than the conservative one the team noticed. B and C would also stop 1.0004 being reported PASS. A and D leave both of those in place, and D's proposed test would make the envelope fix harder to land later. For a code-review deliverable the gap between C and the rest is material; the gap among A, B and D is modest and mostly about breadth.

##### 6. Manual-review watch-outs
- Confirm the arithmetic each response leans on: 366 cm³ × 275 MPa / 1e6 = 100.65 kNm; 649 cm³ → 178.475 kNm; 50 / 100.65 = 0.4968. All four are consistent with these; A and D round 100.65 to 100.7 / 10.07 in tables.
- C's `abs()` envelope: check the sign-loss in the summary column is acceptable to downstream consumers, and whether "reject invalid `Mz_kNm`" and "reject multiple sections" should be errors or warnings in this codebase.
- D's `"DATA"` status: verify no downstream code or report template assumes exactly two status values, and re-check the resulting sort order.
- D's `test_build_member_summary_takes_max_moment` and A's absence of any sign test: a reviewer should decide the envelope rule before merging any test that pins `max`.
- B's line numbers (`:10`, `:15`) do not match the supplied files; C's do. Verify against the real repo.
- The Mz-vs-Wpl_y axis mapping raised by C and D is a genuine open question about the solver's local-axis convention; nobody should "fix" it without checking the analysis export's documentation.
- A's zero-capacity guard: confirm it is unreachable with the current library before merging dead code.

### `v2-deep-02` - Repo review with unit, combination, and reporting traps

Label key: A = `qwen-3.8-27b-high`, B = `gpt5.4-xhigh`, C = `minimax-m2.7-cloud`, D = `gpt5.6-sol-xhigh`

#### Blind judgement: v2-deep-02

##### 1. Task summary
Code-review three tiny Python files for a major-axis steel beam ULS screening package, where the planted defects are an unfactored imposed load (`ULS_GAMMA_Q` unused), a cm³-vs-mm³ resistance divisor (`/1e6` should be `/1e3`), and a report that sorts ascending and returns only `output[:1]` (the least-utilised row).

##### 2. Score table

| Response | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Note |
|---|---|---|---|---|---|---|---|
| A | 5 | 5 | 5 | 5 | 4 | 4 | Finds all three planted bugs with correct severity, adds the combination-label and rounding points, and notes that bugs 1 and 2 mask each other; slightly long with one garbled derivation line. |
| B | 5 | 5 | 5 | 4 | 4 | 4 | Finds all three planted bugs with accurate line references and test-pinning advice, but is terse and omits the combination-label issue. |
| C | 2 | 2 | 2 | 2 | 3 | 3 | Misses the units bug and explicitly certifies `/1e6` as correct, substitutes a dubious γ_M0 "Critical", and misdescribes the returned row as the worst case. |
| D | 5 | 4 | 5 | 4 | 4 | 5 | Finds all three planted bugs with a clean numerical unit check and the combination-label issue; several cited line numbers are wrong. |

##### 3. Top weaknesses per response

**Response A**
- The unit derivation in Finding 2 contains a half-finished line: "`Wpl_y_cm3 × fy_MPa = 1000 × (N·mm) / 1000 = ...`" — the conclusion (`/1000`) is right but the working is muddled and would confuse a checker.
- Typo "per-comcombination" in Finding 4; minor, but it is in the safety-relevant argument.
- Longest of the four; the Summary table repeats content already stated. Still within "short, high-signal" but at the edge.
- Finding 4 (combination label) is rated Medium yet arguably duplicates the root cause of Finding 1 (a single hard-coded factor set); not wrong, but the boundary between them is not drawn.

**Response B**
- Omits the combination-label issue entirely (the `combination` column is emitted but never drives factors) — a reporting-integrity point squarely within the stated focus.
- Finding 4's wording "the status check uses `< 1.0` rather than the raw value" conflates two different points (rounding vs. threshold rule) into one clause.
- Ranks the 1000× resistance error below the reporting truncation as "High"; defensible because the error is conservative, but it makes every result unusable and most reviewers would treat it as release-blocking.
- No worked numerical example for the unit error, which would have made the finding self-verifying.

**Response C**
- Misses the planted unit bug and asserts the opposite: "The `1e6` conversion is correct but opaque." This is a false sign-off on a 1000× resistance error.
- Finding 2 (missing γ_M0) is rated Critical while the text itself says resistance is "overstated by a factor of 1.0 (if γ_M0 = 1.0)" — i.e. no numerical effect under the UK NA; the severity is not supported by the reasoning.
- Finding 3 describes the single returned row as "the worst-case beam only" — the sort is ascending, so it is the best case; this reverses the direction of the reporting failure and understates its danger.
- Finding 4's minimum fix (`util <= 1.0` on the rounded value) does not address the rounding-before-classification problem it describes, and the sentence "Python float arithmetic rarely lands precisely on 1.0" is not the mechanism at play.
- "simply supported fixed-end-moment formula `wL²/8`" is self-contradictory.
- Proposed `CM3_TO_M3 = 1e-6` constant "for maintainability" would enshrine the wrong conversion path.

**Response D**
- Line references are wrong for two of the three planted bugs: `reporting.py:14–15` (sort/return are lines 17–18) and `load_factors.py:6–7` (lines 5–6); `reporting.py:10` for the combination field is also off (line 12). The file names are right, so the findings are still locatable, but it suggests reading from a paraphrase rather than the supplied text.
- Puts the report truncation above the unconservative load factor; defensible (it hides failures) but the unfactored Q is the only bug that produces a wrong PASS on a correctly reported member.
- States "the usual resistance check accepts `utilisation <= 1.0`" as normal without flagging it as a project-convention question.

##### 4. Ranking (best to worst)
1. **A** — complete on all three planted bugs, correct severity, two well-judged secondary findings, and the only response to point out that bugs 1 and 2 partially cancel in a single test case.
2. **D** — complete, with the clearest unit check (1000 cm³ × 355 MPa → 355 kNm) and the combination-label issue; loses ground only on inaccurate line citations.
3. **B** — complete and precisely cited, with good test-pinning advice; ranked just below D because it drops the combination-label point and offers less self-verifying detail (B and D are effectively tied).
4. **C** — fails the review: misses the units bug, certifies it as correct, invents a γ_M0 Critical with no numerical consequence, and misstates which row the report returns.

##### 5. Practical significance
A, B and D would each be safe to act on as a pre-release review: all three planted defects are found, the minimum fixes are correct and minimal, and none proposes an unsafe refactor. The differences between them are presentational (length, line references, one extra secondary finding). C is materially different in kind: a reader following it would ship the 1000× resistance error with a written statement that the conversion was checked and found correct, and would believe the report shows the governing member when it shows the least-utilised one.

##### 6. Manual-review watch-outs
- Verify independently that the correct divisor is `1e3` (cm³ × N/mm² = 10³ N·mm = 10⁻³ kN·m): A, B and D agree; C says `1e6` is correct.
- Confirm the sort direction: `list.sort` is ascending, so `output[:1]` is the minimum utilisation (A, B, D correct; C says "worst-case").
- Check D's cited line numbers against the actual files before pasting them into a ticket.
- A's Finding 2 derivation has a garbled intermediate line; the final expression `Wpl_y_cm3 * fy_MPa / 1000` is what should be taken from it.
- C's γ_M0 point: whether a material partial factor belongs in this package is a scope decision, not a Critical bug, and C's own text concedes it changes nothing under γ_M0 = 1.0.
- The `< 1.0` vs `<= 1.0` acceptance rule (raised by C and D) is a project-convention question; do not treat either as a correctness fix without confirming the intended rule.
- None of the responses ran code; all fixes are stated, not demonstrated. B is the only one that explicitly recommends regression tests to pin the corrected behaviour.

### `v2-deep-03` - Scoped feature design on an existing package

Label key: A = `gpt5.4-xhigh`, B = `qwen-3.8-27b-high`, C = `gpt5.6-sol-xhigh`, D = `qwen-3.6plus`

#### Blind judgement: v2-deep-03

##### 1. Task summary
Produce a decision-complete design plan for adding an optional serviceability (deflection-ratio) summary to a three-file pandas design package while leaving ULS-only callers and the `RESULT_COLUMNS`-based `report_rows()` output contract unchanged.

##### 2. Score table

| Response | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Note |
|---|---|---|---|---|---|---|---|
| A | 3 | 4 | 5 | 3 | 4 | 4 | Safe, purely additive plan, but explicitly leaves the deflection aggregation rule undecided and leans toward the engineering-dubious "ratio after aggregation" default. |
| B | 4 | 5 | 4 | 4 | 4 | 5 | Thorough and well-gated plan with row-wise ratio then max, concrete edge cases and golden tests; slightly over-broad surface (two combined paths, extra status field) and a keyword-only claim its own snippet does not honour. |
| C | 5 | 5 | 5 | 5 | 4 | 4 | Cleanest engineering: computes ratio per row, carries the whole governing row, fails loudly on invalid data, touches nothing existing; less illustrative than B. |
| D | 2 | 3 | 2 | 2 | 3 | 4 | Well presented, but the sketched code aggregates numerator and denominator from different rows, the zero-guard would crash the status lambda, and `report_rows` is changed to silently drop missing columns, which alters the existing contract. |

##### 3. Top weaknesses per response

**Response A**
- Not decision-complete: "One design choice needs to be fixed before implementation: the aggregation rule for `Deflection_mm` and `AllowableDeflection_mm`" — the task asked for the decision, not a deferral.
- Recommends the wrong default: "Compute `DeflectionRatio = Deflection_mm / AllowableDeflection_mm` after aggregation, not per raw row, unless domain rules explicitly require worst-row ratio." Aggregating numerator and denominator separately can pair a deflection from one load case with an allowable from another; the governing ratio should come from a single row.
- Edge-case handling left open ("decide whether such rows are excluded, set to null, or flagged"), and the API itself is left as alternatives ("`build_serviceability_summary(df)` or a small wrapper", "a new opt-in writer ... or a combined writer with an explicit flag").
- Tests are stated as intents without concrete inputs/expected values, so they are not directly actionable.

**Response B**
- Claims "keyword-only opt-in flag" and lists it as "New keyword-only param", but the snippet `def report_rows(summary_df, include_serviceability: bool = False)` has no `*`, so it is positional-capable; the risk-table mitigation for positional callers rests on a property the code does not have.
- Two overlapping combined paths (`report_rows(merged, include_serviceability=True)` and `report_rows_combined(uls_df, sls_df)`) with different input expectations; the flagged path requires the caller to pre-merge, which is surface creep for a "scoped" feature.
- Zero allowable deflection is mapped to `inf`/FAIL and NaN to "N/A" rather than being treated as invalid input; defensible but it silently converts bad data into a result. The "N/A" fill after the left join is asserted but the fill step is not specified.
- Adds `Status_SLS` and a PASS/FAIL semantic that the request did not ask for (request asked only for the ratio); minor scope expansion.

**Response C**
- Very strict validation ("Reject non-numeric or non-finite values, negative deflections, and allowable deflections less than or equal to zero" via `ValueError`) means one dirty row aborts the whole SLS summary; acceptable for an opt-in path, but the plan does not offer a per-row diagnostic alternative.
- Uses an empty schema-correct DataFrame as the "absent" sentinel while `report_sections` also accepts `None`; two representations of the same state.
- Tests list mostly qualitative expectations (only one concrete value: 12/20 = 0.6); no golden-file mechanics or whitespace-normalisation test called out.
- Does not sketch signatures beyond stubs, so a reader must infer the column-detection and idxmax implementation.

**Response D**
- Engineering error in the sketched code: `Deflection_mm=("Deflection_mm", "max")` with `AllowableDeflection_mm=("AllowableDeflection_mm", "first")` then divides — numerator and denominator may come from different rows/cases, and "first" is order-dependent.
- Unsafe refactor of the existing writer: `available = [c for c in cols if c in summary_df.columns]` makes `report_rows` silently omit missing columns, so a malformed ULS summary that today raises `KeyError` would now emit partial records; the plan even enshrines this ("`test_report_rows_missing_columns_graceful` ... Silently omits missing columns, no `KeyError`") and then states "No existing logic is modified", which is false.
- Proposed zero guard is inconsistent with its own code: `.replace(0, pd.NA)` before division yields `pd.NA`, and `lambda ratio: "PASS" if ratio <= 1.0 else "FAIL"` raises on `pd.NA` (ambiguous boolean).
- Not decision-complete: "Alternatively, add an optional `include_sls: bool = False` parameter to `build_uls_summary` and return a combined DataFrame" — leaves the core API choice open, and the alternative would widen the ULS builder's output shape.
- `has_sls_data(df)` appears in the risk table but not in the file-change list; `io_contract.py` rationale says the contract "needs to be extended to include serviceability columns", contradicting the later "no breaking changes to `RESULT_COLUMNS`".

##### 4. Ranking (best to worst)
1. **C** — Only response that both keeps every existing symbol untouched and gets the governing-row aggregation right, with deterministic tie-breaks and fail-loud validation; the strictness is a reasoned choice, not an oversight.
2. **B** — Equally backward-compatible in effect and the most complete on tests and risks, computes the ratio row-wise before taking the max; loses to C on surface economy, the keyword-only inconsistency and converting invalid input into results.
3. **A** — Correct instincts on compatibility and identifies the aggregation hazard, but defers the key decision and suggests the weaker default, so it is not the decision-complete plan requested.
4. **D** — Presentation is good but the plan contains a real numerator/denominator mismatch, a crash path in its own zero-guard, and a silent-omission change to `report_rows` that erodes the report contract it claims to protect.

##### 5. Practical significance
C and B are both safe to hand to an implementer; the gap between them is mostly about how much redundancy and scope creep the reviewer tolerates, and about whether invalid deflection data should raise (C) or produce `inf`/"N/A" (B). A would need a follow-up decision meeting before coding and, if implemented as its default suggests, could report incoherent ratios for multi-row members. D would, if implemented as sketched, ship an aggregation bug, a runtime `TypeError` on zero allowables when the guard is applied, and a behavioural change to the existing writer that hides missing-column failures for all current consumers — the only response that materially threatens the "keep report output stable" requirement.

##### 6. Manual-review watch-outs
- B: verify whether the implementer actually makes `include_serviceability` keyword-only (`*`), and how "N/A" is filled for unmatched members after the left join (Status_SLS will be NaN after `merge` unless filled).
- B: confirm the project wants `inf`/FAIL for zero allowables rather than input rejection; this is a policy decision with engineering-reporting consequences.
- C: confirm stakeholders accept whole-summary `ValueError` on any invalid deflection row, and that the empty-DataFrame sentinel does not confuse downstream callers that check `is None`.
- C: verify the governing-row selection is implemented via a per-group idxmax that also carries `Deflection_mm`/`AllowableDeflection_mm` from that row, as the plan promises.
- A: the aggregation rule must be decided before implementation; check that the chosen rule is row-wise ratio then max, not max/first of the raw columns.
- D: reject the `available = [...]` silent-omission change to `report_rows`; reject `"first"` aggregation of `AllowableDeflection_mm`; check the pd.NA guard against the status lambda.
- All: none of the responses can see the existing test suite or downstream consumers; claims like "all pre-existing tests pass unmodified" and "byte-identical golden output" are assertions to be verified, not facts established in the plan.

### `v2-deep-04` - Safe refactor with behaviour preservation constraints

Label key: A = `qwen-3.8-27b-high`, B = `gemma4:31b-cloud`, C = `gpt5.4-xhigh`, D = `gpt5.6-sol-xhigh`

#### Blind judgement: v2-deep-04

##### 1. Task summary
Review a proposed "deduplicate shared utilisation helpers" refactor across `concrete_checks.py` and `steel_checks.py`, where the hidden trap is that the two modules deliberately diverge on non-positive capacity (concrete: `None` -> `"CHECK INPUT"`; steel: `0.0` -> `"PASS"`) and downstream spreadsheets depend on the exact status text.

##### 2. Score table

| Response | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Note |
|---|---|---|---|---|---|---|---|
| A | 5 | 5 | 5 | 5 | 5 | 5 | Identifies the sentinel split precisely, recommends effectively no code change, flags the steel zero-capacity `PASS` as a separate decision item, and specifies a pre/post golden-file diff against spreadsheet rows. |
| B | 4 | 4 | 4 | 3 | 3 | 4 | Behaviour-preserving parameterised helper, but never questions whether the refactor is worth doing, puts arithmetic in `common_formatting.py`, and the regression tests omit utilisation-level return values and the `1.0` boundary. |
| C | 5 | 4 | 4 | 4 | 4 | 4 | Correct and compact, with a good test list, but offers two helper shapes without committing, gives no module code or helper location, and does not consider leaving the code alone. |
| D | 5 | 5 | 5 | 5 | 4 | 5 | Recommends leaving the functions as-is, notes `format_status(None)` would raise `TypeError`, argues against a configurable sentinel, and supplies runnable parametrised tests; the steel `None -> 0.0` re-mapping adds a small indirection. |

##### 3. Top weaknesses per response

**Response A**
- Suggests an optional `divide(num, den)` helper in `common_formatting.py` and then concedes it is "arguably not worth even this" — hedged noise that a reader could still act on; a division helper in a formatting module is a poor home.
- Attributes intent to the steel sentinel ("treat as no demand, passes") that is not evidenced in the repo; it is an inference presented as the encoded meaning, though A does later call it "arguably a latent bug".
- "Assert the exact string set each module can emit" is not directly testable as stated; it needs to be operationalised as per-input assertions or a golden file (which A does also propose).

**Response B**
- Regression tests only exercise `*_status`; there is no assertion that `concrete_utilisation(10, 0) is None` or `steel_utilisation(10, 0) == 0.0`, so a change to the utilisation-level contract (which other callers may rely on) would pass its suite. The `util == 1.0` inclusive boundary is also untested, despite `format_status` using `<=`.
- Places `calculate_utilisation(ed, rd, fallback)` in `common_formatting.py`; a numeric helper in a formatting module is misleading. The `fallback` parameter makes it one wrong argument away from concrete inheriting steel semantics (D's point).
- Answers "should the refactor happen at all" only implicitly; never states that the duplicated logic is a single division and that leaving the code alone is a valid, lower-risk outcome.
- Uses LaTeX (`$\rightarrow$`, `$\le 1.0$`, `$rd = 0$`) in what is meant to be a Markdown review; renders poorly in most review tools.

**Response C**
- "Extract only the positive-denominator division into a tiny shared helper, or extract a parameterised helper" — two different refactors offered, neither chosen; only the second is sketched, and the module wrappers are described in prose rather than shown.
- Does not say which file `utilisation_or` lives in, nor discuss the risk of a configurable `invalid_value` being misused.
- Does not consider the no-op option even though its own analysis shows the shared logic is one line of arithmetic.
- No integration/golden-file check against actual spreadsheet inputs, only unit-level literal checks.

**Response D**
- Steel now does two mappings (`utilisation_or_none` -> `None`, then `0.0 if util is None else util`); the `None` intermediate is a value the steel module never previously produced, which is slightly more indirection than the code it replaces.
- Places `utilisation_or_none` in `common_formatting.py` (same misplacement as B, though less harmful since it has no policy parameter).
- Tests compare against `None` with `==` rather than `is`, and rely on `101 / 100 == 1.01` float equality (true in CPython but fragile as a pattern).
- Says "Yes" to "safe in principle" before qualifying it; the qualification is sound, but the headline is more permissive than A's "Partially".

##### 4. Ranking (best to worst)
1. **A** — Most proportionate answer: correctly concludes the "duplication" is a single division, recommends leaving the sentinels and status functions untouched, separates the latent steel bug into an explicit decision item, and includes a pre/post spreadsheet-column diff as the merge gate.
2. **D** — Effectively equal in analysis quality, with the extra `format_status(None)` `TypeError` observation and a well-argued case against configurable sentinels, plus runnable tests; loses a point for the slightly heavier steel wrapper.
3. **C** — Correct on every substantive point and a good regression list, but under-specified as a refactor recommendation (two options, no code for the modules, no helper location).
4. **B** — Correct code, but the weakest test coverage of the four, no consideration of doing nothing, and a helper design that D explicitly warns against.

##### 5. Practical significance
All four responses catch the planted trap and none proposes anything that would change zero-denominator behaviour or status text, so none is dangerous to act on. The real differences are in proportionality and audit quality: A and D would let a reviewer merge (or decline) with confidence and a regression suite that pins both the utilisation-level and status-level contracts; C would need the reviewer to pick a shape and write the code; B's suite would need augmenting before it could be trusted as a behaviour lock. The gap between A and D is negligible; the gap between A/D and B is meaningful for a merge decision but not for safety.

##### 6. Manual-review watch-outs
- Verify whether any callers of `concrete_utilisation` depend on the `None` return (A raises this; B's tests would not catch a change to it).
- Confirm whether a spreadsheet fixture or export exists to run A's pre/post status-column diff; if not, a golden file of representative rows (including zero and negative capacity per material) should be created before merging anything.
- Decide separately, with the spreadsheet owners, whether steel returning `"PASS"` for zero/negative capacity is intended (A flags it; all four correctly refuse to change it under this task).
- If B's or C's parameterised helper is adopted, check that the sentinel argument is required (B makes it positional-required, which is good) and that it does not live in `common_formatting.py` without renaming or relocation.
- D's test relies on `101 / 100 == 1.01`; confirm it holds on the target interpreter or switch to `pytest.approx`.
- Clarify with the refactor author whether "utilisation helpers" was meant to include the `*_status` functions; A and C explicitly forbid unifying them, B and D keep them separate implicitly.

### `v2-medium-05` - Large dataset engineering summary pipeline

Label key: A = `gpt5.6-sol-xhigh`, B = `gemma4:31b-cloud`, C = `gpt5.4-xhigh`, D = `qwen-3.8-27b-high`

#### Blind judgement: v2-medium-05

##### Task summary

Review or rewrite a pandas module that computes a span/250 deflection utilisation per member row and summarises it by Storey and Material, addressing performance at several hundred thousand rows, data cleaning/validation, correctness of the utilisation summary, and maintainability.

##### Score table

| Response | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Note |
|---|---|---|---|---|---|---|---|
| A | 5 | 5 | 4 | 5 | 4 | 5 | Fully vectorised, explicit validation with a raise/drop policy, abs() ratio and a member-envelope step; the strongest and most auditable answer, slightly heavier than the task strictly needs. |
| B | 3 | 3 | 2 | 2 | 3 | 4 | Vectorises the loop but mutates the caller's DataFrame in place, leaves negative lengths and signed deflections unhandled, and adds no schema check. |
| C | 4 | 5 | 4 | 4 | 4 | 4 | Compact, proportionate rewrite with schema check, fail-fast validation, abs() and a member envelope; loses a little on unconditional string coercion of keys and a location-free error message. |
| D | 3 | 4 | 3 | 3 | 3 | 4 | Good review table and patch plan, but the code silently drops invalid rows from a PASS/FAIL summary while the docstring and prose claim they are reported, keeps a full-frame copy, and contains one false claim about the original. |

##### Top weaknesses per response

**Response A**
- Changes the aggregation grain by default: "Multiple result rows for the same member are first reduced to that member's maximum ratio. MeanRatio is therefore the mean of governing member ratios." Nothing in the supplied context establishes multiple rows per member; this is a semantic change to `MeanRatio` and `MemberCount` for existing callers, although it is documented and the response admits "If the input contract guarantees exactly one row per member, this envelope step is harmless."
- Default `errors="raise"` aborts the whole run on a single dirty row in a several-hundred-thousand-row export (the original also crashed, so this is not a regression, but the drop path is opt-in only).
- `sort=False` on both group-bys changes output ordering relative to the original sorted `groupby`; not called out.
- Identifier normalisation skips categorical dtype keys, so blank categories would not be masked; minor.
- Length/complexity: parameter validation, reason counts, example indices and a `Literal` policy type are all reasonable, but the answer is at the upper end of what "without making the solution unnecessarily complex" allows.

**Response B**
- Mutates the input: `df[col] = pd.to_numeric(df[col], errors='coerce')` and `df["DeflectionRatio"] = ...` overwrite the caller's frame, and the text sells this as a benefit ("By modifying the DataFrame in place ... memory overhead is significantly reduced"). That is an unsafe refactor for a shared export frame and will also emit `SettingWithCopyWarning` if `df` is a slice.
- Only zero lengths are handled (`lengths = df["Length_m"].replace(0, np.nan)`); negative lengths still produce negative ratios that PASS, and signed deflections are never discussed.
- No required-column check, no handling of missing `Storey`/`Material` keys (groupby drops them silently), and `MemberCount=("Member", "count")` still counts rows whose ratio became NaN, so counts and statistics disagree within a group.
- Inaccurate claim about the original: "The original code would produce `inf` or crash" for zero length; Python float division by zero always raises, so it only crashes.
- The "Edge Cases" section notes NaN `MaxRatio` groups are labelled FAIL and shrugs ("or can be adjusted to 'UNKNOWN' if required") rather than resolving it.

**Response C**
- `_clean_text` is applied unconditionally: `series.astype("string").str.strip()` converts numeric `Storey`/`Member` identifiers to strings, changing output key dtypes for downstream consumers (Response A explicitly guards against this).
- Fail-fast error gives only a count: "f\"{int(invalid.sum())} rows have missing ids/group keys, non-numeric values, or non-positive lengths.\"" with no row indices or per-reason breakdown, which makes triage on a large export slow.
- `isna()` checks do not catch `inf` parsed from strings such as "inf"; an infinite ratio would flow through to `MaxRatio`. Minor.
- Same default grain change as A (member envelope before storey/material stats), flagged only as a "Medium" finding rather than as a behaviour change to confirm with the data owner.

**Response D**
- Silent data loss in a safety summary: `clean = clean.loc[valid]` discards rows with bad length/deflection without any warning or count, so a group can PASS because its worst member had an unparseable length. The prose says the revision "**excludes** rows ... (and reports how many were excluded)" and the docstring says "the number excluded is returned in the console-free way of simply not appearing in any group (see `excluded` note below)"; there is no `excluded` variable, no note, and nothing is reported. The follow-ups then concede "Log or return the count of excluded rows".
- Full copy retained: `clean = df.copy()` copies the whole (possibly wide) export after section 1 criticised "unnecessary memory pressure"; the fix is deferred to "Suggested follow-ups".
- Incorrect claim about the original: "it **silently drops the original index** (the reconstructed frame gets a fresh `RangeIndex`)". `pd.DataFrame(list_of_Series)` uses each Series' `name` (the original index label) as the row index, so the index is preserved.
- Assigning a new column after boolean `.loc` filtering (`clean = clean.loc[valid]; clean["DeflectionRatio"] = ...`) triggers `SettingWithCopyWarning` on pandas < 3; the claimed test on "pandas 3.0.6" would hide this.
- The `N/A` status branch is effectively dead in the revised code (NaN ratios are filtered out before grouping), and the reasoning for it ("if every ratio in a group is `NaN`") describes the original, not the revision.
- Unverifiable performance and verification claims ("~0.09 s (measured, pandas 3.0.6)", "executed against ... a dirty 6-row frame").

##### Ranking (best to worst)

1. **A** — Correct, vectorised, every validation path explicit and documented, abs() and envelope choices justified with a test list; the only real cost is that it changes `MeanRatio` semantics by default and is somewhat heavier than necessary.
2. **C** — Same core design as A in about half the code, with line-referenced findings and a clear clean/member/summary pipeline; slightly less careful about key dtypes, error diagnostics and infinite values.
3. **D** — The best written review of the original's failure modes and a usable patch plan, but the delivered code silently drops rows while claiming to report them, keeps the full copy it criticised, and includes a false statement about index handling.
4. **B** — Removes the loop and the `float()` crash, but mutates the caller's frame, ignores negative lengths and signed deflections, adds no schema validation, and leaves counts inconsistent with the statistics.

##### Practical significance

All four eliminate the `iterrows()` bottleneck, so on raw speed the differences are small; the meaningful gaps are in safety and correctness of the PASS/FAIL output. A and C are both applyable after a reviewer confirms two intended behaviour changes (absolute deflection and the member-envelope grain); choosing between them is largely a matter of how much diagnostic machinery the project wants. D would need its silent-exclusion path replaced with a warning or returned count before it is safe to use for a governing-utilisation report, and its docstring needs correcting. B should not be merged as-is because it mutates the input DataFrame and can still report PASS for negative-length or negatively-signed rows.

##### Manual-review watch-outs

- A and C: confirm with the data owner whether exports really contain multiple rows per member; if not, the envelope step is redundant and `MeanRatio` should be compared against the original definition.
- A and C: `abs()` on deflection changes results for any export that carries signed values; verify the sign convention before adopting it.
- A: `df.loc[:, _REQUIRED_COLUMNS]` and `work.loc[:, _MEMBER_KEYS]` index with a tuple rather than a list; this works on a flat column index in current pandas but is worth a quick check on the project's pinned version.
- A and C: `values.mask(values.eq(""))` relies on pandas treating `<NA>` in a nullable-boolean mask as "keep"; confirm on the pinned pandas version.
- C: run with integer `Storey`/`Member` columns and check whether the string coercion of keys is acceptable downstream.
- D: verify the "~0.09 s on 500k rows" and "dirty 6-row frame" runs; verify the index-preservation behaviour of `pd.DataFrame(rows)` (the "fresh RangeIndex" claim appears to be wrong); test on pandas < 3 for `SettingWithCopyWarning`.
- D: confirm that no excluded-row count is actually produced anywhere despite the docstring and section 2 text.
- B: run once on a frame and inspect the original object afterwards to confirm the in-place mutation; test a negative `Length_m` row and a negative `Deflection_mm` row for false PASS.

### `v2-medium-06` - Review plus targeted test design

Label key: A = `qwen-3.8-27b-high`, B = `gpt5.6-sol-xhigh`, C = `gpt5.4-xhigh`, D = `deepseek-v3.2`

#### Blind judgement: v2-medium-06

**Task summary:** Review a 15-line foundation-settlement helper (`settlement_ratio`, `differential_slope`, `status_from_ratio`), name the key bugs, propose minimum fixes, and give a small high-value test set, with explicit sign conventions and units; the planted issues are the silent `0.0` for zero allowable, the mm/m unit mix in `differential_slope`, and the pass/fail boundary.

##### Score table

| Response | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Note |
|---|---|---|---|---|---|---|---|
| A | 4 | 4 | 4 | 4 | 4 | 5 | Finds all planted issues, headlines the 1000x unit bug correctly and keeps fixes proportionate, but ships one test (`status_from_ratio(-0.5) == "FAIL"`) that fails against its own fixed code. |
| B | 4 | 4 | 3 | 4 | 4 | 4 | Most thorough and internally consistent (code and tests agree), with the genuinely insightful multi-point-spacing ambiguity, but the `len != 2` restriction is a breaking API change beyond "minimum" and the NaN-gives-PASS claim is wrong for `status_from_ratio`. |
| C | 3 | 3 | 4 | 3 | 3 | 3 | Covers the three planted issues and is safe to apply, but keeps the silent `0.0` for fewer than two points (even tests it as intended), leaves the misnamed mm/m output, cites wrong line numbers, and the test set has gaps. |
| D | 2 | 2 | 1 | 1 | 2 | 2 | Identifies the bugs but invents a default 5 % pass tolerance that makes over-limit results PASS, its status tests contradict its own code, and its "integration" test contains a unit error (`5000mm/300 = 16.7 mm/m`). |

##### Top weaknesses per response

**Response A**
- Internal inconsistency: `test_status_negative_ratio_fails` asserts `status_from_ratio(-0.5) == "FAIL"`, but the proposed fix is `return "PASS" if ratio <= 1.0 else "FAIL"`, which returns PASS for `-0.5`. The suite as written is red against the proposed code. The response never guards negative `settlement_mm` (heave) in `settlement_ratio`, so the "uplift must not auto-PASS" intent stated in the test comment is not actually enforced anywhere.
- Silently flips `<` to `<=` and converts the slope output to m/m (a 1000x change in returned magnitude) without any caller context; it does flag both as decisions ("flip to `<` only if...", "If the codebase actually wants mm/m... rename"), which is the right hedge, but the code applies the change unconditionally.
- Raising on `len < 2` and on `spacing_m <= 0` changes exception behaviour for existing callers; reasonable, but slightly beyond "minimum" and not called out as a compatibility risk.

**Response B**
- Change safety: `if len(settlements_mm) != 2: raise ValueError("exactly two settlements are required")` breaks any existing caller that passes more than two points (the original explicitly accepted lists). This is an API redesign presented as a "minimum fix", albeit labelled "deliberately".
- Incorrect claim: "`NaN` can silently produce a PASS because comparisons with `NaN` are false" is wrong for `status_from_ratio` — `nan < 1.0` is False, so the current code returns FAIL (fail-safe). The claim is only partly right for `max`/`min` over a NaN-containing list.
- Rejecting `settlement_mm < 0` outright means real heave data raises rather than being assessed; the response asserts "positive downward" as an assumption and does not offer the magnitude alternative that C does.

**Response C**
- Keeps `if len(settlements_mm) < 2: return 0.0` and then writes test 7 (`differential_slope([12.0], 2.0) == 0.0`, "Confirms the chosen behavior for insufficient points"), which locks in the exact silent-benign-default pattern it criticises for `allowable_mm == 0`.
- Leaves `differential_slope` returning mm/m under a name that implies dimensionless slope; the response says "Either rename it ... or convert" but does neither, only adding a docstring.
- Line references are wrong for the supplied file (`:3` for the sign issue points at `return 0.0`; `:10` for `status_from_ratio` points at the `delta_mm` line; `:8` for units points at the `len` check). Test set omits negative allowable, negative spacing, and a just-over-1.0 case; tests are prose-only, not runnable.

**Response D**
- `def status_from_ratio(ratio, tolerance=0.05)` with `return "PASS" if ratio < (1.0 + tolerance)` changes every existing caller's result in the unsafe direction by default (a utilisation of 1.04 now PASSes). No engineering basis is given for 5 %.
- Tests contradict the code: `assert status_from_ratio(1.00) == "FAIL"` and `assert status_from_ratio(1.01) == "FAIL"` under the comment "Strict boundary (default tolerance)" both fail because the default tolerance is 0.05.
- Unit error in the "integration" test: "For 5m span: 5000mm/300 = 16.7mm/m" — L/300 as a slope is 1/300 ≈ 3.33 mm/m; 16.7 mm is a differential *settlement* limit, not a gradient. The assertion `slope < 16.7` is therefore vacuous (actual value 1.4 mm/m).
- Inconsistent list handling: empty list raises, single element returns `0.0`. Declares negative settlements "physically impossible" (heave exists). Leaves the unit mix unfixed and the name unchanged, calling it a "design issue" while ranking the `ZeroDivisionError` as the critical bug over the silent false PASS.

##### Ranking (best to worst)

1. **A** — Correct severity ordering (1000x unit bug first), proportionate API-preserving fixes, an explicit "why these 10 and not more" rationale; docked for one self-contradicting test and an unenforced heave guard.
2. **B** — Broadest and only fully self-consistent code+test pair, plus the sharp observation that `max - min` over a single `spacing_m` is ill-defined for >2 points; docked for a breaking two-point restriction and a wrong NaN claim. Very close to A; a reviewer who values internal consistency over proportionality could reasonably swap 1 and 2.
3. **C** — Sound, safe, and honest about assumptions (heave by magnitude, mm/m retained), but lighter: retains a silent default it should have removed, wrong line refs, and a thinner test set.
4. **D** — Actively unsafe if applied (default 5 % tolerance), red tests against its own code, and a units mistake in the very test meant to demonstrate unit awareness.

##### Practical significance

A and B would both be acceptable review outputs after a one-line correction each (A: drop or rewrite the negative-ratio test, or add a `settlement_mm < 0` guard; B: relax `!= 2` to `< 2` or keep the coordinate-based redesign as a separate proposal). C is usable as-is but would leave a reviewer to re-raise the silent-zero and naming points. D should not be merged: it degrades the pass/fail semantics and its tests do not run green against its own code, so the difference between D and the rest is a real safety gap, not a style preference. The gap between A and B is small and mostly a matter of what "minimum fix" means.

##### Manual-review watch-outs

- A: run `test_status_negative_ratio_fails` against A's `status_from_ratio` — it fails as written.
- D: run `test_status_from_ratio` against D's default `tolerance=0.05` — the `1.00` and `1.01` assertions fail; confirm the `16.7 mm/m` arithmetic is wrong (1/300 = 3.33 mm/m).
- B: confirm `nan < 1.0` is False in Python (so current `status_from_ratio(nan)` returns FAIL, not PASS); confirm whether any caller passes >2 settlements before accepting the `len != 2` restriction.
- C: check the line numbers against the supplied file; confirm whether callers expect mm/m before keeping that convention.
- All four assume no caller context (none was supplied); whether the slope should be m/m or mm/m, and whether `ratio == 1.0` should PASS, are project conventions that need confirming before any of these fixes land.
- All responses that change `<` to `<=` alter results for exactly-at-limit cases; verify this is the intended serviceability convention.

### `v2-anchor-07` - Historical anchor from v1 Task 6 EC3 bending check

Label key: A = `gpt5.6-sol-xhigh`, B = `qwen-3.8-27b-high`, C = `gpt5.4-xhigh`, D = `minimax-m2.7-cloud`

#### Blind judgement: v2-anchor-07

##### Task summary
Review a short EC3 bending-check snippet for a 254x102x28 UB (simply supported, UDL 18.5 kN/m over 6.2 m), find the planted faults (minor-axis `Wpl_z` used instead of major-axis `Wpl_y`; missing N.mm to kN.m conversion), correct them with sourced section properties, and state whether the section is adequate.

##### Score table

| Response | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Note |
|---|---|---|---|---|---|---|---|
| A | 5 | 5 | 5 | 4 | 4 | 4 | Finds both planted faults, uses the correct Wpl,y = 353 cm3, gets util 0.916 PASS (cross-section) with an independent Blue Book cross-check, but adds shear, LTB and load-factor commentary beyond the brief. |
| B | 2 | 3 | 2 | 2 | 4 | 4 | Diagnoses both planted faults correctly but substitutes a wrong Wpl,y (588 cm3) backed by a fabricated property table, giving a non-conservative util 0.55. |
| C | 5 | 4 | 5 | 5 | 4 | 5 | Finds both planted faults, correct properties and result (97.1 kN.m, util 0.916), proportionate scope, clean minimal code diff, sources cited. |
| D | 1 | 2 | 2 | 1 | 3 | 3 | Names both planted faults but uses a wrong Wpl,y (106 cm3), silently applies a 1.35 load factor, and reaches a false FAIL with a redesign recommendation. |

##### Top weaknesses per response

**Response A**
- Scope creep beyond the planted objective: adds a shear check ("V_Ed/V_c,Rd = 0.203 < 0.5"), an LTB estimate ("M_Ed/M_b,Rd approx 2.83") and a load-factor caveat; all flagged as conditional, but the task asked for a review of the snippet as written.
- Internal inconsistency in the LTB aside: quotes "C1 = 1.13" for UDL, then interpolates tabulated Mb,Rd values (32.3 and 28.1 kN.m) without stating whether those are C1 = 1.0 values or how C1 was applied, so the "2.83" figure is unaudited.
- Opening line "The code's unconditional PASS is incorrect" is slightly muddled, since the corrected cross-section check also passes; the reader has to get to the conclusion to see that the PASS was right for the wrong reasons.
- Long, LaTeX-heavy presentation for a five-line snippet; the corrected code changes the STATUS string format, a small unrequested behaviour change.

**Response B**
- Wrong major-axis property: "Wpl,y = 588 cm3 = 588x10^3 mm3" is not the 254x102x28 UB value (353 cm3); the resulting "M_Rd = 161.70 kN.m" and "util = 0.5497" overstate capacity by about 67 percent, a non-conservative error.
- Fabricated property table presented as "standard published values": "I_y 6920 cm4", "Z_y 545 cm3", "I_z 115.4 cm4", "Z_z 22.7 cm3", "h = 254.0 mm, t_w = 5.8 mm, t_f = 9.0 mm" do not match this section (I_y is about 4000 cm4, h about 260 mm).
- Overconfident false claim: "The code's 49.0e3 mm3 matches the tabulated Wpl,z exactly, confirming the value was copied correctly" - tabulated Wpl,z is about 54.8 cm3.
- Vague sourcing ("e.g. the tables in Structural Steelwork to Eurocodes / the standard BS 4 / Eurocode UB section tables") despite the prompt asking where values come from.
- Redeeming detail: correctly reproduces what the original prints ("M_Rd = 13475000.00 kN.m", "Util = 6.6e-06"), showing genuine reading of the snippet.

**Response C**
- Shows less working than A: no independent cross-check of Mc,y,Rd against tabulated values, and section class is assumed ("the section is Class 1") rather than confirmed, though the prompt does state Class 1.
- Corrected code strips the original header comments and the "<- plastic modulus" annotation, reducing traceability slightly.
- LTB remark "it would fail by lateral-torsional buckling ... Mb,Rd is only about 31 to 32 kN.m" is asserted without working, and "it governs" is stated unconditionally in the findings before the restraint assumption is introduced.
- Sourcing is by URL only (British Steel datasheet, SCI P363) with no page or row reference for Wpl,y.

**Response D**
- Wrong major-axis property: "Wpl,y approx 106 x 10^3 mm3" (actual about 353 cm3), producing "M_Rd = 29.15 kN.m" and a false "FAIL", plus fabricated supporting values ("elastic modulus ... approx 69 x 10^3 mm3; minor-axis plastic modulus approx 23 x 10^3 mm3").
- Replaces the planted objective with a different design problem: introduces "gamma_G = 1.35" and treats 18.5 kN/m as characteristic ("w_design = gamma_G * w_char"), giving "Utilisation = 4.12 (412 %)" and a recommendation for "a 305 x 102 x 33 UB or a 305 x 165 x 46 UB" - all built on the wrong modulus.
- Incorrect quantitative claim: "The moment-resistance is roughly doubled if the correct axis is used" (the true ratio Wpl,y/Wpl,z is about 6.4, or 7.2 against the snippet's 49 cm3).
- Code introduces an unused `gamma_Q` and changes the meaning of the input variable without being asked; "EC3-1-1 Table 5" is not where gamma_M0 lives (Cl. 6.1).
- Table formatting is broken by hard line-wraps inside cells, hurting readability.

##### Ranking (best to worst)
1. **A** - both planted faults corrected with the right property, right utilisation, sources with page references, and a tabulated cross-check; loses only for over-scoping and an unaudited LTB aside.
2. **C** - equally correct on the planted faults and the adequacy result, and the most proportionate and auditable answer; ranked just below A because it shows less verification depth.
3. **B** - correct diagnosis of both faults and good reading of the snippet, but the fabricated 588 cm3 value makes the corrected result and adequacy margin wrong in the unsafe direction.
4. **D** - wrong property, unrequested load factoring, wrong conclusion and a redesign recommendation; the response drifts furthest from the planted objective.

##### Practical significance
The split is large and binary. A and C deliver a corrected check a reviewer could adopt directly (M_Ed 88.89 kN.m vs M_c,y,Rd 97.1 kN.m, util 0.92, PASS for cross-section bending with a proper caveat on lateral restraint); the difference between them is presentation and scope, not substance. B would leave an engineer believing there is 45 percent spare capacity when there is about 8 percent, which is the more dangerous failure mode. D would trigger an unnecessary section upsize and would embed a hidden change in what the load input means. Both B and D correctly name the two planted faults, so a reviewer skimming only the "errors identified" section would not see that their corrected numbers are wrong.

##### Manual-review watch-outs
- Confirm Blue Book values for 254x102x28 UB: Wpl,y = 353 cm3, Wpl,z = 54.8 cm3, Mc,y,Rd (S275) = 97.1 kN.m; this decides A/C vs B/D.
- A: verify the SCI P363 page anchors (p.72, p.205, p.231, pp.35-36), the V_c,Rd = 283 kN figure, and the Mb,Rd values 32.3 kN.m at 6.0 m and 28.1 kN.m at 7.0 m, including whether they are C1 = 1.0 tabulations.
- B: the entire property table and the claim that 49.0 cm3 is the tabulated Wpl,z; also the Class 1 ratios "flange c/t approx 3.6, web d/t_w approx 36.3".
- C: the British Steel datasheet URL and whether the row actually gives 353 cm3; the "31 to 32 kN.m" Mb,Rd claim.
- D: the "106 x 10^3 mm3" value and its attribution to the "British Steel Blue Book (Tata Steel)", and the Class 1 ratios "flange c/t approx 6, web d/t approx 39".
- All responses assume 18.5 kN/m is already a ULS design load (D alternates); a reviewer should confirm which the original author intended before accepting any adequacy statement.

### `v3-notebook-01` - Square pad footing sizing notebook draft

Label key: A = `gemma4:31b-cloud`, B = `gpt5.6-sol-xhigh`, C = `gpt5.4-xhigh`, D = `qwen-3.8-27b-high`

#### Blind judgement: v3-notebook-01

##### 1. Task summary

Produce a notebook-style draft (alternating Markdown and standard-library Python cells) that sizes the smallest square pad footing from 2.4 m to 3.2 m under three service load cases with axial load plus biaxial moment, using a rigid-footing linear-pressure model with a derived edge-pressure expression, checking only `qmax <= 220 kPa` and `qmin >= 0`, and reporting the selected size, governing case, and omitted checks (expected: 3.0 m, LC2 governing via uplift, 2.9 m rejected at `qmin = -0.41 kPa`).

##### 2. Score table

| Response | Calculation correctness | Code quality/executability | Engineering judgement | Unit/assumption handling | Notebook traceability/clarity | Completeness of deliverable | Note |
|---|---|---|---|---|---|---|---|
| A | 3 | 4 | 2 | 3 | 2 | 2 | Pressures and the 3.0 m selection are right, but the governing case is derived from qmax (would report LC3), the conclusion is placeholders rather than stated values, and 2.9 m is never explained. |
| B | 5 | 5 | 4 | 4 | 4 | 4 | Numerically flawless and well engineered code with a clear LC2/2.9 m explanation, but the pressure formula is quoted with absolute values rather than derived, the model is not justified, and eccentricity directions are never defined. |
| C | 5 | 5 | 5 | 5 | 5 | 5 | Full derivation from `N/A + My x/Iy + Mx y/Ix`, a four-corner implementation faithful to that derivation, a transparent sweep table, and a programmatically derived governing case (LC2). |
| D | 5 | 4 | 5 | 5 | 5 | 5 | Full derivation, the best model justification, a complete pre-stated sweep table matching the reference to 0.01 kPa, and a flagged small uplift margin; only a float-accumulated candidate list and a moment-sum shortcut hold the code back. |

##### 3. Top weaknesses per response

**Response A**
- Governing case is chosen by peak compression: `if q_max > max_q_found: ... governing_case = lc_name`. At 3.0 m this yields LC3 (178.9 kPa), so the printed "Governing Case" would be LC3, not LC2. The selection itself is driven by uplift in LC2, which the response never identifies.
- The conclusion does not state the answer: "**Selected Footing Size:** `selected_B` metres (Square)" and "**Governing Load Case:** `governing_case`" are variable-name placeholders in Markdown. The prompt requires the size in metres and the governing case to be stated clearly.
- No explanation of why 2.4 m to 2.9 m fail; the search loop `break`s on the first failure and prints only the selected width, and no sweep table is produced.
- Derivation is abbreviated: it jumps to `Z = B^3/6` without showing `I = B^4/12` and `y = B/2`; sign convention is vague ("Positive moments acting about the x and y axes, respectively") and the worst-corner assumption is implicit; `e_x`, `e_y` are defined but never used or reported.
- Section structure deviates from the brief: there is no "Input data" Markdown cell (the inputs sit as a bare code block under section 1), and the required six sections are collapsed to five.
- Adds "overturning stability" to the exclusions, which the brief did not list (harmless, but not proportionate).

**Response B**
- Does not show the mechanics: `q_max = N/B^2 + 6|Mx|/B^3 + 6|My|/B^3` is quoted directly in Markdown Cell 1 with no `N/A ± Mx*y/Ix ± My*x/Iy`, `I = B^4/12`, or `y = B/2` step. The prompt explicitly asks to "show briefly how your edge-pressure expression is obtained from axial stress plus bending stress."
- No justification of why the rigid linear model is appropriate; it is stated only as an assumption ("The footing is rigid, and soil pressure varies linearly").
- Eccentricities are never defined or reported (`ex`, `ey` do not appear), so "define ... eccentricity directions clearly" is unmet; the use of `|Mx|`, `|My|` is the only implicit statement of the worst-corner convention.
- The search summary prints only `B | PASS/FAIL`, not the pressures, so the reason for each rejection is visible only in the Markdown narrative, not the code output.
- Code Cell 6 hardcodes `assert selected_width_m == 3.0` and `candidate["B_m"] == 2.9`; acceptable as a verification cell but brittle if inputs change.

**Response C**
- Code Cell 1 under "Assumptions" is only a `print_markdown_table` helper; the assumptions section itself has no calculation content, so the first code cell is structurally a utility rather than part of the section.
- The model justification is a single sentence ("captures the first-order effect of eccentric service loading ... using a simple elastic distribution"); adequate for "briefly" but thinner than D.
- `selected = next(row for row in search_results if row["all_ok"])` raises an uncaught `StopIteration` if no candidate passes; no explicit guard or message.
- Printed markdown tables in stdout will not render as tables in a notebook output cell (cosmetic).

**Response D**
- `B_CANDIDATES = [2.4 + 0.1 * i for i in range(9)]` accumulates float error; the `.1f` table formatting masks it, but `print("Selected footing size B =", selected_B, "m")` is unformatted and equality-based logic elsewhere would be fragile (A rounds, B and C use integer tenths).
- `pressures()` uses `6.0 * (Mx + My) / B**3`, which is only valid because the response declares "All given moments are taken as acting in the direction that adds to the pressure at the same corner"; the code is not sign-general, unlike C's four-corner evaluation.
- "the rigid-plate assumption is conservative and standard practice" is a mild overclaim (rigidity is not universally conservative for bearing), though it does not affect this check.
- The "Expected output of the search" table is a hand-stated claim in Markdown rather than computed output; it is correct, but a reviewer must trust or verify it.

##### 4. Ranking (best to worst)

1. **C** - complete, general, and self-consistent: the four-corner code implements exactly the derived `q(x,y)` expression, the governing case is derived from the search (last case to pass), the sweep and per-case tables expose the uplift check, and every prompt requirement is met.
2. **D** - equal in engineering content and slightly stronger in narrative (best model justification, full near-miss table, flags the +2.22 kPa margin), but the float candidate list and moment-sum shortcut are small code warts C does not have.
3. **B** - correct numbers, robust code, and a clear LC2/2.9 m explanation, but it quotes rather than derives the formula, omits the model justification, and never defines eccentricities.
4. **A** - correct selection but wrong governing-case logic (qmax-based, would print LC3), placeholder conclusion with no stated 3.0 m, no near-miss explanation, and a structure that drops the input-data section.

##### 5. Practical significance

- C and D are usable as preliminary design drafts as written: a checking engineer could audit the derivation, run the cells, and see why 2.9 m fails. The gap between them is stylistic, not technical.
- B would produce the right answer and a clean code base but would be sent back for the theory cell (derivation, justification, eccentricity definitions) before it could be filed as an engineering note.
- A would actively mislead: an engineer reading its printed output would record LC3 as governing and would not learn that the size is controlled by a 0.4 kPa uplift shortfall in LC2 at 2.9 m. It requires rework of the conclusion and governing-case logic.
- None of the four responses selected 2.9 m by checking qmax only; all four apply the `qmin >= 0` condition in the selection loop. A's governing-case reporting is qmax-only, but its selection is not.

##### 6. Manual-review watch-outs

- **A**: run the results cell and confirm the printed "Governing Case" is LC3; confirm the Markdown conclusion literally contains `selected_B` and `governing_case` rather than values.
- **B**: confirm `29/10.0 == 2.9` and `30/10.0 == 3.0` so the hardcoded asserts in Code Cell 6 pass; confirm the tabulated increments (`Δqx = 20.00, 44.44, 15.56`; `Δqy = 13.33, 31.11, 24.44` kPa) match `6M/B^3` at B = 3.0 m.
- **C**: verify `governing_selection_case` logic (largest first-passing width) returns LC2 (LC1 first passes at 2.6 m, LC3 at 2.8 m, LC2 at 3.0 m); confirm `itertools` is accepted as standard library.
- **D**: verify the hand-stated "Expected output" table against the code output (spot checks: LC1 at 2.4 m = 256.08/125.87, LC3 at 3.1 m = 166.33/93.82, LC2 at 2.9 m = 166.88/-0.41 all match the reference); check whether `selected_B` prints as `3.0` or `3.0000000000000004` given the float-accumulated candidate list.
- **All**: the sign of `qmin` at 2.9 m (`-0.410 kPa`) is the entire basis for rejecting 2.9 m; any response that had used `qmin > -tolerance` with a coarse tolerance would flip the answer. B's tolerance is `1e-9 kPa`, which is safe; A, C, D use exact comparisons.
- No response used non-standard-library imports; no unit conversions were needed and none were mis-applied (kN, kNm, m to kPa is direct in all four).
