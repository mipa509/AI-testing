# September 2026 Refresh: Then-vs-Now Summary

How `gpt5.6-sol-xhigh` and `gpt5.6-luna-max` compare with the April 2026 slate on the same v2 and v3 tasks. Scores for the new models were produced blind and calibrated against April anchors; the full procedure, judge replies and calibration tables are in `benchmarks/refresh_2026-09_calibration.md`. April scores are unchanged.

## Headline

- **v2 primary (six tasks):** both new models top the cross-task table. `gpt5.6-luna-max` 4.48 and `gpt5.6-sol-xhigh` 4.45 against April's leader `gpt5.4-xhigh` at 4.14 and the best free/cloud model `gemma4:31b-cloud` at 4.10. On the six technical criteria alone Sol averages 4.69 and Luna 4.72 against 4.36 for `gpt5.4-xhigh`; the practicality column (3 for both, the same as the April premium reference) is what keeps the overall gap to about 0.3.
- **Like-for-like successor:** judged blind side by side by the same judge, Sol out-scored its predecessor `gpt5.4-xhigh` on five of the six primary tasks and the anchor, lost narrowly on the repo review (4.50 vs 4.67) and clearly on the v3 notebook (3.67 vs 4.83). Sol now holds the task-3 (scoped feature design) and task-5 (dataset pipeline) wins and the task-1 (bug hunt) win on a tie-break with Luna; `gemma4:31b-cloud` keeps task 2 and `kimi-k2-thinking` keeps task 4.
- **Budget tier:** Luna matches Sol on the v2 primary tasks at roughly one-sixteenth of Sol's list output price, and takes the task-6 (review plus tests) win outright. It is the slowest of the three in wall-clock terms (about 3 to 4 minutes per task) and it is the weakest on v3.
- **Anchor (EC3 trap):** all three reach the correct cross-section `PASS` at utilisation about 0.916 with `Wpl,y = 353 cm3`. Sol ties `gpt5.4-xhigh` at 4.43 overall with a fuller audit trail; Luna 4.29. Winner unchanged.
- **v3 notebook:** `gpt5.4-xhigh` remains the winner at 4.86. Sol (4.29) selects `3.0 m` with `LC2` governing and its code runs end to end, but it quotes the pressure formula without the requested derivation and never defines eccentricities. Luna (3.57) states the right answer and derivation in Markdown, but its point-pressure code uses `6*M*x/B^3` instead of `12*M*x/B^4`, so the notebook stops on its own consistency assert at code cell 4 and produces no result.

## Cross-task averages, v2 primary tasks (seven criteria)

| Model | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Economics/practicality | Overall | April rank | Sept rank |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `gpt5.6-luna-max` | 4.83 | 5.00 | 4.67 | 4.67 | 4.50 | 4.67 | 3.00 | **4.48** | new | 1 |
| `gpt5.6-sol-xhigh` | 4.83 | 4.67 | 4.50 | 4.67 | 4.67 | 4.83 | 3.00 | **4.45** | new | 2 |
| `gpt5.4-xhigh` | 4.33 | 4.50 | 4.00 | 4.33 | 4.17 | 4.83 | 2.83 | **4.14** | 1 | 3 |
| `gemma4:31b-cloud` | 4.00 | 4.00 | 3.83 | 4.00 | 4.00 | 4.17 | 4.67 | **4.10** | 2 | 4 |
| `glm-5.1:cloud` | 3.83 | 3.83 | 3.50 | 3.67 | 4.00 | 4.50 | 3.83 | **3.88** | 3 | 5 |
| `qwen-3.6plus` | 4.00 | 4.17 | 3.33 | 3.67 | 4.00 | 4.00 | 3.00 | **3.74** | 4 | 6 |
| `minimax-m2.7-cloud` | 3.67 | 4.00 | 3.50 | 3.50 | 4.17 | 4.17 | 3.00 | **3.72** | 5 | 7 |
| `kimi-k2-thinking` | 3.50 | 3.50 | 3.33 | 3.33 | 3.50 | 4.17 | 4.33 | **3.67** | 6 | 8 |
| `deepseek-v3.2` | 2.67 | 2.83 | 2.33 | 2.50 | 2.86 | 3.17 | 2.17 | **2.65** | 7 | 9 |

## Per-task overall means, all nine models

Overall mean of the seven scorecard columns per task. Winner per task in bold; the April winner is shown where it changed.

