TASK:
"Write Python code to analyse a large structural results DataFrame and produce a concise engineering review output.

Input columns:
Project
Member
Storey
LoadCase
Mz_kNm
Vy_kN
Deflection_mm
Length_m
Material

Requirements:
1. Group by Storey and Material.
2. Calculate:
   - count of members
   - max absolute Mz_kNm
   - max absolute Vy_kN
   - max Deflection_mm
   - mean Deflection_mm
3. Create a utilisation-style metric called DeflectionRatio = Deflection_mm / (Length_m * 1000 / 250)
   and find the max DeflectionRatio per Storey.
4. Produce a summary DataFrame.
5. Plot:
   - bar chart of max absolute Mz by Storey
   - bar chart of max DeflectionRatio by Storey
6. Keep the code clean and structured, with reusable functions.

Assume the dataset may be large, so avoid unnecessary copies and inefficient loops."

## Output — Qwen3.5 27B:
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple

# Set plotting style for better readability
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10


def add_engineering_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates vectorized engineering metrics required for analysis.
    Avoids loops for performance on large datasets.

    Args:
        df: Input DataFrame with structural results.

    Returns:
        DataFrame with additional metric columns.
    """
    # Create a copy to avoid SettingWithCopyWarning if the input is a slice
    # However, for memory efficiency on large data, we operate directly if possible.
    # Here we assume df is the main object to be processed.

    # 1. Absolute Values for Forces/Moments
    df['Abs_Mz_kNm'] = df['Mz_kNm'].abs()
    df['Abs_Vy_kN'] = df['Vy_kN'].abs()

    # 2. Deflection Ratio (Utilisation)
    # Limit = Length_m * 1000 / 250 (Converting m to mm for L/250 criteria)
    # Avoid division by zero
    length_mm = df['Length_m'] * 1000
    limit_mm = length_mm / 250.0

    # Calculate ratio, handle potential zero lengths safely
    df['DeflectionRatio'] = np.where(
        limit_mm > 0,
        df['Deflection_mm'] / limit_mm,
        0.0
    )

    return df


def generate_summary_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Groups data by Storey and Material and calculates required statistics.

    Args:
        df: DataFrame with engineering metrics (output of add_engineering_metrics).

    Returns:
        Summary DataFrame indexed by Storey and Material.
    """
    # Define aggregation operations
    agg_config = {
        'Member': 'count',                  # Count of members
        'Abs_Mz_kNm': 'max',                # Max absolute Mz
        'Abs_Vy_kN': 'max',                 # Max absolute Vy
        'Deflection_mm': ['max', 'mean'],   # Max and Mean Deflection
        'DeflectionRatio': 'max'            # Max Utilisation Ratio
    }

    # Perform GroupBy
    summary = df.groupby(['Storey', 'Material']).agg(agg_config)

    # Flatten column names for cleaner output
    summary.columns = [
        'Member_Count',
        'Max_Abs_Mz_kNm',
        'Max_Abs_Vy_kN',
        'Max_Deflection_mm',
        'Mean_Deflection_mm',
        'Max_DeflectionRatio'
    ]

    # Reset index to make Storey and Material columns accessible
    summary = summary.reset_index()

    return summary


def plot_engineering_review(summary_df: pd.DataFrame) -> None:
    """
    Generates bar charts for Storey-level Max Moment and Max Deflection Ratio.
    Aggregates the detailed summary to Storey level for plotting.

    Args:
        summary_df: The detailed summary DataFrame (Storey + Material).
    """
    # Aggregate to Storey level for plotting (Req 5: "by Storey")
    # We take the max across materials for each storey to find the critical case
    storey_plot_data = summary_df.groupby('Storey').agg({
        'Max_Abs_Mz_kNm': 'max',
        'Max_DeflectionRatio': 'max'
    }).reset_index()

    # Sort by Storey to ensure logical order (assuming Storey can be sorted)
    try:
        storey_plot_data = storey_plot_data.sort_values('Storey')
    except TypeError:
        # Fallback if Storey is string mixed types
        storey_plot_data = storey_plot_data.sort_values('Storey', key=lambda x: x)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Plot 1: Max Absolute Mz by Storey
    ax1.bar(storey_plot_data['Storey'].astype(str),
            storey_plot_data['Max_Abs_Mz_kNm'],
            color='steelblue', edgecolor='black')
    ax1.set_title('Max Absolute Bending Moment (Mz) by Storey')
    ax1.set_xlabel('Storey')
    ax1.set_ylabel('Moment (kNm)')
    ax1.tick_params(axis='x', rotation=45)

    # Add value labels
    for i, v in enumerate(storey_plot_data['Max_Abs_Mz_kNm']):
        ax1.text(i, v, f'{v:.1f}', ha='center', va='bottom', fontsize=8)

    # Plot 2: Max Deflection Ratio by Storey
    # Add a reference line for L/250 limit (Ratio = 1.0)
    ax2.bar(storey_plot_data['Storey'].astype(str),
            storey_plot_data['Max_DeflectionRatio'],
            color='coral', edgecolor='black')
    ax2.axhline(y=1.0, color='red', linestyle='--', linewidth=2, label='L/250 Limit')
    ax2.set_title('Max Deflection Ratio (Utilisation) by Storey')
    ax2.set_xlabel('Storey')
    ax2.set_ylabel('Deflection Ratio (Defl / Limit)')
    ax2.tick_params(axis='x', rotation=45)
    ax2.legend()

    # Add value labels
    for i, v in enumerate(storey_plot_data['Max_DeflectionRatio']):
        ax2.text(i, v, f'{v:.2f}', ha='center', va='bottom', fontsize=8)

    plt.tight_layout()
    plt.show()


