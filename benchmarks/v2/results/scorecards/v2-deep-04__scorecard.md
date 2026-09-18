# Task Scorecard

- `task_id`: `v2-deep-04`
- `task_title`: `Safe refactor with behaviour preservation constraints`
- `task_group`: `primary`
- `judge_prompt_version`: `templates/judge_prompt_template.md`
- `manual_reviewer`: `Codex (full seven-model manual pass including gpt5.4-xhigh)`

## Scores

| Model | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Economics/practicality | Overall notes |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `gemma4:31b-cloud` | 5 | 5 | 5 | 5 | 5 | 4 | 5 | Excellent answer: it preserved the zero-denominator split and extracted only a minimal shared helper with configurable fallback behaviour. |
| `glm-5.1:cloud` | 5 | 5 | 5 | 5 | 5 | 5 | 4 | Very strong: preserved zero-capacity behaviour and exact status text with a minimal shared helper approach. |
| `gpt5.4-xhigh` | 5 | 5 | 5 | 5 | 5 | 4 | 3 | Excellent and fully grounded: it identifies the real behavioural trap, keeps the material-specific zero-denominator split, and proposes a safely parameterised helper boundary. |
| `qwen-3.6plus` | 5 | 5 | 5 | 5 | 5 | 4 | 3 | Very strong and grounded: it preserves the zero-denominator split via a parameterised helper, though the extraction is slightly broader than the most minimal answer. |
| `minimax-m2.7-cloud` | 5 | 5 | 5 | 5 | 5 | 5 | 3 | Very strong and fully grounded: it recognised that the current split is already the safe shape and correctly rejected any shared utilisation helper. |
| `kimi-k2-thinking` | 5 | 5 | 5 | 5 | 5 | 5 | 5 | Excellent answer: it isolated the safe shared logic, preserved the zero-denominator split, and kept downstream status text intact. |
| `deepseek-v3.2` | 1 | 1 | 1 | 1 | 1 | 2 | 1 | Severe context failure: it answered against a fabricated helper structure and zero-denominator behaviour that do not exist in the supplied files. |
| `gpt5.6-sol-xhigh` | 5 | 5 | 5 | 5 | 5 | 5 | 3 | Blind winner in both judging rounds: recommends leave-as-is as the lowest-risk option, gives an explicit-policy helper that preserves the zero-denominator split, notes format_status(None) would raise, and supplies runnable parametrised tests covering the boundary and both denominators. |
| `gpt5.6-luna-max` | 5 | 5 | 5 | 5 | 5 | 5 | 3 | Correct parametrised helper with full code that flags the fallback-argument misuse risk and asks for spreadsheet output comparison, but its regression set misses the inclusive 1.0 boundary and utilisation-level asserts and it lists the <= 0 guard under both shared and distinct. |
| `gemma4:26b-local` | 4 | 5 | 5 | 5 | 4 | 4 | 3 | Spots the planted None-versus-0.0 zero-denominator split and rightly prefers leaving the helpers alone, offering a parameterised fallback helper only if insisted on, but two of its four regression checks expect status strings from functions that return floats, it omits the negative-denominator case its own table names, and the helper's semantics-selecting parameter is given a default. |

## Judge Output Summary

Manual comparative pass completed for all seven models.

Task summary: Assess whether a shared utilisation helper can be extracted without changing material-specific zero-capacity behaviour or downstream status text.

### September 2026 refresh

- Blind pack judged twice: `gpt5.6-sol-xhigh` 4.83 in both rounds, `gpt5.6-luna-max` 4.33 and 4.50, `gpt5.4-xhigh` 3.83 and 4.17, `gemma4:31b-cloud` 3.83 and 3.67.
- All four responses caught the concrete `None`/`CHECK INPUT` versus steel `0.0`/`PASS` trap and preserved the status text; the spread reflects depth of safeguards, not correctness.
- Sol led for recommending leave-as-is as the lowest-risk option, an explicit-policy helper, the `format_status(None)` observation and runnable parametrised tests; Luna's regression set omitted the inclusive 1.0 boundary and utilisation-level asserts.

### Gemma 4 26B local addendum (2026-09-19)

- Blind pack (one judging round, 2026-09-19): `gpt5.6-sol-xhigh` 4.83, `gpt5.4-xhigh` 4.17, `gemma4:31b-cloud` 4.00, `gemma4:26b-local` 3.50 on the six technical criteria; the judge ranked the local model last.
- Judge's one-line reading of the local model's response: Spots the trap and rightly prefers leaving the code alone, but its regression tests are mis-specified (expects `"PASS"`/`"FAIL"` from `concrete_utilisation`, which returns floats) and omit negative denominators.
- Judge's deduction: Regression checks 3 and 4 call `concrete_utilisation(1.0, 1.0)` / `concrete_utilisation(1.1, 1.0)` and expect `"PASS"` / `"FAIL"`; those functions return `1.0` and `1.1`. The tests as written would fail or would be quietly rewritten by whoever implements them; for a task that is explicitly about exactness of status text, that is a real defect.
- Judge's deduction: No negative-denominator test even though its own table says "Zero/Negative Denominator" and the code uses `<= 0`.
- Judge's deduction: The optional helper gives `fallback_value` a default of `None`; a default makes it easier for a call site to silently pick up the wrong semantics (here a missed argument in steel would propagate `None` into `format_status` and raise, which is at least loud, but a default on a semantics-selecting parameter is still poor design).

## Manual Override Notes