| Task | `gemma4:31b-cloud` | `glm-5.1:cloud` | `gpt5.4-xhigh` | `qwen-3.6plus` | `minimax-m2.7-cloud` | `kimi-k2-thinking` | `deepseek-v3.2` | `gpt5.6-sol-xhigh` | `gpt5.6-luna-max` | Winner (April winner) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Task 1 - Multi-file bug hunt | 4.29 | 4.14 | 4.00 | 3.57 | 3.57 | 1.14 | 3.57 | **4.71** | 4.71 | `gpt5.6-sol-xhigh` (April: `gemma4:31b-cloud`) |
| Task 2 - Repo review traps | **4.71** | 3.43 | 4.43 | 4.14 | 3.00 | 4.71 | 1.14 | 4.29 | 4.29 | `gemma4:31b-cloud` (unchanged) |
| Task 3 - Scoped feature design | 4.14 | 4.14 | 4.57 | 3.71 | 3.86 | 4.29 | 3.86 | **4.71** | 4.71 | `gpt5.6-sol-xhigh` (April: `gpt5.4-xhigh`) |
| Task 4 - Safe refactor | 4.86 | 4.86 | 4.57 | 4.57 | 4.71 | **5.00** | 1.14 | 4.71 | 4.71 | `kimi-k2-thinking` (unchanged) |
| Task 5 - Large dataset pipeline | 3.86 | 3.86 | 3.86 | 3.71 | 3.71 | 4.00 | 3.71 | **4.57** | 4.43 | `gpt5.6-sol-xhigh` (April: `kimi-k2-thinking`) |
| Task 6 - Review plus tests | 2.71 | 2.86 | 3.43 | 2.71 | 3.43 | 2.86 | 2.29 | 3.71 | **4.00** | `gpt5.6-luna-max` (April: `glm-5.1:cloud`) |
| Anchor - EC3 planted-error trap | 4.00 | 4.14 | **4.43** | 3.86 | 2.43 | 4.71 | 3.43 | 4.43 | 4.29 | `gpt5.4-xhigh` (unchanged) |
| v3 Task 1 - Pad footing notebook | 3.71 | 4.71 | **4.86** | 4.00 | 4.43 | 4.29 | 4.14 | 4.29 | 3.57 | `gpt5.4-xhigh` (unchanged) |

## Blind head-to-head against `gpt5.4-xhigh`

Six-criterion technical means from the blind packs, before calibration (the same judge scored all four responses in each pack; two-round tasks show the pooled mean). This is the cleanest like-for-like comparison in the refresh because it removes the judge change entirely.

| Task | `gpt5.4-xhigh` (blind) | `gpt5.6-sol-xhigh` (blind) | `gpt5.6-luna-max` (blind) | Low anchor (blind) | `gpt5.4-xhigh` April |
|---|---:|---:|---:|---:|---:|
| Task 1 - Multi-file bug hunt | 3.33 | 4.50 | 4.50 | `qwen-3.6plus` 3.17 | 4.17 |
| Task 2 - Repo review traps | 4.67 | 4.50 | 4.50 | `minimax-m2.7-cloud` 2.33 | 4.83 |
| Task 3 - Scoped feature design | 3.08 | 4.83 | 4.33 | `qwen-3.6plus` 2.75 | 4.83 |
| Task 4 - Safe refactor | 4.00 | 4.83 | 4.42 | `gemma4:31b-cloud` 3.75 | 4.83 |
| Task 5 - Large dataset pipeline | 4.33 | 4.75 | 4.50 | `gemma4:31b-cloud` 2.67 | 4.00 |
| Task 6 - Review plus tests | 3.00 | 3.83 | 4.17 | `deepseek-v3.2` 2.50 | 3.50 |
| Anchor - EC3 planted-error trap | 4.67 | 4.83 | 4.67 | `minimax-m2.7-cloud` 2.50 | 4.83 |
| v3 Task 1 - Pad footing notebook | 4.83 | 3.67 | 3.00 | `gemma4:31b-cloud` 2.42 | 5.00 |

## Practicality: latency, tokens and cost

From the run records. Both new models ran through the Codex VS Code extension in an empty sandbox, one fresh chat per run, the same route as April's `gpt5.4-xhigh`. Token counts are as reported by Codex. **Cost figures are list-price upper-bound estimates** (every token priced as output: Sol about $20 per 1M, Luna $1.20 per 1M); the runs actually counted against a subscription plan. April's `gpt5.4-xhigh` records captured timing only for the anchor (about 4 min 38 s with web research) and v3 (thought for 3 min 45 s).

