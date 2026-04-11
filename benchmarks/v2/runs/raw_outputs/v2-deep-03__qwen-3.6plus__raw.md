# Raw Output

- task_id: `v2-deep-03`
- model_id_used: `qwen-3.6plus`
- run_date: `2026-04-10`
- thinking_mode_used: `yes`

## Prompt Used

Same as in the prompt file

## Context Files Shared

- `context/io_contract.py`
- `context/design_engine.py`
- `context/report_writer.py`

## Raw Model Output
# Task 3 — Scoped Feature Design: Optional Serviceability Summary

## 1. Files to Change and Why

### `context/io_contract.py`
**Why:** This file defines the canonical column contract (`RESULT_COLUMNS`) that flows between the engine and the report writer. It needs to be extended to include serviceability columns so downstream consumers can optionally access them.

**Changes:**
- Add a new constant `SLS_COLUMNS` listing the serviceability output columns.
- Optionally add a combined `ALL_RESULT_COLUMNS` for consumers that want both ULS and SLS.

### `context/design_engine.py`
**Why:** This is where the aggregation logic lives. Currently it only computes ULS summaries. It needs a new function (or an optional parameter on the existing function) to compute serviceability metrics when deflection data is present.

**Changes:**
- Add a new function `build_sls_summary(df: pd.DataFrame) -> pd.DataFrame | None` that computes `DeflectionRatio` and returns `None` when deflection columns are absent.
- Alternatively, add an optional `include_sls: bool = False` parameter to `build_uls_summary` and return a combined DataFrame.

### `context/report_writer.py`
**Why:** The `report_rows` function currently projects only `RESULT_COLUMNS`. It must be able to include SLS columns when they are present, without breaking callers that only pass ULS data.

**Changes:**
- Make `report_rows` accept an optional `columns` parameter (defaulting to `RESULT_COLUMNS`) so callers can pass `SLS_COLUMNS` or a combined list.
- Add a helper `report_rows_combined(uls_df, sls_df)` that merges ULS and SLS records when both are present.

---

## 2. Public Interface / Schema Changes

### New Constants in `io_contract.py`
```python
SLS_COLUMNS = [
    "Member",
    "Section",
    "Deflection_mm",
    "AllowableDeflection_mm",
    "DeflectionRatio",
    "Status_SLS",
]
```

### New Function in `design_engine.py`
```python
def build_sls_summary(df: pd.DataFrame) -> pd.DataFrame | None:
    """
    Compute serviceability summary if deflection data is present.
    Returns None if required columns are missing.
    """
    required = {"Deflection_mm", "AllowableDeflection_mm"}
    if not required.issubset(df.columns):
        return None

    out = df.groupby(["Member", "Section"], as_index=False).agg(
        Deflection_mm=("Deflection_mm", "max"),
        AllowableDeflection_mm=("AllowableDeflection_mm", "first"),
    )
    out["DeflectionRatio"] = out["Deflection_mm"] / out["AllowableDeflection_mm"]
    out["Status_SLS"] = out["DeflectionRatio"].map(
        lambda ratio: "PASS" if ratio <= 1.0 else "FAIL"
    )
    return out
```

### Updated Function Signature in `report_writer.py`
```python
def report_rows(summary_df, columns=None):
    """
    Project summary DataFrame to record dicts.
    If columns is None, defaults to RESULT_COLUMNS (backward compatible).
    """
    cols = columns if columns is not None else RESULT_COLUMNS
    # Only include columns that actually exist in the DataFrame
    available = [c for c in cols if c in summary_df.columns]
    return summary_df.loc[:, available].to_dict(orient="records")
```

---

## 3. Data-Flow Changes (Input → Report)

### Current Flow
```
Input DataFrame
    → normalise_columns()
    → build_uls_summary()
    → report_rows(uls_df)  [projects RESULT_COLUMNS]
    → Downstream consumer
```

### New Flow (with SLS enabled)
```
Input DataFrame
    → normalise_columns()
    → build_uls_summary()        → uls_df
    → build_sls_summary()        → sls_df (or None)
    → if sls_df is not None:
          merged = uls_df.merge(sls_df, on=["Member", "Section"], how="left")
          report_rows(merged, columns=RESULT_COLUMNS + SLS_COLUMNS[2:])
      else:
          report_rows(uls_df)    [unchanged behavior]
    → Downstream consumer
```

