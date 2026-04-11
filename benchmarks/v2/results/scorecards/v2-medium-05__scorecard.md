# Task Scorecard

- `task_id`: `v2-medium-05`
- `task_title`: `Large dataset engineering summary pipeline`
- `task_group`: `primary`
- `judge_prompt_version`: `templates/judge_prompt_template.md`
- `manual_reviewer`: `Codex (full seven-model manual pass including gpt5.4-xhigh)`

## Scores

| Model | Correctness | Repo comprehension | Change safety | Engineering judgement | Maintainability | Clarity | Economics/practicality | Overall notes |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `gemma4:31b-cloud` | 4 | 4 | 3 | 4 | 4 | 4 | 4 | Good vectorised rewrite and sensible validation, but it mutates the input frame in place and still broadens the task into a fuller redesign. |
| `glm-5.1:cloud` | 4 | 4 | 3 | 4 | 4 | 4 | 4 | Good vectorisation and validation instincts, but it jumped to a larger rewrite and changed output semantics with `UNKNOWN` statuses. |
| `gpt5.4-xhigh` | 4 | 4 | 3 | 4 | 4 | 5 | 3 | Strong vectorised rewrite with clear validation and member-level roll-up reasoning, but it still broadens the task into a fuller redesign with new assumptions about deflection sign and aggregation semantics. |
| `qwen-3.6plus` | 4 | 4 | 3 | 4 | 4 | 4 | 3 | Solid vectorised rewrite and validation instincts, but it becomes a broad redesign with new parameters, helper functions, and optimistic benchmark claims. |
| `minimax-m2.7-cloud` | 4 | 4 | 3 | 4 | 4 | 4 | 3 | Technically sound on vectorisation and validation, but it grows into a broad redesign with custom exceptions, warnings, optional percentiles, and unsupported performance claims. |
| `kimi-k2-thinking` | 4 | 4 | 3 | 4 | 4 | 4 | 5 | Technically strong on vectorisation and validation, but it turns the review into a broader redesign with new parameters and data-handling policy. |
| `deepseek-v3.2` | 4 | 4 | 3 | 4 | 4 | 4 | 3 | Strong on vectorisation and validation, but it expands the scope into a much larger redesign with extra stats, helper functions, and reporting features. |

## Judge Output Summary

Manual comparative pass completed for all seven models.

Task summary: Review a member-summary pipeline for large-data performance, cleaning, correctness, and maintainability under several-hundred-thousand-row workloads.

## Manual Override Notes

Provisional `glm-5.1:cloud` review:
- Correctly targeted the main scaling problem by removing `iterrows()` and moving the ratio calculation to vectorised column operations.
- Added useful numeric coercion and basic input validation for large messy exports.
- Main weakness is proportionality: it jumps straight to a full rewrite, introduces a new `UNKNOWN` status, and does not discuss how dropping invalid rows affects grouped counts and report semantics.

Provisional `qwen-3.6plus` review:
- Correctly targeted `iterrows()` as the main bottleneck and moved to a workable vectorised implementation with clearer validation.
- It also improves some details such as counting rows with `size` rather than `count`.
- Main deductions are for proportion: the answer expands into a broad redesign with new parameters, helpers, and speculative performance claims rather than a tighter patch plan.

Provisional `gpt5.4-xhigh` review:
- Correctly targeted `iterrows()` as the main scaling bottleneck and moved to a vectorised implementation with explicit schema and numeric validation.
- The response is clearer than most on why row-wise loops and bare `float()` casts are dangerous at this scale.
- Main deductions are for proportionality: it introduces a fuller redesign, including member-level re-aggregation and an absolute-deflection assumption that goes beyond the minimum safe patch.

Provisional `minimax-m2.7-cloud` review:
- Correctly targeted `iterrows()` as the main scale bottleneck and moved toward vectorised numeric conversion and aggregation.
- It also calls out the real validation gaps around non-numeric values and zero lengths.
- Main deductions are for proportionality: the answer balloons into a much larger redesign with custom exceptions, warnings, optional percentile reporting, and speculative benchmark timings.

Provisional `kimi-k2-thinking` review:
- Correctly targeted the main large-data problem by removing `iterrows()` and replacing it with vectorised numeric conversion and ratio calculation.
- Validation and maintainability suggestions are mostly sensible, and unlike `glm` it keeps the final status vocabulary unchanged.
- Main deductions are for scope and contract drift: it adds `deflection_limit` and `drop_invalid` parameters, changes invalid-row handling policy, and presents a fairly broad rewritten implementation rather than a tightly scoped patch plan.

Provisional `deepseek-v3.2` review:
- It correctly recognises `iterrows()` as the main large-data bottleneck and offers a valid minimal patch alternative using vectorised conversion and aggregation.
- The broader revised implementation is technically plausible, but it adds a lot of new surface area: logging, multiple helper functions, new stats, configurable grouping, and a separate reporting layer.
- That makes the answer less proportionate than ideal for a one-file review task, even though the core performance/correctness instincts are good.

Provisional `gemma4:31b-cloud` review:
- Correctly targeted `iterrows()` as the main scaling problem and moved the calculation to vectorised numeric conversion and aggregation.
- It keeps the existing status vocabulary intact, which helps change safety.
- Main deductions are for mutating the input `df` in place and still pushing toward a larger revised implementation rather than the smallest patch plan.

## Winner

- Winner: `kimi-k2-thinking`
- Difference size: `Small`
- Why it matters in practice: `All six recognised the vectorisation need, but kimi still best balanced performance improvement with a stable output contract.`
