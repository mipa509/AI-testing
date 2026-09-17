# Raw Output

- task_id: `v2-medium-05`
- model_id_used: `gpt5.6-sol-xhigh`
- api_model: `gpt-5.6-sol`
- reasoning_effort: `xhigh`
- run_route: `Codex VS Code extension, fresh session, empty sandbox workspace; inputs from neutral copy (D:\bench-inputs\task6)`
- run_date: `2026-09-17`
- thinking_mode_used: `yes (reasoning effort xhigh)`

## Prompt Used

Same as in the prompt file (`tasks/medium_05_large_dataset_pipeline/prompt.md`), sent as message 1. `tasks/medium_05_large_dataset_pipeline/context_combined.md` sent as message 2.

## Context Files Shared

- `context/member_summary.py`

## Raw Model Output

The main issues are the row-by-row Python loop and ambiguous aggregation grain. For structural results, the safer interpretation is: calculate absolute utilisation per result row, envelope each member across its results, then summarise those governing member values.

```py
from __future__ import annotations

import warnings
from typing import Literal

import numpy as np
import pandas as pd


_REQUIRED_COLUMNS = (
    "Member",
    "Storey",
    "Material",
    "Length_m",
    "Deflection_mm",
)
_MEMBER_KEYS = ("Storey", "Material", "Member")


def summarise_members(
    df: pd.DataFrame,
    *,
    span_ratio_limit: float = 250.0,
    errors: Literal["raise", "drop"] = "raise",
) -> pd.DataFrame:
    """
    Summarise governing deflection utilisation by storey and material.

    DeflectionRatio is:

        abs(deflection_mm) / (length_m * 1000 / span_ratio_limit)

    Multiple result rows for the same member are first reduced to that
    member's maximum ratio. MeanRatio is therefore the mean of governing
    member ratios, not the mean of all raw result rows.

    Invalid rows raise by default. With errors="drop", invalid rows are
    removed and a warning is emitted.
    """
    if errors not in {"raise", "drop"}:
        raise ValueError("errors must be either 'raise' or 'drop'")

    if not np.isfinite(span_ratio_limit) or span_ratio_limit <= 0:
        raise ValueError("span_ratio_limit must be a positive finite number")

    missing_columns = [
        column for column in _REQUIRED_COLUMNS if column not in df.columns
    ]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    # Only copy columns needed by the calculation. This matters for wide exports.
    work = df.loc[:, _REQUIRED_COLUMNS].copy()

    # Normalise textual identifiers without converting numeric identifiers.
    for column in _MEMBER_KEYS:
        dtype = work[column].dtype
        if (
            pd.api.types.is_object_dtype(dtype)
            or pd.api.types.is_string_dtype(dtype)
        ):
            values = work[column].astype("string").str.strip()
            work[column] = values.mask(values.eq(""))

    work["Length_m"] = pd.to_numeric(
        work["Length_m"], errors="coerce"
    ).astype("float64")
    work["Deflection_mm"] = pd.to_numeric(
        work["Deflection_mm"], errors="coerce"
    ).astype("float64")

    lengths = work["Length_m"].to_numpy()
    deflections = work["Deflection_mm"].to_numpy()

    missing_identifiers = work.loc[:, _MEMBER_KEYS].isna().any(axis=1).to_numpy()
    invalid_lengths = ~np.isfinite(lengths) | (lengths <= 0)
    invalid_deflections = ~np.isfinite(deflections)
    invalid_rows = (
        missing_identifiers | invalid_lengths | invalid_deflections
    )

    if invalid_rows.any():
        reason_counts = {
            "missing/blank identifiers": int(missing_identifiers.sum()),
            "invalid or non-positive lengths": int(invalid_lengths.sum()),
            "invalid deflections": int(invalid_deflections.sum()),
        }
        details = ", ".join(
            f"{reason}: {count}"
            for reason, count in reason_counts.items()
            if count
        )
        example_indices = work.index[invalid_rows][:5].tolist()
        message = (
            f"{int(invalid_rows.sum())} invalid result rows "
            f"({details}); example indices: {example_indices}"
        )

        if errors == "raise":
            raise ValueError(message)

        warnings.warn(f"Dropping {message}", RuntimeWarning, stacklevel=2)
        work = work.loc[~invalid_rows].copy()

    allowable_deflection_mm = (
        work["Length_m"] * 1000.0 / span_ratio_limit
    )
    work["DeflectionRatio"] = (
        work["Deflection_mm"].abs() / allowable_deflection_mm
    )

    # A result export may have multiple load cases or stations per member.
    member_envelope = (
        work.groupby(
            list(_MEMBER_KEYS),
            as_index=False,
            observed=True,
            sort=False,
        )
        .agg(DeflectionRatio=("DeflectionRatio", "max"))
    )

    summary = (
        member_envelope.groupby(
            ["Storey", "Material"],
            as_index=False,
            observed=True,
            sort=False,
        )
        .agg(
            MemberCount=("Member", "size"),
            MaxRatio=("DeflectionRatio", "max"),
            MeanRatio=("DeflectionRatio", "mean"),
        )
    )

    summary["Status"] = np.where(
        summary["MaxRatio"].le(1.0),
        "PASS",
        "FAIL",
    )
    return summary
```

### Review findings

1. Performance

`iterrows()`, per-row copies, and rebuilding a DataFrame create substantial Python overhead and temporary allocations. The revised version uses vectorised conversion and arithmetic, followed by two native Pandas group-bys. It also copies only five required columns. Several hundred thousand rows should be routine, assuming reasonable group cardinality.

`observed=True` avoids generating unused combinations when grouping categorical columns, while `sort=False` avoids an unnecessary group-key sort.

2. Data cleaning and validation

The original code:

- fails without identifying which rows are bad;
- accepts zero or negative lengths, producing invalid or infinite ratios;
- does not reject `NaN` or infinity;
- does not handle blank grouping identifiers;
- silently excludes null members from `count()`.

The revision validates required columns, identifiers, numeric conversion, finiteness, and positive length. Strict failure is the default; controlled dropping is available but emits a warning. Plausible-but-incorrect units cannot be detected automatically, so the metre/millimetre contract should remain explicit.

3. Summary correctness

The original calculation uses signed deflection. A large negative deflection produces a negative ratio and may incorrectly pass. Utilisation should normally use deflection magnitude.

The original `MemberCount` counts result rows with non-null member IDs, not necessarily members. Likewise, its mean weights members with more exported load cases or result stations more heavily. The revised implementation first takes the governing ratio for each member, then calculates:

- `MemberCount`: number of distinct member envelopes;
- `MaxRatio`: governing ratio among those members;
- `MeanRatio`: mean governing member ratio.

If the input contract guarantees exactly one row per member, this envelope step is harmless. If the intended mean is genuinely over raw result observations, that different statistic should be named accordingly.

4. Maintainability

The revision makes the required schema, utilisation formula, aggregation grain, failure policy, and span criterion explicit. It removes row mutation and inline lambdas.

Focused tests should cover:

- a 4 m member with 16 mm deflection giving ratio `1.0` and `PASS`;
- the same case with `-20 mm` giving ratio `1.25` and `FAIL`;
- repeated results for one member using only its maximum ratio;
- unique member counts rather than raw-row counts;
- missing IDs, malformed numerics, zero/negative lengths, `NaN`, and infinity;
- empty input and categorical grouping columns.
