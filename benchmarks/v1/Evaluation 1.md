TASK:
"I am a structural engineer working with analysis results exported from software into CSV files.
Write Python code using pandas to process a results table with columns like:

Member
Case
Combination
Position_m
N_kN
Vy_kN
Vz_kN
Mx_kNm
My_kNm
Mz_kNm

Requirements:
1. Load the CSV.
2. Clean column names.
3. Convert numeric columns safely, coercing bad data to NaN.
4. Create a new column called ResultCase which uses Combination if present, otherwise Case.
5. For each Member, find:
   - max and min Mz_kNm
   - max absolute Vy_kN
   - max absolute N_kN
6. Also return the row where each governing value occurs.
7. Output two DataFrames:
   - a summary table by Member
   - a governing rows table
8. Make the code robust and readable, with comments and clear function structure.

Assume there may be blank strings, duplicated rows, and mixed numeric/string values."


--------------------------------------------------------------------------------------------------------
## Output — Qwen3.5 27B:
Here is a robust, well-structured Python script using `pandas` to process your structural analysis results.

This script includes:
1.  **Data Loading & Cleaning:** Handles whitespace, numeric conversion errors, and logic for the `ResultCase`.
2.  **Analysis Logic:** Calculates specific extrema (Max/Min Mz, Max Abs Vy/N) per member.
3.  **Traceability:** Identifies the exact rows (Load Case/Position) where these governing values occur.
4.  **Demonstration:** Includes a block to generate dummy data so you can run the script immediately to verify
behavior.

