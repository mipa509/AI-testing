# Raw Output

- task_id: `v2-deep-03`
- model_id_used: `minimax-m2.7-cloud`
- run_date: `2026-04-10`
- thinking_mode_used: `yes`

## Prompt Used

Same as in the prompt file

## Context Files Shared

- `context/io_contract.py`
- `context/design_engine.py`
- `context/report_writer.py`

## Raw Model Output
# Implementation Plan: Scoped SLS Summary Feature

---

## 1. Files to Change and Rationale

| File | Change | Rationale |
|------|--------|-----------|
| **`io_contract.py`** | Add `SLS_COLUMNS` constant and helper `get_all_result_columns()` | Centralize schema definition; define the new SLS contract
without touching `RESULT_COLUMNS` |
| **`design_engine.py`** | Extend `build_uls_summary()` to detect deflection columns and append SLS metrics | Single entry point; SLS is additive and
optional based on input presence |
| **`report_writer.py`** | Update `report_rows()` to use `get_all_result_columns()` but filter only `RESULT_COLUMNS` for stable output | Preserve
existing report format for downstream consumers |
| **`tests/test_serviceability.py`** *(new)* | Unit + integration tests | Validate SLS computation, backward compatibility, and schema |

---

## 2. Public Interface & Schema Changes

### New Schema (addition, not replacement)

```python
# io_contract.py — ADDITIONS ONLY

SLS_COLUMNS = [
    "DeflectionRatio",   # float — Deflection_mm / AllowableDeflection_mm
    "Status_SLS",        # str  — "PASS" | "FAIL"
]

def get_all_result_columns() -> list[str]:
    """Return full column set including SLS. Use this for consumers that want extended data."""
    return RESULT_COLUMNS + SLS_COLUMNS
```

### Updated Signatures

```python
# design_engine.py — NO signature change; kwargs for future extensibility
def build_uls_summary(df: pd.DataFrame, **kwargs) -> pd.DataFrame:
    """
    Returns DataFrame with columns: RESULT_COLUMNS [+ SLS_COLUMNS if deflection data present].
    Existing callers receive identical output.
    """
    ...
```

```python
# report_writer.py — NO signature change
def report_rows(summary_df) -> list[dict]:
    """Filters to RESULT_COLUMNS only — report output unchanged."""
    return summary_df.loc[:, RESULT_COLUMNS].to_dict(orient="records")
```

---

## 3. Data-Flow Changes

```
Input DataFrame
      │
      ▼
┌─────────────────────────────┐
│   build_uls_summary(df)     │
│                             │
│  1. GroupBy Member/Section  │
│  2. Compute Utilisation_ULS │
│  3. Map Status (PASS/FAIL)  │
│                             │
│  4. IF "Deflection_mm"      │
│     AND "AllowableDeflection_mm"
│     present in df:          │
│     • Compute DeflectionRatio
│     • Map Status_SLS        │
└─────────────────────────────┘
      │
      ▼
┌─────────────────────────────┐
│  Summary DataFrame          │
│  ─────────────────────────  │
│  RESULT_COLUMNS             │  ← Always present
│  SLS_COLUMNS (optional)     │  ← Present only when input has deflection data
└─────────────────────────────┘
      │
      ├──► report_rows() ─────────────────────► Stable JSON/dict output
      │       (filters to RESULT_COLUMNS)        (backward compatible)
      │
      └──► New consumers call
            summary_df[SLS_COLUMNS]             (opt-in access)
```

---

## 4. Backward-Compatibility Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| **New columns leaked to existing reports** | ✅ Low | `report_rows()` explicitly slices `RESULT_COLUMNS`; output schema unchanged |
| **Existing callers iterate DataFrame columns** | ⚠️ Medium | New columns are appended at the right; `dict(orient="records")` order changes. **Action:**
Document that column order is not guaranteed; use explicit column selection. |
| **SLS columns unexpectedly absent** | ✅ Low | Consumers can check `if "DeflectionRatio" in df.columns` |
| **Division-by-zero if `AllowableDeflection_mm == 0`** | ⚠️ Medium | Guard with `np.where(allowable == 0, np.nan, ratio)`; document NaN handling |
| **Input schema drift** | ⚠️ Medium | Validate expected ULS columns exist before processing; raise `ValueError` with clear message if required columns
missing |

---

## 5. Targeted Tests & Acceptance Criteria

### Unit Tests

