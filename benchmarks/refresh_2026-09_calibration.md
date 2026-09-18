# September 2026 Refresh: Calibration Record

Blind scoring of `gpt5.6-sol-xhigh` and `gpt5.6-luna-max` against the frozen April 2026 results, with calibration of the new judge against April anchors. Produced 2026-09-17 on branch `feat/sept-2026-model-refresh`. The April rows in every scorecard and ranking file are unchanged.

## 1. Method

- Tasks: the six v2 primary tasks, the v2 anchor (`v2-anchor-07`) and `v3-notebook-01`.
- For each task a blind pack held: the task prompt (anchor: text-block content only), `context_combined.md` (v2 primary tasks), `_evaluator_notes.md` (plus `reference_solution_review.md` for v3), the April judge template amended to score only the six technical criteria, and four responses labelled A to D in a seeded random order.
- The four responses were the two new models, `gpt5.4-xhigh` as the high calibration anchor, and a low calibration anchor: the April model with the lowest mean of the six technical scores on that task's scorecard, excluding rows where all six scores are 2 or less, ties broken by table order.
- Responses were the text under `## Raw Model Output` in each raw output file with all metadata stripped. The Sol v3 response, whose Markdown fences were lost when copied, carried one neutral line: "Formatting was lost when this response was copied; judge content, not formatting." Packs were checked to contain no model or vendor names.
- Judges: one fresh Claude Code subagent (Claude Fable 5.1) per pack, given only the pack path, told to read nothing else, not to browse, and not to guess authorship. Run records and scorecards were never shown to judges. Scores are integers 1 to 5.
- Round 1 judged all eight tasks. After the calibration gate failed, round 2 re-judged the four most drifted tasks (`v2-deep-03`, `v2-deep-04`, `v2-medium-05`, `v3-notebook-01`) with fresh subagents, new seeds and a different label order. Where a task was judged twice, the blind score used below is the mean of the two rounds.
- The judge templates, packs, mapping, judge replies and execution logs live in the session scratchpad outside the repository; the mapping and de-anonymised replies are reproduced in sections 11 and 12.

## 2. Round 1 calibration against April

Blind scores of the two April anchor responses per task compared with their frozen April scores on the six technical criteria. MAD is the mean absolute difference over six criteria; signed is blind minus April.

| Task | Low anchor | High anchor MAD / signed | Low anchor MAD / signed | Anchor order preserved? |
|---|---|---:|---:|---|
| v2-deep-01 | `qwen-3.6plus` | 0.83 / -0.83 | 0.83 / -0.50 | yes (April 4.17 vs 3.67; blind 3.33 vs 3.17) |
| v2-deep-02 | `minimax-m2.7-cloud` | 0.17 / -0.17 | 0.67 / -0.67 | yes (April 4.83 vs 3.00; blind 4.67 vs 2.33) |
| v2-deep-03 | `qwen-3.6plus` | 1.83 / -1.83 | 1.00 / -1.00 | yes (April 4.83 vs 3.83; blind 3.00 vs 2.83) |
| v2-deep-04 | `gemma4:31b-cloud` | 1.00 / -1.00 | 1.00 / -1.00 | yes (April 4.83 vs 4.83; blind 3.83 vs 3.83) |
| v2-medium-05 | `gemma4:31b-cloud` | 0.33 / +0.33 | 1.17 / -1.17 | yes (April 4.00 vs 3.83; blind 4.33 vs 2.67) |
| v2-medium-06 | `deepseek-v3.2` | 0.83 / -0.50 | 0.17 / +0.17 | yes (April 3.50 vs 2.33; blind 3.00 vs 2.50) |
| v2-anchor-07 | `minimax-m2.7-cloud` | 0.50 / -0.17 | 1.00 / +0.00 | yes (April 4.83 vs 2.50; blind 4.67 vs 2.50) |
| v3-notebook-01 | `gemma4:31b-cloud` | 0.17 / -0.17 | 1.17 / -1.17 | yes (April 5.00 vs 3.67; blind 4.83 vs 2.50) |

- Overall MAD across 16 anchor rows (96 criterion pairs): **0.792**
- Overall signed mean (blind minus April): **-0.604**
- Worst single anchor row MAD: **1.83** (`v2-deep-03`, high anchor)
- Proposed gate: overall MAD <= 0.5 and no single task MAD > 1.0. **Outcome: FAIL.**
- Anchor order preserved in 8 of 8 tasks (deep-04 was a tie in April and a tie blind).
- Read: the new judge is harsher than April by about 0.6 points per criterion, unevenly. It is close to April on deep-02, anchor-07 and the `gpt5.4-xhigh` rows of medium-05 and v3; a full point lower across the board on deep-04, where April awarded near-perfect scores to almost every model; harder on the weaker cloud anchors on medium-05 and v3; and in outright disagreement with April on deep-03, where April called the `gpt5.4-xhigh` plan the clearest in the set and both blind judges read it as hedged and not decision-complete.

## 3. Round 2 re-run and judge agreement

| Task | Model | April | R1 blind | R2 blind | R1 signed | R2 signed | R1 vs R2 MAD |
|---|---|---:|---:|---:|---:|---:|---:|
| v2-deep-03 | `gpt5.4-xhigh` | 4.83 | 3.00 | 3.17 | -1.83 | -1.67 | 0.17 |
| v2-deep-03 | `qwen-3.6plus` | 3.83 | 2.83 | 2.67 | -1.00 | -1.17 | 0.17 |
| v2-deep-04 | `gpt5.4-xhigh` | 4.83 | 3.83 | 4.17 | -1.00 | -0.67 | 0.33 |
| v2-deep-04 | `gemma4:31b-cloud` | 4.83 | 3.83 | 3.67 | -1.00 | -1.17 | 0.17 |
| v2-medium-05 | `gpt5.4-xhigh` | 4.00 | 4.33 | 4.33 | +0.33 | +0.33 | 0.33 |
| v2-medium-05 | `gemma4:31b-cloud` | 3.83 | 2.67 | 2.67 | -1.17 | -1.17 | 0.00 |
| v3-notebook-01 | `gpt5.4-xhigh` | 5.00 | 4.83 | 4.83 | -0.17 | -0.17 | 0.33 |
| v3-notebook-01 | `gemma4:31b-cloud` | 3.67 | 2.50 | 2.33 | -1.17 | -1.33 | 0.17 |

| Task | Model | R1 blind | R2 blind | R1 vs R2 MAD |
|---|---|---:|---:|---:|
| v2-deep-03 | `gpt5.6-sol-xhigh` | 4.83 | 4.83 | 0.00 |
| v2-deep-03 | `gpt5.6-luna-max` | 4.17 | 4.50 | 0.33 |
| v2-deep-04 | `gpt5.6-sol-xhigh` | 4.83 | 4.83 | 0.00 |
| v2-deep-04 | `gpt5.6-luna-max` | 4.33 | 4.50 | 0.17 |
| v2-medium-05 | `gpt5.6-sol-xhigh` | 4.83 | 4.67 | 0.17 |
| v2-medium-05 | `gpt5.6-luna-max` | 4.67 | 4.33 | 0.33 |
| v3-notebook-01 | `gpt5.6-sol-xhigh` | 3.67 | 3.67 | 0.33 |
| v3-notebook-01 | `gpt5.6-luna-max` | 3.17 | 2.83 | 0.67 |

The second judge reproduced the first to within about a third of a point on every anchor row and every new-model row except Luna on v3 (0.67), while both sat well below April on the same anchors. The drift is therefore a systematic scale difference between this judge and April's scorer, not single-judge noise. On deep-03 both judges independently scored the `gpt5.4-xhigh` plan about 3.1 against April's 4.83.

## 4. Pooled calibration and per-task offsets

| Task | Rounds | High anchor MAD / signed | Low anchor MAD / signed | Per-task offset |
|---|---|---:|---:|---:|
| v2-deep-01 | 1 | 0.83 / -0.83 | 0.83 / -0.50 | +0.67 |
| v2-deep-02 | 1 | 0.17 / -0.17 | 0.67 / -0.67 | +0.42 |
| v2-deep-03 | 1,2 | 1.75 / -1.75 | 1.08 / -1.08 | +1.42 |
| v2-deep-04 | 1,2 | 0.83 / -0.83 | 1.08 / -1.08 | +0.96 |
| v2-medium-05 | 1,2 | 0.33 / +0.33 | 1.17 / -1.17 | +0.42 |
| v2-medium-06 | 1 | 0.83 / -0.50 | 0.17 / +0.17 | +0.17 |
| v2-anchor-07 | 1 | 0.50 / -0.17 | 1.00 / +0.00 | +0.08 |
| v3-notebook-01 | 1,2 | 0.17 / -0.17 | 1.25 / -1.25 | +0.71 |

Pooled overall MAD 0.792, signed -0.604, worst row MAD 1.75; the gate still fails. The per-task offset is the negated mean of the two anchors' signed differences on that task.

## 5. User decision

The user was shown the round-1 calibration table and asked to choose between using raw blind scores, a flat offset, per-task offsets, a second blind pass, or manual re-anchoring. Decision (2026-09-17): re-run the four most drifted tasks with a second blind judge, then adjust the new models' blind scores onto the April scale with a **per-task offset** (the user first suggested a flat 0.6 shift, then chose per-task after seeing that the drift ranged from 0.08 on the anchor to 1.42 on deep-03). Adjusted score per criterion = round(pooled blind score + per-task offset), clamped to 1 to 5. No April score was changed.

## 6. Adjusted technical scores for the new models

### v2-deep-01 (offset +0.67)

| Model | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| `gpt5.4-xhigh` April (frozen) | 4 | 4 | 4 | 4 | 4 | 5 | 4.17 |
| `gpt5.4-xhigh` pooled blind | 3 | 3 | 4 | 3 | 3 | 4 | 3.33 |
| `gpt5.6-sol-xhigh` pooled blind | 5 | 5 | 4 | 5 | 4 | 4 | 4.50 |
| `gpt5.6-sol-xhigh` **adjusted** | 5 | 5 | 5 | 5 | 5 | 5 | **5.00** |
| `gpt5.6-luna-max` pooled blind | 5 | 5 | 4 | 4 | 4 | 5 | 4.50 |
| `gpt5.6-luna-max` **adjusted** | 5 | 5 | 5 | 5 | 5 | 5 | **5.00** |

### v2-deep-02 (offset +0.42)

| Model | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| `gpt5.4-xhigh` April (frozen) | 5 | 5 | 5 | 5 | 4 | 5 | 4.83 |
| `gpt5.4-xhigh` pooled blind | 5 | 5 | 5 | 5 | 4 | 4 | 4.67 |
| `gpt5.6-sol-xhigh` pooled blind | 5 | 4 | 5 | 4 | 4 | 5 | 4.50 |
| `gpt5.6-sol-xhigh` **adjusted** | 5 | 4 | 5 | 4 | 4 | 5 | **4.50** |
| `gpt5.6-luna-max` pooled blind | 5 | 5 | 5 | 4 | 4 | 4 | 4.50 |
| `gpt5.6-luna-max` **adjusted** | 5 | 5 | 5 | 4 | 4 | 4 | **4.50** |

### v2-deep-03 (offset +1.42)

| Model | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| `gpt5.4-xhigh` April (frozen) | 5 | 5 | 5 | 5 | 4 | 5 | 4.83 |
| `gpt5.4-xhigh` pooled blind | 3 | 3.5 | 4 | 2 | 3 | 3 | 3.08 |
| `gpt5.6-sol-xhigh` pooled blind | 5 | 5 | 5 | 4 | 5 | 5 | 4.83 |
| `gpt5.6-sol-xhigh` **adjusted** | 5 | 5 | 5 | 5 | 5 | 5 | **5.00** |
| `gpt5.6-luna-max` pooled blind | 4.5 | 4.5 | 5 | 4 | 4 | 4 | 4.33 |
| `gpt5.6-luna-max` **adjusted** | 5 | 5 | 5 | 5 | 5 | 5 | **5.00** |

### v2-deep-04 (offset +0.96)

| Model | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| `gpt5.4-xhigh` April (frozen) | 5 | 5 | 5 | 5 | 5 | 4 | 4.83 |
| `gpt5.4-xhigh` pooled blind | 4.5 | 4.5 | 4 | 4 | 3 | 4 | 4.00 |
| `gpt5.6-sol-xhigh` pooled blind | 5 | 5 | 5 | 5 | 4 | 5 | 4.83 |
| `gpt5.6-sol-xhigh` **adjusted** | 5 | 5 | 5 | 5 | 5 | 5 | **5.00** |
| `gpt5.6-luna-max` pooled blind | 5 | 4.5 | 5 | 4 | 4 | 4 | 4.42 |
| `gpt5.6-luna-max` **adjusted** | 5 | 5 | 5 | 5 | 5 | 5 | **5.00** |

### v2-medium-05 (offset +0.42)

| Model | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| `gpt5.4-xhigh` April (frozen) | 4 | 4 | 3 | 4 | 4 | 5 | 4.00 |
| `gpt5.4-xhigh` pooled blind | 4.5 | 5 | 3.5 | 4 | 4 | 5 | 4.33 |
| `gpt5.6-sol-xhigh` pooled blind | 5 | 5 | 4 | 5 | 4.5 | 5 | 4.75 |
| `gpt5.6-sol-xhigh` **adjusted** | 5 | 5 | 4 | 5 | 5 | 5 | **4.83** |
| `gpt5.6-luna-max` pooled blind | 5 | 5 | 4 | 4.5 | 4 | 4.5 | 4.50 |
| `gpt5.6-luna-max` **adjusted** | 5 | 5 | 4 | 5 | 4 | 5 | **4.67** |

### v2-medium-06 (offset +0.17)

| Model | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| `gpt5.4-xhigh` April (frozen) | 3 | 4 | 2 | 3 | 4 | 5 | 3.50 |
| `gpt5.4-xhigh` pooled blind | 3 | 3 | 3 | 3 | 3 | 3 | 3.00 |
| `gpt5.6-sol-xhigh` pooled blind | 4 | 4 | 3 | 4 | 4 | 4 | 3.83 |
| `gpt5.6-sol-xhigh` **adjusted** | 4 | 4 | 3 | 4 | 4 | 4 | **3.83** |
| `gpt5.6-luna-max` pooled blind | 4 | 5 | 4 | 4 | 4 | 4 | 4.17 |
| `gpt5.6-luna-max` **adjusted** | 4 | 5 | 4 | 4 | 4 | 4 | **4.17** |

