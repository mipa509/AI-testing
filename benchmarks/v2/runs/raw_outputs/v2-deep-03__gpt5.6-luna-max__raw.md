# Raw Output

- task_id: `v2-deep-03`
- model_id_used: `gpt5.6-luna-max`
- api_model: `gpt-5.6-luna`
- reasoning_effort: `max`
- run_route: `Codex VS Code extension, fresh session, empty sandbox workspace; inputs from neutral copy (D:\bench-inputs\task4)`
- run_date: `2026-09-17`
- thinking_mode_used: `yes (reasoning effort max)`

## Prompt Used

Same as in the prompt file (`tasks/deep_03_scoped_feature_design/prompt.md`), sent as message 1. `tasks/deep_03_scoped_feature_design/context_combined.md` sent as message 2.

## Context Files Shared

- `context/io_contract.py`
- `context/design_engine.py`
- `context/report_writer.py`

## Raw Model Output

The safest design is additive: leave the existing ULS table and `report_rows()` contract untouched, and add a separate serviceability table plus an opt-in combined report.

### 1. Files to change

- `context/io_contract.py`
  - Keep `RESULT_COLUMNS` exactly as-is.
  - Add:
    - `SERVICEABILITY_INPUT_COLUMNS = ["Deflection_mm", "AllowableDeflection_mm"]`
    - `SERVICEABILITY_RESULT_COLUMNS = ["Member", "Section", "Deflection_mm", "AllowableDeflection_mm", "DeflectionRatio", "Status"]`
  - Leave `normalise_columns()` behavior unchanged.

- `context/design_engine.py`
  - Leave `build_uls_summary(df)` unchanged in signature, grouping, calculations, and output columns.
  - Add `build_serviceability_summary(df) -> DataFrame | None`.
  - Optionally add an orchestration helper such as `build_design_summaries(df)` that normalises the input and returns both summaries.

- `context/report_writer.py`
  - Leave `report_rows(summary_df)` unchanged.
  - Add `serviceability_report_rows(serviceability_df)`.
  - Add an opt-in `report_payload(uls_summary_df, serviceability_summary_df=None)` that emits separate `uls` and `serviceability` sections.

- Tests, using the repository’s existing test layout:
  - Design-engine tests for calculation and omission rules.
  - Report-writer tests for legacy and combined output.
  - Contract tests for column names and ordering.

### 2. Public interface and schema changes

Existing interfaces remain unchanged:

```text
build_uls_summary(df) -> ULS DataFrame
normalise_columns(df) -> DataFrame
report_rows(summary_df) -> list[dict]
```

New interfaces are additive:

```text
build_serviceability_summary(df) -> DataFrame | None
serviceability_report_rows(serviceability_df) -> list[dict]
report_payload(uls_summary_df, serviceability_summary_df=None) -> dict
```

The existing ULS schema remains exactly:

```text
Member, Section, Utilisation_ULS, Status
```

The new serviceability schema is:

```text
Member, Section, Deflection_mm,
AllowableDeflection_mm, DeflectionRatio, Status
```

`report_payload()` should omit the `serviceability` key when no serviceability data exists. Existing consumers should continue using `report_rows()` and receive the same list shape and fields.

### 3. Data flow

```text
Input DataFrame
    -> normalise_columns()
    -> build_uls_summary()
    -> build_serviceability_summary()
    -> report_payload()
         -> existing ULS rows
         -> optional serviceability rows
```

Serviceability rules:

- If neither deflection column exists, return `None`.
- If only one exists, raise a clear schema error rather than silently omitting data.
- Ignore rows where both optional values are null.
- Reject incomplete pairs, non-numeric values, non-finite values, or `AllowableDeflection_mm <= 0`.
- Compute the literal requested formula:

```text
DeflectionRatio = Deflection_mm / AllowableDeflection_mm
```

- For multiple rows per `Member`/`Section`, calculate the ratio per row and retain the row with the maximum ratio. This keeps the reported deflection and allowable value paired correctly.
- Derive serviceability `Status` using the existing convention: `PASS` when the ratio is `<= 1.0`, otherwise `FAIL`.
- Do not round the ratio inside the engine.

### 4. Backward-compatibility risks

- Expanding `RESULT_COLUMNS` would add fields to existing reports and must be avoided.
- Adding serviceability fields directly to ULS rows would break consumers expecting exactly four fields.
- Changing `report_rows()` to return a dictionary or mixed row types would break callers; keep it unchanged.
- Zero or invalid allowable deflections require explicit validation.
- Deflection sign conventions must be established upstream; this change should use the supplied value literally and should not silently apply `abs()`.
- Callers adopting `report_payload()` must understand that it is a new nested report contract.

### 5. Targeted tests and acceptance criteria

Tests should verify:

- Legacy input without deflection columns still produces the identical ULS DataFrame and `report_rows()` records.
- `build_serviceability_summary()` returns `None` when deflection data is absent.
- A valid example computes the expected ratio and status.
- Multiple rows select the maximum ratio and preserve its matching deflection/allowable values.
- Whitespace-stripped column names work after normalisation.
- Partial columns, missing pairs, non-numeric values, and zero/negative allowable values fail clearly.
- Adding deflection columns does not alter the ULS output.
- `report_payload()` preserves the ULS section exactly and adds serviceability only when available.
- Serviceability and ULS column ordering is deterministic.
- The input DataFrame is not mutated.

Acceptance is met when all existing tests pass unchanged, all legacy report consumers see the original four-column output, and new callers can obtain a separate serviceability summary containing a correct `DeflectionRatio`.
