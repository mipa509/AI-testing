# Run Record

- `task_id`: `v2-deep-03`
- `task_title`: `Scoped feature design on an existing package`
- `model_id_used`: `gemma4:26b-local`
- `run_date`: `2026-09-19`
- `thinking_mode_used`: `yes (hidden; the generated-token counts include it)`
- `prompt_version`: `tasks/deep_03_scoped_feature_design/prompt.md`
- `context_files_shared`: `context/design_engine.py`, `context/io_contract.py`, `context/report_writer.py` (pasted as `context_combined.md`)
- `raw_output_path`: `runs/raw_outputs/v2-deep-03__gemma4-26b-local__raw.md`
- `run_route`: `ollama run gemma4:26b --verbose` in a PowerShell terminal on the user's machine (local weights, no harness, tools, skills or web access)
- `rate_limit_or_refusal_notes`: none; no refusal or truncation
- `latency_notes`: `5 min 31 s` for the answer after the context message (eval 2995 tokens at 9.09 tokens/s) plus `31.3 s` for the prompt-only reply (eval 333 tokens); from `ollama --verbose`. Hardware: Intel Core i7-9700K, 64 GB RAM, RTX 2070 SUPER 8 GB; llama-server held about 4 GB and about 50 percent CPU while generating, so the 26B weights run mostly on CPU with partial GPU offload, which is consistent with the 8 to 12 tokens per second observed.
- `token_usage_or_cost`: generated 2995 tokens for the answer (hidden thinking included) and 333 for the prompt-only reply; prompt eval 566 tokens on the context message (224 cached) and 229 on the prompt; free local inference, no API cost. Not comparable with the harness token totals of the other routes, so not charted.
- `manual_observations`: First reply said it would deliver the five requested sections once the files were provided; it waited for the pasted context. Free local model on consumer hardware; the two-message protocol was followed.

## First-Pass Output Summary

Five-section plan: three files to change (engine, io contract, report writer); new constants `SLS_COLUMNS` and `EXTENDED_RESULT_COLUMNS` and an optional `columns` parameter on `report_rows` defaulting to `RESULT_COLUMNS`; an SLS summary built only when the deflection columns are present and left-merged onto the ULS summary on `["Member", "Section"]`; risks (downstream keys, merge NaNs, missing columns) each with a mitigation; four tests and four acceptance criteria. The new function is named `build_slli_summary` in one place and `build_sls_summary` elsewhere.

## Operational Notes

- Did the model appear to understand the codebase shape? Yes; it cites the supplied files and functions.
- Did it truncate, refuse, or drift? No.
- Did it require a larger-than-expected amount of context steering? No.
- Did it start answering before the context files were supplied? No; it waited for the context message.
