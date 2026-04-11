# Raw Output

- task_id: `v2-deep-03`
- model_id_used: `kimi-k2-thinking`
- run_date: `2026-04-09`
- thinking_mode_used: `yes`

## Prompt Used

Same as in the prompt file

## Context Files Shared

All files from context folder

## Raw Model Output
----------------------------------------------------------------------------------------------
Here is a decision-complete implementation plan for adding optional serviceability summaries to the structural
design package.

---

### 1. Files to Change and Why

**`io_contract.py`**
- Add constants for deflection input columns, computed serviceability columns, and extended result columns.
- **Why**: Centralizes column name definitions, maintains backward compatibility of `RESULT_COLUMNS`, and provides
a clear contract for extended outputs.

**`design_engine.py`**
- Modify `build_uls_summary()` to accept `include_serviceability: bool = False`.
- **Why**: Enables optional deflection ratio computation while preserving existing ULS-only behavior. The function
becomes the single entry point for both legacy and extended summaries.

**`report_writer.py`**
- Modify `report_rows()` to accept `include_serviceability: bool = False`.
- **Why**: Guarantees stable ULS-only output for existing downstream consumers while allowing new callers to
retrieve extended serviceability data.

---

### 2. Public Interface or Schema Changes

**New Constants in `io_contract.py`:**
```python
DEFLECTION_ACTUAL_COL = "Deflection_mm"
DEFLECTION_ALLOWABLE_COL = "AllowableDeflection_mm"
DEFLECTION_RATIO_COL = "DeflectionRatio"
SERVICEABILITY_STATUS_COL = "ServiceabilityStatus"

EXTENDED_RESULT_COLUMNS = RESULT_COLUMNS + [
    DEFLECTION_RATIO_COL,
    SERVICEABILITY_STATUS_COL,
]
```

**Modified Function Signatures:**
```python
# design_engine.py
def build_uls_summary(df: pd.DataFrame, include_serviceability: bool = False) -> pd.DataFrame:
    # Returns DataFrame with columns per RESULT_COLUMNS or EXTENDED_RESULT_COLUMNS

# report_writer.py
def report_rows(summary_df, include_serviceability: bool = False):
    # Returns List[Dict] with keys from RESULT_COLUMNS or EXTENDED_RESULT_COLUMNS
```

**Schema Extension (when enabled):**
- `DeflectionRatio`: Float, computed as `Deflection_mm / AllowableDeflection_mm`
- `ServiceabilityStatus`: String enum `"PASS"` / `"FAIL"` / `None`

---

### 3. Data-Flow Changes

```
Input DataFrame
    ├── Required: ["Member", "Section", "Utilisation_ULS"]
    └── Optional: ["Deflection_mm", "AllowableDeflection_mm"]
            │
            ▼
build_uls_summary(df, include_serviceability=False/True)
            │
            ├── ULS Path (unchanged)
            │   ├── Groupby ["Member", "Section"]
            │   ├── Agg max("Utilisation_ULS")
            │   └── Map "Status" (PASS if ≤1.0)
            │
            └── Serviceability Path (NEW, when enabled)
                ├── Verify deflection columns exist
                ├── Compute "DeflectionRatio" (handles zero allowable → inf)
                ├── Groupby ["Member", "Section"], agg max("DeflectionRatio")
                ├── Map "ServiceabilityStatus" (PASS if ≤1.0, else FAIL, None if NaN)
                └── Left-merge with ULS summary on ["Member", "Section"]
            │
            ▼
summary_df (columns per mode)
            │
            ▼
report_rows(summary_df, include_serviceability=False/True)
            │
            ├── False: Filter to RESULT_COLUMNS only
            └── True: Validate EXTENDED_RESULT_COLUMNS present, then filter
            │
            ▼
Dict records (stable schema for existing consumers, extended for new)
```

---

### 4. Backward-Compatibility Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| **Function signature change** | Low | Default parameter `include_serviceability=False` preserves call semantics.
|
| **Output schema mutation** | None | Existing consumers receive identical ULS-only output; extended schema
requires explicit opt-in. |
| **Column name collision** | Medium | Document `DeflectionRatio` and `ServiceabilityStatus` as reserved. If
`include_serviceability=True` and these columns pre-exist in input, raise `ValueError` to prevent silent
overwrites. |
| **Performance regression** | Low | Serviceability calculations execute only when enabled; ULS path unchanged. |
| **Input schema assumption** | Low | Deflection columns are optional; missing columns result in NaN/None output
without error. |

---

### 5. Targeted Tests and Acceptance Criteria

**Test 1: Backward Compatibility**
- **Input**: DataFrame with only `Member`, `Section`, `Utilisation_ULS`.
- **Action**: Call `build_uls_summary(df)` and `report_rows(summary_df)` (no flags).
- **Acceptance**: Output DataFrame and dict records match pre-feature format exactly (column order, values,
types).

**Test 2: Full Serviceability Calculation**
- **Input**: DataFrame with ULS and deflection columns, multiple rows per Member/Section, mixed PASS/FAIL ratios.
- **Action**: Call `build_uls_summary(df, include_serviceability=True)`.
- **Acceptance**:
  - `DeflectionRatio` = `Deflection_mm / AllowableDeflection_mm` (max per group).
  - `ServiceabilityStatus` = `"PASS"` if ratio ≤ 1.0, else `"FAIL"`.
  - All `EXTENDED_RESULT_COLUMNS` present; no extraneous columns.

**Test 3: Missing Deflection Data**
- **Input**: DataFrame without deflection columns.
- **Action**: Call `build_uls_summary(df, include_serviceability=True)`.
- **Acceptance**: Extended columns present, filled with `NaN` (ratio) and `None` (status); no exceptions.

**Test 4: Zero Allowable Deflection Edge Case**
- **Input**: DataFrame where `AllowableDeflection_mm = 0` for some rows.
- **Action**: Call `build_uls_summary(df, include_serviceability=True)`.
- **Acceptance**: `DeflectionRatio` = `inf` for those rows; `ServiceabilityStatus` = `"FAIL"`.

**Test 5: Report Writer Column Filtering**
- **Input**: Summary DataFrame with extended columns.
- **Action**: Call `report_rows(df, include_serviceability=False)` and `report_rows(df,
include_serviceability=True)`.
- **Acceptance**:
  - `False`: dict keys exactly match `RESULT_COLUMNS`.
  - `True`: dict keys exactly match `EXTENDED_RESULT_COLUMNS`.
  - Values are unmodified from input DataFrame.

**Test 6: NaN Handling**
- **Input**: DataFrame with `NaN` deflection values.
- **Action**: Call `build_uls_summary(df, include_serviceability=True)`.
- **Acceptance**: `DeflectionRatio` is `NaN`; `ServiceabilityStatus` is `None`.

**Test 7: Reserved Column Collision**
- **Input**: DataFrame containing pre-existing `DeflectionRatio` column.
- **Action**: Call `build_uls_summary(df, include_serviceability=True)`.
- **Acceptance**: Raises `ValueError` with clear message; prevents data corruption.

---

**Implementation Note**: Use `df.copy()` internally to avoid mutating input DataFrames, and `pandas.isna()` for
robust null checks. Log a warning when serviceability is requested but deflection columns are absent.