```python
import pandas as pd
import numpy as np
from pathlib import Path

# ==============================================================================
# CONFIGURATION
# ==============================================================================

# Define expected columns for validation and processing
EXPECTED_COLUMNS = [
    'Member', 'Case', 'Combination', 'Position_m',
    'N_kN', 'Vy_kN', 'Vz_kN', 'Mx_kNm', 'My_kNm', 'Mz_kNm'
]

NUMERIC_COLUMNS = [
    'Position_m', 'N_kN', 'Vy_kN', 'Vz_kN', 'Mx_kNm', 'My_kNm', 'Mz_kNm'
]

# ==============================================================================
# FUNCTIONS
# ==============================================================================

def load_and_clean_data(filepath: str) -> pd.DataFrame:
    """
    Loads CSV, cleans column names, converts numeric types safely,
    and creates the ResultCase column.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {filepath}")

    # 1. Load CSV
    df = pd.read_csv(filepath)

    # 2. Clean Column Names (strip whitespace, standardize)
    df.columns = df.columns.str.strip()

    # Validate critical columns exist
    missing_cols = set(EXPECTED_COLUMNS) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns in CSV: {missing_cols}")

    # 3. Convert Numeric Columns Safely
    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # 4. Handle ResultCase Logic
    # Replace empty strings in Combination with NaN so combine_first works correctly
    df['Combination'] = df['Combination'].replace('', np.nan)
    df['Case'] = df['Case'].replace('', np.nan)

    # Use Combination if present, otherwise fall back to Case
    df['ResultCase'] = df['Combination'].combine_first(df['Case'])

    # Fill any remaining NaN cases with a placeholder for clarity
    df['ResultCase'] = df['ResultCase'].fillna('Unknown_Case')

    # 5. Remove Exact Duplicates
    df = df.drop_duplicates()

    # 6. Remove rows where Member is missing (cannot group without it)
    df = df.dropna(subset=['Member'])
    df['Member'] = df['Member'].astype(str).str.strip()

    return df


def _get_idx_safe(series: pd.Series, method: str = 'max') -> int:
    """
    Helper to get idxmax/idxmin safely, handling all-NaN series.
    method: 'max' or 'min' or 'abs_max'
    """
    if series.isna().all():
        return None

    if method == 'abs_max':
        return series.abs().idxmax()
    elif method == 'max':
        return series.idxmax()
    elif method == 'min':
        return series.idxmin()
    else:
        raise ValueError(f"Unknown method: {method}")


def analyze_members(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Processes the dataframe to find governing values per member.

    Returns:
        summary_df: One row per Member with governing values.
        governing_rows_df: The specific rows from original data where values occurred.
    """
    if df.empty:
        return pd.DataFrame(), pd.DataFrame()

    # Store results here
    summary_data = []
    governing_rows_data = []

    # Group by Member
    grouped = df.groupby('Member')

    for member_id, group in grouped:
        # Initialize record for summary
        record = {'Member': member_id}

        # Define criteria to check
        # Format: (Output_Column_Name, Source_Column, Method)
        criteria = [
            ('Max_Mz_kNm', 'Mz_kNm', 'max'),
            ('Min_Mz_kNm', 'Mz_kNm', 'min'),
            ('Max_Abs_Vy_kN', 'Vy_kN', 'abs_max'),
            ('Max_Abs_N_kN', 'N_kN', 'abs_max'),
        ]

        for out_col, src_col, method in criteria:
            # Find the index in the original DataFrame where this occurs
            idx = _get_idx_safe(group[src_col], method=method)

            if idx is not None:
                # Get the value
                val = df.loc[idx, src_col]
                record[out_col] = val

                # Capture the governing row details
                row_info = df.loc[idx].copy()
                row_info['Governing_Criterion'] = out_col
                row_info['Governing_Value'] = val
                governing_rows_data.append(row_info)
            else:
                # If no valid data (all NaN)
                record[out_col] = np.nan

        summary_data.append(record)

    # Create DataFrames
    summary_df = pd.DataFrame(summary_data)

    if governing_rows_data:
        governing_rows_df = pd.DataFrame(governing_rows_data)
        # Reorder columns for readability (put new columns at front)
        new_cols = ['Member', 'Governing_Criterion', 'Governing_Value', 'ResultCase', 'Position_m']
        existing_cols = [c for c in governing_rows_df.columns if c not in new_cols]
        governing_rows_df = governing_rows_df[new_cols + existing_cols]
    else:
        governing_rows_df = pd.DataFrame()

    return summary_df, governing_rows_df


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

def main():
    # -------------------------------------------------------------------------
    # 1. SETUP (For Demonstration: Create a dummy CSV)
    # -------------------------------------------------------------------------
    # In production, comment out this block and use your actual file path.
    demo_file = 'structural_results_demo.csv'

    data = {
        'Member': ['B1', 'B1', 'B1', 'C1', 'C1', 'C1', 'B2'],
        'Case': ['DL', 'LL', 'EQ', 'DL', 'LL', 'EQ', 'DL'],
        'Combination': ['COMB1', 'COMB1', '', 'COMB1', '', '', ''], # Mix of Comb/Case
        'Position_m': [0, 2.5, 5, 0, 2.5, 5, 0],
        'N_kN': ['-10.5', ' -5.2 ', 'bad_data', '-20', '-15', '-25', ''], # Strings/Blanks
        'Vy_kN': [5, 10, -15, 2, 3, 4, 0],
        'Vz_kN': [0, 0, 0, 0, 0, 0, 0],
        'Mx_kNm': [0, 0, 0, 0, 0, 0, 0],
        'My_kNm': [0, 0, 0, 0, 0, 0, 0],
        'Mz_kNm': [10, 50, -100, 20, 30, 40, 0] # B1 Max 50, Min -100
    }

    df_demo = pd.DataFrame(data)
    df_demo.to_csv(demo_file, index=False)
    print(f"Created demo file: {demo_file}\n")

    # -------------------------------------------------------------------------
    # 2. PROCESS DATA
    # -------------------------------------------------------------------------
    try:
        print("Loading and cleaning data...")
        df_clean = load_and_clean_data(demo_file)

        print("Analyzing members...")
        summary_df, governing_df = analyze_members(df_clean)

        # -------------------------------------------------------------------------
        # 3. OUTPUT RESULTS
        # -------------------------------------------------------------------------
        print("\n--- SUMMARY TABLE (By Member) ---")
        print(summary_df.to_string(index=False))

        print("\n--- GOVERNING ROWS TABLE (Critical Cases) ---")
        if not governing_df.empty:
            # Display key columns for brevity
            display_cols = ['Member', 'Governing_Criterion', 'Governing_Value', 'ResultCase', 'Position_m']
            print(governing_df[display_cols].to_string(index=False))

            # Optional: Save to CSV
            summary_df.to_csv('member_summary.csv', index=False)
            governing_df.to_csv('governing_rows.csv', index=False)
            print("\nResults saved to 'member_summary.csv' and 'governing_rows.csv'")
        else:
            print("No governing rows found (check input data).")

    except Exception as e:
        print(f"\nError during processing: {e}")


if __name__ == "__main__":
    main()
```
### Key Features of this Code:

1.  **Robust Cleaning (`load_and_clean_data`)**:
    *   **Whitespace:** Strips spaces from column headers and string data (e.g., `' -5.2 '` becomes `-5.2`).
    *   **Numeric Coercion:** Uses `errors='coerce'` to turn invalid strings (like `'bad_data'`) into `NaN`
instead of crashing.
    *   **ResultCase Logic:** Prioritizes `Combination`. If `Combination` is empty/NaN, it falls back to `Case`.
    *   **Duplicates:** Removes exact duplicate rows which often occur in exported FEA results.

2.  **Safe Aggregation (`_get_idx_safe`)**:
    *   Standard `idxmax()` crashes or behaves unexpectedly if a group contains only `NaN` values. This helper
checks for all-NaN groups before attempting to find an index.
    *   Handles **Absolute Maximums**: Standard pandas aggregation doesn't support `max(abs(x))` while retaining
the original sign. The code calculates the index based on the absolute value but retrieves the original signed
value from the dataframe.

3.  **Traceability**:
    *   **Summary Table:** Gives you a quick spreadsheet-style view of the critical values per member.
    *   **Governing Rows Table:** Tells you exactly *which* load case (`ResultCase`) and *where* (`Position_m`)
the critical value happened. This is crucial for engineering verification.

4.  **Extensibility**:
    *   The `criteria` list inside `analyze_members` allows you to easily add more checks (e.g., `Max_My_kNm`)
without rewriting the loop logic.

### How to Use:
1.  Save the code as `process_results.py`.
2.  Install pandas if needed: `pip install pandas`.
3.  **For Testing:** Run the script as-is. It will generate a dummy CSV (`structural_results_demo.csv`) and
process it.
4.  **For Production:**
    *   Delete or comment out the "Demo" block in `main()`.
    *   Change `demo_file = 'structural_results_demo.csv'` to your actual file path (e.g., `filepath =
'C:/Projects/Analysis/results.csv'`).
    *   Call `load_and_clean_data(filepath)`.

--------------------------------------------------------------------------------------------------------
## Output — Qwen3-Coder-Next:
Here's a robust, well-documented Python script using `pandas` to process your structural analysis results CSV as
requested. It handles common data quality issues (blanks, duplicates, mixed types), performs safely typed
conversions, and extracts governing design values with their associated rows.