def run_structural_review(df: pd.DataFrame) -> pd.DataFrame:
    """
    Main orchestration function to run the analysis pipeline.

    Args:
        df: Raw structural results DataFrame.

    Returns:
        The detailed summary DataFrame.
    """
    # 1. Preprocess (Vectorized calculations)
    df_processed = add_engineering_metrics(df)

    # 2. Generate Summary (Group by Storey & Material)
    summary_df = generate_summary_dataframe(df_processed)

    # 3. Plot Results (Aggregated by Storey)
    plot_engineering_review(summary_df)

    return summary_df


if __name__ == "__main__":
    # ------------------------------------------------------------------
    # Mock Data Generation for Demonstration
    # ------------------------------------------------------------------
    np.random.seed(42)
    n_rows = 10000  # Simulating a large dataset

    data = {
        'Project': 'Project_Alpha',
        'Member': [f'BM-{i}' for i in range(n_rows)],
        'Storey': np.random.choice(['L01', 'L02', 'L03', 'L04', 'Roof'], n_rows),
        'LoadCase': np.random.choice(['DL', 'LL', 'WL'], n_rows),
        'Mz_kNm': np.random.uniform(-500, 500, n_rows),
        'Vy_kN': np.random.uniform(-200, 200, n_rows),
        'Deflection_mm': np.random.uniform(1, 50, n_rows),
        'Length_m': np.random.choice([4.0, 6.0, 8.0, 10.0], n_rows),
        'Material': np.random.choice(['Steel', 'Concrete', 'Timber'], n_rows)
    }

    df_input = pd.DataFrame(data)

    # ------------------------------------------------------------------
    # Execute Analysis
    # ------------------------------------------------------------------
    print("Starting Structural Review Analysis...")
    try:
        final_summary = run_structural_review(df_input)

        # Display first few rows of the summary
        print("\n--- Detailed Summary (Storey & Material) ---")
        print(final_summary.to_string(index=False))

        # Quick Storey Level Check for Console Output
        print("\n--- Storey Level Critical Check ---")
        storey_critical = final_summary.groupby('Storey')[['Max_Abs_Mz_kNm', 'Max_DeflectionRatio']].max()
        print(storey_critical.to_string())

    except Exception as e:
        print(f"An error occurred during analysis: {e}")