### v2-anchor-07 (offset +0.08)

| Model | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| `gpt5.4-xhigh` April (frozen) | 5 | 5 | 4 | 5 | 5 | 5 | 4.83 |
| `gpt5.4-xhigh` pooled blind | 5 | 5 | 5 | 4 | 5 | 4 | 4.67 |
| `gpt5.6-sol-xhigh` pooled blind | 5 | 5 | 5 | 5 | 4 | 5 | 4.83 |
| `gpt5.6-sol-xhigh` **adjusted** | 5 | 5 | 5 | 5 | 4 | 5 | **4.83** |
| `gpt5.6-luna-max` pooled blind | 5 | 5 | 5 | 4 | 4 | 5 | 4.67 |
| `gpt5.6-luna-max` **adjusted** | 5 | 5 | 5 | 4 | 4 | 5 | **4.67** |

### v3-notebook-01 (offset +0.71)

| Model | Calculation correctness | Code quality/executability | Engineering judgement | Unit/assumption handling | Notebook traceability/clarity | Completeness of deliverable | Mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| `gpt5.4-xhigh` April (frozen) | 5 | 5 | 5 | 5 | 5 | 5 | 5.00 |
| `gpt5.4-xhigh` pooled blind | 5 | 4.5 | 5 | 5 | 4.5 | 5 | 4.83 |
| `gpt5.6-sol-xhigh` pooled blind | 5 | 4 | 3 | 3.5 | 3.5 | 3 | 3.67 |
| `gpt5.6-sol-xhigh` **adjusted** | 5 | 5 | 4 | 4 | 4 | 4 | **4.33** |
| `gpt5.6-luna-max` pooled blind | 2.5 | 2 | 3.5 | 3.5 | 3 | 3.5 | 3.00 |
| `gpt5.6-luna-max` **adjusted** | 3 | 3 | 4 | 4 | 4 | 4 | **3.67** |

## 7. Execution re-verification (v3-notebook-01)

