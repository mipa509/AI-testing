# Raw Output

- task_id: `v2-deep-03`
- model_id_used: `qwen-3.8-27b-high`
- api_model: `qwen/qwen3.8-27b` (OpenRouter), reasoning effort high
- reasoning_effort: `high`
- run_route: `GitHub Copilot agent chat in VS Code via OpenRouter (qwen/qwen3.8-27b, reasoning effort high), fresh chat per task, local sandbox folder with one subfolder per task holding only its inputs; no evaluator or reference files`
- run_date: `2026-09-26`
- thinking_mode_used: `yes (reasoning effort high)`

## Prompt Used

Same as in the prompt file (`tasks/deep_03_scoped_feature_design/prompt.md`), with `context_combined.md` in the task folder. The deliverable is `response.md` in that folder.

## Raw Model Output

# Task 3 Response — Scoped Feature Design: Optional Serviceability Summary

## 0. Summary of the change

Add an **optional** serviceability (SLS) summary computed from deflection data, alongside the existing ULS summary. The feature is strictly additive:

- `build_uls_summary` is **not modified**.
- `RESULT_COLUMNS` is **not modified** (report output for existing consumers is byte-for-byte stable).
- New code is opt-in: SLS is computed only when deflection columns are present in the input, and SLS columns appear in report output only when explicitly requested.

---

## 1. Files to change and why

### 1.1 `context/design_engine.py` — **modify (additive)**

**Why:** This is where summaries are derived from the raw results frame. The SLS summary belongs here, next to the ULS one.

Changes:

- **Add** `build_serviceability_summary(df: pd.DataFrame) -> pd.DataFrame`:
  - Precondition: `df` contains `Deflection_mm` and `AllowableDeflection_mm` columns.
  - Compute `DeflectionRatio = Deflection_mm / AllowableDeflection_mm` row-wise.
  - Aggregate per `["Member", "Section"]` with `max` of `DeflectionRatio` (mirrors the ULS convention of taking the governing/max utilisation).
  - Add `Status_SLS = "PASS" if ratio <= 1.0 else "FAIL"`.
  - Edge handling:
    - `AllowableDeflection_mm == 0` → `DeflectionRatio = inf` (FAIL), never raise.
    - `AllowableDeflection_mm` is `NaN` → `DeflectionRatio = NaN`, `Status_SLS = "N/A"`.
    - `Deflection_mm` is `NaN` → `DeflectionRatio = NaN`, `Status_SLS = "N/A"`.
- **Add** a helper `has_deflection_data(df) -> bool` returning `True` only if both `Deflection_mm` and `AllowableDeflection_mm` are present (after `normalise_columns`).
- **Add** `build_combined_summary(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame | None]` (or a small dataclass `DesignSummary(uls: DataFrame, sls: DataFrame | None)`):
  - Always calls `build_uls_summary(df)` (unchanged behaviour).
  - Calls `build_serviceability_summary(df)` only if `has_deflection_data(df)` is true; otherwise `sls=None`.
  - This is the new recommended entry point; existing callers of `build_uls_summary` keep working untouched.

**Not changed:** `build_uls_summary` — zero edits, so any existing caller importing it is unaffected.

### 1.2 `context/io_contract.py` — **modify (additive)**

**Why:** This module is the single source of truth for column names; the new SLS columns must be declared here, not hardcoded in the engine or writer.

Changes:

- **Add** constants:
  ```py
  DEFLECTION_INPUT_COLUMNS = ["Deflection_mm", "AllowableDeflection_mm"]

  SERVICEABILITY_COLUMNS = [
      "Member",
      "Section",
      "DeflectionRatio",
      "Status_SLS",
  ]
  ```
- **Do NOT modify** `RESULT_COLUMNS`. It stays `["Member", "Section", "Utilisation_ULS", "Status"]`.
- **Add** (optional convenience) `COMBINED_COLUMNS = RESULT_COLUMNS + ["DeflectionRatio", "Status_SLS"]` for the opt-in combined report. SLS columns are always **appended after** ULS columns so existing column positions are preserved.
- **Do NOT modify** `normalise_columns`.

### 1.3 `context/report_writer.py` — **modify (additive, backward-compatible signature)**

**Why:** This is the last gate before downstream consumers; it must keep emitting exactly `RESULT_COLUMNS` by default.

Changes:

- **Modify** `report_rows` with a keyword-only opt-in flag (default preserves current behaviour):
  ```py
  def report_rows(summary_df, include_serviceability: bool = False):
      if include_serviceability:
          cols = COMBINED_COLUMNS
      else:
          cols = RESULT_COLUMNS
      return summary_df.loc[:, cols].to_dict(orient="records")
  ```
  - When `include_serviceability=False` (default), output is identical to today for any input, including inputs that carry deflection data.
  - When `True`, the caller must pass the combined/merged summary frame; missing SLS columns raise a clear `KeyError` (or we guard with an explicit `ValueError("serviceability data not present")` — recommended, friendlier for downstream).
- **Add** `report_rows_combined(uls_df, sls_df) -> list[dict]`:
  - Merges `uls_df` and `sls_df` on `["Member", "Section"]` (left join, so ULS-only members still appear with `NaN`/`"N/A"` SLS fields).
  - Returns records in `COMBINED_COLUMNS` order.
  - This is a **new** function, so it cannot break anything existing.

### 1.4 No other files

No changes to callers, tests, or packaging are required for the feature itself (tests are new files, see §5).

---

## 2. Public interface / schema changes

| Item | Kind | Breaking? |
|---|---|---|
| `design_engine.build_serviceability_summary(df)` | New public function | No |
| `design_engine.has_deflection_data(df)` | New public function | No |
| `design_engine.build_combined_summary(df)` | New public function (recommended entry point) | No |
| `io_contract.DEFLECTION_INPUT_COLUMNS` | New constant | No |
| `io_contract.SERVICEABILITY_COLUMNS` | New constant | No |
| `io_contract.COMBINED_COLUMNS` | New constant | No |
| `report_writer.report_rows(summary_df, include_serviceability=False)` | New keyword-only param, default `False` | No (default path unchanged) |
| `report_writer.report_rows_combined(uls_df, sls_df)` | New public function | No |
| `RESULT_COLUMNS` | **Unchanged** | — |
| `build_uls_summary` | **Unchanged** | — |

**Output schema (opt-in combined report), per record:**

```
Member, Section, Utilisation_ULS, Status, DeflectionRatio, Status_SLS
```

- ULS fields keep their exact names, order, and semantics.
- `DeflectionRatio`: float, `inf` when allowable is 0, `NaN` when data missing.
- `Status_SLS`: `"PASS" | "FAIL" | "N/A"`.

**Input schema (new, optional):** input frame may now carry `Deflection_mm` and `AllowableDeflection_mm` (numeric, per row, same grain as ULS rows). Both must be present for SLS to activate; one present and the other missing → treated as "no deflection data" (log a warning, do not fail).

---

## 3. Data-flow changes (input → report)

```
raw input df
   │
   ▼
normalise_columns(df)                      [unchanged]
   │
   ├──► build_uls_summary(df)               [unchanged]
   │        │
   │        ▼
   │   ULS summary: Member, Section, Utilisation_ULS, Status
   │
   └──► has_deflection_data(df)?            [new gate]
            │ yes
            ▼
        build_serviceability_summary(df)    [new]
            │  DeflectionRatio = Deflection_mm / AllowableDeflection_mm
            │  groupby(Member, Section).max
            ▼
        SLS summary: Member, Section, DeflectionRatio, Status_SLS

   ▼
report path:
   • existing callers:  report_rows(uls_summary)            → RESULT_COLUMNS only  [unchanged]
   • new callers:       report_rows_combined(uls, sls)      → COMBINED_COLUMNS
                        (or report_rows(merged, include_serviceability=True))
```

Key properties:

- The ULS branch is a straight line through unchanged code — no behavioural drift possible.
- SLS is a side branch gated on data presence; its absence changes nothing downstream.
- The merge for combined output is a **left join on (Member, Section)** so ULS rows are never dropped; members without deflection data get `NaN`/`"N/A"` SLS fields.

---

## 4. Backward-compatibility risks

| # | Risk | Likelihood | Mitigation |
|---|---|---|---|
| 1 | Downstream consumer iterates *all* columns of the summary/report and chokes on new columns | Medium | Default `report_rows` still selects exactly `RESULT_COLUMNS`; SLS columns only appear via the explicit opt-in. ULS summary DataFrame itself is never augmented. |
| 2 | Consumer compares report output by exact dict equality (golden files) | Medium | Default path is byte-identical; covered by a golden test (§5). |
| 3 | `report_rows` signature change breaks positional-arg callers | Low | New param is keyword-only with default `False`; positional calls `report_rows(df)` are unaffected. |
| 4 | Input frames that already contain a column named `DeflectionRatio` or `Status_SLS` collide | Low | Document that SLS output columns are owned by the package; engine overwrites them deterministically. |
| 5 | Deflection data at a different grain than ULS (e.g., per-load-case vs per-member) causes silent mis-merge | Medium | `groupby(["Member","Section"]).max` mirrors ULS aggregation; document the expected grain; add a test with multi-row members. |
| 6 | `AllowableDeflection_mm = 0` or `NaN` in production data | Medium | Explicit edge handling: `inf`/FAIL for zero, `NaN`/`"N/A"` for NaN; no exceptions raised. |
| 7 | One deflection column present, the other missing (partial data) | Medium | `has_deflection_data` requires **both**; partial data → SLS skipped with a warning, ULS unaffected. |
| 8 | `import pandas` cost / new dependency | None | pandas already a dependency. |