```

### Key Features of this Implementation:

1.  **Efficiency & Vectorization:**
    *   Uses `numpy` operations (`np.where`, `.abs()`) for column creation instead of `apply` or loops. This is
crucial for large DataFrames.
    *   Calculates metrics *before* grouping. This ensures the groupby aggregation is simple and fast (`max`,
`mean`, `count`).

2.  **Modular Structure:**
    *   `add_engineering_metrics`: Handles raw data transformation.
    *   `generate_summary_dataframe`: Handles the specific grouping logic (Req 1 & 2).
    *   `plot_engineering_review`: Handles visualization logic (Req 5), re-aggregating the summary to Storey-level
specifically for the charts.
    *   `run_structural_review`: Orchestrates the pipeline.

3.  **Requirement Compliance:**
    *   **Grouping:** Groups by `Storey` and `Material`.
    *   **Metrics:** Calculates Count, Max Abs Mz/Vy, Max/Mean Deflection.
    *   **Deflection Ratio:** Implements $Deflection / (Length \times 1000 / 250)$ and finds the max.
    *   **Plots:** Produces two distinct bar charts (Moment and Ratio) aggregated by Storey.
    *   **Clean Code:** Includes type hints, docstrings, and separates data logic from plotting logic.

4.  **Robustness:**
    *   Handles potential division by zero in the Deflection Ratio calculation.
    *   Flattens MultiIndex columns after aggregation for easier downstream use.
    *   Includes a mock data generator to verify the code runs immediately.

5.  **Visualization:**
    *   Adds a reference line at 1.0 for the Deflection Ratio plot to immediately highlight failures (Ratio > 1).
    *   Adds data labels to bars for precise engineering review.
    *   Uses `tight_layout` to prevent label clipping.
------------------------------------------------------------------------------------------------------------------
## Output — Qwen3-Coder-Next:
Here's clean, efficient, and scalable Python code using `pandas` and `matplotlib` to analyze structural results.
The implementation avoids unnecessary copies, uses vectorized operations, and is structured with reusable
functions.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Optional

def compute_utilisation_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute utilisation metrics (max utilisation ratio and max deflection ratio)
    and aggregate structural results per Storey and Material.
    """
    # Ensure necessary columns exist
    required_cols = {'Storey', 'Material', 'Mz_kNm', 'Vy_kN', 'Deflection_mm', 'Length_m'}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"Missing required columns: {required_cols - set(df.columns)}")

    # Compute DeflectionRatio: Deflection (mm) / [L (mm) / 250] = Deflection / (L_m * 1000 / 250)
    # = Deflection / (L_m * 4) → simplified: DeflectionRatio = Deflection_mm / (Length_m * 1000 / 250)
    df = df.assign(
        AbsMz=np.abs(df['Mz_kNm']),
        AbsVy=np.abs(df['Vy_kNm']),
        DeflectionRatio=df['Deflection_mm'] / (df['Length_m'] * 1000 / 250)
    )

    # Group by Storey and Material, compute aggregates
    agg_df = (
        df.groupby(['Storey', 'Material'], as_index=False)
        .agg(
            MemberCount=('Member', 'count'),
            MaxAbsMz_kNm=('AbsMz', 'max'),
            MaxAbsVy_kN=('AbsVy', 'max'),
            MaxDeflection_mm=('Deflection_mm', 'max'),
            MeanDeflection_mm=('Deflection_mm', 'mean'),
            MaxDeflectionRatio=('DeflectionRatio', 'max')
        )
    )
    return agg_df


def compute_storey_summary(agg_df: pd.DataFrame) -> pd.DataFrame:
    """
    Further aggregate per Storey to produce final summary: pick worst-case per Storey (max Mz or max
DeflectionRatio).
    """
    # Get storey-level max of MaxAbsMz_kNm and MaxDeflectionRatio (representing critical members)
    summary = (
        agg_df
        .groupby('Storey', as_index=False)
        .agg(
            TotalMembers=('MemberCount', 'sum'),
            MaxAbsMz_kNm=('MaxAbsMz_kNm', 'max'),
            MaxAbsVy_kN=('MaxAbsVy_kN', 'max'),
            MaxDeflection_mm=('MaxDeflection_mm', 'max'),
            MeanDeflection_mm=('MeanDeflection_mm', 'mean'),
            MaxDeflectionRatio=('MaxDeflectionRatio', 'max')
        )
        # Sort by Storey numerically/lexicographically (if numeric, sort numerically)
        .sort_values('Storey', key=lambda s: pd.to_numeric(s, errors='ignore'))
        .reset_index(drop=True)
    )
    return summary


def plot_storey_results(
    storey_summary: pd.DataFrame,
    value_col: str,
    ylabel: str,
    title: str,
    color: str = 'steelblue',
    ax: Optional[plt.Axes] = None
) -> plt.Axes:
    """
    Generic bar plot helper for storey-level metrics.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 4))

    storey = storey_summary['Storey'].astype(str)  # Convert to string for cleaner labels
    values = storey_summary[value_col]

    bars = ax.bar(storey, values, color=color, edgecolor='black', linewidth=0.5)

    ax.set_xlabel('Storey')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.tick_params(axis='x', rotation=0)

    # Add value labels on bars
    for bar, val in zip(bars, values):
        if pd.notna(val):
            ax.text(
                bar.get_x() + bar.get_width()/2,
                bar.get_height() + 0.02 * max(values) if len(values) > 0 else 0,
                f"{val:.2f}",
                ha='center',
                va='bottom',
                fontsize=8
            )
    return ax


def analyze_structural_results(df: pd.DataFrame, plot_figures: bool = True) -> Tuple[pd.DataFrame,
Optional[plt.Figure]]:
    """
    Main analysis function.
    Returns:
        - Summary DataFrame per storey
        - Figure if plot_figures=True, else None
    """
    if df.empty:
        raise ValueError("Input DataFrame is empty.")

    # Step 1: Compute detailed aggregates (Storey × Material)
    agg_df = compute_utilisation_metrics(df)

    # Step 2: Storey-level summary (for review)
    summary_df = compute_storey_summary(agg_df)

    # Step 3: Optional plotting
    fig = None
    if plot_figures:
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))

        # Plot 1: Max absolute Mz by Storey
        plot_storey_results(
            summary_df,
            'MaxAbsMz_kNm',
            ylabel='Max |Mz| (kN·m)',
            title='Storey-wise Maximum Absolute Moment (Mz)',
            color='tab:blue',
            ax=axes[0]
        )

        # Plot 2: Max DeflectionRatio by Storey (utilization-style metric)
        plot_storey_results(
            summary_df,
            'MaxDeflectionRatio',
            ylabel='Deflection Ratio',
            title='Storey-wise Maximum Deflection Ratio',
            color='tab:orange',
            ax=axes[1]
        )

        fig.suptitle('Structural Review Summary', fontsize=14, fontweight='bold')
        fig.tight_layout()

    return summary_df, fig


# Example usage (uncomment and replace with your actual data loading):
# if __name__ == "__main__":
#     # Load large dataset efficiently (e.g., from CSV, SQL, etc.)
#     # df = pd.read_csv('large_results.csv', dtype={'Storey': str})
#     # For demo, create synthetic data:
#     np.random.seed(42)
#     n = 5000
#     df = pd.DataFrame({
#         'Project': ['P1'] * n,
#         'Member': [f'M{i}' for i in range(n)],
#         'Storey': np.repeat([f'F{i}' for i in range(1, 11)], 500),
#         'LoadCase': np.random.choice(['Dead', 'Live', 'Wind', 'Seismic'], n),
#         'Mz_kNm': np.random.normal(100, 50, n),
#         'Vy_kN': np.random.normal(20, 5, n),
#         'Deflection_mm': np.abs(np.random.exponential(5, n)),
#         'Length_m': np.random.uniform(3, 6, n),
#         'Material': np.random.choice(['Concrete', 'Steel'], n)
#     })
#
#     summary, fig = analyze_structural_results(df, plot_figures=True)
#     print(summary.to_string(index=False))
#     if fig:
#         plt.show()
```

