# Task Scorecard

- `task_id`: `v2-deep-03`
- `task_title`: `Scoped feature design on an existing package`
- `task_group`: `primary`
- `judge_prompt_version`: `templates/judge_prompt_template.md`
- `manual_reviewer`: `Codex (full seven-model manual pass including gpt5.4-xhigh)`

## Scores

| Model | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Economics/practicality | Overall notes |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `gemma4:31b-cloud` | 4 | 4 | 4 | 4 | 4 | 4 | 5 | Solid implementation plan with good opt-in compatibility thinking, though still somewhat generic and broader than the minimum surface area needed. |
| `glm-5.1:cloud` | 4 | 4 | 4 | 4 | 4 | 5 | 4 | Strong scoped plan with compatibility thinking; mild risk from expanding the report API and output schema. |
| `gpt5.4-xhigh` | 5 | 5 | 5 | 5 | 4 | 5 | 3 | Strongest task-3 plan in the current set: it preserves current ULS interfaces, avoids widening `report_rows()` by default, and gives the clearest file-by-file optional SLS design. |
| `qwen-3.6plus` | 4 | 4 | 3 | 4 | 4 | 4 | 3 | Grounded and workable plan, but it changes `report_rows()` surface area and introduces extra merging mechanics beyond the minimum compatibility path. |
| `minimax-m2.7-cloud` | 4 | 4 | 4 | 4 | 4 | 4 | 3 | Coherent additive plan that preserves existing report output, though it expands the schema and is slightly internally mixed about how extended consumers should access SLS data. |
| `kimi-k2-thinking` | 4 | 4 | 4 | 4 | 4 | 5 | 5 | Solid scoped plan with backward-compatibility intent; slightly broader than necessary but still well grounded in the given package shape. |
| `deepseek-v3.2` | 4 | 4 | 4 | 4 | 4 | 4 | 3 | Reasonable implementation plan with good compatibility intent, though it introduces extra APIs and acceptance criteria that are broader than necessary. |

## Judge Output Summary

Manual comparative pass completed for all seven models.

Task summary: Plan an optional serviceability summary that preserves existing ULS callers and keeps report output stable for downstream consumers.

## Manual Override Notes

Provisional `glm-5.1:cloud` review:
- Produced a coherent file-by-file implementation plan with clear data flow, compatibility risks, and targeted tests.
- Kept the default ULS path stable, which matches the prompt's backward-compatibility constraint.
- Main caution is scope: adding `include_sls` to `report_rows` changes an existing interface, and `Status_SLS` is extra output not explicitly required by the request.

Provisional `qwen-3.6plus` review:
- Produced a grounded, decision-complete plan with optional SLS handling and a clear attempt to keep current ULS-only callers working.
- Its main risk is interface drift: adding a `columns` parameter to `report_rows()` and introducing extra merge helpers broadens the surface area more than necessary.
- That makes it usable but slightly less compatibility-safe than the best task-3 plans.

Provisional `gpt5.4-xhigh` review:
- Produced the clearest compatibility-preserving task-3 plan in the set: existing `build_uls_summary()` and `report_rows()` stay stable by default, while serviceability is added through new opt-in surfaces.
- It handled the hidden contract trap correctly by avoiding changes to `RESULT_COLUMNS` ordering and by keeping current ULS callers unchanged.
- The only material deduction is economics/practicality: this is a premium slower run rather than a cheap/free cloud answer.

Provisional `minimax-m2.7-cloud` review:
- Produced a coherent additive plan with optional SLS columns and clear intent to keep `report_rows()` stable for existing consumers.
- The answer is grounded in the supplied package shape, but it is a little internally mixed about whether extended consumers should rely on new helpers or direct column access.
- Deductions are mainly for scope: extra schema helpers and broader validation policy beyond the minimum decision-complete plan.

Provisional `kimi-k2-thinking` review:
- Produced a coherent implementation plan with clear schema additions, opt-in behaviour, and targeted acceptance tests.
- It handled the main compatibility constraint correctly by preserving default ULS-only outputs for existing consumers.
- Deductions are mainly for scope expansion: changing `build_uls_summary()` itself, adding extra status semantics, and introducing collision-handling policy that the prompt did not require.

Provisional `deepseek-v3.2` review:
- The answer is grounded in the supplied package shape and keeps backward compatibility as a central constraint.
- It proposes a sensible separation between existing ULS-only flows and optional serviceability reporting.
- Main deductions are for extra surface area: new functions, additional result schemas, and performance targets that go beyond the minimum decision-complete plan.

Provisional `gemma4:31b-cloud` review:
- Produced a sound opt-in plan that preserves default ULS behaviour for existing consumers.
- The answer is a bit generic compared with the best responses, but it remains grounded in the supplied three-file package and does not make unsafe leaps.
- Main deductions are for broadness: additional helper functions and schema additions that are acceptable but not uniquely well justified.

## Winner

- Winner: `gpt5.4-xhigh`
- Difference size: `Small`
- Why it matters in practice: `GPT-5.4 gave the cleanest file-by-file design that preserves current ULS contracts and adds serviceability only through explicit new paths, which is exactly what this task was testing.`