| Task | Model | Latency | Codex tokens | Est. cost (list, upper bound) | Notes |
|---|---|---|---:|---:|---|
| Task 1 - Multi-file bug hunt | `gpt5.6-sol-xhigh` | 56 s after context | ~24k | $0.48 | context delivered as attached files |
| Task 1 - Multi-file bug hunt | `gpt5.6-luna-max` | about 3 min after context | ~28k | $0.03 |  |
| Task 2 - Repo review traps | `gpt5.6-sol-xhigh` | under 1 min after context | ~21k | $0.42 |  |
| Task 2 - Repo review traps | `gpt5.6-luna-max` | about 3 min after context | ~26k | $0.03 |  |
| Task 3 - Scoped feature design | `gpt5.6-sol-xhigh` | up to about 2 min after context | ~25k | $0.50 |  |
| Task 3 - Scoped feature design | `gpt5.6-luna-max` | about 4 min after context | ~31k | $0.04 |  |
| Task 4 - Safe refactor | `gpt5.6-sol-xhigh` | under 1 min after context | ~21k | $0.42 |  |
| Task 4 - Safe refactor | `gpt5.6-luna-max` | about 1 min after context | ~20k | $0.02 |  |
| Task 5 - Large dataset pipeline | `gpt5.6-sol-xhigh` | under 2 min after context | ~25k | $0.50 |  |
| Task 5 - Large dataset pipeline | `gpt5.6-luna-max` | about 3 min to first output | ~28k | $0.03 |  |
| Task 6 - Review plus tests | `gpt5.6-sol-xhigh` | under 1 min after context | ~21k | $0.42 |  |
| Task 6 - Review plus tests | `gpt5.6-luna-max` | about 1 min 40 s to first output | ~24k | $0.03 |  |
| Anchor - EC3 planted-error trap | `gpt5.6-sol-xhigh` | 3 min 30 s | ~85k | $1.70 | web lookup (SCI P363) |
| Anchor - EC3 planted-error trap | `gpt5.6-luna-max` | over 6 min 30 s | ~131k | $0.16 | web lookup (SCI P363, third-party EN 1993-1-1 PDF) |
| v3 Task 1 - Pad footing notebook | `gpt5.6-sol-xhigh` | not captured | ~23k | $0.46 | fences lost in copy |
| v3 Task 1 - Pad footing notebook | `gpt5.6-luna-max` | about 4 min (3 min before output) | ~31k | $0.04 |  |
| All eight tasks | `gpt5.6-sol-xhigh` | | ~245k | $4.90 | |
| All eight tasks | `gpt5.6-luna-max` | | ~319k | $0.38 | |

Practicality scores given: Sol 3 on the six primary tasks, 2 on the anchor, 4 on v3 (identical to the April `gpt5.4-xhigh` reference except on task 2, where Sol answered within a minute and scores 3 against the reference 2); Luna 3 on the primary tasks, 2 on the anchor, 3 on v3. Reasoning is in the calibration record, section 9.

## Calibration result

- The new judge re-scored two April responses per task blind (`gpt5.4-xhigh` and the weakest eligible April model). Against the frozen April scores the overall mean absolute difference was 0.79 points per criterion with a signed mean of -0.60 (the new judge is harsher), against a proposed gate of 0.5; the worst single row was 1.83 (task 3, `gpt5.4-xhigh`). The gate failed.
- The blind judge preserved April's order of the two anchors on every task, and a second blind judge on the four most drifted tasks reproduced the first to within about a third of a point, so the drift is a systematic scale difference rather than noise.
- Decision (user, 2026-09-17): shift the new models' blind scores onto the April scale with a per-task offset equal to the mean anchor drift on that task (from +0.08 on the anchor to +1.42 on task 3), rounded to integers and clamped to 1 to 5. No April score was touched.
- Effect: on tasks 1, 3 and 4 the shift saturates at 5 for both new models, so the tables above understate Sol's blind margin over Luna on tasks 3 and 4 (about 0.4 to 0.6) and both models' margin over `gpt5.4-xhigh`.

## Caveats

