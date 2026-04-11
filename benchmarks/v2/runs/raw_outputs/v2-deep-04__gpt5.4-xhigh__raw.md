# Raw Output

- task_id: `v2-deep-04`
- model_id_used: `gpt5.4-xhigh`
- run_date: `2026-04-11`
- thinking_mode_used: `yes`

## Prompt Used

Same as in the prompt file

## Context Files Shared

- `context/concrete_checks.py`
- `context/steel_checks.py`
- `context/common_formatting.py`

## Raw Model Output

1. The refactor is only safe in principle if it is narrowly scoped. A generic “shared utilisation helper” is unsafe if it normalises zero- or negative-denominator cases, because steel and concrete intentionally behave differently there.

2. Logic that may be shared:
- The numeric division path when denominator is valid: `ed / rd`.
- The status threshold formatter already in `format_status(util)` for real numeric utilisations.

Behaviour that must remain distinct:
- `concrete_utilisation(..., v_rd <= 0)` returns `None`.
- `concrete_status(..., v_rd <= 0)` returns exact text `"CHECK INPUT"`.
- `steel_utilisation(..., n_rd <= 0)` returns `0.0`.
- `steel_status(..., n_rd <= 0)` therefore returns `"PASS"` via `format_status(0.0)`.

That zero-denominator split is not an implementation detail; it is current behaviour. Changing it would silently change outputs, especially status text consumed by spreadsheets.

3. Minimal refactor approach:
- Extract only the positive-denominator division into a tiny shared helper, or extract a parameterised helper that accepts the invalid-case sentinel.
- Keep module-specific wrappers and status functions intact.

Example shape:

```py
def utilisation_or(ed, rd, invalid_value):
    if rd <= 0:
        return invalid_value
    return ed / rd
```

Then:
- concrete calls it with `invalid_value=None`
- steel calls it with `invalid_value=0.0`
- concrete keeps its explicit `"CHECK INPUT"` branch
- steel keeps routing straight through `format_status`

That is the safest deduplication boundary. Do not unify the status functions into one generic function unless it also preserves the exact concrete special case.

4. Tests and regression checks needed before merge:
- `concrete_utilisation(10, 0)` returns `None`
- `concrete_utilisation(10, -1)` returns `None`
- `steel_utilisation(10, 0)` returns `0.0`
- `steel_utilisation(10, -1)` returns `0.0`
- `concrete_status(10, 0)` returns exact `"CHECK INPUT"`
- `steel_status(10, 0)` returns exact `"PASS"`
- Threshold checks: utilisation `1.0 -> "PASS"`, `> 1.0 -> "FAIL"` in both modules for valid denominators
- Exact string regression checks for all exported status text, because downstream spreadsheets depend on those literals

Bottom line: a small refactor is acceptable, but only if it preserves the existing zero-denominator semantics and exact status strings. Any refactor that makes concrete and steel share the same invalid-input behaviour should be rejected.