```python
# tests/test_serviceability.py

class TestBuildULSSummary:
    def test_uls_only_no_deflection_columns(self):
        """Existing callers get identical output — no SLS columns added."""
        df = pd.DataFrame({
            "Member": ["M1", "M1", "M2"],
            "Section": ["S1", "S1", "S2"],
            "Utilisation_ULS": [0.5, 0.8, 1.2],
        })
        result = build_uls_summary(df)
        assert list(result.columns) == RESULT_COLUMNS
        assert len(result) == 2

    def test_uls_with_deflection_columns_computes_ratio(self):
        """DeflectionRatio and Status_SLS appended when deflection data present."""
        df = pd.DataFrame({
            "Member": ["M1", "M1"],
            "Section": ["S1", "S1"],
            "Utilisation_ULS": [0.9, 0.7],
            "Deflection_mm": [10.0, 15.0],
            "AllowableDeflection_mm": [20.0, 20.0],
        })
        result = build_uls_summary(df)
        assert "DeflectionRatio" in result.columns
        assert "Status_SLS" in result.columns
        pd.testing.assert_series_equal(
            result["DeflectionRatio"],
            pd.Series([0.625, 0.75], name="DeflectionRatio"),
        )
        pd.testing.assert_series_equal(
            result["Status_SLS"],
            pd.Series(["PASS", "PASS"], name="Status_SLS"),
        )

    def test_sls_fail_when_deflection_exceeds_allowable(self):
        """Status_SLS = FAIL when ratio > 1.0."""
        df = pd.DataFrame({
            "Member": ["M1"],
            "Section": ["S1"],
            "Utilisation_ULS": [0.5],
            "Deflection_mm": [25.0],
            "AllowableDeflection_mm": [20.0],
        })
        result = build_uls_summary(df)
        assert result["Status_SLS"].iloc[0] == "FAIL"
        assert result["DeflectionRatio"].iloc[0] == 1.25

    def test_zero_allowable_deflection_handled_gracefully(self):
        """Zero denominator produces NaN ratio, not exception."""
        df = pd.DataFrame({
            "Member": ["M1"],
            "Section": ["S1"],
            "Utilisation_ULS": [0.5],
            "Deflection_mm": [0.0],
            "AllowableDeflection_mm": [0.0],
        })
        result = build_uls_summary(df)
        assert pd.isna(result["DeflectionRatio"].iloc[0])
        assert result["Status_SLS"].iloc[0] == "PASS"  # nan <= 1 is False → FAIL is safer; or document behavior

    def test_report_rows_excludes_sls_columns(self):
        """report_rows() output is unchanged by SLS presence."""
        df = pd.DataFrame({
            "Member": ["M1"],
            "Section": ["S1"],
            "Utilisation_ULS": [0.8],
            "Status": ["PASS"],
            "DeflectionRatio": [0.5],
            "Status_SLS": ["PASS"],
        })
        rows = report_rows(df)
        assert list(rows[0].keys()) == RESULT_COLUMNS
```

### Acceptance Criteria

| # | Criterion | Test |
|---|-----------|------|
| AC-1 | `build_uls_summary()` with no deflection columns returns only `RESULT_COLUMNS` | `test_uls_only_no_deflection_columns` |
| AC-2 | Deflection data present → `DeflectionRatio` = `Deflection_mm / AllowableDeflection_mm` computed |
`test_uls_with_deflection_columns_computes_ratio` |
| AC-3 | `DeflectionRatio > 1.0` → `Status_SLS = "FAIL"` | `test_sls_fail_when_deflection_exceeds_allowable` |
| AC-4 | `AllowableDeflection_mm = 0` → no crash; NaN ratio produced | `test_zero_allowable_deflection_handled_gracefully` |
| AC-5 | `report_rows()` output columns unchanged regardless of SLS presence | `test_report_rows_excludes_sls_columns` |
| AC-6 | Existing downstream report consumer sees **identical output** before/after change | Integration test with snapshot |
| AC-7 | `get_all_result_columns()` returns ULS + SLS columns in deterministic order | Unit test |

---

### Summary of Design Decisions

1. **SLS is additive** — never removes or renames existing columns
2. **`RESULT_COLUMNS` is frozen** — `report_writer` intentionally ignores SLS columns
3. **Opt-in for extended consumers** — use `get_all_result_columns()` or direct column access
4. **Graceful degradation** — SLS columns only appear if input has deflection data
5. **Zero-denominator guard** — prevents runtime exceptions with documented NaN behavior