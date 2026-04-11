# Raw Output

- task_id: `v2-deep-04`
- model_id_used: `glm-5.1-cloud`
- run_date: `2026-04-09`
- thinking_mode_used: `yes`

## Prompt Used

Same as in the prompt file

## Context Files Shared

All files from context folder

## Raw Model Output:
----------------------------------------------------------------
1. **Whether the refactor is safe in principle:**
A naive refactor is **unsafe**. While extracting a shared utilisation helper seems straightforward, the two
modules handle a zero-denominator (capacity `<= 0`) fundamentally differently:
- Concrete returns `None`, leading to a `"CHECK INPUT"` status.
- Steel returns `0.0`, leading to a `"PASS"` status.
If a single shared function is created without explicitly handling this divergence, the zero-denominator behavior
for one or both materials will silently change, violating the core constraint and breaking downstream spreadsheet
logic. The refactor is only safe if this distinct behavior is parameterized or preserved via wrapper logic.

2. **Which logic may be shared and which behaviour must remain distinct:**
- **May be shared:** The core mathematical calculation (`demand / capacity`) and the `format_status` threshold
logic (`"PASS"` if `<= 1.0` else `"FAIL"`).
- **Must remain distinct:** The zero/negative capacity handling. Concrete must evaluate to `"CHECK INPUT"`, while
Steel must evaluate to `"PASS"`.

3. **A minimal refactor approach that preserves behaviour:**
Add a `fallback` parameter to a shared utilisation helper. This deduplicates the math and the capacity-zero-check
logic while explicitly requiring the caller to define what happens when capacity is `<= 0`, preventing silent
shifts.

**`context/common_formatting.py`**
```python
def format_status(util):
    return "PASS" if util <= 1.0 else "FAIL"

def calculate_utilisation(demand, capacity, zero_capacity_fallback=None):
    if capacity <= 0:
        return zero_capacity_fallback
    return demand / capacity
```

**`context/concrete_checks.py`**
```python
from common_formatting import format_status, calculate_utilisation

def concrete_utilisation(v_ed, v_rd):
    return calculate_utilisation(v_ed, v_rd, zero_capacity_fallback=None)

def concrete_status(v_ed, v_rd):
    util = concrete_utilisation(v_ed, v_rd)
    if util is None:
        return "CHECK INPUT"
    return format_status(util)
```

**`context/steel_checks.py`**
```python
from common_formatting import format_status, calculate_utilisation

def steel_utilisation(n_ed, n_rd):
    return calculate_utilisation(n_ed, n_rd, zero_capacity_fallback=0.0)

def steel_status(n_ed, n_rd):
    return format_status(steel_utilisation(n_ed, n_rd))
```
*Why this works:* It consolidates the duplicated `if capacity <= 0` and division logic, but forces future
contributors to explicitly declare the fallback behavior, entirely preserving the original module APIs and output
behaviors.

4. **Tests or regression checks needed before merging:**
To protect downstream spreadsheets and prevent regression, the following specific tests must be implemented and
pass before merging:

- **Zero-Denominator Regression Tests (Critical):**
  - Assert `concrete_status(100, 0) == "CHECK INPUT"`
  - Assert `concrete_status(100, -5) == "CHECK INPUT"`
  - Assert `steel_status(100, 0) == "PASS"`
  - Assert `steel_status(100, -5) == "PASS"`
- **Boundary Tests (Exact status text match):**
  - Assert `concrete_status(50, 100) == "PASS"` (util = 0.5)
  - Assert `steel_status(50, 100) == "PASS"` (util = 0.5)
  - Assert `concrete_status(100, 100) == "PASS"` (util = 1.0)
  - Assert `steel_status(100, 100) == "PASS"` (util = 1.0)
  - Assert `concrete_status(101, 100) == "FAIL"` (util = 1.01)
  - Assert `steel_status(101, 100) == "FAIL"` (util = 1.01)
- **Underlying Utilisation Value Tests:**
  - Assert `concrete_utilisation(100, 0) is None`
  - Assert `steel_utilisation(100, 0) == 0.0`