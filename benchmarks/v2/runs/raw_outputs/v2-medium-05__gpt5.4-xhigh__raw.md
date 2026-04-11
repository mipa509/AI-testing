# Raw Output

- task_id: `v2-medium-05`
- model_id_used: `gpt5.4-xhigh`
- run_date: `2026-04-11`
- thinking_mode_used: `yes`

## Prompt Used

Same as in the prompt file

## Context Files Shared

- `context/member_summary.py`

## Raw Model Output

**Findings**
- High: `context/member_summary.py:6-13` uses `iterrows()`, copies each row, and rebuilds a second `DataFrame`. On several hundred thousand rows this becomes the main performance and memory bottleneck.
- High: `context/member_summary.py:8-10` coerces values with bare `float(...)` and never validates required columns, nulls, or non-positive `Length_m`. Dirty exports will fail unpredictably or produce invalid ratios.
- High: `context/member_summary.py:10` uses signed `Deflection_mm`. If the export uses negative values for downward deflection, large deflections can become negative ratios and incorrectly pass.
- Medium: `context/member_summary.py:17-20` summarises raw rows directly. If the export has multiple rows per member/load case, `MemberCount` and especially `MeanRatio` are not true member-level utilisation summaries.
- Medium: `context/member_summary.py:18` uses `count` on `Member`, which ignores nulls. That undercounts silently instead of making the counting rule explicit.

**Revised implementation**
```py
import pandas as pd

REQUIRED_COLUMNS = {"Storey", "Material", "Member", "Length_m", "Deflection_mm"}
SUMMARY_COLUMNS = ["Storey", "Material", "MemberCount", "MaxRatio", "MeanRatio", "Status"]
ALLOWABLE_DEFLECTION_LIMIT = 250.0


def _clean_text(series: pd.Series) -> pd.Series:
    cleaned = series.astype("string").str.strip()
    return cleaned.mask(cleaned == "")


def summarise_members(df: pd.DataFrame) -> pd.DataFrame:
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    if df.empty:
        return pd.DataFrame(columns=SUMMARY_COLUMNS)

    clean = df.loc[:, ["Storey", "Material", "Member", "Length_m", "Deflection_mm"]].copy()
    clean["Storey"] = _clean_text(clean["Storey"])
    clean["Material"] = _clean_text(clean["Material"])
    clean["Member"] = _clean_text(clean["Member"])
    clean["Length_m"] = pd.to_numeric(clean["Length_m"], errors="coerce")
    clean["Deflection_mm"] = pd.to_numeric(clean["Deflection_mm"], errors="coerce")

    invalid = (
        clean["Storey"].isna()
        | clean["Material"].isna()
        | clean["Member"].isna()
        | clean["Length_m"].isna()
        | clean["Deflection_mm"].isna()
        | (clean["Length_m"] <= 0)
    )
    if invalid.any():
        raise ValueError(
            "Cannot summarise members: "
            f"{int(invalid.sum())} rows have missing ids/group keys, non-numeric values, or non-positive lengths."
        )

    clean["DeflectionRatio"] = (
        clean["Deflection_mm"].abs() / (clean["Length_m"] * 1000.0 / ALLOWABLE_DEFLECTION_LIMIT)
    )

    member_level = (
        clean.groupby(["Storey", "Material", "Member"], as_index=False, observed=True, sort=False)
        .agg(DeflectionRatio=("DeflectionRatio", "max"))
    )

    summary = (
        member_level.groupby(["Storey", "Material"], as_index=False, observed=True, sort=False)
        .agg(
            MemberCount=("Member", "size"),
            MaxRatio=("DeflectionRatio", "max"),
            MeanRatio=("DeflectionRatio", "mean"),
        )
    )

    summary["Status"] = summary["MaxRatio"].le(1.0).map({True: "PASS", False: "FAIL"})
    return summary[SUMMARY_COLUMNS]
```

**Why this addresses the task**
- Performance: vectorised numeric conversion and ratio calculation, no Python row loop, and only required columns are copied.
- Data cleaning/validation: required schema is checked first, text keys are normalised, bad numerics are handled deterministically, and divide-by-zero/negative-length cases are rejected.
- Correctness: pass/fail uses the worst ratio, the ratio uses absolute deflection magnitude, and the summary rolls up each member by its governing result before calculating storey/material metrics.
- Maintainability: constants, a small text-cleaning helper, and explicit `clean -> member_level -> summary` stages make the function easier to test and modify.

Tests I would add next: empty input, bad numeric strings, zero/negative lengths, negative deflection signs, and duplicated member rows across multiple result cases. If the pipeline must tolerate bad rows instead of failing fast, return or log an `invalid_rows` table rather than silently dropping them.