```python
import pandas as pd
import numpy as np
from typing import Tuple, List, Dict, Any

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean column names: strip whitespace, standardize case (lowercase + underscores),
    replace invalid characters, and remove duplicates.
    """
    def _clean_name(name: str) -> str:
        # Strip whitespace, convert to lowercase, replace non-alphanumeric (except underscore) with underscore
        cleaned = str(name).strip().lower().replace(" ", "_")
        # Replace any non-alphanumeric/non-underscore characters with underscores, collapse duplicates
        cleaned = "".join(c if (c.isalnum() or c == '_') else '_' for c in cleaned)
        # Collapse multiple underscores to one
        while "__" in cleaned:
            cleaned = cleaned.replace("__", "_")
        # Remove leading/trailing underscores
        cleaned = cleaned.strip("_")
        # Ensure no empty strings after cleaning (fallback)
        return cleaned or "column"

    df.columns = [_clean_name(col) for col in df.columns]
    # Remove duplicate column names (keep first occurrence)
    df = df.loc[:, ~df.columns.duplicated(keep='first')]
    return df

def load_and_preprocess(csv_path: str) -> pd.DataFrame:
    """
    Load CSV, clean column names, handle duplicates, and ensure basic integrity.
    """
    # Read CSV with low_memory=False to avoid mixed type inference warnings
    df = pd.read_csv(csv_path, low_memory=False, skip_blank_lines=True)

    # Drop completely empty rows
    df = df.dropna(how='all')

    # Drop duplicate rows (keep first)
    df = df.drop_duplicates()

    # Clean column names
    df = clean_column_names(df)

    return df

def safe_convert_to_numeric(df: pd.DataFrame, numeric_cols: List[str]) -> pd.DataFrame:
    """
    Attempt to convert specified columns to numeric, coercing errors to NaN.
    Returns DataFrame with converted columns.
    """
    df = df.copy()
    for col in numeric_cols:
        if col in df.columns:
            # pd.to_numeric with errors='coerce' converts non-numeric strings to NaN
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def create_result_case_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create 'result_case' column: use 'combination' if non-null/blank, else 'case'.
    Falls back to 'Case' (case-insensitive match).
    """
    # Normalize case of key columns to support variations
    col_case = next((c for c in df.columns if c.lower() == 'case'), None)
    col_comb = next((c for c in df.columns if c.lower() == 'combination'), None)

    if col_case is None or col_comb is None:
        raise ValueError("Required columns 'Case' and/or 'Combination' not found in data.")

    # Ensure both exist and create ResultCase
    df["result_case"] = np.where(
        (df[col_comb].notna()) & (df[col_comb].astype(str).str.strip() != ""),
        df[col_comb].astype(str).str.strip(),
        df[col_case].astype(str).str.strip()
    )

    return df

def compute_governing_values(df: pd.DataFrame, member_col: str = 'member') -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    For each member, compute:
      - max_Mz, min_Mz
      - max_abs_vy (max absolute Vy)
      - max_abs_n (max absolute N)
    Returns:
      - summary_df: governing *values* per member
      - governing_rows_df: full rows where each governing value occurs
    """
    # Ensure member_col exists
    if member_col not in df.columns:
        raise ValueError(f"Member column '{member_col}' not found. Available columns: {list(df.columns)}")

    # Ensure required analysis columns exist and are numeric
    required_cols = ['mz_knm', 'vy_kn', 'n_kn']
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Required analysis columns missing: {missing}")

    # Define aggregation rules
    aggregations = {
        'mz_knm': ['max', 'min'],
        'vy_kn': lambda x: x.abs().max(),
        'n_kn': lambda x: x.abs().max()
    }

    # Compute summary stats (but we need row indices for governing values)
    # Use groupby + agg + idxmax(idxmin) approach for governing row extraction

    summary_rows = []
    governing_rows_list = []

    # Sort for consistent ordering (optional but helpful)
    df = df.sort_values([member_col, 'position_m']).reset_index(drop=True)

    for member, group in df.groupby(member_col, sort=False):
        # Max Mz and its row
        idx_max_mz = group['mz_knm'].idxmax()
        row_max_mz = df.loc[idx_max_mz].copy()

        # Min Mz and its row
        idx_min_mz = group['mz_knm'].idxmin()
        row_min_mz = df.loc[idx_min_mz].copy()

        # Max abs Vy and its row
        abs_vy = group['vy_kn'].abs()
        idx_max_abs_vy = abs_vy.idxmax()
        row_max_abs_vy = df.loc[idx_max_abs_vy].copy()

        # Max abs N and its row
        abs_n = group['n_kn'].abs()
        idx_max_abs_n = abs_n.idxmax()
        row_max_abs_n = df.loc[idx_max_abs_n].copy()

        # Build summary row
        summary_row = {
            member_col: member,
            'max_Mz_kNm': group['mz_knm'].max(),
            'min_Mz_kNm': group['mz_knm'].min(),
            'max_abs_Vy_kN': abs_vy.max(),
            'max_abs_N_kN': abs_n.max(),
            'n_cases': len(group),
            'result_cases': '; '.join(group['result_case'].unique().astype(str).tolist()),
        }
        summary_rows.append(summary_row)

        # Collect governing rows (add metadata: which governing value, which case, etc.)
        for row, label, value, value_col in [
            (row_max_mz, 'max_Mz', row_max_mz['mz_knm'], 'mz_knm'),
            (row_min_mz, 'min_Mz', row_min_mz['mz_knm'], 'mz_knm'),
            (row_max_abs_vy, 'max_abs_Vy', row_max_abs_vy['vy_kn'], 'vy_kn'),
            (row_max_abs_n, 'max_abs_N', row_max_abs_n['n_kn'], 'n_kn'),
        ]:
            row['governing_type'] = label
            row['governing_value'] = value
            row['governing_column'] = value_col
            governing_rows_list.append(row)

    # Convert to DataFrames
    summary_df = pd.DataFrame(summary_rows)
    governing_rows_df = pd.DataFrame(governing_rows_list)

    # Optional: reorder summary columns for readability
    col_order = [
        member_col,
        'max_abs_N_kN',
        'max_abs_Vy_kN',
        'max_Mz_kNm',
        'min_Mz_kNm',
        'n_cases',
        'result_cases'
    ]
    summary_df = summary_df[[c for c in col_order if c in summary_df.columns]]

    # Ensure governing rows retains original column order + added metadata
    extra_cols = ['governing_type', 'governing_value', 'governing_column', 'result_case']
    govern_order = [c for c in df.columns if c not in extra_cols] + extra_cols
    governing_rows_df = governing_rows_df[[c for c in govern_order if c in governing_rows_df.columns]]

    return summary_df, governing_rows_df

def process_results(csv_path: str, output_summary: str = None, output_govern: str = None) -> Tuple[pd.DataFrame,
pd.DataFrame]:
    """
    Main processing pipeline:
      1. Load CSV
      2. Clean column names
      3. Convert numeric columns safely
      4. Create ResultCase
      5. Compute governing values and rows
      6. Optionally save to CSVs
    """
    # Step 1–2: Load and preprocess
    df = load_and_preprocess(csv_path)

    # Step 3: Identify and convert numeric columns
    # Use sensible defaults (adjust if needed)
    numeric_columns = [
        'position_m', 'n_kn', 'vy_kn', 'vz_kn',
        'mx_knm', 'my_knm', 'mz_knm'
    ]
    df = safe_convert_to_numeric(df, numeric_columns)

    # Step 4: Create ResultCase column
    df = create_result_case_column(df)

    # Drop rows where critical numeric columns are NaN (optional, but recommended)
    critical = ['n_kn', 'vy_kn', 'mz_knm']
    df = df.dropna(subset=critical, how='all')

    # Step 5: Compute governing values
    summary_df, governing_rows_df = compute_governing_values(df, member_col='member')

    # Step 6: Output to CSV if paths provided
    if output_summary:
        summary_df.to_csv(output_summary, index=False)
        print(f"Summary saved to: {output_summary}")
    if output_govern:
        governing_rows_df.to_csv(output_govern, index=False)
        print(f"Governing rows saved to: {output_govern}")

    return summary_df, governing_rows_df

# Example usage (uncomment and customize path)
if __name__ == "__main__":
    # Replace with your actual file path
    csv_file = "analysis_results.csv"

    # Run full pipeline and optionally save outputs
    summary, govern = process_results(
        csv_file,
        output_summary="summary_governing_values.csv",
        output_govern="governing_rows.csv"
    )

    # Display first few rows (for debugging/verification)
    print("\n=== SUMMARY BY MEMBER ===")
    print(summary.head())

    print("\n=== GOVERNING ROWS (sample) ===")
    print(govern.head(10))
```
### ✅ Key Features & Rationale:

1. **Robust Column Handling**
   - `clean_column_names()` normalizes names (lowercase, underscores, no duplicates), preventing case-sensitive
errors.

2. **Safe Numeric Conversion**
   - `safe_convert_to_numeric()` uses `pd.to_numeric(..., errors='coerce')` to safely handle non-numeric strings,
blanks, or text in numeric columns (e.g., `"N/A"` → `NaN`).

3. **ResultCase Logic**
   - `create_result_case_column()` intelligently uses `Combination` if present/valid, falls back to `Case`.
Handles mixed-case column names and trailing whitespace.

4. **Governing Value Extraction**
   - Uses `.idxmax()`/`.idxmin()` on each group to get exact rows of governing values — *not just the values*.
   - For `max abs Vy`/`max abs N`, computes `abs()` before `idxmax`.

5. **Two Output Tables**
   - `summary_df`: One row per member with min/max/Mz, max abs Vy, max abs N.
   - `governing_rows_df`: Full rows (all original columns + metadata: `governing_type`, `governing_value`,
`governing_column`).
   - Metadata helps trace *which* extreme value and *which* case it came from.

6. **Error Handling & Validation**
   - Checks for missing required columns (`member`, `case`, `combination`, analysis columns).
   - Drops completely empty/duplicate rows.
   - Ensures critical columns are non-null before analysis.