Provisional `glm-5.1:cloud` review:
- Read the behavioural trap correctly and made the right call that a naive deduplication is unsafe.
- Proposed a genuinely minimal shared helper with explicit fallback behaviour, preserving both current APIs and status outputs.
- Regression tests are well targeted to the exact zero-denominator and boundary behaviours that matter for this refactor.

Provisional `qwen-3.6plus` review:
- Read the behavioural trap correctly and preserved the concrete versus steel zero-capacity split via a fallback-parameterised helper.
- The helper extraction is slightly broader than the most conservative task-4 answers, but it does keep the downstream semantics intact.
- So this is a strong, grounded refactor review, just not the most minimal one in the set.

Provisional `gpt5.4-xhigh` review:
- Read the behavioural trap correctly and made the right call that only the valid-denominator division path should be shared.
- The recommended `utilisation_or(ed, rd, invalid_value)` boundary is safe and keeps the exact concrete/steel invalid-case split intact.
- This is technically in the top pack, but not enough better than `kimi`, `glm`, or `gemma` to overturn the practicality edge they already had.

Provisional `minimax-m2.7-cloud` review:
- Read the core behavioural trap correctly and explicitly rejected any shared utilisation helper that would collapse the concrete versus steel zero-capacity split.
- Its recommendation is even more conservative than the best refactor proposals: it effectively concludes that the current package shape is already the safe minimum.
- That is fully acceptable for this task because the brief prioritised behaviour preservation over deduplication.

Provisional `kimi-k2-thinking` review:
- Read the behavioural constraint correctly and explicitly rejected any refactor that would unify the concrete and steel zero-capacity paths.
- The proposed `_safe_ratio()` extraction is genuinely minimal and preserves both status text and public behaviour.
- Regression tests are well targeted to the exact branch behaviour that the prompt said must not change.

Provisional `deepseek-v3.2` review:
- This run is not a weak refactor review; it is a fabricated-code answer. It invents helpers, thresholds, status colours, and zero-denominator semantics that are absent from the real files.
- Because the proposal targets a nonexistent code structure, it fails repo comprehension and cannot be treated as a safe engineering answer.
- The run record also indicates it did not reliably wait for the actual files before answering, which materially hurts practicality.

Provisional `gemma4:31b-cloud` review:
- Correctly rejected a naive deduplication and preserved the concrete versus steel zero-capacity split.
- The proposed shared helper is genuinely minimal and preserves both downstream status text and public behaviour.
- This is essentially tied with the best task-4 responses; the only minor deduction is that it is slightly less explicit than the strongest write-ups.

### September 2026 refresh

- Scoring: technical criteria for `gpt5.6-sol-xhigh` and `gpt5.6-luna-max` were scored blind by a new judge alongside two April anchor responses, then shifted onto the April scale with a per-task offset of +0.96 derived from those anchors (see `benchmarks/refresh_2026-09_calibration.md`). The April rows above are unchanged.
- Manual overrides: none. The de-anonymised judgements were checked against the evaluator notes and no score was changed.
- Practicality `gpt5.6-sol-xhigh` = 3: same premium Codex route as `gpt5.4-xhigh`, faster on every task with a recorded time, no refusal or truncation, waited for context; scored as the April premium reference.
- Practicality `gpt5.6-luna-max` = 3: same Codex route on the budget API tier ($0.20 / $1.20 per 1M tokens list price), about 3 to 4 minutes per v2 task, no refusal or truncation, waited for context; low price offset by the slowest latency in the set.

### Gemma 4 26B local addendum (2026-09-19)

- Scoring: technical criteria for `gemma4:26b-local` were scored blind on 2026-09-19 by the same judge family as the September refresh, in a pack with the two April anchors plus `gpt5.6-sol-xhigh` as a consistency check. Over the model's eight packs the anchors failed the calibration gate (MAD 0.59, worst row 1.17), so the blind scores [3, 4, 4, 4, 3, 3] were shifted onto the April scale with the September per-task offset of +0.96, the standing user decision (see `benchmarks/addendum_2026-09-19_gemma4-26b-local.md`). Earlier rows above are unchanged.
- Manual overrides: none. The judge's claims about the response were checked against the response text; the defects it names are present as described.
- Practicality `gemma4:26b-local` = 3: free local inference on the user's own hardware, no API cost, no refusal, the two-message protocol followed; on the timed tasks the answer took 3 min 35 s to 7 min 32 s after a 30 to 45 s prompt-only reply (7.7 to 10.8 generated tokens per second, CPU-bound on an 8 GB card), so on the latency-only reading that applies to routes where cost is not counted it is scored as the 3 to 6 minute runs of `gpt5.6-luna-max` and the 2026-09-18 addendum models, not the 4 to 5 April gave the free cloud route for one-to-two-minute answers.

## Winner

- Winner: `kimi-k2-thinking`
- Difference size: `Very small`
- Why it matters in practice: `Kimi, glm, gemma, and qwen were all strong here. The ranking edge is mostly about presentation and practicality, not a major technical gap.`

September 2026 refresh: `gpt5.6-sol-xhigh` (overall mean 4.71) and `gpt5.6-luna-max` (4.71) do not beat the April result of `kimi-k2-thinking` (5.00), so the winner line is unchanged.

Gemma 4 26B local addendum (2026-09-19): `gemma4:26b-local` (overall mean 4.29) does not beat the April result of `kimi-k2-thinking` (5.00), so the winner line is unchanged.