**Key points:**
- SLS computation is **opt-in** — existing pipelines that don't call `build_sls_summary` are unaffected.
- When SLS data is absent, `build_sls_summary` returns `None` and the pipeline falls back to ULS-only output.
- The merge uses `how="left"` so members without SLS data still appear in the report with `NaN` for SLS columns.

---

## 4. Backward-Compatibility Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| **Downstream consumers expect exactly `RESULT_COLUMNS`** | High | `report_rows` defaults to `RESULT_COLUMNS` when no `columns` arg is passed. Existing callers are unchanged. |
| **`build_sls_summary` returns `None` and caller doesn't handle it** | Medium | Document the `None` return clearly. Provide a helper `has_sls_data(df)` for pre-checks. |
| **Division by zero if `AllowableDeflection_mm` is 0** | Medium | Add a guard: `out["AllowableDeflection_mm"].replace(0, pd.NA)` before division, or use `np.where`. |
| **Column name collisions if input already has `DeflectionRatio`** | Low | The function overwrites it via aggregation, but worth documenting. |
| **Schema drift if `SLS_COLUMNS` is extended later** | Low | Version the contract or use a dataclass/TypedDict for stronger typing in a future iteration. |

---

## 5. Targeted Tests and Acceptance Criteria

### Test Suite

| Test | Description | Acceptance Criteria |
|------|-------------|---------------------|
| `test_build_uls_summary_unchanged` | Verify ULS summary output is identical to current behavior | Same columns, same values, same `Status` logic |
| `test_build_sls_summary_with_data` | Pass DataFrame with deflection columns | Returns DataFrame with `DeflectionRatio` and `Status_SLS` |
| `test_build_sls_summary_without_data` | Pass DataFrame without deflection columns | Returns `None` |
| `test_build_sls_summary_zero_allowable` | `AllowableDeflection_mm` contains 0 | No `ZeroDivisionError`; ratio is `inf` or `NaN` with `FAIL` status |
| `test_report_rows_default_columns` | Call `report_rows(uls_df)` without `columns` arg | Returns only `RESULT_COLUMNS` |
| `test_report_rows_with_sls_columns` | Call `report_rows(merged_df, columns=RESULT_COLUMNS + SLS_COLUMNS[2:])` | Returns combined columns |
| `test_report_rows_missing_columns_graceful` | Request columns not in DataFrame | Silently omits missing columns, no `KeyError` |
| `test_end_to_end_uls_only` | Full pipeline with ULS-only input | Output matches current production behavior |
| `test_end_to_end_uls_and_sls` | Full pipeline with deflection data | Output contains both ULS and SLS columns |
| `test_backward_compat_existing_callers` | Simulate existing caller that only imports `RESULT_COLUMNS` and `build_uls_summary` | No import errors, no behavior change |

### Acceptance Criteria Summary
1. **Zero regressions** in existing ULS-only pipelines (all current tests pass).
2. **SLS is opt-in** — no new columns appear unless `build_sls_summary` is explicitly called.
3. **`DeflectionRatio`** is computed correctly as `Deflection_mm / AllowableDeflection_mm`.
4. **Graceful degradation** when deflection data is missing (returns `None`, pipeline continues with ULS only).
5. **No breaking changes** to `RESULT_COLUMNS` — it remains exactly as defined today.
6. **Report writer** handles missing columns gracefully without raising exceptions.

---

## Summary of Changes

| File | Change Type | Lines Changed (est.) |
|------|-------------|---------------------|
| `io_contract.py` | Add `SLS_COLUMNS` constant | +6 |
| `design_engine.py` | Add `build_sls_summary()` function | +18 |
| `report_writer.py` | Add optional `columns` parameter to `report_rows()` | +5 |
| **Tests** | New test file `test_serviceability.py` | ~120 |

**Total new code:** ~150 lines (including tests). No existing logic is modified — only additions and optional parameters.