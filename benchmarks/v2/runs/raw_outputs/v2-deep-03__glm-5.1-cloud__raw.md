# Raw Output

- task_id: `v2-deep-03`
- model_id_used: `glm-5.1-cloud`
- run_date: `2026-04-09`
- thinking_mode_used: `yes`

## Prompt Used

Same as in the prompt file

## Context Files Shared

All files from context folder

## Raw Model Output:
----------------------------------------------------------------
Here is the decision-complete implementation plan based on the provided context files.

### 1. Files to Change and Why

*   **`io_contract.py`**
    *   *Why:* To define the new schema for SLS (Serviceability Limit State) data and deflection inputs without
modifying the existing `RESULT_COLUMNS`, which downstream consumers depend on.
    *   *Change:* Add `SLS_RESULT_COLUMNS` (for the output schema) and `DEFLECTION_INPUT_COLUMNS` (to check if
deflection data is present).
*   **`design_engine.py`**
    *   *Why:* To encapsulate the business logic for calculating the `DeflectionRatio` and SLS status. Keeping it
separate from ULS ensures existing ULS callers are undisturbed.
    *   *Change:* Add a new function `build_sls_summary(df)` that groups by Member/Section, calculates
`DeflectionRatio = Deflection_mm / AllowableDeflection_mm`, takes the max ratio per group, and determines an SLS
status.
*   **`report_writer.py`**
    *   *Why:* Currently strictly filters output to `RESULT_COLUMNS`. It needs to optionally include SLS columns
while preserving the default ULS-only behavior.
    *   *Change:* Modify `report_rows` to accept an optional parameter `include_sls=False`. If true, it will
select the union of `RESULT_COLUMNS` and `SLS_RESULT_COLUMNS`.

### 2. Public Interface or Schema Changes

*   **Schema Additions (`io_contract.py`):**
    *   `DEFLECTION_INPUT_COLUMNS = ["Deflection_mm", "AllowableDeflection_mm"]`
    *   `SLS_RESULT_COLUMNS = ["DeflectionRatio", "Status_SLS"]`
*   **API Addition (`design_engine.py`):**
    *   `def build_sls_summary(df: pd.DataFrame) -> pd.DataFrame:`
        *   *Contract:* Expects the input DataFrame to contain `DEFLECTION_INPUT_COLUMNS`. Returns a DataFrame
indexed by `["Member", "Section"]` with `SLS_RESULT_COLUMNS`.
*   **API Modification (`report_writer.py`):**
    *   `def report_rows(summary_df, include_sls=False):`
        *   *Contract:* If `include_sls` is `False` (default), output remains identical to current behavior. If
`True`, output dictionaries will include the keys from `SLS_RESULT_COLUMNS`.

### 3. Data-Flow Changes from Input to Report

*   **Current Flow:**
    `Input DF` -> `normalise_columns()` -> `build_uls_summary()` -> `report_rows()` -> `List[Dict]`
*   **New Flow:**
    1. `Input DF` -> `normalise_columns()`
    2. `build_uls_summary(normalised_df)` -> `uls_df`
    3. *Condition:* Check if `DEFLECTION_INPUT_COLUMNS` are a subset of `normalised_df.columns`.
    4. If True: `build_sls_summary(normalised_df)` -> `sls_df`. Left-merge `uls_df` and `sls_df` on `["Member",
"Section"]` -> `combined_df`.
    5. If False: `combined_df` = `uls_df` (or `uls_df` with empty SLS columns to maintain consistent shape).
    6. `report_rows(combined_df, include_sls=<boolean_flag_passed_by_caller>)` -> `List[Dict]`

### 4. Backward-Compatibility Risks

*   **Risk 1: Downstream dictionary consumers break on new keys.**
    *   *Mitigation:* The `include_sls` flag defaults to `False` in `report_rows`. The default data-flow will
strictly slice `RESULT_COLUMNS`. Downstream systems will only see SLS data if they explicitly opt in.
*   **Risk 2: Division-by-zero in `DeflectionRatio` calculation if `AllowableDeflection_mm` is 0.**
    *   *Mitigation:* `build_sls_summary` must guard against zero/nan allowables. If `AllowableDeflection_mm` <=
0, `DeflectionRatio` should be set to `NaN` or `inf` per engineering convention, and `Status_SLS` set to `FAIL` or
`ERROR`.
*   **Risk 3: Existing ULS callers are impacted by DataFrame merge.**
    *   *Mitigation:* Because `build_uls_summary` remains untouched and the merge is a left-join on
Member/Section, ULS columns and their groupings remain perfectly intact. Callers only using ULS outputs will see
no difference in the ULS portion of the combined DataFrame.

### 5. Targeted Tests and Acceptance Criteria

*   **Test 1: ULS-Only Preservation (Backward Compatibility)**
    *   *Input:* DataFrame with ULS data, but no Deflection data.
    *   *Action:* Pass through new flow with `include_sls=False`.
    *   *Acceptance:* Output matches the old `report_rows` output exactly (dicts contain only `RESULT_COLUMNS`
keys).
*   **Test 2: SLS Calculation Accuracy**
    *   *Input:* DataFrame with `Member="A"`, `Deflection_mm=12`, `AllowableDeflection_mm=24`.
    *   *Action:* Run `build_sls_summary()`.
    *   *Acceptance:* Resulting DataFrame has `DeflectionRatio=0.5` and `Status_SLS="PASS"`.
*   **Test 3: SLS Grouping (Max Ratio)**
    *   *Input:* DataFrame with two rows for `Member="A"`: (10mm/20mm -> 0.5) and (15mm/20mm -> 0.75).
    *   *Action:* Run `build_sls_summary()`.
    *   *Acceptance:* Grouped result takes the max, yielding `DeflectionRatio=0.75` and `Status_SLS="PASS"`.
*   **Test 4: SLS Opt-In Report Generation**
    *   *Input:* Combined DataFrame (ULS + SLS).
    *   *Action:* Call `report_rows(combined_df, include_sls=True)`.
    *   *Acceptance:* Output dictionaries contain all keys from `RESULT_COLUMNS` plus `DeflectionRatio` and
`Status_SLS`.
*   **Test 5: Zero Allowable Deflection Guard**
    *   *Input:* DataFrame where `AllowableDeflection_mm = 0`.
    *   *Action:* Run `build_sls_summary()`.
    *   *Acceptance:* Does not raise `ZeroDivisionError`. Returns `DeflectionRatio=inf` (or `NaN`) and
`Status_SLS="FAIL"`.