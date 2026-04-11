# Combined Context

Copy the full contents below as the task context.

## context/foundation_settlement.py

```py
def settlement_ratio(settlement_mm, allowable_mm):
    if allowable_mm == 0:
        return 0.0
    return settlement_mm / allowable_mm


def differential_slope(settlements_mm, spacing_m):
    if len(settlements_mm) < 2:
        return 0.0
    delta_mm = max(settlements_mm) - min(settlements_mm)
    return delta_mm / spacing_m


def status_from_ratio(ratio):
    return "PASS" if ratio < 1.0 else "FAIL"

```
