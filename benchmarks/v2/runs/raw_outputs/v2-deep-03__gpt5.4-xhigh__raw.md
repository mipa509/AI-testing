# Raw Output

- task_id: `v2-deep-03`
- model_id_used: `gpt5.4-xhigh`
- run_date: `2026-04-11`
- thinking_mode_used: `yes`

## Prompt Used

Same as in the prompt file

## Context Files Shared

- `context/io_contract.py`
- `context/design_engine.py`
- `context/report_writer.py`

## Raw Model Output

**1. Files To Change**

`context/design_engine.py`
Reason: this is where the summary is computed today. I would keep `build_uls_summary(df)` unchanged for backward compatibility and add a separate serviceability path, ideally `build_serviceability_summary(df)` or a small wrapper that returns both summaries when requested.

`context/io_contract.py`
Reason: this defines the report/result schema. I would keep `RESULT_COLUMNS` unchanged and add a new serviceability-specific column set, for example `SERVICEABILITY_COLUMNS`, plus any input-column constants if the package uses them elsewhere.

`context/report_writer.py`
Reason: this is where the public report rows are shaped. I would preserve `report_rows(summary_df)` exactly as-is for existing ULS consumers, and add a new opt-in writer for serviceability output such as `serviceability_report_rows(summary_df)` or a combined writer with an explicit flag that defaults to current behavior.

**2. Public Interface Or Schema Changes**

Keep existing public behavior unchanged:
- `build_uls_summary(df)` continues returning `Member`, `Section`, `Utilisation_ULS`, `Status`.
- `report_rows(summary_df)` continues emitting only `RESULT_COLUMNS`.

Add new opt-in surface area rather than widening existing outputs by default:
- New serviceability summary dataframe schema:
  - `Member`
  - `Section`
  - `Deflection_mm`
  - `AllowableDeflection_mm`
  - `DeflectionRatio`
  - optionally `ServiceabilityStatus` if the package wants a pass/fail field analogous to ULS

Add new constant(s) instead of changing `RESULT_COLUMNS`:
- `SERVICEABILITY_COLUMNS = [...]`

If a combined API is needed, prefer a new function over changing existing return types:
- Example: `build_design_summaries(df, include_serviceability=False) -> {"uls": ..., "serviceability": ...}`
- Do not change `build_uls_summary` to return extra columns or a different object type.

**3. Data Flow Changes From Input To Report**

Input normalization:
- `normalise_columns(df)` remains unchanged unless column aliasing is needed.
- Serviceability logic should only activate when both `Deflection_mm` and `AllowableDeflection_mm` are present after normalization.

Computation:
- Existing ULS flow stays unchanged.
- New serviceability flow groups by `Member` and `Section`, using a defined aggregation rule for deflection fields.
- Compute `DeflectionRatio = Deflection_mm / AllowableDeflection_mm` after aggregation, not per raw row, unless domain rules explicitly require worst-row ratio.
- Guard against divide-by-zero and missing allowable values; decide whether such rows are excluded, set to null, or flagged.

Reporting:
- Existing report path keeps calling `report_rows(uls_summary_df)` and remains byte-for-byte stable in shape.
- New consumers can call a new serviceability writer to get serviceability rows.
- If a combined report is required, expose it as a separate opt-in structure, not by changing the current row payload.

**4. Backward-Compatibility Risks**

Changing `RESULT_COLUMNS`
Risk: `report_rows()` would start requiring new columns and break existing summaries immediately.

Changing `build_uls_summary()` output shape
Risk: callers may depend on exact dataframe columns or semantics.

Auto-including serviceability in `report_rows()`
Risk: downstream consumers may reject extra keys or changed ordering.

Unclear aggregation rule for deflection fields
Risk: wrong engineering meaning if multiple rows exist per member/section. This should be specified explicitly in the implementation plan.

Division edge cases
Risk: `AllowableDeflection_mm == 0` or null values can produce invalid ratios and unstable reports.

**5. Targeted Tests And Acceptance Criteria**

Tests:
- `build_uls_summary()` returns exactly the current columns and values for existing ULS-only input.
- `report_rows()` output is unchanged for existing ULS summaries.
- Serviceability summary is not produced unless requested or unless required input columns are present, depending on chosen API.
- When `Deflection_mm` and `AllowableDeflection_mm` are present, `DeflectionRatio` is computed correctly.
- Missing one or both deflection columns does not break ULS flow.
- Null or zero allowable deflection is handled per spec without crashing.
- Grouped summaries preserve one row per `Member`/`Section`.

Acceptance criteria:
- Existing ULS-only callers run with no code changes.
- Existing report payload from `report_rows()` is unchanged in columns and ordering.
- Serviceability output is available through a new explicit API/path.
- `DeflectionRatio` is present only in the serviceability summary and is computed as `Deflection_mm / AllowableDeflection_mm`.
- Edge cases for missing/invalid deflection data are deterministic and covered by tests.

One design choice needs to be fixed before implementation: the aggregation rule for `Deflection_mm` and `AllowableDeflection_mm` when multiple rows exist per `Member`/`Section`. I would recommend documenting that explicitly in `design_engine.py` tests and keeping it separate from the ULS max-utilization rule.