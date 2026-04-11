import pandas as pd


def summarise_members(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in df.iterrows():
        row = row.copy()
        row["Length_m"] = float(row["Length_m"])
        row["Deflection_mm"] = float(row["Deflection_mm"])
        row["DeflectionRatio"] = row["Deflection_mm"] / (row["Length_m"] * 1000.0 / 250.0)
        rows.append(row)

    clean = pd.DataFrame(rows)

    summary = (
        clean.groupby(["Storey", "Material"])
        .agg(
            MemberCount=("Member", "count"),
            MaxRatio=("DeflectionRatio", "max"),
            MeanRatio=("DeflectionRatio", "mean"),
        )
        .reset_index()
    )

    summary["Status"] = summary["MaxRatio"].map(lambda ratio: "PASS" if ratio <= 1.0 else "FAIL")
    return summary
