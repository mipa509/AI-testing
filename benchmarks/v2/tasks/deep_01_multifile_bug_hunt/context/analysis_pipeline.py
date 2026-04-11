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
