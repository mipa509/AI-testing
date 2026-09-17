# Raw Output

- task_id: `v2-medium-05`
- model_id_used: `gpt5.6-luna-max`
- api_model: `gpt-5.6-luna`
- reasoning_effort: `max`
- run_route: `Codex VS Code extension, fresh session, empty sandbox workspace; inputs from neutral copy (D:\bench-inputs\task6)`
- run_date: `2026-09-17`
- thinking_mode_used: `yes (reasoning effort max)`

## Prompt Used

Same as in the prompt file (`tasks/medium_05_large_dataset_pipeline/prompt.md`), sent as message 1. `tasks/medium_05_large_dataset_pipeline/context_combined.md` sent as message 2.

## Context Files Shared

- `context/member_summary.py`

## Raw Model Output

Recommendation: replace the row loop with vectorized preparation and explicit validation.

```py
import numpy as np
import pandas as pd


_REQUIRED = ("Storey", "Material", "Member", "Length_m", "Deflection_mm")
_KEYS = ("Storey", "Material", "Member")
_NUMERIC = ("Length_m", "Deflection_mm")
_DEFLECTION_LIMIT = 250.0


def summarise_members(df: pd.DataFrame) -> pd.DataFrame:
    """Summarise member deflection utilisation against an L/250 limit.

    Deflection is treated as a magnitude. Invalid required values fail fast.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")

    missing = [column for column in _REQUIRED if column not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Select only required columns and avoid modifying the caller's DataFrame.
    clean = df.loc[:, _REQUIRED].copy()

    for column in _NUMERIC:
        clean[column] = pd.to_numeric(clean[column], errors="coerce")

    for column in _KEYS:
        clean[column] = clean[column].astype("string").str.strip()

    invalid = clean[list(_KEYS)].isna().any(axis=1)
    invalid |= clean[list(_KEYS)].eq("").fillna(False).any(axis=1)
    invalid |= clean[list(_NUMERIC)].isna().any(axis=1)
    invalid |= clean[list(_NUMERIC)].isin([np.inf, -np.inf]).any(axis=1)
    invalid |= clean["Length_m"].le(0).fillna(False)

    if invalid.any():
        examples = clean.index[invalid][:5].tolist()
        raise ValueError(
            f"{int(invalid.sum())} invalid row(s); "
            f"check keys, finite numeric values, and Length_m > 0. "
            f"Example indices: {examples}"
        )

    # allowable deflection = length in mm / 250
    clean["DeflectionRatio"] = (
        clean["Deflection_mm"].abs() * _DEFLECTION_LIMIT
        / (clean["Length_m"] * 1000.0)
    )

    summary = (
        clean.groupby(["Storey", "Material"], sort=False, observed=True)
        .agg(
            # Assumes one result row per member.
            MemberCount=("Member", "count"),
            MaxRatio=("DeflectionRatio", "max"),
            MeanRatio=("DeflectionRatio", "mean"),
        )
        .reset_index()
    )

    summary["Status"] = np.where(
        summary["MaxRatio"] <= 1.0,
        "PASS",
        "FAIL",
    )
    return summary
```

Review findings:

- Performance: `iterrows()`, per-row copying, and constructing a list of `Series` are expensive for hundreds of thousands of rows. Vectorized conversion and arithmetic require one compact copy and one groupby.
- Cleaning and validation: the original silently allows `NaN` values and silently drops rows with missing grouping keys. The revised version rejects missing/invalid keys, non-finite values, and non-positive lengths.
- Correctness: the original ratio is dimensionally correct for an L/250 limit, but signed deflections can produce a misleading pass. Using `abs()` makes the summary govern on deflection magnitude. `Status` correctly depends on `MaxRatio`, not `MeanRatio`.
- `MemberCount`: the implementation preserves the original row-count behaviour. If exports can contain multiple rows per member, use `nunique` and define whether ratios should first be reduced to one governing row per member.
- Maintainability: named constants, a docstring specifying units and assumptions, no input mutation, and vectorized status logic make the behaviour easier to test and change.

Tests should cover the exact boundary (`MaxRatio == 1.0`), negative deflection, invalid/missing fields, zero length, empty input, duplicate members, and preservation of the input DataFrame.