7. **Extensibility**
   - Easily extend `numeric_columns` or `required_cols` for other analysis variables.
   - Output files optional (comment out `output_summary`/`output_govern` to just get DataFrames).

### 📝 Tips for Use:
- Save this as `structural_results_processor.py`.
- If your CSV uses different column names (e.g., `Axial_kN`, `Mz_kNm`), adjust `numeric_columns` and
`required_cols` accordingly — the column-cleaning step will normalize them to match (e.g., `mz_knm`).
- For large datasets (>100k rows), consider `chunksize` or `dask`, but this is sufficient for typical analysis
exports.

Let me know if you'd like to add filters (e.g., only design combinations), group by member + section, or export to
Excel/Pandas Styling!

--------------------------------------------------------------------------------------------------------
## Output gemma4:31b-cloud

This is a common challenge in structural engineering workflows. Analysis software often exports "dirty" CSVs with
trailing spaces, mixed types, or empty cells.

The following code implements a robust pipeline. I have used a helper function to handle the "Governing Row"
logic, as finding the specific row index for multiple different metrics (max, min, and max-absolute) requires a
specific approach in pandas.

```python
import pandas as pd
import numpy as np

def process_structural_results(file_path):
    """
    Processes structural analysis CSV results to find governing
    member forces and the associated load cases.
    """
    # 1. Load the CSV
    # Using keep_default_na=False allows us to handle blank strings manually
    df = pd.read_csv(file_path, keep_default_na=False)

    # 2. Clean column names (strip trailing/leading whitespace)
    df.columns = df.columns.str.strip()

    # Remove complete duplicates
    df = df.drop_duplicates()

    # 3. Convert numeric columns safely
    # List of columns that must be numeric
    numeric_cols = ['Position_m', 'N_kN', 'Vy_kN', 'Vz_kN', 'Mx_kNm', 'My_kNm', 'Mz_kNm']

    for col in numeric_cols:
        if col in df.columns:
            # coerce turns non-numeric strings/blanks into NaN
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # 4. Create ResultCase: Use Combination if it exists and isn't empty, otherwise use Case
    # We treat empty strings as NaN to make fillna work
    df['Combination'] = df['Combination'].replace('', np.nan)
    df['Case'] = df['Case'].replace('', np.nan)
    df['ResultCase'] = df['Combination'].fillna(df['Case']).fillna('Unknown')

    # --- PREPARATION FOR GOVERNING ROWS ---
    # To find the row for "Max Absolute", we create temporary helper columns
    df['abs_Vy'] = df['Vy_kN'].abs()
    df['abs_N'] = df['N_kN'].abs()

    # 5. Aggregate Summary by Member
    # We group by Member and calculate the specific metrics requested
    summary = df.groupby('Member').agg({
        'Mz_kNm': ['max', 'min'],
        'abs_Vy': 'max',
        'abs_N': 'max'
    })

    # Flatten the multi-index columns from the aggregation
    summary.columns = ['Max_Mz', 'Min_Mz', 'Max_Abs_Vy', 'Max_Abs_N']
    summary = summary.reset_index()

    # 6. Identify Governing Rows
    # We find the index (row ID) where these maximums occur for each member
    idx_max_mz = df.groupby('Member')['Mz_kNm'].idxmax()
    idx_min_mz = df.groupby('Member')['Mz_kNm'].idxmin()
    idx_max_vy = df.groupby('Member')['abs_Vy'].idxmax()
    idx_max_n  = df.groupby('Member')['abs_N'].idxmax()

    # Combine all unique indices that represent a "governing" state
    all_governing_indices = pd.unique(np.concatenate([
        idx_max_mz, idx_min_mz, idx_max_vy, idx_max_n
    ]))

    # Extract the full rows for these indices
    governing_rows = df.loc[all_governing_indices].copy()

    # Cleanup: Remove the helper absolute columns before returning
    governing_rows = governing_rows.drop(columns=['abs_Vy', 'abs_N'])

    return summary, governing_rows

# ==========================================
# TEST BLOCK
# ==========================================
if __name__ == "__main__":
    # Creating a dummy CSV to demonstrate functionality
    import io
    csv_data = """Member,Case,Combination,Position_m,N_kN,Vy_kN,Vz_kN,Mx_kNm,My_kNm,Mz_kNm
B1,1, ,0, 10, 5, 0, 0, 0, 10
B1,2,Comb1,0, 12, -15, 0, 0, 0, 12
B1,3,Comb2,0, -20, 2, 0, 0, 0, -5
B2,1, ,0, 50, 0, 0, 0, 0, 5
B2,2,Comb1,0, 40, 10, 0, 0, 0, 20
B2,3,Comb2,0, 30, -25, 0, 0, 0, -10
B2,4, ,0, Invalid, 0, 0, 0, 0, 0
"""
    # Save to a local file for the function to read
    with open("analysis_results.csv", "w") as f:
        f.write(csv_data)

    try:
        summary_df, governing_df = process_structural_results("analysis_results.csv")

        print("--- Summary Table (Per Member) ---")
        print(summary_df.to_string(index=False))

        print("\n--- Governing Rows (Specific Cases) ---")
        print(governing_df[['Member', 'ResultCase', 'N_kN', 'Vy_kN', 'Mz_kNm']].to_string(index=False))

    except Exception as e:
        print(f"An error occurred: {e}")
```

