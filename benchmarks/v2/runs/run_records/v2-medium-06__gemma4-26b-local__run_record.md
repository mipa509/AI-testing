# Run Record

- `task_id`: `v2-medium-06`
- `task_title`: `Review plus targeted test design`
- `model_id_used`: `gemma4:26b-local`
- `run_date`: `2026-09-19`
- `thinking_mode_used`: `yes (hidden; the generated-token counts include it)`
- `prompt_version`: `tasks/medium_06_review_plus_tests/prompt.md`
- `context_files_shared`: `context/foundation_settlement.py` (pasted as `context_combined.md`)
- `raw_output_path`: `runs/raw_outputs/v2-medium-06__gemma4-26b-local__raw.md`
- `run_route`: `ollama run gemma4:26b --verbose` in a PowerShell terminal on the user's machine (local weights, no harness, tools, skills or web access)
- `rate_limit_or_refusal_notes`: none; no refusal or truncation
- `latency_notes`: `4 min 21 s` for the answer after the context message (eval 2687 tokens at 10.38 tokens/s) plus `36.4 s` for the prompt-only reply (eval 424 tokens); from `ollama --verbose`. Hardware: Intel Core i7-9700K, 64 GB RAM, RTX 2070 SUPER 8 GB; llama-server held about 4 GB and about 50 percent CPU while generating, so the 26B weights run mostly on CPU with partial GPU offload, which is consistent with the 8 to 12 tokens per second observed.
- `token_usage_or_cost`: generated 2687 tokens for the answer (hidden thinking included) and 424 for the prompt-only reply; prompt eval 449 tokens on the context message (133 cached) and 138 on the prompt; free local inference, no API cost. Not comparable with the harness token totals of the other routes, so not charted.
- `manual_observations`: First reply listed its review criteria and asked for the code; it waited for the pasted context. Free local model on consumer hardware; the two-message protocol was followed.

## First-Pass Output Summary

Three findings: `settlement_ratio` returning `0.0` for a zero allowable (a false PASS, called critical), `differential_slope` dividing the max-min difference by a single spacing regardless of the number of points, and no guard on zero spacing. Minimum fixes: return `inf` for a zero allowable, guard short lists and non-positive spacing (returning `0.0`), keep the strict `< 1.0` status. A four-row test table (zero allowable, zero spacing, a three-point sequence, the ratio-equals-1.0 boundary) and a units note (mm, m, mm/m).

## Operational Notes

- Did the model appear to understand the codebase shape? Yes; it cites the supplied files and functions.
- Did it truncate, refuse, or drift? No.
- Did it require a larger-than-expected amount of context steering? No.
- Did it start answering before the context files were supplied? No; it waited for the context message.
