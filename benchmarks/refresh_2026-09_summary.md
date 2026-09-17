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
