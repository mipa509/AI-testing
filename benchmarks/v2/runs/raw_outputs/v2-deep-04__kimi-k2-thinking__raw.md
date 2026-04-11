# Raw Output

- task_id: `v2-deep-04`
- model_id_used: `kimi-k2-thinking`
- run_date: `2026-04-09`
- thinking_mode_used: `yes`

## Prompt Used

Same as in the prompt file

## Context Files Shared

All files from context folder

## Raw Model Output
----------------------------------------------------------------------------------------------
### 1. Safety Assessment
**Unsafe in principle** if deduplication blindly merges the `_utilisation` functions. The zero/negative
denominator handling is **intentionally different**:
- **Concrete** treats `v_rd <= 0` as an *input error*, returning `"CHECK INPUT"`
- **Steel** treats `n_rd <= 0` as *no load capacity*, returning `"PASS"` (since utilisation = 0.0)

Changing steel to return `"CHECK INPUT"` or concrete to return `"PASS"` would break downstream spreadsheet logic
that depends on these exact status strings.

---

### 2. Shared vs. Distinct Logic

| Logic | Status | Rationale |
|-------|--------|-----------|
| `format_status()` | **Already shared** | Pure formatting, no domain logic |
| Core ratio `ed / rd` | **Can be shared** | Pure arithmetic, identical in both |
| Denominator validation | **Must remain distinct** | Different business rules (error vs. valid edge case) |
| Special status text (`"CHECK INPUT"`) | **Must remain distinct** | Concrete-specific requirement; steel has no
equivalent |

---

### 3. Minimal Refactor Approach

Preserve behaviour by extracting only the **safe division** logic, leaving validation and status mapping in place:

```python
# common_formatting.py (add this helper)
def _safe_ratio(numerator, denominator):
    """Pure calculation without validation. Assumes denominator > 0."""
    return numerator / denominator

# concrete_checks.py
from common_formatting import format_status, _safe_ratio

def concrete_utilisation(v_ed, v_rd):
    if v_rd <= 0:
        return None
    return _safe_ratio(v_ed, v_rd)  # Deduplicated core logic

def concrete_status(v_ed, v_rd):
    util = concrete_utilisation(v_ed, v_rd)
    if util is None:
        return "CHECK INPUT"
    return format_status(util)

# steel_checks.py
from common_formatting import format_status, _safe_ratio

def steel_utilisation(n_ed, n_rd):
    if n_rd <= 0:
        return 0.0
    return _safe_ratio(n_ed, n_rd)  # Deduplicated core logic

def steel_status(n_ed, n_rd):
    return format_status(steel_utilisation(n_ed, n_rd))
```

**Why this works:**
- Zero-denominator paths are **unchanged** and **explicit**
- Only the division operation is deduplicated
- Status text logic remains intact
- No change to public API or return values

---

### 4. Required Tests Before Merging

Create regression tests that **lock in current behaviour** before refactoring:

```python
# test_concrete_steel_regression.py
import pytest
from concrete_checks import concrete_utilisation, concrete_status
from steel_checks import steel_utilisation, steel_status

class TestConcrete:
    def test_zero_denominator_returns_check_input(self):
        assert concrete_status(100, 0) == "CHECK INPUT"
        assert concrete_status(100, -5) == "CHECK INPUT"

    def test_normal_calculation(self):
        assert concrete_utilisation(50, 100) == 0.5
        assert concrete_status(50, 100) == "PASS"
        assert concrete_status(110, 100) == "FAIL"

class TestSteel:
    def test_zero_denominator_returns_pass(self):
        assert steel_status(100, 0) == "PASS"  # 0.0 utilisation
        assert steel_status(100, -5) == "PASS"

    def test_normal_calculation(self):
        assert steel_utilisation(50, 100) == 0.5
        assert steel_status(50, 100) == "PASS"
        assert steel_status(110, 100) == "FAIL"

def test_boundary_at_1_0():
    """Critical for spreadsheets: exactly 1.0 must be PASS"""
    assert concrete_status(100, 100) == "PASS"
    assert steel_status(100, 100) == "PASS"
```

**Additional checks:**
- Run `grep -r "CHECK INPUT" spreadsheets/` to find downstream dependencies
- Add type hints to prevent accidental misuse of `_safe_ratio`
- Consider a comment in `common_formatting.py` documenting why denominator validation is **not** included in the
helper

---

**Verdict:** The refactor is safe **only** if it extracts the division logic while preserving the separate
validation and status mapping. Any attempt to unify the `None` vs `0.0` return values would silently break
production behaviour.