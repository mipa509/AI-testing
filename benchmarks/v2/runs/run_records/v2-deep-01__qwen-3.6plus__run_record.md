# Run Record Template

- `task_id`: `v2-deep-01`
- `task_title`: `Multi-file bug hunt in a member check pipeline`
- `model_id_used`: `qwen-3.6plus`
- `run_date`: `2026-04-10`
- `thinking_mode_used`: `not sure`
- `prompt_version`: `tasks/deep_01_multifile_bug_hunt/prompt.md`
- `context_files_shared`:
- `context/analysis_pipeline.py`
- `context/section_library.py`
- `context/reporting.py`
- `raw_output_path`: `runs/raw_outputs/v2-deep-01__qwen-3.6plus__raw.md`
- `rate_limit_or_refusal_notes`:
- `latency_notes`:
- `manual_observations`:

## First-Pass Output Summary

Qwen3.6-plus is available via OpenRouter only not Ollama. I am using VS Code chat to run it with API call to OpenRouter. I am not sure whether VS code applies any sort of edits/instructions as the harness on top of the bare model but obviously the rpesentation is going to be visually better as it exists in the chat window here which has formatting etc. I can't unfortunately run it in terminal i dont think. Qwen 3.6 seems very cheap though but i will check actual pricing later.

## Operational Notes

- Did the model appear to understand the codebase shape?
- Did it truncate, refuse, or drift?
- Did it require a larger-than-expected amount of context steering?
