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

## Judge Output Summary

Manual comparative pass completed for all seven models.

Task summary: Assess whether a shared utilisation helper can be extracted without changing material-specific zero-capacity behaviour or downstream status text.

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

## Winner

- Winner: `kimi-k2-thinking`
- Difference size: `Very small`
- Why it matters in practice: `Kimi, glm, gemma, and qwen were all strong here. The ranking edge is mostly about presentation and practicality, not a major technical gap.`
