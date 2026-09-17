# Raw Output

- task_id: `v2-deep-03`
- model_id_used: `gpt5.6-sol-xhigh`
- api_model: `gpt-5.6-sol`
- reasoning_effort: `xhigh`
- run_route: `Codex VS Code extension, fresh session, empty sandbox workspace; inputs from neutral copy (D:\bench-inputs\task4)`
- run_date: `2026-09-17`
- thinking_mode_used: `yes (reasoning effort xhigh)`

## Prompt Used

Same as in the prompt file (`tasks/deep_03_scoped_feature_design/prompt.md`), sent as message 1. `tasks/deep_03_scoped_feature_design/context_combined.md` sent as message 2.

## Context Files Shared

- `context/io_contract.py`
- `context/design_engine.py`
- `context/report_writer.py`

## Raw Model Output

The safest design is an additive SLS path: keep the existing ULS builder, schema, and report function unchanged, while introducing separate serviceability APIs and an opt-in combined report.

## 1. Files to change

### `context/io_contract.py`

Add separate serviceability contracts:

```py
SERVICEABILITY_INPUT_COLUMNS = [
    "Deflection_mm",
    "AllowableDeflection_mm",
]

SERVICEABILITY_RESULT_COLUMNS = [
    "Member",
    "Section",
    "Deflection_mm",
    "AllowableDeflection_mm",
    "DeflectionRatio",
]
```

Keep `RESULT_COLUMNS` exactly as it is. Appending serviceability fields to it would break ULS-only frames and change existing report output.

`normalise_columns()` remains unchanged and applies before either design path.

### `context/design_engine.py`

Leave `build_uls_summary()` unchanged.

Add:

```py
def build_serviceability_summary(df: pd.DataFrame) -> pd.DataFrame:
    ...
```

The function always returns a DataFrame with `SERVICEABILITY_RESULT_COLUMNS`. It returns an empty DataFrame with that schema when serviceability data is absent.

Processing rules:

- If neither deflection input column exists, return an empty summary.
- If only one exists, raise `ValueError`; the input is incomplete rather than absent.
- Permit rows where both deflection values are null, so ULS-only rows can coexist in the same input.
- Reject rows where only one of the two values is null.
- Reject non-numeric or non-finite values, negative deflections, and allowable deflections less than or equal to zero.
- Calculate the ratio row by row using the requested formula, without rounding:

```py
DeflectionRatio = Deflection_mm / AllowableDeflection_mm
```

- Group by `Member` and `Section`, matching the ULS summary.
- Select the row with the maximum `DeflectionRatio` in each group.
- Carry `Deflection_mm` and `AllowableDeflection_mm` from that same governing row. They must not be independently aggregated, because that could produce a ratio whose numerator and denominator came from different cases.
- Resolve equal-ratio ties by retaining the first input row, making the result deterministic.

No serviceability pass/fail field should be introduced unless separately requested. The requested result is the ratio, and reusing the generic ULS `Status` name would be ambiguous.

### `context/report_writer.py`

Keep `report_rows(summary_df)` unchanged.

Add:

```py
def serviceability_report_rows(serviceability_df):
    ...
```

It projects exactly `SERVICEABILITY_RESULT_COLUMNS`, just as the existing writer explicitly projects `RESULT_COLUMNS`.

Also add an opt-in combined API:

```py
def report_sections(uls_summary, serviceability_summary=None):
    ...
```

Its result is:

```py
{"uls": report_rows(uls_summary)}
```

when serviceability is absent or empty, and:

```py
{
    "uls": report_rows(uls_summary),
    "serviceability": serviceability_report_rows(serviceability_summary),
}
```

when serviceability results exist.

Existing consumers continue calling `report_rows()` and receive the same list-of-records structure as before.

## 2. Public interface and schema changes

All changes are additive:

