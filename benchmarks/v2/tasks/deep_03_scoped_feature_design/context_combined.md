# Combined Context

Copy the full contents below as the task context.

## context/design_engine.py

```py
import pandas as pd


def build_uls_summary(df: pd.DataFrame) -> pd.DataFrame:
    out = df.groupby(["Member", "Section"], as_index=False).agg(
        Utilisation_ULS=("Utilisation_ULS", "max")
    )
    out["Status"] = out["Utilisation_ULS"].map(lambda util: "PASS" if util <= 1.0 else "FAIL")
    return out

```

## context/io_contract.py

```py
RESULT_COLUMNS = [
    "Member",
    "Section",
    "Utilisation_ULS",
    "Status",
]


def normalise_columns(df):
    return df.rename(columns=str.strip)

```

## context/report_writer.py

```py
from io_contract import RESULT_COLUMNS


def report_rows(summary_df):
    return summary_df.loc[:, RESULT_COLUMNS].to_dict(orient="records")

```
