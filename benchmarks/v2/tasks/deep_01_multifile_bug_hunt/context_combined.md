# Combined Context

Copy the full contents below as the task context.

## context/analysis_pipeline.py

```py
import pandas as pd

from section_library import get_section_properties


def prepare_results(df: pd.DataFrame) -> pd.DataFrame:
    clean = df.copy()
    clean["Member"] = clean["Member"].astype(str).str.strip()
    clean["Section"] = clean["Section"].astype(str).str.strip()
    clean["Mz_kNm"] = pd.to_numeric(clean["Mz_kNm"], errors="coerce")
    return clean


def major_axis_utilisation(row: pd.Series) -> float:
    props = get_section_properties(row["Section"])
    m_rd_kNm = props["Wpl_y_mm3"] * props["fy_MPa"] / 1e6
    return row["Mz_kNm"] / m_rd_kNm


def build_member_summary(df: pd.DataFrame) -> pd.DataFrame:
    prepared = prepare_results(df)
    summary = prepared.groupby("Member", as_index=False).agg(
        {
            "Section": "first",
            "Mz_kNm": "max",
        }
    )
    summary["Util_major"] = summary.apply(major_axis_utilisation, axis=1)
    return summary

```

## context/reporting.py

```py
import pandas as pd


def decorate_status(summary: pd.DataFrame) -> pd.DataFrame:
    out = summary.copy()
    out["Util_major"] = out["Util_major"].round(3)
    out["Status"] = out["Util_major"].map(lambda util: "PASS" if util <= 1.0 else "FAIL")
    return out.sort_values(["Status", "Util_major"], ascending=[True, False])

```

## context/section_library.py

```py
SECTIONS = {
    "254x146x31 UB": {"Wpl_y_cm3": 366.0, "fy_MPa": 275.0},
    "305x165x40 UB": {"Wpl_y_cm3": 649.0, "fy_MPa": 275.0},
}


def get_section_properties(name: str) -> dict:
    section = SECTIONS[name]
    return {
        "fy_MPa": section["fy_MPa"],
        "Wpl_y_mm3": section["Wpl_y_cm3"] * 1e2,
    }

```
