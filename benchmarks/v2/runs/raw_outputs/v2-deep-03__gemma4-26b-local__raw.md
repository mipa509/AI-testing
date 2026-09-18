# Raw Output

- task_id: `v2-deep-03`
- model_id_used: `gemma4:26b-local`
- api_model: `gemma4:26b` (Ollama, local)
- reasoning_effort: `not applicable (no setting exposed)`
- run_route: `ollama run gemma4:26b --verbose` in a PowerShell terminal on the user's machine (local weights, no harness, tools, skills or web access)
- run_date: `2026-09-19`
- thinking_mode_used: `yes (hidden; the generated-token counts include it)`

## Prompt Used

Same as in the prompt file (`tasks/deep_03_scoped_feature_design/prompt.md`), pasted into the terminal chat as message 1, followed by the text of `context_combined.md` as message 2. First reply said it would deliver the five requested sections once the files were provided; it waited for the pasted context. The response was copied from the terminal, which wrapped long lines at the window width; the raw output below keeps the wrapping.

## Context Files Shared

- `context/design_engine.py`
- `context/io_contract.py`
- `context/report_writer.py`

## Raw Model Output

This implementation plan focuses on extending the calculation logic and the data schema while ensuring that the
primary reporting contract remains untouched for legacy consumers.

### 1. Files to Change

*   **`context/design_engine.py`**
    *   **Why:** To implement the new logic for calculating `DeflectionRatio` and `Status_SLS`. I will add a new
function `build_slli_summary` that specifically handles the serviceability logic, triggered only when the required
columns are present in the input DataFrame.
*   **`context/io_contract.py`**
    *   **Why:** To define the new column names as constants. This prevents "magic strings" from appearing in the
engine and allows for a new, non-breaking list of columns (`EXTENDED_RESULT_COLUMNS`) that includes the
serviceability data.
*   **`context/report_writer.py`**
    *   **Why:** To allow the `report_rows` function to optionally accept a different column set. By using a
default argument, existing callers that rely on the standard `RESULT_COLUMNS` will continue to receive the exact
same dictionary structure.

---

### 2. Public Interface & Schema Changes

**Schema Changes (Internal DataFrame):**
*   New columns added to the DataFrame during processing: `DeflectionRatio`, `Status_SLS`.

**Interface Changes:**
*   **`io_contract.py`**:
    *   New Constant: `SLS_COLUMNS = ["DeflectionRatio", "Status_SLS"]`
    *   New Constant: `EXTENDED_RESULT_COLUMNS = RESULT_COLUMNS + SLS_COLUMNS`
*   **`report_writer.py`**:
    *   Modify `report_rows(summary_df, columns=RESULT_COLUMNS)`: Added an optional `columns` parameter. It
defaults to the original `RESULT_COLUMNS` to ensure no breaking changes.

---

### 3. Data-Flow Changes

1.  **Input Stage:** The raw DataFrame enters the engine. It may or may not contain `Deflection_mm` and
`AllowableDeflection_mm`.
2.  **Processing Stage (The Engine):**
    *   `build_uls_summary` runs as usual, producing the ULS summary.

    *   **New Step:** A check is performed: `if all(cols in df.columns)`.
    *   If true, `build_sls_summary` is executed. It calculates the ratio and status, then performs a `left merge`
with the ULS summary DataFrame on `["Member", "Section"]`.
    *   If false, the engine proceeds with only the ULS summary.
3.  **Output Stage (The Report):**
    *   The `summary_df` (now potentially containing SLS columns) is passed to `report_rows`.
    *   **Standard Path:** `report_rows` uses the default `RESULT_COLUMNS`, effectively stripping the new SLS
columns out of the final dictionary, maintaining the legacy output.
    *   **Extended Path (New):** A new consumer can call `report_rows(df, columns=EXTENDED_RESULT_COLUMNS)` to see
the full dataset.

---

### 4. Backward-Compatibility Risks

*   **Risk: Downstream Dictionary Keys.** If `report_rows` were to automatically include all columns found in the
DataFrame, legacy systems expecting a specific set of keys would crash when encountering `DeflectionRatio`.
    *   *Mitigation:* Use the explicit `RESULT_COLUMNS` slice in `report_rows` as the default behavior.
*   **Risk: Merging Nulls.** If `build_sls_summary` runs but cannot find matching members in the ULS summary, it
could introduce `NaN` values.
    *   *Mitigation:* Use a `left` join on the ULS summary as the primary driver to ensure the ULS structure is
preserved.
*   **Risk: Input Column Dependency.** If the engine expects deflection columns that aren't there.
    *   *Mitigation:* Implement a guard clause (existence check) before invoking SLS logic.

---

### 5. Targeted Tests & Acceptance Criteria

**Tests:**
1.  **Regression Test (ULS Only):** Pass a DataFrame with only ULS columns. Verify the output dictionary contains
exactly `RESULT_COLUMNS` and no others.
2.  **Feature Test (Full Data):** Pass a DataFrame with ULS and Deflection columns. Verify that `DeflectionRatio`
is calculated correctly (e.g., $0.5 \rightarrow \text{PASS}$, $1.2 \rightarrow \text{FAIL}$).
3.  **Boundary Test:** Pass a DataFrame where `Deflection_mm` equals `AllowableDeflection_mm`. Verify status is
`PASS` (edge case $\le 1.0$).
4.  **Integration Test (Report Writer):** Verify that calling `report_rows` with the default parameters *still*
excludes the new SLS columns, even when they exist in the input `summary_df`.

**Acceptance Criteria:**
*   The dictionary returned by `report_rows(df)` remains identical in keys and length for all existing ULS-only
inputs.
*   The `DeflectionRatio` is mathematically accurate.
*   The system does not raise `KeyError` when deflection columns are missing from the input.
*   A developer can access the new metrics by explicitly passing `EXTENDED_RESULT_COLUMNS` to the reporter.