- Different judge from April: April's scores came from a Codex-based judge pass plus manual engineering review; these come from Claude Code subagents (Claude Fable 5.1) scoring blind. The calibration offsets correct the scale, but two anchors per task (four on the re-run tasks) is a small sample.
- One run per model per task, as in April; no repeat runs, so single-run variance is unquantified.
- Route: Codex VS Code extension with web lookup available on the anchor task, matching April's `gpt5.4-xhigh` but not the cloud or API routes used for the other April models.
- Capture artefacts: the Sol v3 output lost its Markdown fences in the copy and was judged on content; the Sol task-1 run received the context as attached files rather than pasted text, so its output contains absolute file links; all other runs received pasted text.
- Cost figures are list-price upper bounds, not billed amounts.
- Scores for the seven April models, their notes and their April winners are unchanged; only the per-task winner lines changed where a new model's overall mean beat the April winner (tasks 1, 3, 5 and 6).

## Addendum 2026-09-18: DeepSeek V4.1 Flash on three tasks

`deepseek-v4.1-flash` (OpenRouter `deepseek/deepseek-v4.1-flash`, reasoning effort high, run by the user from a VS Code agent chat) was run on the three tasks that separated the models best in the rounds above: the repo review with unit and reporting traps, the EC3 anchor and the pad footing notebook. It was scored with the same blind procedure, in packs holding the same April anchors plus `gpt5.6-sol-xhigh` as a consistency check, and shifted onto the April scale with the September per-task offsets (user decision). Full record, seeds, mapping and judge replies: `benchmarks/addendum_2026-09-18_deepseek-v4.1-flash.md`.

| Task | Blind, six criteria | On April scale | Practicality | Overall | Position on the task |
|---|---:|---:|---:|---:|---|
| Task 2 - Repo review traps | 4.00 | 4.00 | 3 | 3.86 | 7th of 10, between `qwen-3.6plus` (4.14) and `glm-5.1:cloud` (3.43); winner `gemma4:31b-cloud` (4.71) unchanged |
| Anchor - EC3 planted-error trap | 3.17 | 3.17 | 2 | 3.00 | 9th of 10, above `minimax-m2.7-cloud` (2.43) only; winner `gpt5.4-xhigh` (4.43) unchanged |
| v3 Task 1 - Pad footing notebook | 4.83 | 5.00 | 3 | 4.71 | 2nd of 10, level with `glm-5.1:cloud`; winner `gpt5.4-xhigh` (4.86) unchanged |

Read:

- The DeepSeek V3.2 failure mode is gone: on Task 2 the model reviewed the supplied files, found all three planted blockers and scored within half a point of `gpt5.4-xhigh` and `gpt5.6-sol-xhigh` in the same blind pack.
- It was strongest on the executable deliverable: blind 4.83 on the notebook, level with `gpt5.4-xhigh` and above `gpt5.6-sol-xhigh` (3.67); the six code cells run end to end, select `3.0 m` with `LC2` governing and cross-check the no-uplift rule against the kern criterion.
- It was weakest on the hand-calculation anchor: correct corrected numbers, but a headline verdict of not adequate on an LTB check the task did not pose, a narrative that contradicts itself about the original code, and an endorsement of the planted `49.0 cm3` as the tabulated minor-axis value. The run took about 15 minutes with blocked web lookups.
- Cost and time: the three runs were billed about $0.10 in total through OpenRouter (list price $0.15 / $0.60 per 1M tokens); latencies were 2 min 45 s, about 15 min and 4 min 15 s.
- Calibration: anchor MAD 0.64 and signed -0.47 against April with anchor order preserved on every task, and `gpt5.6-sol-xhigh` within 0.17 of its September blind scores, so the judge family is consistent with the September round.

Caveats specific to this addendum: three tasks only, so its v2 average is provisional (Task 2 and the anchor, marked as such in the v2 ranking) until the remaining primary tasks are run; the agent read the task files from the workspace folder rather than receiving them as pasted messages, read the other task folders unasked on two runs, and on the anchor read the two header lines of the prompt file above the text block; web lookups were blocked on the anchor whereas the September models had them; one run per task.

## Addendum 2026-09-18: GLM 5.3 Flash on the same three tasks

`glm-5.3-flash` (OpenRouter `z-ai/glm-5.3-flash`, reasoning effort high, same VS Code agent route as the DeepSeek runs) was run on the same three tasks and scored the same way. Its anchors met the calibration gate (MAD 0.50, no row above 1.0), so the blind scores stand as-is with no offset. Full record: `benchmarks/addendum_2026-09-18_glm-5.3-flash.md`.

