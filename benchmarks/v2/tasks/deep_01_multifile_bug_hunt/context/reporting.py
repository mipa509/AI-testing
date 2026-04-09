import pandas as pd


def decorate_status(summary: pd.DataFrame) -> pd.DataFrame:
    out = summary.copy()
    out["Util_major"] = out["Util_major"].round(3)
    out["Status"] = out["Util_major"].map(lambda util: "PASS" if util <= 1.0 else "FAIL")
    return out.sort_values(["Status", "Util_major"], ascending=[True, False])