---

### Key Features & Design Choices:

- ✅ **Efficiency**:
  - Uses vectorized `assign`, `np.abs`, and `groupby().agg()` instead of loops.
  - No unnecessary `copy()` calls; modifies only a single `df` copy if needed.

- ✅ **Engineering Utility**:
  - `DeflectionRatio = Deflection / (L/250)` is a common serviceability check (L in mm, deflection in mm).
  - Aggregates per **Storey + Material** for targeted review (e.g., concrete vs. steel).
  - Final storey summary picks worst-case (most critical) member metrics.

- ✅ **Clarity & Reusability**:
  - Modular functions for plotting, aggregation, and analysis.
  - Type hints, docstrings, and input validation.
  - Plots auto-scale and annotate for quick interpretation.

- ✅ **Scalability**:
  - Designed to handle large DataFrames (uses `pandas` C-based operations).
  - Optional plotting to avoid overhead when only summary is needed.

> **Note**: For truly *very* large datasets (>10M rows), consider using `dask.dataframe` or chunked processing —
but this implementation is optimal for typical structural datasets (<1M rows).

--------------------------------------------------------------------------------
## Output gemma4:31b-cloud:
To handle large datasets efficiently in Python, the best approach is to use **Pandas** with vectorized operations
and the `.agg()` method for grouping.

Below is the complete professional implementation. I have included a section to generate a synthetic dataset so
you can run the code immediately.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def generate_sample_data(rows=10000):
    """Generates a synthetic structural results dataset for demonstration."""
    np.random.seed(42)
    storeys = ['Basement', 'L1', 'L2', 'L3', 'Roof']
    materials = ['S355 Steel', 'C30/37 Concrete']

    df = pd.DataFrame({
        'Project': 'Project_X',
        'Member': [f'M{i}' for i in range(rows)],
        'Storey': np.random.choice(storeys, rows),
        'LoadCase': np.random.choice(['Dead', 'Live', 'Wind'], rows),
        'Mz_kNm': np.random.uniform(-100, 100, rows),
        'Vy_kN': np.random.uniform(-50, 50, rows),
        'Deflection_mm': np.random.uniform(0, 30, rows),
        'Length_m': np.random.uniform(3, 6, rows),
        'Material': np.random.choice(materials, rows)
    })
    return df

