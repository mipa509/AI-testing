# Combined Context

Copy the full contents below as the task context.

## context/beam_capacity.py

```py
from load_factors import factored_line_load


def design_moment_kNm(row: dict) -> float:
    w_uls = factored_line_load(row)
    return w_uls * row["span_m"] ** 2 / 8.0


def major_axis_resistance_kNm(section: dict) -> float:
    return section["Wpl_y_cm3"] * section["fy_MPa"] / 1e6


def utilisation(row: dict, section: dict) -> float:
    return design_moment_kNm(row) / major_axis_resistance_kNm(section)

```

## context/load_factors.py

```py
ULS_GAMMA_G = 1.35
ULS_GAMMA_Q = 1.50


def factored_line_load(row: dict) -> float:
    return (row["G_kN_per_m"] * ULS_GAMMA_G) + row["Q_kN_per_m"]

```

## context/reporting.py

```py
from beam_capacity import utilisation


def build_review_table(load_rows: list, section_lookup: dict) -> list:
    output = []
    for row in load_rows:
        section = section_lookup[row["section_name"]]
        util = round(utilisation(row, section), 2)
        output.append(
            {
                "member_id": row["member_id"],
                "combination": row["combination"],
                "utilisation": util,
                "status": "PASS" if util < 1.0 else "FAIL",
            }
        )
    output.sort(key=lambda item: item["utilisation"])
    return output[:1]

```