| Task | Blind, six criteria | Practicality | Overall | Position on the task |
|---|---:|---:|---:|---|
| Task 2 - Repo review traps | 4.00 | 3 | 3.86 | 7th equal of 11 with `deepseek-v4.1-flash`; winner `gemma4:31b-cloud` (4.71) unchanged |
| Anchor - EC3 planted-error trap | 4.00 | 2 | 3.71 | 8th of 11, between `qwen-3.6plus` (3.86) and `deepseek-v3.2` (3.43); winner `gpt5.4-xhigh` (4.43) unchanged |
| v3 Task 1 - Pad footing notebook | 4.17 | 3 | 4.00 | 8th of 11, level with `qwen-3.6plus`; winner `gpt5.4-xhigh` (4.86) unchanged |

Read:

- Grounded and complete on the repo review: all three planted blockers found with numeric examples; deductions for a rounding-direction claim the code cannot produce and for length.
- Steadier than DeepSeek on the anchor: both faults corrected, `PASS` at 0.920, LTB kept as a validity condition rather than a headline verdict, but a slightly off major-axis modulus (351.5 for 353) and a wrong minor-axis one (about 25.1 for about 54.8), with no web lookup.
- Weaker than DeepSeek on the notebook: the Markdown has the fullest derivation and sweep of the addendum models and names `LC2`, but the code prints `LC3` as governing (verified by execution) and the middle-third equivalence used to explain the 2.9 m failure is wrong for biaxial loading.
- Cost and time: about $0.03 for the three runs; 4 min 30 s, 5 min 56 s and 10 min 34 s.

Provisional v2 averages: with two partial models in hand, the v2 cross-task table now carries provisional columns for `deepseek-v4.1-flash` and `glm-5.3-flash` averaged over the v2 tasks they ran (Task 2 and the anchor). They include the anchor, so they are not comparable with the six-task composite of the full models and will be replaced when the remaining tasks are run.

## Addendum 2026-09-18: Tencent Hy4 Preview on the same three tasks

`tencent-hy4-preview` (OpenRouter `tencent/hy4-preview`, reasoning effort high, same VS Code agent route, list price $0.83 / $2.50 per 1M tokens, about seven times the two flash models) was run on the same three tasks and scored the same way. Its anchors failed the calibration gate in the usual direction, so the September per-task offsets were applied, as for DeepSeek. Full record: `benchmarks/addendum_2026-09-18_tencent-hy4-preview.md`.

| Task | Blind, six criteria | On April scale | Practicality | Overall | Position on the task |
|---|---:|---:|---:|---:|---|
| Task 2 - Repo review traps | 4.17 | 4.17 | 3 | 4.00 | 7th of 12, the best of the three addendum models; winner `gemma4:31b-cloud` (4.71) unchanged |
| Anchor - EC3 planted-error trap | 3.00 | 3.00 | 2 | 2.86 | 11th of 12, above `minimax-m2.7-cloud` (2.43) only; winner `gpt5.4-xhigh` (4.43) unchanged |
| v3 Task 1 - Pad footing notebook | 4.83 | 5.00 | 3 | 4.71 | 2nd equal of 12 with `deepseek-v4.1-flash` and `glm-5.1:cloud`; winner `gpt5.4-xhigh` (4.86) unchanged |

Read:

- The deepest repo review of the day: all three planted blockers with worked numbers, and the only response in its pack to explain that the two arithmetic errors pull in opposite directions. It lost points on change safety for proposing caller-breaking "minimum" fixes and for length.
- The best notebook of the addendum models by the blind judge, ranked above `gpt5.4-xhigh` in its pack: an `M*c/I` derivation, exact-fraction arithmetic, all four corner pressures, closed-form minimum-width bounds and both governing cases identified; it runs end to end. Deductions only for reversed eccentricity naming and length.
- The same anchor failure as DeepSeek, in a more elaborate form: correct diagnosis and numbers, then a NOT adequate headline on LTB and deflection checks the task did not pose, with factored self-weight added to the input load. Nearly 13 minutes.
- Cost and time: about $0.34 for the three runs, ten times the flash models but still small; 1 min 59 s, 3 min 18 s and 12 min 50 s.

Three-model pattern on the anchor: the two models that headlined an unrequested LTB verdict (`deepseek-v4.1-flash`, `tencent-hy4-preview`) sit at the bottom of the anchor table, while `glm-5.3-flash`, which kept LTB as a validity condition, sits mid-table. The task rewards answering the question asked.