def process_structural_data(df):
    """
    Performs engineering analysis on the structural results DataFrame.
    """
    # 1. Vectorized calculation of absolute values and Deflection Ratio
    # Formula: DeflectionRatio = Deflection / (Length_mm / 250)
    # This is done before grouping to maintain member-level granularity
    df = df.assign(
        abs_Mz = df['Mz_kNm'].abs(),
        abs_Vy = df['Vy_kN'].abs(),
        DeflectionRatio = df['Deflection_mm'] / ((df['Length_m'] * 1000) / 250)
    )

    # 2. Group by Storey and Material and apply aggregations
    summary = df.groupby(['Storey', 'Material']).agg({
        'Member': 'count',
        'abs_Mz': 'max',
        'abs_Vy': 'max',
        'Deflection_mm': ['max', 'mean'],
        'DeflectionRatio': 'max'
    })

    # Flatten the multi-index columns resulting from .agg()
    summary.columns = [
        'Member_Count', 'Max_Mz_kNm', 'Max_Vy_kN',
        'Max_Deflection_mm', 'Mean_Deflection_mm', 'Max_DeflectionRatio'
    ]

    return summary

def plot_engineering_results(summary_df):
    """
    Produces visualisations for the engineering review.
    """
    # To plot by Storey, we need to handle the MultiIndex (Storey, Material)
    # We will group by Storey only for the charts to see the overall building profile
    storey_summary = summary_df.groupby(level='Storey').max()

    # Ensure storeys are sorted logically (Basement -> Roof)
    storey_order = ['Basement', 'L1', 'L2', 'L3', 'Roof']
    storey_summary = storey_summary.reindex(storey_order)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Plot 1: Max Moment by Storey
    storey_summary['Max_Mz_kNm'].plot(kind='bar', ax=axes[0], color='skyblue', edgecolor='black')
    axes[0].set_title('Max Absolute Moment ($M_z$) per Storey', fontweight='bold')
    axes[0].set_ylabel('kNm')
    axes[0].grid(axis='y', linestyle='--', alpha=0.7)

    # Plot 2: Max Deflection Ratio by Storey
    storey_summary['Max_DeflectionRatio'].plot(kind='bar', ax=axes[1], color='salmon', edgecolor='black')
    axes[1].axhline(y=1.0, color='red', linestyle='-', label='Limit (L/250)')
    axes[1].set_title('Max Deflection Ratio per Storey', fontweight='bold')
    axes[1].set_ylabel('Ratio ($\delta / (\delta_{limit})$)')
    axes[1].legend()
    axes[1].grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()

# ==========================================
# Main Execution
# ==========================================
if __name__ == "__main__":
    # Load data
    raw_data = generate_sample_data(20000) # Simulating a large dataset

    # Analysis
    engineering_summary = process_structural_data(raw_data)

    # Display Summary Table
    print("\n--- Engineering Review Summary ---")
    print(engineering_summary)

    # Visualise
    plot_engineering_results(engineering_summary)
```

### Engineering & Technical Explanations:

#### 1. Computational Efficiency (Time & Space Complexity)
*   **Avoided Loops:** I used `.assign()` and vectorized NumPy operations. Using `for index, row in df.iterrows()`
on a large structural dataset (e.g., 100k members) would be orders of magnitude slower.
*   **Aggregated Grouping:** The `.groupby().agg()` pattern is the most memory-efficient way to reduce a large
dataset into a summary table. It processes the data in blocks rather than creating intermediate temporary
DataFrames.
*   **Complexity:** The time complexity is $O(N)$ where $N$ is the number of members.

#### 2. Engineering Logic
*   **Absolute Values:** In structural design, the magnitude of the force (Moment or Shear) is typically more
critical for member sizing than the sign (direction), hence the use of `abs()`.
*   **Deflection Ratio:** The formula $\frac{\delta}{L/250}$ converts the absolute deflection into a percentage of
the allowable limit. A value $> 1.0$ immediately alerts the engineer that the member fails the serviceability
limit state (SLS).
*   **Storey Sorting:** Structural data is often alphabetical (L1, L2, L10), which sorts incorrectly (L1, L10,
L2). I implemented a `storey_order` list to ensure the charts represent the actual building height.

#### 3. Output Description
*   **The Summary Table:** Provides a concise "snapshot" grouped by material and level. This allows the engineer
to see if, for example, the Steel members on Level 3 are performing worse than the Concrete ones.
*   **The Plots:**
    *   **Chart 1:** Identifies the most heavily loaded floor.
    *   **Chart 2:** Specifically highlights "red flags" by plotting a horizontal limit line at $1.0$.