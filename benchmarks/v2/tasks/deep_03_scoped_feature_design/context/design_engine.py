import pandas as pd


def build_uls_summary(df: pd.DataFrame) -> pd.DataFrame:
    out = df.groupby(["Member", "Section"], as_index=False).agg(
        Utilisation_ULS=("Utilisation_ULS", "max")
    )
    out["Status"] = out["Utilisation_ULS"].map(lambda util: "PASS" if util <= 1.0 else "FAIL")
    return out