## Addendum 2026-09-19: Claude Fable 5.1 on the same three tasks

`claude-fable-5.1-high` (Anthropic `claude-fable-5-1`, reasoning effort high, run in Claude Code from the VS Code terminal on a subscription plan; list price $10 / $50 per 1M tokens) was run on the same three tasks, one fresh session per task in a sandbox folder with the task files only, and scored the same way. The user withheld the model's identity from the orchestrator and the judges until scoring was complete. The anchors failed the calibration gate in the usual direction, so the September per-task offsets were applied. The runs were on a subscription plan; each session's own cost summary gives $1.29, $1.48 and $2.65, recorded but not scored under the practicality rule adopted with this addendum (cost neglected for subscription runs, counted for API-billed runs; earlier rows keep the frozen cost-inclusive reading). Full record: `benchmarks/addendum_2026-09-19_claude-fable-5.1-high.md`.

| Task | Blind, six criteria | On April scale | Practicality | Overall | Position on the task |
|---|---:|---:|---:|---:|---|
| Task 2 - Repo review traps | 4.67 | 4.42 (two-judge mean) | 3 | 4.21 | behind `gemma4:31b-cloud`, `kimi-k2-thinking` and `gpt5.4-xhigh`, level with Sol and Luna; the highest technical score of any model on this task since April (ranked first in its pack above `gpt5.4-xhigh` and Sol); winner `gemma4:31b-cloud` (4.71) unchanged |
| Anchor - EC3 planted-error trap | 4.33 | 4.08 (two-judge mean) | 2 | 3.79 | 6th equal of 13 with `gemma4:31b-cloud`; the best addendum result on the anchor by a wide margin; winner `gpt5.4-xhigh` (4.43) unchanged |
| v3 Task 1 - Pad footing notebook | 5.00 | 4.58 (two-judge mean) | 3 | 4.36 | just below the 4.71 group; a straight 5.00 on the technical criteria, ranked first in its pack above `gpt5.4-xhigh`; winner `gpt5.4-xhigh` (4.86) unchanged |

Read:

- The strongest technical showing of any addendum model, and on two of the three tasks the strongest of any model in the repo: first in its blind pack on the repo review (4.67 against `gpt5.4-xhigh` 4.33) and on the notebook (5.00 against 4.67), where the judge re-computed its worked numbers and found no errors.
- The repo review found all three planted blockers, tabulated correct-versus-coded values, and was the only response in its pack to argue that the two arithmetic errors pull in opposite directions, so fixing only the loud one would ship a hidden unconservative PASS. It lost a point each on change safety and clarity for length and for two later findings that drift into design recommendations.
- The notebook is the fullest audit document in the v3 set: Navier derivation with the kern limit, reference eccentricity convention, a hand-check cell, a full pass/fail matrix with failure-type flags, a closed-form minimum-width cross-check and commentary on the thin uplift margin; the six code cells run end to end.
- The anchor is where it gave ground, and differently from the 2026-09-18 addenda: it kept the planted objective (0.92 PASS if restrained) as the headline and stated the LTB failure as conditional, but it answered at design-study length with classification, shear, a full `M_cr` chain and an indicative deflection row on assumed load factors, so it sits behind Sol and `gpt5.4-xhigh` on scope rather than on correctness.
- Time is the drag: API times of 4 to 6 minutes (wall clock 6 to 11 minutes), the slowest run recorded on the repo review and the notebook, mid-pack on the anchor. The practicality column (3 / 2 / 3, latency only, since the runs were on a subscription plan) is what holds it below the April winners. Had the same runs been API-billed, the $5.42 session total would have been sixteen times Tencent Hy4 and about a hundred times the flash models, which is the case for a separate API-cost view of the results for readers billed that way (for example enterprise accounts).

Cross-family check: because the judge and the model under test are both Claude models, the user re-ran the three packs through a judge from another family (GPT-6 Astra at xhigh, in Codex). It was level or more lenient on the nine responses that are not Fable (+0.22 on average) and lower on all three Fable responses (-0.94 on average), keeping the anchor rankings but moving Fable from first to third on the repo review and from first to second on the notebook. That is consistent with same-family favouritism in the first judge and also with the second judge preferring terse responses; two judges cannot separate the two. The user read this as the same-family judge favouring its own model and chose to record Fable's technical rows as the two-judge mean, each judge calibrated through its own anchors first (section 7 of the record): 4.42 / 4.08 / 4.58 against 4.67 / 4.33 / 5.00 on the Claude judge alone. The table above shows the recorded values; every other model keeps its single same-family judge.

