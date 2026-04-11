# Combined Context

Copy the full contents below as the task context.

## context/common_formatting.py

```py
def format_status(util):
    return "PASS" if util <= 1.0 else "FAIL"

```

## context/concrete_checks.py

```py
from common_formatting import format_status


def concrete_utilisation(v_ed, v_rd):
    if v_rd <= 0:
        return None
    return v_ed / v_rd


def concrete_status(v_ed, v_rd):
    util = concrete_utilisation(v_ed, v_rd)
    if util is None:
        return "CHECK INPUT"
    return format_status(util)

```

## context/steel_checks.py

```py
from common_formatting import format_status


def steel_utilisation(n_ed, n_rd):
    if n_rd <= 0:
        return 0.0
    return n_ed / n_rd


def steel_status(n_ed, n_rd):
    return format_status(steel_utilisation(n_ed, n_rd))

```