**Explicit non-goals (to keep scope tight):** no SLS checks other than deflection (vibration, crack width), no new CLI flags, no persistence/schema migration, no change to ULS status logic.

---

## 5. Targeted tests and acceptance criteria

### 5.1 Unit tests — `design_engine`

| Test | Input | Expected |
|---|---|---|
| `test_uls_summary_unchanged` | ULS-only frame (fixture from existing suite) | Output identical to pre-change golden output (regression guard). |
| `test_sls_ratio_computed` | 1 member, `Deflection_mm=12.0`, `AllowableDeflection_mm=24.0` | `DeflectionRatio == 0.5`, `Status_SLS == "PASS"`. |
| `test_sls_fail` | ratio `1.25` | `Status_SLS == "FAIL"`. |
| `test_sls_boundary` | ratio exactly `1.0` | `Status_SLS == "PASS"` (consistent with ULS `<= 1.0` convention). |
| `test_sls_max_per_member` | 2 rows same Member/Section, ratios 0.4 and 0.9 | Single row, ratio `0.9`. |
| `test_sls_zero_allowable` | `AllowableDeflection_mm=0` | ratio `inf`, `Status_SLS == "FAIL"`, no exception. |
| `test_sls_nan_allowable` | `AllowableDeflection_mm=NaN` | ratio `NaN`, `Status_SLS == "N/A"`. |
| `test_has_deflection_data` | (a) both cols, (b) one col, (c) none | `True / False / False`. |
| `test_combined_summary_no_deflection` | ULS-only frame | `sls is None`, `uls` identical to `build_uls_summary` output. |
| `test_combined_summary_with_deflection` | full frame | both summaries returned, correct shapes. |

### 5.2 Unit tests — `report_writer`

| Test | Input | Expected |
|---|---|---|
| `test_report_rows_default_stable` | ULS summary (with and without deflection data in source) | Records contain **exactly** `RESULT_COLUMNS`, values unchanged (golden comparison). |
| `test_report_rows_opt_in` | merged frame, `include_serviceability=True` | Records contain `COMBINED_COLUMNS` in order; ULS fields first. |
| `test_report_rows_opt_in_without_sls` | ULS-only frame, `include_serviceability=True` | Raises `ValueError` with clear message (no silent partial output). |
| `test_report_rows_combined_left_join` | ULS has member A+B, SLS has member A only | 2 records; B has `NaN`/`"N/A"` SLS fields; no rows dropped. |

### 5.3 Integration / contract tests

| Test | Expected |
|---|---|
| `test_end_to_end_uls_only` | Raw ULS frame → `build_combined_summary` → `report_rows` default → output equals pre-feature golden file. |
| `test_end_to_end_with_deflection` | Raw frame with deflection → combined report → 6 columns, correct values, ULS columns byte-identical to ULS-only run. |
| `test_whitespace_columns` | Input with `" Deflection_mm "` etc. → `normalise_columns` path works, SLS activates. |

### 5.4 Acceptance criteria (definition of done)

1. **AC-1 (ULS stability):** All pre-existing tests pass unmodified; the golden report for a ULS-only run is byte-identical before and after the change.
2. **AC-2 (opt-in SLS):** With deflection data present, `report_rows_combined` emits `DeflectionRatio` and `Status_SLS` with correct values for PASS/FAIL/boundary/zero/NaN cases.
3. **AC-3 (graceful absence):** With no (or partial) deflection data, the pipeline runs with zero errors, SLS is `None`/skipped, and ULS output is unaffected.
4. **AC-4 (no breaking signature changes):** `build_uls_summary` and `RESULT_COLUMNS` are untouched; `report_rows` is callable exactly as before.
5. **AC-5 (documentation):** Column contract (`DEFLECTION_INPUT_COLUMNS`, `SERVICEABILITY_COLUMNS`, `COMBINED_COLUMNS`) documented in `io_contract.py` docstrings; expected input grain stated.
6. **AC-6 (coverage):** New code paths (ratio, edge cases, merge, opt-in flag) covered by the tests above; no new warnings in the test run.
