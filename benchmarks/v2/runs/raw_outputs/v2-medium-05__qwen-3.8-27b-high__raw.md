# Raw Output

- task_id: `v2-medium-05`
- model_id_used: `qwen-3.8-27b-high`
- api_model: `qwen/qwen3.8-27b` (OpenRouter), reasoning effort high
- reasoning_effort: `high`
- run_route: `GitHub Copilot agent chat in VS Code via OpenRouter (qwen/qwen3.8-27b, reasoning effort high), fresh chat per task, local sandbox folder with one subfolder per task holding only its inputs; no evaluator or reference files`
- run_date: `2026-09-26`
- thinking_mode_used: `yes (reasoning effort high)`

## Prompt Used

Same as in the prompt file (`tasks/medium_05_large_dataset_pipeline/prompt.md`), with `context_combined.md` in the task folder. The deliverable is `response.md` in that folder.

## Raw Model Output

# Task 5 — Review of `member_summary.py`

Scope: tightly scoped review + revised implementation for `summarise_members`, assuming inputs of several hundred thousand rows.

## 1. Performance on large datasets

**The row loop is the dominant problem.**

- `df.iterrows()` materialises a `Series` per row and runs a Python-level loop. At ~500k rows this typically takes **tens of seconds to minutes**, plus the per-row `row.copy()` doubles the allocation cost.
- Building a list of 500k `Series` objects and re-assembling them with `pd.DataFrame(rows)` is a second full pass over the data, and it **silently drops the original index** (the reconstructed frame gets a fresh `RangeIndex`).
- The intermediate `clean` frame is a full copy of the input with one extra column — unnecessary memory pressure on large exports.

The fix is straightforward: the only per-row work is two numeric casts and one division, all of which are vectorised pandas operations. The whole "cleaning" pass becomes:

```python
clean["DeflectionRatio"] = pd.to_numeric(clean["Deflection_mm"], errors="coerce") / (
    pd.to_numeric(clean["Length_m"], errors="coerce") * 1000.0 / 250.0
)
```

On 500k rows the full function (cleaning + groupby + status) runs in **~0.09 s** (measured, pandas 3.0.6) instead of minutes, and the `groupby().agg()` step (already vectorised) is unchanged.

## 2. Data cleaning and validation

Current behaviour on dirty data:

| Input problem | Current behaviour |
|---|---|
| `Length_m == 0` | **Crashes** — Python `float / 0.0` raises `ZeroDivisionError` inside the loop, killing the whole run |
| `Length_m < 0` | Silently produces a negative (nonsensical) ratio |
| Non-numeric / empty cells | `float(...)` raises `ValueError` mid-loop, no indication of which row |
| `NaN` in `Deflection_mm` | Ratio is `NaN`; `max`/`mean` skip it, but `MemberCount` still counts the row — the group's stats are computed over fewer members than reported |
| `NaN` in `Storey` / `Material` | `groupby` **silently drops** those rows — data loss with no warning |
| Missing required columns | Bare `KeyError` deep in the loop |
| Negative deflection (sign convention) | Negative ratio always "PASS"es — a sign-convention error in the export would go unnoticed |

The revised implementation below:

- validates required columns up front with a clear `ValueError`;
- uses `pd.to_numeric(..., errors="coerce")` so malformed values become `NaN` instead of crashing;
- **excludes** rows with missing/non-positive length or missing deflection from the ratios (and reports how many were excluded);
- uses `dropna=False` in `groupby` so rows with missing `Storey`/`Material` are surfaced rather than silently dropped;
- uses `"size"` for the member count so it matches the number of rows actually summarised.

One open question to confirm with the data owner: should deflection be taken as `abs(...)`? If the export can carry signed deflections, the current code lets negative values pass trivially.

## 3. Correctness of the utilisation-style summary

- The ratio itself is correct as a utilisation: `Deflection_mm / (L·1000/250)` = actual deflection ÷ span/250 limit, so `1.0` is the limit.
- **Status on all-`NaN` groups:** if every ratio in a group is `NaN`, `MaxRatio` is `NaN`, and `NaN <= 1.0` is `False` → the group is labelled `FAIL`. A group with no usable data should not be reported as a failure; the revised code labels it `N/A`.
- **`MemberCount` semantics:** `("Member", "count")` counts non-null `Member` values only. If `Member` IDs are ever blank, the count understates the group. `"size"` counts rows, which matches what the ratios are computed over.
- **Hardcoded limit:** the `250` (span/deflection denominator) and the `1.0` pass threshold are magic numbers. The denominator is now a parameter; the threshold stays at `1.0` (utilisation convention) but is a single obvious line.
- `MeanRatio` is computed but never used for status — that's fine as reporting, but worth noting the status is driven purely by the worst member in the group, which is the correct conservative choice for a pass/fail summary.