Four-model pattern on the anchor: the two models that headlined an unrequested LTB verdict (`deepseek-v4.1-flash`, `tencent-hy4-preview`) sit at the bottom of the anchor table, `glm-5.3-flash`, which kept LTB as a validity condition, sits mid-table, and `claude-fable-5.1-high`, which kept the planted PASS as the headline but surrounded it with a full design check, sits with the April mid-field. The task rewards answering the question asked, at the length asked.

## Addendum 2026-09-19: Gemma 4 26B run locally, all tasks

`gemma4:26b-local` (Ollama `gemma4:26b` on the user's own machine, PowerShell terminal, no harness, tools, skills or web access; free; Intel i7-9700K, 64 GB, RTX 2070 SUPER 8 GB) was run on all eight tasks as a free-tier comparison point and scored the same way. Over its eight packs the anchors failed the calibration gate (MAD 0.59, worst row 1.17), so the September per-task offsets were applied to every task, revising the notebook row first recorded as-is. It is a different model from the April `gemma4:31b-cloud` row. Full record: `benchmarks/addendum_2026-09-19_gemma4-26b-local.md`.

| Task | Blind, six criteria | On April scale | Practicality | Overall | Position on the task |
|---|---:|---:|---:|---:|---|
| Task 1 - Multi-file bug hunt | 2.17 | 3.17 | 3 | 3.14 | 9th of 10; winner `gpt5.6-sol-xhigh` (4.71) unchanged |
| Task 2 - Repo review traps | 4.17 | 4.17 | 3 | 4.00 | 8th equal of 14; winner `gemma4:31b-cloud` (4.71) unchanged |
| Task 3 - Scoped feature design | 3.17 | 4.17 | 3 | 4.00 | 7th of 10; winner `gpt5.6-sol-xhigh` (4.71) unchanged |
| Task 4 - Safe refactor | 3.50 | 4.50 | 3 | 4.29 | 9th of 10; winner `kimi-k2-thinking` (5.00) unchanged |
| Task 5 - Large dataset pipeline | 2.50 | 2.50 | 3 | 2.57 | 10th of 10; winner `gpt5.6-sol-xhigh` (4.57) unchanged |
| Task 6 - Review plus tests | 3.00 | 3.00 | 3 | 3.00 | 5th of 10; winner `gpt5.6-luna-max` (4.00) unchanged |
| Anchor - EC3 planted-error trap | 1.50 | 1.50 | 3 | 1.71 | 14th of 14; winner `gpt5.4-xhigh` (4.43) unchanged |
| v3 Task 1 - Pad footing notebook | 1.83 | 2.83 | 3 | 2.86 | 14th of 14; winner `gpt5.4-xhigh` (4.86) unchanged |

v2 six-task average 3.50, which places it in the lower half of the full table; anchor 1.71, the lowest recorded; v3 2.86, the lowest recorded.

Read:

- Best where the code is in front of it and the ask is a review: Task 2 (all three planted blockers, 4.17 on the technical criteria) and Task 4 (the None-versus-0.0 trap seen, and the right advice to leave the helpers alone). Task 3's plan is safe but undecided on aggregation and zero division.
- Weak wherever it has to write code that must run or supply numbers from memory: the notebook does not execute (non-breaking space in a literal, widths scaled twice), the Task 1 patch has a `SEIONS` typo that raises on every call, the Task 5 rewrite has a walrus-in-subscript artefact and silently drops rows, the Task 6 fix reintroduces a silent zero, and the anchor cites a Blue Book modulus that does not exist in the table.
- The pattern the judges kept naming: right diagnosis, unverified deliverable. Every one of its patches and tests would need a human pass before use; two of its own tests contradict its own code.
- Practicality: free, and it waited for the context every time, but on consumer hardware with an 8 GB card the 26B weights run mostly on CPU at 8 to 12 tokens per second, so each answer took 3.5 to 7.5 minutes after a 30 to 45 s prompt-only reply. Scored 3 on every task on the latency-only reading.
- Against its cloud sibling: April's `gemma4:31b-cloud` scored 4.10 on the v2 composite and 4.00 on the anchor with runnable code; the 26B local model shows what the smaller weights and the lack of tooling cost on these tasks.