Method: code cells extracted from the raw outputs and exec'd in order in one shared namespace
(tools/exec_v3.py). Sol cells rebuilt from the fence-less text using the `# Code Cell N` markers;
Luna cells taken from the fenced ```python blocks. Per-cell logs in exec/<model>/run_log.txt.

### gpt5.6-sol-xhigh
- 6 code cells; runs end to end, all asserts pass.
- Selected width: 3.0 m x 3.0 m.
- Governing case: LC2 (no-uplift check; 2.9 m fails on LC2 qmin). Maximum-bearing case at 3.0 m: LC3 (178.89 kPa).
- Printed table at B = 3.0 m matches the reference values (LC1 88.89/155.56, LC2 2.22/153.33, LC3 98.89/178.89 kPa).
- Matches the capture-time execution note in the run record.

### gpt5.6-luna-max
- 6 code cells; cells 1-3 run, cell 4 raises AssertionError inside evaluate_case() (cell 3 line 38),
  so cells 5-6 never run: no selection, table, or conclusion is produced by the code.
- Cause (verified): pressure_at_point() returns N/B^2 + 6*My*x/B^3 + 6*Mx*y/B^3. At the corner x = y = B/2
  this is N/B^2 + 3*My/B^2 + 3*Mx/B^2, not the closed form N/B^2 + 6*(|Mx|+|My|)/B^3 that the same
  function then asserts against. The correct point form is 12*M*x/B^4. For B = 2.4 m, LC1 the corner
  function gives 269.10 kPa against the closed form 256.08 kPa, so the isclose assert fails.
- Selected width / governing case from code: none (not reached). The Markdown conclusion states 3.0 m,
  LC2 governing, LC3 maximum bearing, but those numbers are not produced by the notebook's own code.
- Matches the capture-time execution note in the run record.

## 8. Manual override notes (Step 4.1)

No technical score was overridden. Items considered, with the reason for leaving the adjusted blind score in place:

- `v3-notebook-01`, `gpt5.6-luna-max`, Code quality/executability (adjusted 3) and Calculation correctness (adjusted 3). Both blind judges found by inspection that `pressure_at_point()` uses `6*M*x/B^3` instead of `12*M*x/B^4`, so the corner pressures disagree with the closed form and the notebook's own `isclose` assert fails on the first candidate. Direct execution with the venv Python (standard library only) confirms this: cells 1 to 3 run, cell 4 raises `AssertionError`, cells 5 and 6 never run, and no width or governing case is produced by the code. The narrative conclusion (3.0 m, LC2, LC3 maximum bearing) is correct but is not produced by the notebook. April never scored a notebook that failed to run; its lowest executability score (4) went to notebooks that ran with conclusion-level errors. An adjusted 3 sits one point below that floor, which is consistent, so no override.
- `v3-notebook-01`, `gpt5.6-sol-xhigh`, Engineering judgement / Unit-assumption handling / Notebook traceability / Completeness (adjusted 4, 4, 4, 4). Both judges deducted for quoting the compact `6|M|/B^3` formula without the requested derivation, giving no justification for the rigid linear model beyond one sentence, and never defining eccentricities or their directions. A text search of the raw output confirms none of `B^4`, `/12`, `I_x`, `e_x` or "eccentric" appears. These are content gaps against explicit "you must" items in the brief and match the evaluator notes' scoring guidance, so no override. The copy-time loss of Markdown fences was neutralised in the pack and was not penalised by either judge.
- `v2-medium-06`, `gpt5.6-sol-xhigh`, Correctness (adjusted 4). The judge noted that the response claims `NaN` "can silently produce a PASS" in the current code, whereas `nan < 1.0` is `False` and the supplied `status_from_ratio()` therefore returns `FAIL`. The raw output contains that claim verbatim, so the deduction is grounded. No override.
- `v2-deep-01`, `gpt5.6-sol-xhigh`, Clarity. The judge listed the absolute local file-path links as minor noise. Those links are a capture artefact (this run received the context as attached files; see the run record) rather than a model-quality issue, but the adjusted Clarity score is already 5, so an override would change nothing.
- Saturation. On deep-01, deep-03 and deep-04 the per-task offset pushes every criterion for both new models to the 5 cap. The blind margins over `gpt5.4-xhigh` on those tasks (about 1.2 to 1.8 points on the six-criterion mean) are therefore understated by the April-scale scores. This is a limit of the 1 to 5 scale, not an override, and the raw blind scores are recorded below for reference.

## 9. Practicality scores (Step 4.2, unblinded)

April's principles, read from the seven April scorecards and the v2 report: the free Ollama cloud route scored 4 to 5 unless a run failed operationally; the paid API middle tier (`qwen-3.6plus`) scored 3 on the primary tasks and 2 on the anchor; the premium route (`gpt5.4-xhigh`) scored 3 on the primary tasks, 2 where the run was "slower and less economical than the best free/cloud answers" (deep-02, anchor-07), and 4 on v3, where latency was treated as a light secondary factor. Refusals, truncation and failure to wait for context were not observed for either new model on any task.

`gpt5.6-sol-xhigh` (same Codex VS Code route as April's `gpt5.4-xhigh`, premium subscription/API tier, list price about $20 per 1M output tokens): answered in under 1 to about 2 minutes on every v2 primary task (April's `gpt5.4-xhigh` was noted as "relatively slow"), used about 21k to 25k Codex tokens per v2 task, waited for the context message every time, and had no refusals or truncation. It is therefore scored exactly as the reference premium run: 3 on the six primary tasks (including deep-02, where it answered within a minute), 2 on the anchor (3 min 30 s with web lookup and about 85k tokens; faster than April's 4 min 38 s but still the slowest and most expensive class of answer), and 4 on v3 (latency not captured, about 23k tokens, notebook runs end to end).

`gpt5.6-luna-max` (same Codex route, budget API tier listed at $0.20 / $1.20 per 1M input / output tokens, so cheaper than `qwen-3.6plus`): answered in about 3 to 4 minutes on most v2 primary tasks (1 min on deep-04), used about 20k to 31k tokens per v2 task, waited for the context message every time, and had no refusals or truncation. The low list price argues for a 4, the observed latency (comparable to the slowest April runs) and the subscription route used for this capture argue for a 3; on balance it is scored 3 on the six primary tasks, in line with the paid-API tier April used for `qwen-3.6plus`. On the anchor it took over 6 min 30 s and about 131k tokens, the slowest run in the whole set, so 2. On v3 it took about 4 minutes and its notebook stops with an `AssertionError` at code cell 4 until a one-line formula fix is applied, so 3, matching the April scores given to `kimi-k2-thinking` and `deepseek-v3.2` for long think time alone.

| Task | `gpt5.4-xhigh` April | `gpt5.6-sol-xhigh` | `gpt5.6-luna-max` |
|---|---:|---:|---:|
| v2-deep-01 | 3 | 3 | 3 |
| v2-deep-02 | 2 | 3 | 3 |
| v2-deep-03 | 3 | 3 | 3 |
| v2-deep-04 | 3 | 3 | 3 |
| v2-medium-05 | 3 | 3 | 3 |
| v2-medium-06 | 3 | 3 | 3 |
| v2-anchor-07 | 2 | 2 | 2 |
| v3-notebook-01 | 4 | 4 | 3 |

## 10. Final scores written to the scorecards

### v2-deep-01

| Model | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Economics/practicality | Overall mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `gpt5.6-sol-xhigh` | 5 | 5 | 5 | 5 | 5 | 5 | 3 | 4.71 |
| `gpt5.6-luna-max` | 5 | 5 | 5 | 5 | 5 | 5 | 3 | 4.71 |

### v2-deep-02

| Model | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Economics/practicality | Overall mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `gpt5.6-sol-xhigh` | 5 | 4 | 5 | 4 | 4 | 5 | 3 | 4.29 |
| `gpt5.6-luna-max` | 5 | 5 | 5 | 4 | 4 | 4 | 3 | 4.29 |

### v2-deep-03

| Model | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Economics/practicality | Overall mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `gpt5.6-sol-xhigh` | 5 | 5 | 5 | 5 | 5 | 5 | 3 | 4.71 |
| `gpt5.6-luna-max` | 5 | 5 | 5 | 5 | 5 | 5 | 3 | 4.71 |

### v2-deep-04

| Model | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Economics/practicality | Overall mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `gpt5.6-sol-xhigh` | 5 | 5 | 5 | 5 | 5 | 5 | 3 | 4.71 |
| `gpt5.6-luna-max` | 5 | 5 | 5 | 5 | 5 | 5 | 3 | 4.71 |

### v2-medium-05

| Model | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Economics/practicality | Overall mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `gpt5.6-sol-xhigh` | 5 | 5 | 4 | 5 | 5 | 5 | 3 | 4.57 |
| `gpt5.6-luna-max` | 5 | 5 | 4 | 5 | 4 | 5 | 3 | 4.43 |

### v2-medium-06

| Model | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Economics/practicality | Overall mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `gpt5.6-sol-xhigh` | 4 | 4 | 3 | 4 | 4 | 4 | 3 | 3.71 |
| `gpt5.6-luna-max` | 4 | 5 | 4 | 4 | 4 | 4 | 3 | 4.00 |

### v2-anchor-07

| Model | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Economics/practicality | Overall mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `gpt5.6-sol-xhigh` | 5 | 5 | 5 | 5 | 4 | 5 | 2 | 4.43 |
| `gpt5.6-luna-max` | 5 | 5 | 5 | 4 | 4 | 5 | 2 | 4.29 |

### v3-notebook-01

| Model | Calculation correctness | Code quality/executability | Engineering judgement | Unit/assumption handling | Notebook traceability/clarity | Completeness of deliverable | Practical usability | Overall mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `gpt5.6-sol-xhigh` | 5 | 5 | 4 | 4 | 4 | 4 | 4 | 4.29 |
| `gpt5.6-luna-max` | 3 | 3 | 4 | 4 | 4 | 4 | 3 | 3.57 |

## 11. Seeds and label mapping

### Round 1 (base seed 20260917)

| Task | Seed | A | B | C | D |
|---|---:|---|---|---|---|
| v2-deep-01 | 20260918 | `gpt5.6-luna-max` | `qwen-3.6plus` | `gpt5.6-sol-xhigh` | `gpt5.4-xhigh` |
| v2-deep-02 | 20260919 | `gpt5.4-xhigh` | `minimax-m2.7-cloud` | `gpt5.6-luna-max` | `gpt5.6-sol-xhigh` |
| v2-deep-03 | 20260920 | `qwen-3.6plus` | `gpt5.6-luna-max` | `gpt5.6-sol-xhigh` | `gpt5.4-xhigh` |
| v2-deep-04 | 20260921 | `gemma4:31b-cloud` | `gpt5.4-xhigh` | `gpt5.6-sol-xhigh` | `gpt5.6-luna-max` |
| v2-medium-05 | 20260922 | `gpt5.6-luna-max` | `gemma4:31b-cloud` | `gpt5.6-sol-xhigh` | `gpt5.4-xhigh` |
| v2-medium-06 | 20260923 | `deepseek-v3.2` | `gpt5.6-luna-max` | `gpt5.6-sol-xhigh` | `gpt5.4-xhigh` |
| v2-anchor-07 | 20260924 | `gpt5.6-luna-max` | `minimax-m2.7-cloud` | `gpt5.4-xhigh` | `gpt5.6-sol-xhigh` |
| v3-notebook-01 | 20260925 | `gpt5.6-luna-max` | `gemma4:31b-cloud` | `gpt5.6-sol-xhigh` | `gpt5.4-xhigh` |

### Round 2 (base seed 20261017)

| Task | Seed | A | B | C | D |
|---|---:|---|---|---|---|
| v2-deep-03 | 20261020 | `gpt5.6-sol-xhigh` | `gpt5.6-luna-max` | `gpt5.4-xhigh` | `qwen-3.6plus` |
| v2-deep-04 | 20261021 | `gpt5.6-luna-max` | `gpt5.6-sol-xhigh` | `gpt5.4-xhigh` | `gemma4:31b-cloud` |
| v2-medium-05 | 20261022 | `gpt5.6-sol-xhigh` | `gpt5.6-luna-max` | `gemma4:31b-cloud` | `gpt5.4-xhigh` |
| v3-notebook-01 | 20261025 | `gpt5.4-xhigh` | `gpt5.6-sol-xhigh` | `gpt5.6-luna-max` | `gemma4:31b-cloud` |

Shuffle: Python `random.Random(seed).shuffle` over the list `[gpt5.6-sol-xhigh, gpt5.6-luna-max, gpt5.4-xhigh, <low anchor>]`, then labelled A to D in the shuffled order.

## 12. De-anonymised judge replies

Each reply is reproduced verbatim from the judge subagent, with the model name added after each response label. Judges never saw these names.

### Round 1: v2-deep-01

Key: A = `gpt5.6-luna-max`, B = `qwen-3.6plus`, C = `gpt5.6-sol-xhigh`, D = `gpt5.4-xhigh`

#### Blind judge report: v2-deep-01

**Task summary:** Review a three-file pandas beam-check package (section library, analysis pipeline, reporting) to find why major-axis utilisations are ~10x too high after a refactor, identify secondary risks, propose the smallest safe multi-file fix, and list pre-merge tests.

##### Score table

| Response | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Note |
|---|---|---|---|---|---|---|---|
| A (`gpt5.6-luna-max`) | 5 | 5 | 4 | 4 | 4 | 5 | Finds the 1e2/1e3 root cause, the signed-max envelope, the first/max mismatch, rounding-before-status and the raw KeyError, and ships complete runnable code, but ranks a speculative axis-naming question above the real envelope defect and rewrites more than strictly necessary. |
| B (`qwen-3.6plus`) | 3 | 2 | 4 | 2 | 4 | 4 | Correct root cause with a good numeric table and a minimal, compatible patch (KeyError message, 1e3), but misses the signed-max envelope, the rounding-before-status bug and the first/max mismatch, and proposes a test that enshrines silent NaN propagation. |
| C (`gpt5.6-sol-xhigh`) | 5 | 5 | 4 | 5 | 4 | 4 | Root cause, envelope, rounding, mismatch and NaN handling all found in the right severity order with an explicit unit chain and stated engineering assumptions, but the pipeline validations are described in prose rather than code and the unknown-section guard is not mentioned. |
| D (`gpt5.4-xhigh`) | 3 | 3 | 4 | 3 | 3 | 4 | Correct root cause with clean dimensional analysis plus the rounding and section/moment mismatch issues, but misses the signed-max envelope despite quoting the offending line, gives the fix almost entirely as prose, and has off-by-one line references. |

##### Top weaknesses per response

**A (`gpt5.6-luna-max`)**
- Severity ordering is off: the "Mz vs Wpl_y" axis-convention question (a confirm-this item, not a demonstrated defect) is ranked High and above the signed-max envelope bug, which the task explicitly asks to order by severity.
- Flags the uncontextualised KeyError for unknown sections (finding 6) but the patch does not add the guard.
- The "recommended" patch replaces three function bodies and adds a custom groupby aggregator, which is proportionate but not minimal; the NaN check inside `major_axis_utilisation` is unreachable once `_governing_signed_moment` raises first.
- New `ValueError`s on all-NaN members and multi-section members are behaviour changes that will break previously tolerated dirty inputs (fail-loud is right, but it is not called out as a compatibility change).

**B (`qwen-3.6plus`)**
- Misses the signed-max envelope entirely: `"Mz_kNm": "max"` will still select +80 over -120 after this patch, so hogging-governed members remain under-reported.
- Misses the rounding-before-status bug in `reporting.py` even while analysing how NaN flows through `decorate_status`; also misses the first/max section mismatch.
- `return float("inf")` on non-positive capacity silently converts a data/library problem into a FAIL instead of surfacing it; the guard is also effectively unreachable with the current library.
- Test 6 ("NaN input produces NaN utilisation, not crash") locks in the very behaviour it lists as risk 2c; the boundary test (1.0 / 1.001) does not exercise the rounding defect.

**C (`gpt5.6-sol-xhigh`)**
- The "smallest safe patch" for `analysis_pipeline.py` is partly bullets ("reject invalid moments", "reject multiple sections") with only the abs/max aggregation shown "conceptually", so an implementer has to design the validations.
- Does not mention the unknown-section guard at all.
- The proposed `Mz_abs_kNm` approach makes the summary's `Mz_kNm` column unsigned, changing an output column's meaning (acknowledged, but still a downstream compatibility change).
- Absolute local file-path links and rating rounding-before-status as "High" (on par with the envelope) add minor noise to an otherwise well-ordered review.

**D (`gpt5.4-xhigh`)**
- Misses the signed-max envelope even though it cites lines 20-25 and quotes `"Mz_kNm": "max"`; no governing-moment test proposed.
- Fix is under-specified: the only code shown is the trivial section-library function; the member consistency guard and the reporting change are prose only.
- Line references are off by one (`section_library.py:10` is the `fy_MPa` line, the bug is line 11; `analysis_pipeline.py:15` is `props =`, the formula is line 16).
- No mention of unknown-section handling or NaN coercion.

##### Ranking (best to worst)

1. **C (`gpt5.6-sol-xhigh`)** – mean 4.50
2. **A (`gpt5.6-luna-max`)** – mean 4.50
3. **D (`gpt5.4-xhigh`)** – mean 3.33
4. **B (`qwen-3.6plus`)** – mean 3.17

A and C tie on the mean; C is placed first because its severity ordering and patch scope track the brief more closely (envelope ranked directly under the unit bug, minimal aggregation change, explicit assumptions on Wpl vs Wel, section class, LTB and gamma_M0), while A is more concrete and auditable as code but mis-orders the axis question and patches more broadly. Either ordering of A/C is defensible.

##### Practical significance

The gap between the top pair (A, C) and the bottom pair (D, B) is practically significant: all four find the 1e2-vs-1e3 conversion and would remove the reported 10x symptom, but only A and C catch the signed-maximum envelope, so a patch merged from B or D would still under-report members governed by hogging moment and could even emit negative utilisations, which is a genuine engineering-safety residual rather than a style difference. Within the top pair the differences are presentational (complete code vs. prose validations, severity ordering, sign retention in the summary column) and would be resolved in a normal review round. Within the bottom pair D edges B because its residual set after merge (raw KeyError, silent NaN) is less dangerous than B's (false PASS at 1.000x, section/moment mismatch), and B's NaN-propagation test would actively cement a bad behaviour.

##### Manual-review watch-outs

- Confirm with the analysis export that `Mz_kNm` is the major-axis (y-y, `Wpl_y`) moment; A and C flag this correctly, neither changes it, and the fix must not be extended to rename fields without that confirmation.
- Named-aggregation syntax used by A and C (`agg(Section=("Section", "first"), ...)`) requires pandas >= 0.25; check the project's pinned version.
- A's and C's raise-on-NaN and raise-on-multiple-sections are behaviour changes; check whether real result exports contain such rows before merging, and decide whether the error should name the member (A's aggregator error does not).
- C's abs-then-max makes the summary `Mz_kNm` column unsigned; A's `_governing_signed_moment` keeps the sign and takes abs only in the ratio. Prefer the sign-preserving variant if downstream consumers read the summary moment.
- Reject B's `float("inf")` sentinel and its "NaN propagates" test; both mask data problems.
- D's line numbers are off by one; do not use them as-is in a PR description.
- Verify the numeric anchors before writing tests: M_pl,Rd = 100.65 kNm (254x146x31) and 178.475 kNm (305x165x40); 50 kNm / 100.65 = 0.4968; 50.325 kNm gives exactly 0.5.
- The rounding fix must keep `sort_values(["Status", "Util_major"])` semantics; sorting on the rounded column is fine for display but status must come from the raw value.
- gamma_M0 = 1.0, no LTB reduction and plastic (Class 1/2) resistance are implicit in the formula; C names these, A names gamma_M0 only. Document them in the API rather than in the fix.
- No response addressed the unknown-section guard and the envelope together; the merged patch should combine B's KeyError message with A/C's envelope change.

### Round 1: v2-deep-02

Key: A = `gpt5.4-xhigh`, B = `minimax-m2.7-cloud`, C = `gpt5.6-luna-max`, D = `gpt5.6-sol-xhigh`

#### Blind judge report: v2-deep-02

**Task summary:** Code-review a three-file steel-beam ULS screening package (load factors, major-axis resistance, review table) and report severity-ordered findings, engineering impact, minimum fix directions, and deliberately unescalated items, focusing on units, combinations, and reporting integrity.

##### Score table

| Response | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Note |
|---|---|---|---|---|---|---|---|
| A (`gpt5.4-xhigh`) | 5 | 5 | 5 | 5 | 4 | 4 | Finds all three planted bugs with exact line references, correct severity ordering, and proportionate test-backed fixes; misses only the unused `combination` label. |
| B (`minimax-m2.7-cloud`) | 2 | 2 | 2 | 2 | 3 | 3 | Misses the 1000x unit error and explicitly declares the `1e6` conversion "correct", misreads the ascending sort as returning the worst case, and promotes a non-bug (gamma_M0) to Critical. |
| C (`gpt5.6-luna-max`) | 5 | 5 | 5 | 4 | 4 | 4 | All three primary bugs found with a correct worked numeric example, plus useful observations on the unused combination label and package imports; the finding-1 fix direction over-reaches the "minimum". |
| D (`gpt5.6-sol-xhigh`) | 5 | 4 | 5 | 4 | 4 | 5 | All three primary bugs with a full dimensional derivation and a well-argued extra finding on the combination label, but line references do not match the supplied files and the unconservative load-factor bug is rated only High. |

##### Top weaknesses per response

**A (`gpt5.4-xhigh`)**
- Does not observe that `row["combination"]` is copied to the output but never influences the factors, which is part of the "combination trap" the task title advertises.
- Finding 4 wording is muddled ("the status check uses `< 1.0` rather than the raw value" conflates the threshold rule with the rounding problem).
- Line reference for finding 1 says `load_factors.py:5-6` "defines" `ULS_GAMMA_Q`; the constant is on line 2, the function on 5-6 (minor).

**B (`minimax-m2.7-cloud`)**
- Misses the `cm3` vs `mm3` unit error entirely and, worse, asserts in the not-escalated table that "The `1e6` conversion is correct but opaque" — an overconfident endorsement of a hidden 1000x error that would ship.
- Misreads `sort` ascending + `[:1]` as returning "the worst-case beam only"; it returns the least-utilised row, so the reporting bug is far more dangerous than B describes.
- Rates missing gamma_M0 as Critical while admitting it produces correct numbers under gamma_M0 = 1.0; the "overstated by a factor of 1.0" and "elastic analysis" reasoning is confused.
- Finding-4 fix (`util <= 1.0` on the rounded value) would pass a raw utilisation of 1.004, and the claim "No type hints on function signatures" is false — every function is annotated.

**C (`gpt5.6-luna-max`)**
- "Minimum fix" for finding 1 proposes making the combination an input and applying psi factors, which is a larger API change than the one-line factor correction the task asks for.
- Gives no line references, which slightly reduces auditability compared with A.
- Psi-factor mention goes beyond anything the supplied inputs can support.

**D (`gpt5.6-sol-xhigh`)**
- Line references are consistently off (`reporting.py:14-15` for the sort/slice at 17-18, `reporting.py:7-11` for rounding at 8-14, `load_factors.py:6-7` for the function at 5-6).
- Rates the unfactored imposed load as High rather than Critical, even though it is the archetypal unconservative ULS error affecting every row.
- Finding 5 (combination label) and the not-escalated list are good but slightly lengthen a review that was asked to be short.

##### Ranking (best to worst)

1. **A (`gpt5.4-xhigh`)** — mean 4.67
2. **C (`gpt5.6-luna-max`)** — mean 4.50
3. **D (`gpt5.6-sol-xhigh`)** — mean 4.50
4. **B (`minimax-m2.7-cloud`)** — mean 2.33

C is placed above D on tie-break because its severity labelling of the unconservative load-factor bug is sounder and it contains no inaccurate location claims; D's superior clarity and extra combination-label finding nearly offset this.

##### Practical significance

A, C, and D would all correctly block the release: each identifies the missing 1.50 factor on imposed load, the 1000x resistance underestimate from treating cm3 as mm3, and the review table that silently returns only the least-utilised member. The differences among them are second-order — precision of line references, proportionality of fix direction, and whether the unused `combination` label is called out. B is materially different in kind: it would leave the 1000x unit error in place while certifying it as correct, would mislead readers into thinking the truncated report shows the governing case rather than hiding it, and would spend reviewer attention on a gamma_M0 "Critical" that B itself concedes yields correct numbers. The gap between B and the other three is a pass/fail gap for the review's purpose; the gaps among A, C, and D are stylistic and would not change the engineering outcome.

##### Manual-review watch-outs

- Independently confirm the unit fix: 100 cm3 x 355 MPa = 100,000 mm3 x 355 N/mm2 = 35.5e6 Nmm = 35.5 kNm, so the correct divisor is 1e3; C's and D's worked examples are arithmetically right and A's statement is consistent.
- Do not let B's confident "the 1e6 conversion is correct" pass; it is false, and it is the single most consequential error in any of the four responses.
- B's description of the reporting bug ("worst-case beam only") is a sort-direction misread; ascending sort plus `[:1]` returns the minimum utilisation.
- B's `<= 1.0` applied to the rounded value is unconservative (raw 1.004 rounds to 1.00 and passes); the correct fix, as A, C, and D state, is to compare the unrounded value.
- B's claim that functions lack type hints is false; all signatures in the supplied files are annotated.
- D's line numbers do not match the supplied files; A's do. Use A's references if citing locations.
- C's psi-factor and combination-as-input suggestions exceed the "minimum fix" brief; treat as optional direction, not a requirement.
- The High vs Critical label on the unit error is a judgement call: it is conservative in direction (every beam fails) but renders the tool unusable; all of A, C, D chose High, which is defensible.
- gamma_M0 omission is a documentation/scope gap, not a defect, under national annexes where gamma_M0 = 1.0; D's decision to leave it unescalated is the appropriate treatment.

### Round 1: v2-deep-03

Key: A = `qwen-3.6plus`, B = `gpt5.6-luna-max`, C = `gpt5.6-sol-xhigh`, D = `gpt5.4-xhigh`

#### Blind judge report: v2-deep-03

**Task summary:** Produce a decision-complete implementation plan for adding an optional serviceability summary (`DeflectionRatio = Deflection_mm / AllowableDeflection_mm`) to a small pandas-based design package (`io_contract.py`, `design_engine.py`, `report_writer.py`) without breaking ULS-only callers or the existing `RESULT_COLUMNS`-based report contract.

##### Score table

| Response | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Note |
|---|---|---|---|---|---|---|---|
| A (`qwen-3.6plus`) | 3 | 3 | 2 | 2 | 3 | 4 | Concrete and readable, but it silently changes `report_rows()` semantics (missing columns are dropped instead of raising), aggregates numerator and denominator independently (`max` / `first`), and leaves key decisions as "alternatively". |
| B (`gpt5.6-luna-max`) | 4 | 4 | 5 | 4 | 4 | 4 | Fully additive design with per-row governing ratio and explicit validation; slightly less decision-complete than C (tie-break, empty-frame handling, optional orchestration helper) and reuses the generic `Status` name. |
| C (`gpt5.6-sol-xhigh`) | 5 | 5 | 5 | 4 | 5 | 5 | Most decision-complete plan: additive APIs, always-DataFrame contract, paired governing-row selection with deterministic tie-break, strict fail-loud validation, and precise tests; the only debatable calls are rejecting negative deflections and omitting an SLS pass/fail field. |
| D (`gpt5.4-xhigh`) | 3 | 3 | 4 | 2 | 3 | 3 | Safe direction but not decision-complete: hedges nearly every choice ("or", "ideally", "depending on chosen API"), tentatively recommends the risky aggregate-then-divide rule, then explicitly defers the aggregation decision the task asked it to make. |

##### Top weaknesses per response

**A (`qwen-3.6plus`)**
- Modifies the existing `report_rows()` default path so that missing columns are silently omitted (`available = [c for c in cols if c in summary_df.columns]`); today `.loc[:, RESULT_COLUMNS]` raises `KeyError`, so this is a fail-fast regression for existing callers, contradicting the closing claim "No existing logic is modified".
- `build_sls_summary` aggregates `Deflection_mm` with `max` and `AllowableDeflection_mm` with `first`, then divides; if allowable limits vary across rows (e.g. different load cases/limits per member) the reported ratio pairs values from different rows.
- Not decision-complete: offers "alternatively add `include_sls` to `build_uls_summary`", mentions a `report_rows_combined` helper that is never specified, and leaves divide-by-zero handling as "replace with `pd.NA` or use `np.where`". The `pd.NA` suggestion would also break the `lambda ratio: ... if ratio <= 1.0` status mapping (ambiguous truth value of NA).
- Left-merge design puts `NaN` into report records for members without SLS data, with no mention of serialisation consequences downstream.

**B (`gpt5.6-luna-max`)**
- Some decisions left open: no tie-break rule for equal governing ratios, unspecified behaviour when deflection columns exist but every row is null (None vs empty frame, and whether `report_payload` then omits the key), and the orchestration helper is "optional".
- Uses the literal signed deflection with no `abs()` and flags sign convention as upstream; a negative deflection would silently yield a negative ratio and PASS. Acknowledged but not mitigated.
- Reuses the generic `Status` column name in the serviceability table, which is ambiguous if the two tables are ever joined.
- Refers to "the repository's existing test layout", which is not in the supplied context (minor invented assumption).

**C (`gpt5.6-sol-xhigh`)**
- Rejects negative deflections as invalid; this assumes an unsigned/magnitude convention and could reject legitimate signed FE output. It fails loudly rather than silently, but the sign convention is never discussed.
- Deliberately omits a serviceability pass/fail field; defensible scoping, but it leaves the SLS summary asymmetric with the ULS summary and pushes the PASS/FAIL derivation onto consumers.
- Empty-DataFrame sentinel is a good contract choice, but dtypes for the empty frame are not specified, which matters for concat/golden comparisons.

**D (`gpt5.4-xhigh`)**
- Not decision-complete: function names, writer shape, combined API, divide-by-zero handling and activation rule are all presented as options; the plan even closes by stating the aggregation rule "needs to be fixed before implementation".
- Tentatively recommends computing the ratio "after aggregation, not per raw row", which is the rule most likely to pair mismatched numerator/denominator values, and then lists that same rule as an unresolved risk.
- Tests are generic ("handled per spec without crashing" with no spec given; "depending on chosen API") and would not be executable as written.
- No worked schema, example values, or diagram; shallow reading of `normalise_columns` (mentions aliasing that the code does not do).

##### Ranking (best to worst)
1. **C (`gpt5.6-sol-xhigh`)** — mean 4.83
2. **B (`gpt5.6-luna-max`)** — mean 4.17
3. **D (`gpt5.4-xhigh`)** — mean 3.00
4. **A (`qwen-3.6plus`)** — mean 2.83

##### Practical significance
C and B occupy the same safe design space (fully additive, `RESULT_COLUMNS` and `report_rows()` untouched, opt-in sectioned report, per-row governing ratio) and either could be implemented without a further design round; the gap between them is mostly decision-completeness, with C fixing tie-breaks, empty-frame semantics and validation rules that B leaves for the implementer. The gap from B/C to D and A is material. D is safe but is effectively a pre-plan: an implementer would have to make the aggregation, activation and error-handling decisions themselves, and its one tentative recommendation points the wrong way. A is the only response that would ship a behavioural regression to an existing function (silent column dropping in `report_rows()`) and an engineering-meaning defect (independently aggregated max/first values), while asserting that no existing logic changed, so despite being the most concrete it is the riskiest to apply as written.

##### Manual-review watch-outs
- Confirm the judgement that A's `report_rows()` change is a regression: it converts a `KeyError` on malformed frames into silent field omission on the default (ULS-only) path, not just the new opt-in path.
- Check the engineering claim underlying the B/C vs A/D split: whether `AllowableDeflection_mm` can vary per row within a `Member`/`Section` group in this package. If it is guaranteed constant, A's `max`/`first` pairing is harmless and D's "after aggregation" hint is acceptable; if not, the per-row governing ratio is required.
- A's suggested `pd.NA` divide-by-zero guard would raise `TypeError` in the `Status_SLS` lambda; verify if reviewers weight the un-shown mitigation.
- C's rejection of negative deflections and B's literal use of signed values are opposite calls on sign convention; the "right" one depends on upstream data that the context does not define.
- C omits an SLS pass/fail column; decide whether the evaluator considers this proportionate scoping or a missed expectation of "summary alongside ULS results".
- Both B and C raise `ValueError` when only one deflection column is present; this only fires on the new SLS path, but confirm that is acceptable rather than silently treating the input as ULS-only.
- A's merged single-row report emits `NaN` for members without SLS data; if downstream consumers serialise to JSON this is a hidden compatibility issue not flagged in A's risk table.
- None of the responses address the flat `from io_contract import RESULT_COLUMNS` import style; irrelevant to this task but note if packaging changes are ever in scope.

### Round 1: v2-deep-04

Key: A = `gemma4:31b-cloud`, B = `gpt5.4-xhigh`, C = `gpt5.6-sol-xhigh`, D = `gpt5.6-luna-max`

#### Blind judge report: v2-deep-04

**Task summary:** Review a proposed deduplication of steel and concrete utilisation helpers, where the hidden trap is that concrete returns `None` → `"CHECK INPUT"` on non-positive capacity while steel returns `0.0` → `"PASS"`, and downstream spreadsheets depend on the exact status text.

##### Score table

| Response | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Note |
|---|---|---|---|---|---|---|---|
| A (`gemma4:31b-cloud`) | 4 | 4 | 4 | 3 | 4 | 4 | Correctly identifies the trap and gives a behaviour-preserving parametrised helper with full code, but the regression set is thin (no inclusive-1.0 boundary, no utilisation-level asserts, no snapshot comparison) and no misuse caveat or alternative is considered. |
| B (`gpt5.4-xhigh`) | 4 | 4 | 4 | 4 | 3 | 4 | Correct analysis with the best prose regression list of the parametrised-helper group, but the refactor is only sketched (no module wiring, no helper location) and its first suggested option is vacuous. |
| C (`gpt5.6-sol-xhigh`) | 5 | 5 | 5 | 5 | 4 | 5 | Most complete: recommends leave-as-is as lowest risk, gives an explicit-policy helper that preserves behaviour, notes `format_status(None)` would raise, and supplies runnable parametrised tests covering boundary, zero and negative denominators. |
| D (`gpt5.6-luna-max`) | 5 | 4 | 5 | 4 | 4 | 4 | Correct parametrised helper with full code, explicitly flags the fallback-argument misuse risk and the leave-separate alternative, and asks for spreadsheet output comparison; minor muddle listing the `<= 0` guard under both shared and distinct. |

##### Top weaknesses per response

**A (`gemma4:31b-cloud`)**
- Tests miss the inclusive `util == 1.0` boundary and never assert utilisation-level return values (`None` vs `0.0`), only status strings.
- No warning that a configurable `fallback` parameter makes it easy for one module to silently inherit the other's semantics; no alternative (leave-as-is) considered.
- No request for spreadsheet/integration snapshot comparison despite the stated downstream dependency.
- LaTeX `$\rightarrow$` arrows in Markdown may not render; calls steel's PASS-on-zero "business logic" without any hint that it is engineering-suspect.

**B (`gpt5.4-xhigh`)**
- Refactor is described, not shown: no module wiring, no statement of where `utilisation_or` lives, so the change is less auditable.
- First suggested option ("extract only the positive-denominator division") is a helper that would just do `ed / rd`, which deduplicates nothing.
- No mention of `format_status(None)` raising, and no explicit integration/snapshot comparison step (only "exact string regression checks").
- No consideration of the leave-as-is option or of the misuse risk of the sentinel parameter.

**C (`gpt5.6-sol-xhigh`)**
- Steel wrapper takes an indirect route (`None` then mapped to `0.0`); if `utilisation_or_none` is later changed to return something other than `None`, steel silently changes. The trade-off is acknowledged only from the other direction.
- Parametrised test uses `== expected_util` where `expected_util` may be `None` (works, but non-idiomatic; lint E711).
- Like all four, places a calculation helper in `common_formatting.py` without noting the naming mismatch.

**D (`gpt5.6-luna-max`)**
- Lists "the `denominator <= 0` guard" under "may be shared" and "the existing `<= 0` check" under "must remain distinct", which reads as contradictory even if the intent (share the guard, preserve its negative coverage) is recoverable.
- Does not note that `format_status(None)` would raise `TypeError`, which is the concrete reason the `None` branch must precede formatting.
- Tests are prose only; no runnable code and no docstring on the new helper.

##### Ranking (best to worst)

1. **C (`gpt5.6-sol-xhigh`)** — mean 4.83
2. **D (`gpt5.6-luna-max`)** — mean 4.33
3. **B (`gpt5.4-xhigh`)** — mean 3.83
4. **A (`gemma4:31b-cloud`)** — mean 3.83

B and A tie on mean; B is ranked above A because its regression list covers the inclusive boundary, utilisation-level values, and exact-string checks on the dimension the task emphasises, and it states an explicit rejection criterion, whereas A's fuller code does not compensate for the thinner test coverage on a review task.

##### Practical significance

All four responses catch the behavioural trap, refuse a naive merge, and propose a change that would preserve current outputs, so none of them would let the silent zero-denominator regression through. The differences are in depth of safety framing rather than correctness: C and D anticipate misuse of a shared helper and demand integration/snapshot comparison, making them merge-ready review notes; A and B would each need a reviewer to top up the regression set (A) or fill in the concrete wiring and helper location (B) before the refactor could be applied with confidence. The roughly one-point gap between C and A/B reflects thoroughness and auditability, not a difference in whether the core hazard was understood.

##### Manual-review watch-outs

- All four put a calculation helper into `common_formatting.py`; if the repo has a non-formatting shared module, the helper should live there instead.
- None of the responses clearly flags that steel's `0.0` → `"PASS"` on zero or negative capacity is engineering-suspect (a zero-resistance member "passes"); C hints at it. This should be ticketed separately even though preserving it is correct for this refactor.
- C's test `(101, 100, 1.01, "FAIL")` relies on `101/100 == 1.01` float equality; this holds under IEEE-754 correctly rounded division but a reviewer may prefer `pytest.approx` or `1.0 + 1e-9`-style inputs.
- C's claim that `format_status(None)` raises `TypeError` is correct in Python 3 (`None <= 1.0`), and is the reason the concrete `None` branch must stay ahead of formatting.
- D's shared/distinct lists both mention the `<= 0` guard; confirm the intended reading before treating it as an inconsistency.
- A's tests should be extended with `util == 1.0` → `"PASS"` and utilisation-level asserts before merge.
- None of the responses discuss NaN/inf or non-numeric inputs; not required by the task but worth a reviewer's note if such inputs can arrive from spreadsheets.
- Do not attribute any response to a model or vendor; this judgement is content-only.

### Round 1: v2-medium-05

Key: A = `gpt5.6-luna-max`, B = `gemma4:31b-cloud`, C = `gpt5.6-sol-xhigh`, D = `gpt5.4-xhigh`

#### Blind judge report: v2-medium-05

**Task summary:** Review a pandas module that computes an L/250 deflection utilisation ratio per row and aggregates it by Storey/Material, and either rewrite it or give a scoped patch plan covering performance at several hundred thousand rows, data cleaning/validation, summary correctness, and maintainability.

##### Score table

| Response | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Note |
|---|---|---|---|---|---|---|---|
| A (`gpt5.6-luna-max`) | 5 | 5 | 4 | 5 | 4 | 5 | Proportionate vectorised rewrite with fail-fast validation (incl. infinity and non-positive length) and deliberately preserved aggregation semantics; the only unflagged side-effects are the unconditional string cast of key columns and the changed group ordering. |
| B (`gemma4:31b-cloud`) | 3 | 3 | 2 | 2 | 3 | 3 | Vectorises correctly but mutates the caller's DataFrame (and advertises it as a memory benefit), lets coerced-NaN rows silently vanish from Max/Mean while still being counted, and leaves negative lengths, missing columns and signed deflection unhandled. |
| C (`gpt5.6-sol-xhigh`) | 5 | 5 | 4 | 5 | 5 | 5 | Most rigorous rewrite (dtype-aware key normalisation, finiteness checks, reason-coded diagnostics, raise/drop policy, documented formula and grain) at the cost of extra length and a member-envelope grain change that is well documented but still an assumption. |
| D (`gpt5.4-xhigh`) | 4 | 5 | 4 | 4 | 4 | 5 | Precise line-referenced findings and a compact staged implementation with explicit empty-input and column-order handling, but no docstring on a function whose semantics changed, no example rows in the error, no infinity guard, and unconditional string cast of keys. |

##### Top weaknesses per response

**A (`gpt5.6-luna-max`)**
- `astype("string")` is applied to Storey/Material/Member unconditionally, so integer storey or member IDs come back as strings in the summary; this compatibility change is not flagged.
- `sort=False` changes the output group order versus the original sorted groupby; not mentioned.
- `df.loc[:, _REQUIRED]` with a tuple works on a plain column Index but is non-idiomatic and easy to misread as a MultiIndex key; a list would be safer.
- Strict-only policy: coerced values are rejected rather than cleaned; there is no tolerant path for a pipeline that must process partially dirty exports (acceptable choice, but the task asked for cleaning as well as validation).

**B (`gemma4:31b-cloud`)**
- Mutates the input DataFrame in place (`df[col] = ...`, `df["DeflectionRatio"] = ...`), a regression from the original which did not mutate, and can trigger SettingWithCopyWarning on sliced inputs.
- Coerced NaN values are silently skipped by `max`/`mean` while `MemberCount` still counts those rows, so an unparseable deflection can produce a false PASS with no signal; the original at least failed loudly.
- No required-column validation, no negative-length handling (negative ratio can pass), signed deflection retained without discussion, no test plan.
- Overconfident prose ("slowest possible way", "milliseconds rather than minutes") and presenting in-place mutation as a memory feature.

**C (`gpt5.6-sol-xhigh`)**
- Changes the aggregation grain (per-member envelope before storey/material stats), which alters `MemberCount` and `MeanRatio` whenever the export has multiple rows per member; documented, and harmless under a one-row-per-member contract, but still an assumption about the data.
- Longest solution: `errors` policy, span-limit parameter, dtype branch and reason-coded message push toward the upper bound of proportionality for this task.
- `sort=False` ordering change not flagged; tuple used in `.loc` column selection (works, but same caveat as A).
- `.astype("float64")` after `to_numeric` and the object/string dtype branch are minor redundancies that add surface area.

**D (`gpt5.4-xhigh`)**
- No docstring on `summarise_members` even though the function now envelopes per member, uses absolute deflection, and fails fast; the semantics live only in the prose.
- Error message gives a count only, with no example indices or reason breakdown, which weakens diagnosability on a 500k-row export.
- No infinity guard: an "inf" length passes validation and yields a ratio of 0 (PASS); A and C cover this.
- Unconditional string cast of key columns and `sort=False` ordering change, both unflagged; grain change is flagged as a finding but implemented with no opt-out.

##### Ranking (best to worst)

1. **C (`gpt5.6-sol-xhigh`)** – mean 4.83
2. **A (`gpt5.6-luna-max`)** – mean 4.67
3. **D (`gpt5.4-xhigh`)** – mean 4.33
4. **B (`gemma4:31b-cloud`)** – mean 2.67

##### Practical significance

C, A and D are all safe-to-apply vectorised rewrites that would take several hundred thousand rows from a Python-loop bottleneck to a fraction of a second, and all three catch the three issues the task cares about (row loop, unsafe float casts, zero/missing lengths). The gap between them is second-order: C is more rigorous about dtypes, finiteness and diagnostics and offers a drop policy; A is the most proportionate and preserves the original aggregation semantics exactly; D is compact and precisely diagnosed but leaves the function undocumented. Any of the three would be mergeable after a one-line review of two questions (are key columns numeric in real exports, and does the export contain multiple rows per member). B is materially different: it would run fast on clean data but is not safe to merge as-is, because it mutates the caller's frame and converts the original's loud failure on dirty data into a silent exclusion that can yield a false PASS on a structural check.

##### Manual-review watch-outs

- Confirm whether Storey/Member are integers in real exports; A and D convert them to string dtype in the output, which can break downstream numeric sorting or joins. C preserves numeric IDs.
- Confirm whether exports contain multiple rows per member (load cases/stations). If yes, C and D change `MemberCount` and `MeanRatio` relative to the original; if no, the envelope step is a no-op.
- A, C and D all pass `sort=False`, so group order differs from the original sorted output; check any consumer that relies on ordering.
- A and C select columns with a tuple in `.loc[:, ...]`; this works on a plain column Index in current pandas but should be verified against the project's pinned version and ideally changed to a list.
- All of A, C and D switch to `abs(Deflection_mm)`; verify the export's sign convention and that upward deflection should be governed by magnitude (reasonable, but a behaviour change).
- B: check for SettingWithCopyWarning and for callers that reuse the input frame after the call; check groups where some rows coerced to NaN, because Max/Mean will silently ignore them.
- D has no infinity guard; A and C do. Only relevant if exports can emit "inf"/"-inf" strings.
- None of the responses ships actual tests; C gives concrete numeric cases (4 m / 16 mm = 1.0 PASS, -20 mm = 1.25 FAIL) that are the easiest to turn into a test file.
- No response questions whether L/250 is the correct limit for the element types in the export; all keep 250 as a constant (C and B parameterise it).

### Round 1: v2-medium-06

Key: A = `deepseek-v3.2`, B = `gpt5.6-luna-max`, C = `gpt5.6-sol-xhigh`, D = `gpt5.4-xhigh`

#### Blind judge report: v2-medium-06

**Task summary:** Review a three-function Python helper for foundation settlement checks (utilisation ratio, differential slope in mixed mm/m units, PASS/FAIL status), report the key bugs, propose minimum fixes, and design a small high-value test set with explicit sign conventions and units.

##### Score table

| Response | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Note |
|---|---|---|---|---|---|---|---|
| A (`deepseek-v3.2`) | 2 | 3 | 2 | 2 | 3 | 3 | Finds the two headline issues but introduces a default 5% acceptance tolerance that relaxes the limit-state check, and its own boundary tests (`status_from_ratio(1.00) == "FAIL"`, `1.01 == "FAIL"`) would fail against that fix. |
| B (`gpt5.6-luna-max`) | 4 | 5 | 4 | 4 | 4 | 4 | Complete and accurate bug list (zero allowable, sign, equality, spacing, NaN/inf, <2 readings, multi-point ambiguity, mm/m vs dimensionless), proportionate fixes, tests consistent with fixes; unit inconsistency is documented rather than resolved in code. |
| C (`gpt5.6-sol-xhigh`) | 4 | 4 | 3 | 4 | 4 | 4 | Most decisive on the unit bug (converts to dimensionless m/m) and clean tests, but delivers a 1000x output change plus an exactly-two-points restriction under the same function name, and misstates that NaN yields PASS in the current code (it yields FAIL). |
| D (`gpt5.4-xhigh`) | 3 | 3 | 3 | 3 | 3 | 3 | Clear narrative findings with explicit sign/unit assumptions, but line references are wrong, the fix keeps and even tests the 0.0-for-missing-data masking, `abs()` silently folds heave into settlement demand, and tests are prose with no borderline FAIL case. |

##### Top weaknesses per response

**A (`deepseek-v3.2`)**
- Adds `tolerance=0.05` to `status_from_ratio` by default, so ratios up to 1.05 PASS; this is an invented assumption and an unsafe relaxation of a serviceability limit.
- Test set contradicts the fix: with default tolerance, `status_from_ratio(1.00)` and `(1.01)` return "PASS", so the asserted "FAIL" cases fail; the comment "Strict boundary (default tolerance)" shows the author did not realise this.
- Hidden unit error in the integration test: "5000mm/300 = 16.7mm/m" confuses a deflection limit (16.7 mm) with a slope (1/300 = 3.33 mm/m), and calls 1/300 "more strict" than 1/500.
- Inconsistent missing-data handling (empty list raises, single reading returns 0.0) and an overconfident closing claim that the tests "catch all critical bugs".

**B (`gpt5.6-luna-max`)**
- `differential_slope` keeps mm/m output; the in-code comment reads as an instruction to the caller ("Convert ... by dividing by 1000") rather than a fix, so the numeric inconsistency flagged in the task remains.
- Multi-point ambiguity (max-min over a single spacing) is identified but left in the code, with only a documentation suggestion.
- Rejecting negative values in `differential_slope` precludes a legitimate heave-versus-settlement differential; no test covers negative settlements there.
- Raising for <2 readings and switching `<` to `<=` are both behaviour changes; they are flagged, but callers relying on the old 0.0 return would break.

**C (`gpt5.6-sol-xhigh`)**
- Changes `differential_slope` output by a factor of 1000 and restricts input to exactly two points while keeping the same function name; any downstream mm/m threshold comparison would silently pass. The rename alternative is mentioned but not delivered.
- Factual error: claims NaN "can silently produce a PASS" in the current logic; `nan < 1.0` is False, so the current code returns "FAIL".
- "Minimum fixes" exceed minimum scope (API contract change on point count, unit change).
- Negative-settlement rejection in `settlement_ratio` is implemented but not tested.

**D (`gpt5.4-xhigh`)**
- Line references (`:3`, `:10`, `:8`, `:5-8`) do not match the supplied file; invented precision reduces trust.
- Fix retains `return 0.0` for fewer than two readings and test 7 enshrines it as intended behaviour, cementing the missing-data mask; also, the `<2` check precedes the spacing check, so `differential_slope([12.0], 0.0)` returns 0.0 without raising.
- `abs(settlement_mm)` treats heave against the settlement allowable symmetrically and hides sign-convention errors instead of surfacing them; finding 4 recommends rename-or-convert but the fix does neither.
- Tests are prose rather than runnable code, omit negative spacing, NaN, and any just-above-1.0 FAIL case, so the borderline threshold is only half covered.

##### Ranking (best to worst, mean of six technical scores)

1. **B (`gpt5.6-luna-max`)** - 4.17
2. **C (`gpt5.6-sol-xhigh`)** - 3.83
3. **D (`gpt5.4-xhigh`)** - 3.00
4. **A (`deepseek-v3.2`)** - 2.50

##### Practical significance

B and C are close and both would be acceptable review outputs with minor edits: B is the safer, more proportionate patch and has no factual slips, while C resolves the unit inconsistency more decisively but at the cost of a breaking 1000x magnitude change under an unchanged name and one incorrect claim about NaN behaviour; the choice between them turns on whether the project wants the unit fix in code now or documented and deferred. D is a meaningful step down: it reads well and states conventions explicitly, but it leaves the missing-data mask in place and tests it as correct, has wrong line references, and under-covers the pass/fail boundary. A is a clear outlier and should not be applied as written; its default tolerance is a safety-relevant regression to the acceptance criterion, its own tests would fail against its fix, and its integration test embeds a deflection-versus-slope unit error.

##### Manual-review watch-outs

- Run A's tests against A's fix: `status_from_ratio(1.00)` and `(1.01)` return "PASS" with the default `tolerance=0.05`, so two assertions fail.
- A's "5000mm/300 = 16.7mm/m" conflates a deflection allowance with a slope; 1/300 is 3.33 mm/m.
- C's NaN claim is wrong for the current code (NaN yields "FAIL", not "PASS"); check that reviewers do not carry this over into the risk register.
- C's `differential_slope` now returns m/m and rejects anything other than exactly two readings; confirm there are no callers comparing against mm/m limits or passing multi-point arrays.
- D's line numbers do not correspond to the supplied file; verify findings against actual lines.
- D's `abs()` in `settlement_ratio` assumes heave and settlement share one allowable; confirm with the project before adopting.
- D's check ordering lets `differential_slope([x], 0.0)` return 0.0 silently.
- B, C, and D all flip `<` to `<=` in `status_from_ratio`; this must be confirmed against the project's limit convention before merging.
- B and C change `<2 readings` from returning 0.0 to raising; audit callers for reliance on the old default.
- B and D keep mm/m output for `differential_slope`; ensure nothing downstream feeds that value directly into `status_from_ratio` as a dimensionless ratio.

### Round 1: v2-anchor-07

Key: A = `gpt5.6-luna-max`, B = `minimax-m2.7-cloud`, C = `gpt5.4-xhigh`, D = `gpt5.6-sol-xhigh`

#### Task summary

Review a short EC3 bending-resistance script for a 254x102x28 UB (6.2 m simply supported, 18.5 kN/m UDL), find and fix the errors (the planted faults being the minor-axis `Wpl_z` used in place of `Wpl_y` and the missing N·mm to kN·m conversion), show working, and state whether the section is adequate.

#### Score table

| Response | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Note |
|---|---|---|---|---|---|---|---|
| A (`gpt5.6-luna-max`) | 5 | 5 | 5 | 4 | 4 | 5 | Finds both planted faults, uses the correct tabulated Wpl,y = 353 cm³, reaches PASS at 0.916, and flags LTB/load-factor/self-weight as caveats without replacing the objective, though its ~31 kN·m LTB figure is asserted without working. |
| B (`minimax-m2.7-cloud`) | 2 | 3 | 2 | 2 | 3 | 3 | Names both planted faults correctly in principle but substitutes a fabricated Wpl,y = 106 cm³ (attributed to the Blue Book), injects an unrequested 1.35 load factor, and reaches the opposite conclusion (FAIL at 3–4x utilisation) with confident upsizing advice. |
| C (`gpt5.4-xhigh`) | 5 | 5 | 5 | 4 | 5 | 4 | Finds both faults, keeps the original variable names and print block so the patch is the minimal two-line fix, shows the N·mm intermediate explicitly, and gives a correct split adequacy answer with cited sources. |
| D (`gpt5.6-sol-xhigh`) | 5 | 5 | 5 | 5 | 4 | 5 | Finds both faults, cross-checks the corrected 97.08 kN·m against the tabulated Mc,y,Rd = 97.1, verifies the low-shear condition so 6.2.5 applies without 6.2.8 reduction, and shows the LTB interpolation; only blemish is an unused `V_Ed` in the code. |

#### Top weaknesses per response

**A (`gpt5.6-luna-max`)**
- The LTB resistance "about 31 kN·m" is claimed from an "indicative EC3 calculation using tabulated Iz, IT, Iw" that is not shown, so it is not auditable from the response.
- Renames variables (`L_m`, `w_uls`, `M_c_Rd`) with no functional need, widening the diff relative to the snippet under review.
- Opening sentence awkwardly conflates the load assumption with the bending-axis statement.
- Class 1 is assumed rather than confirmed (shared with C and D; the snippet asserts it, so minor).

**B (`minimax-m2.7-cloud`)**
- Fabricated section properties: Wpl,y ≈ 106e3 mm³ (correct tabulated value is 353e3), Wel,y ≈ 69e3 (actual ≈ 308e3), Wpl,z ≈ 23e3 (actual ≈ 54.8e3), all attributed to the Blue Book; this produces M_Rd = 29.15 kN·m instead of 97.08 kN·m and the wrong FAIL verdict.
- Drifts from the planted objective by treating 18.5 kN/m as characteristic and applying γG = 1.35, turning the review into a different design problem (explicitly penalised in the evaluator notes); `gamma_Q` is declared and unused.
- Overconfident claims built on the wrong data ("heavily over-stressed", "resistance roughly doubled", recommends 305x102x33 / 305x165x46), and accepts `49e3` as a genuine minor-axis value rather than noting it is not tabulated.
- Markdown table cells are broken across lines in the raw text, and the classification ratios (c/t ≈ 6, d/t ≈ 39) are approximate rather than tabulated, although the Class 1 conclusion holds.

**C (`gpt5.4-xhigh`)**
- LTB resistance "31 to 32 kN·m" is quoted from tables without showing the values or the interpolation.
- Does not call out that the load must be factored or that self-weight should be included beyond listing "design ULS load" as an assumption.
- Adequacy answer is split into two bullets without a single headline verdict; plain text blocks rather than typeset working.
- No cross-check of the computed M_Rd against the tabulated Mc,y,Rd.

**D (`gpt5.6-sol-xhigh`)**
- `V_Ed` is computed in the corrected script but never used in a check (dead variable).
- Four specific page references into SCI P363 and the tabulated Mb,Rd values (32.3 kN·m at 6 m, 28.1 at 7 m) are unverifiable from the pack and would need confirming.
- The shear and LTB material is somewhat more than the planted objective strictly required, though it is clearly separated and labelled as conditional.
- Describes 0.916 utilisation as "only just" passing, which is a little dramatic for a cross-section check.

#### Ranking (best to worst)

1. **D (`gpt5.6-sol-xhigh`)** — mean 4.83
2. **A (`gpt5.6-luna-max`)** — mean 4.67
3. **C (`gpt5.4-xhigh`)** — mean 4.67
4. **B (`minimax-m2.7-cloud`)** — mean 2.50

A and C are tied on mean; A is placed ahead for its more complete error list (explicitly flagging load factoring and self-weight) and headline verdict, while C has the tightest, most auditable patch. The order between them is not significant.

#### Practical significance

Responses A, C and D all identify the two planted faults directly, use the correct tabulated Wpl,y = 353 cm³, arrive at the same corrected result (M_Ed = 88.89 kN·m, Mc,y,Rd = 97.08 kN·m, utilisation 0.916, PASS for cross-section bending) and add a proportionate LTB caveat without displacing the planted objective; the differences among them are in auditability (D shows the tabulated cross-check, the shear interaction check and the LTB interpolation; A and C assert the LTB figure) and in diff minimality (C best), and a checking engineer would accept any of the three. B is materially worse and would be harmful in practice: it fabricates section properties and attributes them to a real source, adds an unrequested load factor, reverses the adequacy verdict, and gives confident section-upsizing advice on the wrong numbers, so a reader relying on it would over-design and the false source attribution would undermine trust in the review.

#### Manual-review watch-outs

- Confirm the Blue Book values for 254x102x28 UB: Wpl,y = 353 cm³, Wpl,z = 54.8 cm³ (A, C, D agree); B's 106 cm³ / 69 cm³ / 23 cm³ set is inconsistent with these and should be treated as fabricated unless a reviewer can source it.
- Spot-check D's cited figures and page references: Mc,y,Rd = 97.1 kN·m, Vc,Rd = 283 kN (consistent with Av ≈ 1780 mm² × 275/√3), Mb,Rd = 32.3 kN·m at 6 m and 28.1 kN·m at 7 m, C1 = 1.13, and P363 pages 35–36, 72, 205, 231.
- A's "about 31 kN·m" LTB figure has no working; it is consistent with C and D but is not auditable from A alone.
- Decide whether the LTB caveats in A, C and D count as "drift": I treated them as caveats because all three keep the cross-section PASS as the answer to the planted objective; B's load-factor injection is the genuine drift case.
- Note that the original script's printed PASS was coincidentally the correct cross-section verdict; A and D correctly say it is "not valid as written" rather than "wrong", which is the right framing.
- B's raw markdown table will not render correctly; if scoring output relies on rendered display, its clarity may look worse or better than the raw text suggests.
- All four assume S275 from `fy = 275` and Class 1 from the snippet comment; none independently verifies the classification except B (with approximate ratios: actual c/tf ≈ 4.0, d/tw ≈ 35.7).

### Round 1: v3-notebook-01

Key: A = `gpt5.6-luna-max`, B = `gemma4:31b-cloud`, C = `gpt5.6-sol-xhigh`, D = `gpt5.4-xhigh`

#### Blind judge report: v3-notebook-01

**Task summary:** Produce a six-section notebook draft that sizes the smallest square pad footing (2.4–3.2 m, 0.1 m steps) for one column under three service load cases with biaxial moments, using a rigid-footing linear-pressure model so that every case satisfies qmax <= 220 kPa and qmin >= 0; the reference answer is 3.0 m governed by LC2, with 2.9 m rejected because LC2 gives qmin = -0.41 kPa despite an acceptable qmax.

##### Score table

| Response | Calculation correctness | Code quality and executability | Engineering judgement | Unit and assumption handling | Notebook traceability and clarity | Completeness of deliverable | Note |
|---|---|---|---|---|---|---|---|
| A (`gpt5.6-luna-max`) | 3 | 2 | 4 | 3 | 3 | 4 | Narrative, closed-form equations and final answers (3.0 m, LC2, -0.41 kPa at 2.9 m) are right, but the coded point-pressure formula uses 6*M*x/B^3 with x = B/2 (equivalent to 3M/B^2, dimensionally kN/m) instead of M*x/I, so its own cross-check assert fails on the first candidate and the notebook cannot run past Code Cell 3. |
| B (`gemma4:31b-cloud`) | 3 | 3 | 2 | 3 | 2 | 2 | Pressure equations and search are correct and executable (would select 3.0 m), but the code defines the governing case as the largest qmax (LC3) and the conclusion prints variable-name placeholders instead of stating 3.0 m or LC2 anywhere in the text. |
| C (`gpt5.6-sol-xhigh`) | 5 | 4 | 3 | 3 | 4 | 3 | Correct, executable and self-verified (3.0 m, LC2, 2.9 m rejected at -0.41 kPa) with all six sections, but it quotes the compact 6|M|/B^3 formula without derivation, gives no justification for the rigid linear model, and never defines eccentricity directions. |
| D (`gpt5.4-xhigh`) | 5 | 5 | 5 | 5 | 4 | 5 | Correct, executable, derived explicitly from q = N/A + My*x/Iy + Mx*y/Ix with four-corner evaluation, a rigorous "last case to pass" governing-case rule and per-candidate worst-case diagnostics; only organisational quirks remain. |

##### Top weaknesses per response

**A (`gpt5.6-luna-max`)**
- `pressure_at_point` returns N/B^2 + 6*My*x/B^3 + 6*Mx*y/B^3 and is called with x = y = B/2, which yields 3(Mx+My)/B^2 rather than 6(Mx+My)/B^3 (the bending term has units kN/m, not kPa). The `isclose(..., abs_tol=1e-12)` assert against the correct closed form therefore raises AssertionError at the first evaluation (B = 2.4, LC1: about 269.1 vs 256.1 kPa), so Code Cells 4, 5 and 6 never execute and no table or selection is printed.
- Markdown Cell 3 is internally inconsistent: it states the point formula with 6/B^3, then correctly derives q_My = 12*My*x/B^4 from I = B^4/12 and only the edge value 6*My/B^3.
- The values quoted in the conclusion (-0.41, 2.22, 178.89 kPa) cannot have come from running this code; the "All load cases pass" print and the hard-coded `assert isclose(selected_B_m, 3.0)` present unverified results with full confidence (rule 4: overconfident claims).
- Minor: unused `report()` helper, float-accumulated candidate widths (2.4 + 0.1*i), and the search summary shows only aggregate max/min without naming the failing case.

**B (`gemma4:31b-cloud`)**
- Governing case is chosen by the largest qmax, which returns LC3; this contradicts the selection rule, where LC2 (uplift) is what forces B up to 3.0 m. The text never explains that uplift controls or why 2.4–2.9 m fail.
- The conclusion states "`selected_B` metres", "`governing_case`" and "`max_q_found` kPa" as literal placeholders; no footing size in metres and no governing case appear in the deliverable text, failing two explicit "You must" items.
- No "Input data" Markdown section (code-only cell), section numbering does not match the required six-section order, the search loop breaks on first failure and prints nothing per candidate, and cells are unlabelled.
- Sign convention is vague ("positive about the axes") with no statement of which edge each moment loads or of eccentricity directions; qmax sums Mx + My without absolute values; Z = B^3/6 is quoted rather than obtained from I and y = B/2; unit consistency is only implied by code comments.

**C (`gpt5.6-sol-xhigh`)**
- No derivation: qmax/qmin are quoted with 6|M|/B^3 from the outset; A, I, Z or the N/A +/- M*y/I path never appear, and there is no statement of why the rigid linear-pressure model is appropriate (both explicit brief requirements; rule 10 rewards the derivation).
- Eccentricities ex, ey are never defined, computed or reported, and the moment sign convention only says moments act about centroidal axes; the brief explicitly asked for eccentricity directions.
- The search summary prints only PASS/FAIL per width, so the code output never shows the -0.41 kPa margin; Markdown Cell 4 asserts the 2.9 m failure before the search cell runs, which reads as pre-empted rather than traced.
- Hard-coded asserts (`== 3.0`, `== 2.9`) and a 1e-9 kPa tolerance on the strict qmin >= 0 rule are defensible but couple the notebook to the expected answer.

**D (`gpt5.4-xhigh`)**
- Equations, derivation and sign convention are all packed into Section 1 "Assumptions", leaving Section 3's Markdown as a short bullet list; a reader of the calculation cell must scroll back for the equations.
- `selected = next(...)` has no guard if no candidate passes; `first_passing_width_by_case` uses a dense nested `next`, and the functions read `load_cases` / `q_allow_kPa` as globals.
- Tables round to 0.1 kPa, so the decisive 2.9 m LC2 margin appears as -0.4 kPa; there is no closing code cell behind the conclusion's quoted values.

##### Ranking (best to worst, mean of six technical scores)

1. **D (`gpt5.4-xhigh`)** — 4.83
2. **C (`gpt5.6-sol-xhigh`)** — 3.67
3. **A (`gpt5.6-luna-max`)** — 3.17
4. **B (`gemma4:31b-cloud`)** — 2.50

No response selected 2.9 m by checking qmax only (rule 9); all four apply the qmin >= 0 test in their search logic.

##### Practical significance

The differences are material, not cosmetic. D is the only response that is simultaneously correct, executable, derived from first principles and fully traceable, and it could be handed to a checker as-is. C is a reliable executable alternative whose gaps are documentary (derivation, model justification, eccentricity convention) and could be fixed without touching the code. A looks the most polished on the page and its narrative conclusions are right, but its calculation core cannot run: anyone trusting the code gets an AssertionError, and anyone reusing the stated q(x,y) formula for interior points would get pressures wrong by a factor of B/2, so the gap between C and A is a real executability gap. B runs but silently reports LC3 as governing and never states the answer in text, so it fails the brief's explicit reporting requirements even though its selection logic is sound; the gap between A and B is one of correctness of the stated conclusions.

##### Manual-review watch-outs

- Run A's Code Cell 4 to confirm the predicted AssertionError on the first `evaluate_case(B = 2.4, LC1)` call; the root cause is `6.0 * M * x_m / B_m**3` with `x_m = B/2` where `12*M*x/B**4` (or `M*x/I`) was intended. This finding is by inspection only, since no code was executed.
- A's Markdown Cell 3 contradicts itself (6/B^3 point formula vs 12/B^4 derivation); do not credit the derivation as consistent.
- Run B's results cell to confirm it prints "Governing Case: LC3"; also confirm the conclusion cell contains no numeric footing size.
- C's Markdown Cell 4 states the 2.9 m failure and -0.41 kPa before the search cell runs; it is correct but should not be read as evidence the code was executed. Also check that the reviewer accepts `29/10.0 == 2.9` as reliable (it is, by correctly rounded division).
- C's `PRESSURE_TOLERANCE_KPA = 1e-9` slightly relaxes the strict qmin >= 0 rule; immaterial here (the 2.9 m margin is -0.41 kPa) but worth noting for reuse.
- D: confirm `first_passing_width_by_case` gives LC1 -> 2.6 m, LC3 -> 2.8 m, LC2 -> 3.0 m so that `max` returns LC2; note the missing no-solution guard and 0.1 kPa table rounding.
- Hard-coded answer asserts (A: 3.0; C: 3.0 and 2.9) will break these notebooks if inputs change; not a correctness issue for this brief but relevant to reuse.
- C's formatting was lost in copying; it was judged on content only, per the pack instruction.

### Round 2: v2-deep-03

Key: A = `gpt5.6-sol-xhigh`, B = `gpt5.6-luna-max`, C = `gpt5.4-xhigh`, D = `qwen-3.6plus`

#### Blind judge report: v2-deep-03

**Task summary:** Produce a decision-complete plan for adding an optional serviceability summary (`DeflectionRatio = Deflection_mm / AllowableDeflection_mm`) to a three-file pandas design package while leaving existing ULS-only callers and the `report_rows()` / `RESULT_COLUMNS` report contract unchanged.

##### Score table

| Response | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Note |
|---|---|---|---|---|---|---|---|
| A (`gpt5.6-sol-xhigh`) | 5 | 5 | 5 | 4 | 5 | 5 | Fully additive, decision-complete plan with per-row ratio then governing-row selection, explicit sentinel and tie-break rules, and golden-output tests; only weakness is an invented "reject negative deflection" constraint. |
| B (`gpt5.6-luna-max`) | 5 | 5 | 5 | 4 | 4 | 4 | Same additive architecture as A, with a good sign-convention caveat, but leaves the orchestration helper optional, assumes a test layout that was not supplied, and under-specifies the columns-present-but-all-null case. |
| C (`gpt5.4-xhigh`) | 3 | 4 | 4 | 2 | 3 | 3 | Correct additive direction but hedged throughout ("ideally", "for example", "optionally") and explicitly defers the governing aggregation rule, so it is not decision-complete and its stated default (ratio after aggregation) leans the wrong way. |
| D (`qwen-3.6plus`) | 2 | 3 | 2 | 2 | 3 | 4 | Concrete and well laid out, but it modifies `report_rows()` to silently drop missing columns, aggregates `Deflection_mm` (max) and `AllowableDeflection_mm` (first) independently before dividing, and then claims "no existing logic is modified". |

##### Top weaknesses per response

**A (`gpt5.6-sol-xhigh`)**
- Rejects negative `Deflection_mm` outright; signed deflection output (e.g. upward/hogging) is common in analysis exports, so this is an invented constraint that could block valid data rather than a requirement of the task.
- Uses two representations of "absent" (an empty schema-correct DataFrame from the builder, and `None` accepted by `report_sections`), a small consistency wart.
- Deliberately omits any SLS pass/fail field; defensible and justified in the text, but the resulting "summary" carries a ratio only, which the product owner may consider incomplete.

**B (`gpt5.6-luna-max`)**
- Leaves `build_design_summaries(df)` as "optionally add", and references "the repository's existing test layout" that was not in the supplied context; both are decisions/assumptions the plan should have closed.
- Returns `None` when columns are absent but does not say what happens when both columns exist and every row is null (empty DataFrame vs `None`), which feeds directly into whether `report_payload()` omits the `serviceability` key.
- Reuses the bare name `Status` in the SLS table; harmless while the tables are separate, but it collides the moment any consumer merges ULS and SLS rows.
- Less concrete than A: no explicit tie-break rule, no data-flow separation of the two branches, no golden-snapshot assertion.

**C (`gpt5.4-xhigh`)**
- Not decision-complete: the aggregation rule for multiple rows per Member/Section is explicitly deferred ("needs to be fixed before implementation"), and the divide-by-zero policy is left as "decide whether excluded, null, or flagged".
- Its stated default, "compute the ratio after aggregation, not per raw row", risks pairing a numerator and denominator from different load cases; the safer per-row option is mentioned only as an exception.
- Function and constant names are all presented as examples ("ideally", "for example", "such as"), and the combined API is conditional ("if needed"), so an implementer cannot start without another design pass.
- Tests are conditional on unchosen API ("depending on chosen API", "handled per spec") and there is no test for the governing-row pairing or for non-mutation of input.

**D (`qwen-3.6plus`)**
- Changes `report_rows()` to project only columns that exist (`available = [...]`), which silently converts today's fail-loud `KeyError` contract into records with missing keys, and adds a test that locks that regression in; the closing claim "No existing logic is modified" is therefore false.
- `build_sls_summary` aggregates `Deflection_mm` by `max` and `AllowableDeflection_mm` by `first` independently, then divides; if allowable varies per row (different combinations/limits) the ratio is incoherent, and no assumption of constant allowable is stated.
- Inconsistent handling of zero allowable (`replace(0, pd.NA)` in the mitigation vs "ratio is inf or NaN with FAIL" in the test), and NaN-to-FAIL turns missing data into a reported failure; partial column presence (one of the two) silently returns `None` and drops data.
- Internal inconsistencies: `report_rows_combined` and `has_sls_data` are named but never specified, `include_sls` on `build_uls_summary` is offered as an alternative, and the summary table omits the combined helper.

##### Ranking (best to worst)

1. **A (`gpt5.6-sol-xhigh`)** — mean 4.83
2. **B (`gpt5.6-luna-max`)** — mean 4.50
3. **C (`gpt5.4-xhigh`)** — mean 3.17
4. **D (`qwen-3.6plus`)** — mean 2.67

##### Practical significance

A and B are architecturally identical (untouched `RESULT_COLUMNS`, `build_uls_summary`, `report_rows`; new SLS constants, builder, writer, and an opt-in combined payload) and either could be handed to an implementer with only minor clarification; A wins on decision completeness (tie-break, sentinel, explicit rejection rules, golden-snapshot tests) while B has the better call on deflection sign convention. The gap to C is material: C points in the same safe direction but cannot be implemented as written because it defers the one engineering decision that matters (how to pick the governing deflection pair) and leans toward the riskier aggregate-then-divide default. D is the only response whose plan would actually change existing behaviour: the silent-column-drop edit to `report_rows()` weakens the report contract that the task said must stay stable, and the max/first aggregation can produce wrong ratios in real multi-case data, so implementing D verbatim would introduce a compatibility regression and a potential engineering error despite its polished presentation.

##### Manual-review watch-outs

- Confirm no implementation touches `report_rows()` behaviour; D's `available` filter converts a fail-loud projection into silent key loss and its own test asserts that regression.
- Establish whether `AllowableDeflection_mm` can vary across rows within a Member/Section in real inputs; if it can, D's `max`/`first` pairing is wrong and only A/B's per-row ratio then governing-row selection is safe.
- Decide the sign convention for `Deflection_mm` before adopting A's "reject negatives" rule or B's "use literally" rule; a max-ratio selection over signed values may need `abs()` upstream.
- Pin the "absent" sentinel (A: empty schema-correct DataFrame; B/D: `None`) and the all-rows-null case so the combined report's key-omission logic is deterministic.
- Resolve SLS pass/fail naming (A: none, B: `Status`, C: `ServiceabilityStatus`, D: `Status_SLS`) against downstream expectations before any merged-table consumer appears.
- D's divide-by-zero guard is undecided (`pd.NA` vs `inf`/`NaN`) and maps NaN to FAIL; D also silently returns `None` when only one of the two deflection columns is present.
- Every hedged/optional item (B's orchestration helper, C's example names and deferred rules, D's `include_sls` alternative and `ALL_RESULT_COLUMNS`) must be closed before implementation.
- None of the responses note that `report_writer.py` uses a flat `from io_contract import ...`; new constants must follow the same import style or the writer will fail to import.
- Verify pandas dtype/NaN behaviour for the ratio column and for `groupby(...).agg("first")` during implementation; no response addresses it.

### Round 2: v2-deep-04

Key: A = `gpt5.6-luna-max`, B = `gpt5.6-sol-xhigh`, C = `gpt5.4-xhigh`, D = `gemma4:31b-cloud`

#### Blind judge report: v2-deep-04

**Task summary:** Review a proposed deduplication of steel/concrete utilisation helpers and determine what can be shared without silently changing the divergent non-positive-denominator behaviour (concrete → `None` → `"CHECK INPUT"`, steel → `0.0` → `"PASS"`) or the downstream-facing status text.

##### Score table

| Response | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Note |
|---|---|---|---|---|---|---|---|
| A (`gpt5.6-luna-max`) | 5 | 5 | 5 | 4 | 4 | 4 | Correctly isolates the trap in a contract table, proposes a behaviour-identical required-sentinel helper with intact wrappers, offers the safer "share only `format_status`" fallback, and lists a complete regression set including spreadsheet output comparison. |
| B (`gpt5.6-sol-xhigh`) | 5 | 5 | 5 | 5 | 4 | 5 | Leads with the most proportionate recommendation (leave the two utilisation functions alone; one duplicated expression versus materially different contracts), gives a single-contract helper with policy kept explicit per module, full parametrised tests, and an explicit merge verdict. |
| C (`gpt5.4-xhigh`) | 5 | 5 | 4 | 4 | 3 | 4 | Analysis and test list are correct and precise (`<= 0`, negatives, exact strings, boundary in both modules), but the refactor is only sketched, one of the two suggested shapes is a no-op helper, and no module code is shown. |
| D (`gemma4:31b-cloud`) | 4 | 4 | 3 | 3 | 4 | 4 | Identifies the trap and proposes an equivalent keyword-fallback helper, but the regression plan omits the inclusive `1.0` boundary and any direct utilisation-value assertions, offers no alternative to refactoring, and never weighs misuse risk of a configurable fallback. |

##### Top weaknesses per response

**A (`gpt5.6-luna-max`)**
- The `<= 0` guard appears under both "may be shared" and "must remain distinct"; the second bullet means "must be preserved", so the labelling contradicts itself on a first read.
- Call sites pass a bare positional sentinel (`safe_utilisation(v_ed, v_rd, None)`), which is less self-documenting than a keyword argument.
- Places an arithmetic helper in `common_formatting.py`, a module whose name signals formatting only.
- Does not flag that steel returning `"PASS"` for zero/negative capacity is engineering-questionable and worth raising with the owners separately (while still preserving it).

**B (`gpt5.6-sol-xhigh`)**
- The argument against a "configurable default such as `invalid_value=0.0`" targets a defaulted parameter; a required parameter (as A and D use) does not silently inherit semantics, so the critique is somewhat overstated.
- Steel now round-trips through a `None` sentinel and maps it back to `0.0`, which is slightly more indirect than a single call.
- Same `common_formatting.py` placement nit as the others.
- Only hints ("even if the new behavior appears more mathematically appropriate") at the dubious steel semantics rather than recommending a separate follow-up.

**C (`gpt5.4-xhigh`)**
- Section 3 is an "example shape" plus prose; the modified modules are not shown, so a reviewer cannot audit the diff for equivalence.
- The first suggested option, "extract only the positive-denominator division", would be a helper wrapping `ed / rd` alone: it deduplicates nothing and adds indirection.
- No discussion of misuse risk of the sentinel parameter, and no consideration of simply not refactoring.
- Does not mention `format_status(None)` raising `TypeError`, nor explicit spreadsheet snapshot comparison beyond "exact string regression checks".

**D (`gemma4:31b-cloud`)**
- Test plan is the thinnest: no `util == 1.0` boundary case, no direct `concrete_utilisation`/`steel_utilisation` return-value assertions (`None` vs `0.0` is part of the contract), asymmetric valid-denominator coverage, no spreadsheet snapshot check.
- Prescribes the fallback helper ("you should implement") without weighing the leave-as-is option or the risk that a configurable fallback invites the exact merge the task warns about.
- Table labels the condition "Zero-Denominator" although the guard is `<= 0`; the docstring likewise omits the negative-denominator semantic.
- Raw LaTeX (`$\rightarrow$`, `$\le 1.0$`, `$rd = 0$`) in a Markdown answer renders as literal text.

##### Ranking (best to worst, mean of six technical scores)

1. **B (`gpt5.6-sol-xhigh`)** – 4.83
2. **A (`gpt5.6-luna-max`)** – 4.50
3. **C (`gpt5.4-xhigh`)** – 4.17
4. **D (`gemma4:31b-cloud`)** – 3.67

##### Practical significance

All four responses catch the hidden behavioural trap, refuse a unified zero-denominator policy, preserve the exact status strings, and stay within a minimal-refactor scope; none would introduce a regression if applied as written, so the spread reflects depth of safeguards and judgement rather than correctness of outcome. B and A are close to interchangeable: B's lead recommendation (do not refactor the utilisation functions; the duplicated code is one expression) and its ready-to-run parametrised tests make it the most auditable, while A's alternative is the same idea offered conditionally. C is technically sound but would require the reviewer to write the diff themselves and to discard a vacuous option. D is the only one whose regression plan would let a plausible regression through (e.g. a `<=` to `<` slip at the `1.0` threshold, or a helper change that returns `0.0` instead of `None` while the status path still happens to read correctly), and it gives the maintainer no basis for choosing not to refactor.

##### Manual-review watch-outs

- Every response that extracts a helper puts it in `common_formatting.py`; check whether a calculation/utility module is the right home and whether the bare `from common_formatting import ...` style implies a flat package or `sys.path` convention that must be respected.
- A, C, and D assert the divergence is "intentional" / "business logic"; the code does not evidence intent. Confirm with the module owners before treating steel's `"PASS"` on non-positive capacity as a deliberate contract, and consider a separate ticket for it (B only hints at this; nobody recommends it explicitly).
- Confirm whether any downstream consumer calls `concrete_utilisation` / `steel_utilisation` directly, not just the status wrappers; the `None` vs `0.0` return type is then part of the public contract and must be asserted in tests (D's plan does not).
- `format_status(None)` raises `TypeError` (B notes this); a test that the concrete `None` branch precedes `format_status` would turn a silent future regression into a loud one.
- B's tests compare floats with `==` (`101/100 == 1.01`); this holds in CPython but `pytest.approx` on the utilisation column would be more robust to future refactors of the arithmetic.
- Any adopted plan should include an actual snapshot/diff of existing spreadsheet integration outputs for cells containing `"PASS"`, `"FAIL"`, and `"CHECK INPUT"` (A and B call this out; C and D do not explicitly).
- If a required sentinel parameter is adopted (A/D style), consider making it keyword-only (`*, invalid_result`) to prevent positional misuse that B warns about.

### Round 2: v2-medium-05

Key: A = `gpt5.6-sol-xhigh`, B = `gpt5.6-luna-max`, C = `gemma4:31b-cloud`, D = `gpt5.4-xhigh`

#### Blind judge report: v2-medium-05

**Task summary:** Review a 25-line pandas module that computes a per-row L/250 deflection utilisation via `iterrows()` and summarises it by Storey/Material, and either rewrite it or give a scoped patch plan covering performance at several hundred thousand rows, cleaning/validation, summary correctness, and maintainability.

##### Score table

| Response | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Note |
|---|---|---|---|---|---|---|---|
| A (`gpt5.6-sol-xhigh`) | 5 | 5 | 4 | 5 | 4 | 5 | Most complete and technically careful rewrite (vectorised, finite/positive checks, abs deflection, dtype-aware key cleaning, documented grain change), at the cost of scope beyond the ask. |
| B (`gpt5.6-luna-max`) | 5 | 5 | 4 | 4 | 4 | 4 | Proportionate, semantics-preserving vectorisation with full validation and fail-fast, but unconditionally stringifies group keys and only notes the multi-row grain question. |
| C (`gemma4:31b-cloud`) | 3 | 3 | 2 | 2 | 3 | 3 | Fixes the loop and the `float()` crash but mutates the caller's DataFrame, keeps signed deflection, ignores negative lengths, and silently discards coerced rows with no validation or reporting. |
| D (`gpt5.4-xhigh`) | 5 | 5 | 3 | 4 | 4 | 5 | Sharp line-referenced findings and a clean staged rewrite with member envelope and empty-input handling, but stringifies keys, skips an infinity check, changes aggregation grain, and has no docstring. |

##### Top weaknesses per response

**A (`gpt5.6-sol-xhigh`)**
- Member-envelope step changes `MemberCount` and `MeanRatio` semantics whenever an export has more than one row per member; it is flagged and defended, but it is still an unrequested behavioural change a reviewer must sign off.
- Scope creep: `errors="drop"` mode, `span_ratio_limit` parameter, reason-count breakdown and dtype-conditional normalisation were not asked for and add test surface (evaluator notes warn against unnecessary complexity).
- `sort=False` in both group-bys silently changes output row order versus the original sorted group-by; not mentioned.
- Uses tuples as `.loc[:, ...]` column indexers (`_REQUIRED_COLUMNS`, `_MEMBER_KEYS`); works on flat columns but would be misread on MultiIndex columns.

**B (`gpt5.6-luna-max`)**
- `astype("string")` is applied to all three key columns unconditionally, so integer Storey/Member IDs come back as string dtype in the summary (unflagged downstream compatibility change; the original inferred int64 back).
- Keeps `count` on `Member` with a code comment "Assumes one result row per member" but gives no cheap duplicate check or warning to make that assumption visible at run time.
- `sort=False` order change unflagged; error message does not say which validation rule failed, only example indices.
- Ratio rearranged to `abs * 250 / (L * 1000)`, which is algebraically identical but less legible against the L/250 formula than the original form.

**C (`gemma4:31b-cloud`)**
- Mutates the caller's DataFrame in place (coerces two columns and adds `DeflectionRatio`) and advertises this as a memory benefit; the original explicitly avoided input mutation via `row.copy()`.
- No validation at all: no required-column check, coerced NaNs and missing group keys are silently dropped by `max`/`mean`/`groupby`, and zero-length members are counted in `MemberCount` while their ratio vanishes from `MaxRatio`/`MeanRatio`.
- Misses the signed-deflection issue (large negative deflection still yields a negative ratio and a PASS) and does not handle negative lengths.
- Overclaims: "may cause memory exhaustion", "milliseconds rather than minutes", "the slowest possible way", and a comment that says the ratio uses a temporary series while the code assigns into `df`.

**D (`gpt5.4-xhigh`)**
- Unconditional key stringification (same compatibility issue as B) and no infinity check on the numeric columns (an `inf` length yields ratio 0 and a silent PASS).
- Envelope-per-member grain change is implemented unconditionally; the finding is well stated but the code does not document the new meaning of `MeanRatio`/`MemberCount` (no docstring at all on the function).
- Validation error reports a count only, with no example indices or reason breakdown, so a 300k-row export failure is hard to triage.
- `sort=False` order change unflagged.

##### Ranking (best to worst)

1. **A (`gpt5.6-sol-xhigh`)** — mean 4.67
2. **B (`gpt5.6-luna-max`)** — mean 4.33
3. **D (`gpt5.4-xhigh`)** — mean 4.33 (tie with B broken toward B on change safety: B preserves the original aggregation semantics and rejects infinities; D changes grain and skips the inf check)
4. **C (`gemma4:31b-cloud`)** — mean 2.67

##### Practical significance

A, B and D all deliver the core fix the task and evaluator notes call for (vectorised conversion and arithmetic, safe numeric coercion, rejection of zero/missing lengths, absolute deflection) and any of them would be mergeable after a short review; the roughly 0.3-point spread between them reflects second-order choices (whether to envelope per member, whether numeric group keys keep their dtype, how diagnostic the failure message is, whether infinity is rejected) rather than differences in whether the summary is right. C is in a different tier: it resolves the performance and `float()` issues but introduces a side effect on the input, leaves the sign problem in place, and converts hard failures into silent data loss, so it would need rework before it could be trusted on a real export. The A-to-C gap of about 2 points is material; the A/B/D differences are within reviewer-preference noise.

##### Manual-review watch-outs

- Confirm whether result exports contain multiple rows per member (load cases, stations). If yes, A and D change `MeanRatio` and `MemberCount` relative to the original; B keeps row-level semantics. Pick one contract and document it.
- B and D convert Storey/Material/Member to pandas `string` dtype unconditionally; if any key is numeric in production, downstream joins or filters on the summary will break. A only normalises object/string columns.
- All three viable responses (A, B, D) use `sort=False`, so summary row order differs from the original sorted group-by; check any consumer that relied on ordering.
- A, B and D raise `ValueError` on any invalid row where the original silently dropped rows with missing keys; callers need to handle that, and a single bad row now halts a several-hundred-thousand-row run (A offers an opt-in `errors="drop"` with a warning).
- D does not reject `inf`; A and B do. Verify export tooling never writes `inf`/`1e999`.
- A and B index with tuples in `.loc[:, tuple]`; fine on flat columns, but verify on the pandas version in use and never on MultiIndex columns.
- Empty-input behaviour: D returns an explicit empty frame with the six columns (object dtype); A and B rely on group-by over an empty frame producing the expected columns. Worth a unit test.
- A's boundary test claims (4 m / 16 mm gives exactly 1.0 and PASS; -20 mm gives 1.25 and FAIL) are arithmetically correct under its formula but should be pinned in tests since `<= 1.0` on floating-point equality is the pass/fail edge.
- If C is considered at all, callers must be audited for reliance on the input DataFrame being unmodified, and the silent NaN drop must be replaced with reporting.

### Round 2: v3-notebook-01

Key: A = `gpt5.4-xhigh`, B = `gpt5.6-sol-xhigh`, C = `gpt5.6-luna-max`, D = `gemma4:31b-cloud`

#### Blind judge report: v3-notebook-01

**Task summary:** Produce a notebook-style draft that sizes the smallest square pad footing (2.4 m to 3.2 m in 0.1 m steps) under three service load cases with biaxial moments, using a rigid-footing linear-pressure model, such that every case satisfies qmax <= 220 kPa and qmin >= 0 kPa, with stated assumptions, derivation, search, results table and conclusion.

##### Score table

| Response | Calculation correctness | Code quality and executability | Engineering judgement | Unit and assumption handling | Notebook traceability and clarity | Completeness of deliverable | Note |
|---|---|---|---|---|---|---|---|
| A (`gpt5.4-xhigh`) | 5 | 4 | 5 | 5 | 5 | 5 | Correct 3.0 m / LC2 with a genuine corner-based derivation from N/A + My*x/Iy + Mx*y/Ix, signed-moment handling, a per-candidate search table that exposes the LC2 uplift failure at 2.9 m, and unit-suffixed code; the only real nit is unguarded next() calls. |
| B (`gpt5.6-sol-xhigh`) | 5 | 4 | 3 | 4 | 3 | 3 | Numerically correct and executable with a guarded search loop, but it quotes the |M| compact formula without the requested derivation, model justification, or eccentricity/sign definitions, and its search summary prints only PASS/FAIL. |
| C (`gpt5.6-luna-max`) | 2 | 2 | 3 | 4 | 3 | 3 | Well structured and correctly reasoned in Markdown, but the point-pressure function uses 6*M*x/B^3 instead of 12*M*x/B^4, inflating corner bending terms by B/2, so its own isclose assert would raise on the first evaluation and halt the notebook before any result is computed. |
| D (`gemma4:31b-cloud`) | 3 | 3 | 2 | 2 | 2 | 2 | Runs and selects 3.0 m, but ignores the required section order and cell labelling, never states the size or governing case in prose, gives no per-candidate output, and reports LC3 (largest qmax) as governing rather than the uplift-controlled LC2. |

##### Top weaknesses per response

**A (`gpt5.4-xhigh`)**
- `selected = next(...)` and the per-case `first_passing_width_by_case` generator have no default, so an all-fail scenario would surface as a bare StopIteration rather than a clear message; the nested `next` inside a generator is dense to read.
- The derivation compresses the substitution step (writes "substituting x = +/-B/2, y = +/-B/2 gives q = N/B^2 +/- 6My/B^3 +/- 6Mx/B^3" without the one-line `My*(B/2)/(B^4/12)` arithmetic), which is acceptable but slightly less explicit than the preferred path.
- Markdown Cell 3 is thin (mostly a pointer to the code) compared with the other Markdown cells.

**B (`gpt5.6-sol-xhigh`)**
- Omits two explicit "you must" items from the brief: no explanation of why the rigid linear model is appropriate, and no derivation of the edge-pressure expression from axial plus bending stress (only the compact |M| formula is quoted; rule 10 not satisfied).
- Never defines eccentricities or moment/eccentricity directions; the |M| formulation is coherent but sidesteps the requested sign convention rather than stating it.
- Search summary prints only B and PASS/FAIL, so the notebook output itself does not show why 2.4 to 2.9 m fail; the reader must rely on prose in Markdown Cells 4 and 6.
- Code Cell 6 hard-codes `assert selected_width_m == 3.0` and looks up `B_m == 2.9`, binding the notebook to the expected answer; Markdown Cell 5 also pre-states a full numeric results table before the code cell that generates it.

**C (`gpt5.6-luna-max`)**
- Calculation bug: `pressure_at_point` returns `N/B^2 + 6*My*x/B^3 + 6*Mx*y/B^3`; with x = B/2 that gives 3*My/B^2, not the correct 6*My/B^3 (the general point form should be 12*M*x/B^4). Corner pressures are therefore overstated by a factor B/2 (1.2 to 1.6 over the candidate range).
- The `assert isclose(qmax_kpa, qmax_formula, abs_tol=1e-12)` in `evaluate_case` would fail on the very first call (B = 2.4, LC1: corners give about 269.1 kPa versus closed form 256.1 kPa), so Code Cell 4 raises AssertionError and Cells 5 and 6 never run; the correct values quoted in the Markdown conclusion are not produced by the code.
- Markdown Cell 3 is internally inconsistent: it states the wrong general `q(x,y)` expression and then, two lines later, the correct `q_My(x) = 12*My*x/B^4`.
- Minor: unused `report()` helper; candidate widths built by float accumulation (`2.4 + 0.1*i`) rather than integer tenths; hard-coded `assert isclose(selected_B_m, 3.0)`.

**D (`gemma4:31b-cloud`)**
- Does not follow the mandated six-section order or cell labelling: there is no "Input data" Markdown section (inputs are a code cell under section 1), "Python calculation cells" is replaced by "Analysis Model and Equations", and the outline stops at section 5.
- Reports the governing case as the case with the largest qmax (LC3), never identifies that qmin under LC2 controls the size, and gives no per-candidate output or any explanation of why 2.9 m fails, even though its loop does check qmin.
- The conclusion contains variable placeholders (`selected_B`, `governing_case`, `max_q_found`) instead of stated values, so the draft never states "3.0 m" or a governing case in prose.
- Sign convention is vacuous ("positive moments acting about the x and y axes"); eccentricities are defined but never used; the formula uses Mx + My without absolute values or a stated corner convention, so it is sign-fragile; Z = B^3/6 is quoted rather than derived from I = B^4/12.

##### Ranking (best to worst, mean of six technical scores)

1. **A (`gpt5.4-xhigh`)** - 4.83
2. **B (`gpt5.6-sol-xhigh`)** - 3.67
3. **C (`gpt5.6-luna-max`)** - 2.83
4. **D (`gemma4:31b-cloud`)** - 2.33

##### Practical significance

A and B both reach the correct decision (3.0 m, LC2 governing via uplift, 2.9 m rejected at qmin = -0.41 kPa) with code that would run; the gap between them is explanatory rather than numerical. A meets every explicit requirement of the analysis-model note and gives a search table from which a checker can see the uplift trap directly, whereas B would need additional annotation (derivation, model justification, eccentricity/sign definitions) before it satisfies the brief as written. The step down to C and D is substantive. C reads as the most polished of the four, but its calculation core is broken by a geometric-factor error and halts on its own consistency assert, so every number in its conclusion is asserted rather than computed; that is a worse auditability failure than it looks because the Markdown is convincing. D executes and selects the right footing, but it discards the required notebook structure, never states the answer in prose, gives no visibility into the candidate sweep, and reports the wrong governing case; a reviewer would not be able to tell from D's output that uplift, not bearing, drove the size. C and D are close in mean score and neither is acceptable without rework; A is usable as-is and B with light editing.

##### Manual-review watch-outs

- Confirm the C bug by inspection or execution: `6.0 * My * x_m / B_m**3` with `x_m = B_m/2` yields `3*My/B^2`, not `6*My/B^3`; the assert in `evaluate_case` should raise at B = 2.4, LC1. If a reviewer reads only C's Markdown they will see correct values and may mis-score it.
- Rule 9 (2.9 m selected by qmax only) is not triggered by any response; all four check qmin in the search. D's governing-case logic, however, is qmax-only and would mislead a reader about what controls the size.
- D's Markdown conclusion never states 3.0 m or a governing case; the values exist only in print output. Decide whether runtime prints satisfy "state a final selected footing size in metres".
- B and C both hard-code the expected answer in asserts (`== 3.0`, `B_m == 2.9`, `isclose(selected_B_m, 3.0)`); treat as answer-baking if the benchmark expects general-purpose notebooks.
- B's Markdown Cell 5 contains a pre-computed numeric table placed before the code that would generate it; verify it matches code output (it does for all three cases) but note the staleness risk.
- C's sign statement combines "right-hand rule about the positive axes" with "positive Mx increases pressure toward +y"; whether those agree depends on the unstated z-axis direction. It does not affect results here but is a latent inconsistency.
- D's formula omits absolute values and A's corner enumeration is the only approach that would remain correct for negative moment inputs; B and C use |M|. Irrelevant for this brief's all-positive moments but relevant if the benchmark is reused with mixed signs.
- A's derivation skips the explicit `M*(B/2)/(B^4/12) = 6M/B^3` line; judge whether that meets the "show briefly" requirement (scored here as meeting it).
- Candidate-width generation: A and B use integer tenths (clean); D uses `round(..., 1)` (fine); C uses `2.4 + 0.1*i` (works for these values, fragile in general).

## 13. Caveats

- Different judge from April: April's technical scores came from a Codex-based judge pass plus manual review; these come from Claude subagents. The calibration above measures that difference on the same April responses and the per-task offsets correct for it, but the correction is only as good as two anchors per task (four on the re-run tasks).
- One run per model per task, as in April.
- Both new models ran through the Codex VS Code extension in an empty sandbox with web lookup available on the anchor task, the same route as April's `gpt5.4-xhigh`; all other April models ran through cloud or API routes.
- Capture artefacts: the Sol v3 output lost its Markdown fences and table pipes in the copy and was judged on content; the Sol deep-01 run received the context as attached files rather than pasted text, which is why its output contains absolute file links.
- Cost figures in the run records are list-price estimates; the runs themselves counted against a subscription plan.
