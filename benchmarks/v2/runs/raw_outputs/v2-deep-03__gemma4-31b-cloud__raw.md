# Raw Output

- task_id: `v2-deep-03`
- model_id_used: `gemma4-31b-cloud`
- run_date: `2026-04-09`
- thinking_mode_used: `yes`

## Prompt Used

Same as in the prompt file

## Context Files Shared

- `context/io_contract.py`
- `context/design_engine.py`
- `context/report_writer.py`

## Raw Model Output

This implementation plan outlines the addition of serviceability checks (deflection ratios) while ensuring that
existing ULS (Ultimate Limit State) workflows remain untouched.

### 1. Files to be Changed

*   **`io_contract.py`**: To define the new schema for serviceability columns.
*   **`design_engine.py`**: To implement the logic for calculating the `DeflectionRatio` and the associated
serviceability status.
*   **`report_writer.py`**: To allow the report to dynamically include serviceability columns based on a flag,
ensuring the default output remains unchanged.

---

### 2. Public Interface and Schema Changes

#### `io_contract.py`
Introduce a new constant to define the serviceability output:
*   `SERVICEABILITY_COLUMNS = ["DeflectionRatio", "Serviceability_Status"]`

#### `design_engine.py`
Introduce a new function or update the existing one to support optional calculations:
*   `build_serviceability_summary(df: pd.DataFrame) -> pd.DataFrame`: A new helper to compute ratios and statuses.
*   *(Alternative)*: Update `build_uls_summary` to a more generic `build_design_summary(df,
include_serviceability=False)`.

#### `report_writer.py`
Update the function signature:
*   `report_rows(summary_df, include_serviceability=False)`: Adds a boolean flag to determine if the output
dictionary should include the serviceability columns.

---

### 3. Data-Flow Changes

1.  **Input**: The input DataFrame enters `design_engine.py`.
2.  **Processing (New Logic)**:
    *   If `include_serviceability` is True, the engine checks for the existence of `Deflection_mm` and
`AllowableDeflection_mm`.
    *   It computes `DeflectionRatio = Deflection_mm / AllowableDeflection_mm`.
    *   It computes `Serviceability_Status` (`PASS` if $\le 1.0$, else `FAIL`).
    *   The results are aggregated (grouped by Member/Section) using `max` to identify the worst-case deflection
ratio.
3.  **Handoff**: The resulting DataFrame (containing both ULS and Serviceability data) is passed to
`report_writer.py`.
4.  **Filtering**: The `report_writer` selects columns based on the flag:
    *   If `False`: Selects only `RESULT_COLUMNS`.
    *   If `True`: Selects `RESULT_COLUMNS + SERVICEABILITY_COLUMNS`.
5.  **Output**: The final list of dictionaries is returned to the consumer.

---

### 4. Backward-Compatibility Risks

*   **Schema Strictness**: If downstream consumers use a strict schema validator that fails when unexpected keys
(like `DeflectionRatio`) are present, adding these columns to the output would be breaking. This is mitigated by
making the feature **opt-in** via the `include_serviceability` flag in `report_rows`.
*   **Zero Division**: If `AllowableDeflection_mm` is $0$ or `NaN`, the ratio calculation will result in `inf` or
`NaN`. This must be handled to prevent the report from crashing.
*   **Column Dependency**: If `build_serviceability_summary` is called on a DataFrame missing the required
deflection columns, it must return an empty/NaN summary rather than raising a `KeyError`.

---

### 5. Targeted Tests and Acceptance Criteria

#### Test Cases
1.  **ULS-Only Regression**: Pass a DataFrame with only ULS data and call `report_rows` without the new flag.
**Expectation**: Output is identical to the current implementation.
2.  **Full Serviceability**: Pass a DataFrame with `Deflection_mm` and `AllowableDeflection_mm` and set
`include_serviceability=True`. **Expectation**: Output contains `DeflectionRatio` and `Serviceability_Status`
correctly calculated.
3.  **Missing Data**: Pass a DataFrame that is missing `AllowableDeflection_mm` but requested serviceability.
**Expectation**: The system should not crash; `DeflectionRatio` should be `NaN`.
4.  **Edge Case (Boundary)**: Pass a ratio of exactly $1.0$. **Expectation**: `Serviceability_Status` is `PASS`.

#### Acceptance Criteria
*   [ ] Existing ULS reports are produced with no changes to the keys or values.
*   [ ] `DeflectionRatio` is correctly computed as $\frac{\text{Actual}}{\text{Allowable}}$.
*   [ ] `Serviceability_Status` is correctly mapped to `PASS`/`FAIL`.
*   [ ] The feature is entirely optional and does not force a change in the output for users who do not explicitly
request it.