- New `SERVICEABILITY_INPUT_COLUMNS` constant.
- New `SERVICEABILITY_RESULT_COLUMNS` constant.
- New `build_serviceability_summary(df)` function.
- New `serviceability_report_rows(df)` function.
- New opt-in `report_sections(uls_summary, serviceability_summary=None)` function.

Unchanged public behavior:

- `build_uls_summary(df)` retains its signature, columns, aggregation, and status logic.
- `RESULT_COLUMNS` remains unchanged and in the same order.
- `report_rows(summary_df)` retains its signature and return shape.
- Deflection columns are not added to existing ULS records.

An empty, schema-correct DataFrame represents “no serviceability summary” inside the calculation layer. The combined report omits the `serviceability` key in that case.

## 3. Data flow from input to report

```text
Input DataFrame
    |
    +-- normalise_columns()
    |
    +-- ULS branch (unchanged)
    |     build_uls_summary()
    |         -> Member, Section, Utilisation_ULS, Status
    |         -> report_rows()
    |         -> existing list of ULS records
    |
    +-- Optional serviceability branch
          detect deflection columns
          -> validate complete value pairs
          -> calculate row-level DeflectionRatio
          -> select maximum-ratio row per Member/Section
          -> serviceability_report_rows()
          -> optional serviceability records
```

Calculating before grouping is important. For example, the governing ratio must be determined from `Deflection_mm / AllowableDeflection_mm` for each individual row, not from separately aggregated numerator and denominator values.

## 4. Backward-compatibility risks

- Changing `RESULT_COLUMNS` would alter existing reports or cause missing-column errors. It must remain untouched.
- Modifying `report_rows()` to sometimes return a dictionary instead of a list would break downstream consumers. The combined structure therefore gets a new function.
- Automatically invoking SLS validation from `build_uls_summary()` could break ULS-only callers whose inputs contain incomplete ancillary columns. The two builders remain independent.
- Inputs containing one deflection column but not the other must fail only when the new serviceability path is requested.
- Zero allowable deflection would otherwise create infinite ratios; it is rejected explicitly.
- Independent aggregation of actual and allowable deflection could report incoherent governing values; the complete governing row is retained instead.
- Existing serialized or golden-report output must remain identical, including field names and order.
- Consumers adopting `report_sections()` must treat `serviceability` as an optional key.

## 5. Targeted tests and acceptance criteria

### Design-engine tests

- Existing ULS input produces exactly the current ULS DataFrame.
- Adding deflection columns does not change `build_uls_summary()` output.
- With no deflection columns, `build_serviceability_summary()` returns an empty DataFrame with the declared serviceability schema.
- A row with `Deflection_mm=12` and `AllowableDeflection_mm=20` produces `DeflectionRatio=0.6`.
- Multiple rows for one member select the maximum row-level ratio and preserve that row’s actual and allowable values.
- Multiple members and sections are grouped independently.
- Rows with both deflection values null are ignored.
- Inputs with only one deflection column raise `ValueError`.
- One-sided null values raise `ValueError`.
- Non-numeric, non-finite, negative deflection, zero allowable, and negative allowable values raise `ValueError`.
- Equal governing ratios select the first input row deterministically.
- The input DataFrame is not mutated.

### Report-writer tests

- Existing `report_rows()` output matches the current golden output exactly.
- `serviceability_report_rows()` emits only the declared serviceability fields and preserves their order.
- `report_sections()` omits `serviceability` for `None` or an empty summary.
- `report_sections()` includes it when results exist.
- The `uls` value from `report_sections()` equals `report_rows(uls_summary)` exactly.

### Acceptance criteria

- All existing ULS tests and downstream report snapshots pass without modification.
- Existing ULS-only callers require no code changes.
- Valid deflection data produces the requested ratio using the exact formula.
- The maximum ratio per `Member`/`Section` is reported with its matching source values.
- Missing optional data produces no serviceability report section.
- Incomplete or unsafe serviceability inputs fail clearly instead of producing misleading ratios.