### Key Technical Decisions Explained:

1.  **`keep_default_na=False`**: By default, pandas converts empty strings to `NaN`. In structural exports, we
often need to distinguish between a cell that is truly empty and one that contains a space. I've handled this by
loading them as strings and then explicitly replacing empty strings with `np.nan` to enable the `.fillna()` logic.
2.  **`pd.to_numeric(..., errors='coerce')`**: This is critical for structural data. If a software export includes
a note like `"Out of Range"` or `"Error"` in a numeric column, this function will turn that specific cell into a
`NaN` rather than crashing the entire script.
3.  **The Absolute Value Strategy**: To find the "Max Absolute" (e.g., the worst compression or tension), you
cannot simply use `.max()` because a value of `-100kN` is more critical than `+10kN`. I created temporary `abs_`
columns to find the index of the maximum absolute value, then returned the *original* signed value from the source
dataframe.
4.  **`idxmax()` vs `max()`**:
    *   `.max()` tells you the value (e.g., $12\text{ kNm}$).
    *   `.idxmax()` tells you the **row index** (e.g., Row 42). This allows us to retrieve the associated
`ResultCase` and `Position_m`.
5.  **Complexity**: The time complexity is $O(N)$ and the space complexity is $O(N)$, making it efficient for
files with hundreds of thousands of rows.

### Expected Output for the Test Data:
The summary will show the peak values for each member, and the governing rows table will show exactly which
`Combination` or `Case` produced those peaks, including the original signs of the forces.