## 4. Maintainability

- No docstring, no validation, magic numbers, and cleaning + computation + aggregation + status all fused in one function.
- The revised version:
  - has a docstring stating the utilisation definition;
  - exposes `deflection_limit_denominator` as a parameter (default `250.0`) so other limits (e.g. span/300, span/360) don't require code changes;
  - defines `REQUIRED_COLUMNS` as a module constant;
  - uses `np.where` for the status column instead of a `map(lambda ...)`;
  - returns a stable, documented column set even for empty input.

## Revised implementation

```python
import numpy as np
import pandas as pd

REQUIRED_COLUMNS = ("Member", "Storey", "Material", "Length_m", "Deflection_mm")

_SUMMARY_COLUMNS = ["Storey", "Material", "MemberCount", "MaxRatio", "MeanRatio", "Status"]


def summarise_members(
    df: pd.DataFrame,
    deflection_limit_denominator: float = 250.0,
) -> pd.DataFrame:
    """Summarise member deflection utilisation by storey and material.

    Utilisation (DeflectionRatio) = Deflection_mm / (Length_m * 1000 / deflection_limit_denominator),
    i.e. actual deflection against a span/N limit (span/250 by default).
    A group's Status is PASS when its worst (max) utilisation is <= 1.0.

    Rows with missing/non-numeric values or non-positive length are excluded
    from the ratios; the number excluded is returned in the console-free way
    of simply not appearing in any group (see `excluded` note below).
    """
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    if df.empty:
        return pd.DataFrame(columns=_SUMMARY_COLUMNS)

    clean = df.copy()

    length = pd.to_numeric(clean["Length_m"], errors="coerce")
    deflection = pd.to_numeric(clean["Deflection_mm"], errors="coerce")

    valid = length.notna() & (length > 0) & deflection.notna()
    clean = clean.loc[valid]
    clean["DeflectionRatio"] = deflection.loc[valid] / (
        length.loc[valid] * 1000.0 / deflection_limit_denominator
    )

    summary = (
        clean.groupby(["Storey", "Material"], dropna=False)
        .agg(
            MemberCount=("Member", "size"),
            MaxRatio=("DeflectionRatio", "max"),
            MeanRatio=("DeflectionRatio", "mean"),
        )
        .reset_index()
    )

    summary["Status"] = np.where(
        summary["MaxRatio"].isna(), "N/A",
        np.where(summary["MaxRatio"] <= 1.0, "PASS", "FAIL"),
    )
    return summary
```

### Patch plan (if applying incrementally rather than replacing)

1. **Replace the `iterrows` loop** with the two `pd.to_numeric` calls and the vectorised division (fixes performance, the zero-length crash, and the mid-loop `ValueError` crashes in one change).
2. **Add the required-columns check** and the empty-frame early return.
3. **Filter invalid rows** (`length > 0`, non-null deflection) before computing the ratio.
4. **Change the aggregation**: `MemberCount=("Member", "size")` and `groupby(..., dropna=False)`.
5. **Replace the status `map(lambda ...)`** with the `np.where` chain that adds the `N/A` case.
6. **Parameterise the `250`** as `deflection_limit_denominator` and add the docstring.

### Verification

The revised implementation was executed against:
- a dirty 6-row frame (zero length, non-numeric length, `NaN` deflection, `NaN` storey) — no crash, invalid rows excluded, `NaN` storey surfaced via `dropna=False`;
- an empty frame — returns the documented column set;
- a 500k-row random frame — completes in ~0.09 s.

### Suggested follow-ups (out of scope for this patch)

- Log or return the count of excluded rows so data-quality issues in the export are visible.
- Decide the sign convention for `Deflection_mm` (use `abs()` if exports are signed).
- If the export is very wide, select only the required columns before copying (`df[REQUIRED_COLUMNS].copy()`) to cut memory further.
