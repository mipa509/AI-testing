# Raw Output

- task_id: `v2-medium-06`
- model_id_used: `glm-5.1-cloud`
- run_date: `2026-04-09`
- thinking_mode_used: `yes`

## Prompt Used

Same as in the prompt file

## Context Files Shared

All files from context folder

## Raw Model Output:
----------------------------------------------------------------
## 1. Key Bugs & Risks

| # | Severity | Function | Issue |
|---|----------|----------|-------|
| 1 | **Critical** | `settlement_ratio` | `allowable_mm == 0` returns `0.0` — masks an impossible criterion as
"fully acceptable." In reality a zero allowable is undefined (or infinitely strict); returning 0.0 will cascade
into a **PASS** in `status_from_ratio`. |
| 2 | **Critical** | `differential_slope` | `spacing_m == 0` causes an unhandled `ZeroDivisionError` crash. No
guard exists. |
| 3 | **High** | `differential_slope` | `len(settlements_mm) < 2` returns `0.0` — same masking problem.
Insufficient data should not pretend the differential is zero. |
| 4 | **High** | All functions | No validation for negative inputs. Negative `settlement_mm` is physically
meaningless; negative `allowable_mm` or `spacing_m` flips the sign of the result and can turn a **FAIL** into a
**PASS**. |
| 5 | **Medium** | `status_from_ratio` | Boundary: `ratio == 1.0` is **FAIL** (`< 1.0` check). Users may expect
exactly-at-limit to pass. More importantly, there is no **WARNING** / marginal zone (e.g., 0.8–1.0), which is
standard geotechnical practice. |

**Sign & unit conventions assumed (standard geotechnical):**
- All settlements in **mm** (positive downward).
- `allowable_mm` must be **strictly positive**.
- `spacing_m` must be **strictly positive**.
- Differential slope is **mm/m** (dimensionless ×10⁻³).

---

## 2. Minimum Code Fixes

```python
def settlement_ratio(settlement_mm, allowable_mm):
    if settlement_mm < 0:
        raise ValueError("settlement_mm must be non-negative")
    if allowable_mm <= 0:
        raise ValueError("allowable_mm must be strictly positive")
    return settlement_mm / allowable_mm


def differential_slope(settlements_mm, spacing_m):
    if len(settlements_mm) < 2:
        raise ValueError("At least 2 settlement points required")
    if any(s < 0 for s in settlements_mm):
        raise ValueError("settlement values must be non-negative")
    if spacing_m <= 0:
        raise ValueError("spacing_m must be strictly positive")
    delta_mm = max(settlements_mm) - min(settlements_mm)
    return delta_mm / spacing_m


def status_from_ratio(ratio):
    if ratio < 0:
        raise ValueError("ratio must be non-negative")
    if ratio < 0.8:
        return "PASS"
    if ratio < 1.0:
        return "WARNING"
    return "FAIL"
```

**Summary of changes:**

| What | Before | After | Rationale |
|------|--------|-------|-----------|
| `allowable_mm == 0` | return `0.0` | `raise ValueError` | Prevents false PASS |
| `allowable_mm < 0` | silent wrong sign | `raise ValueError` | Prevents sign-flipped PASS |
| `spacing_m <= 0` | `ZeroDivisionError` crash | `raise ValueError` | Controlled, explicit failure |
| `len < 2` | return `0.0` | `raise ValueError` | Prevents false zero differential |
| Negative settlements | accepted | `raise ValueError` | Physically meaningless |
| Boundary `ratio == 1.0` | FAIL only | WARNING / FAIL | Adds marginal zone per standard practice |

---

## 3. Focused Test Set

Only **highest-value** tests — each targets a distinct failure mode.

```python
import pytest

# ── settlement_ratio ──────────────────────────────────────

def test_ratio_normal_pass():
    """Typical case: 15 mm settlement vs 25 mm allowable → 0.6"""
    assert settlement_ratio(15.0, 25.0) == pytest.approx(0.6)

def test_ratio_zero_allowable_raises():
    """CRITICAL: allowable=0 must not return 0.0 (old bug)"""
    with pytest.raises(ValueError, match="strictly positive"):
        settlement_ratio(10.0, 0.0)

def test_ratio_negative_allowable_raises():
    """Sign-flip risk: negative allowable could flip PASS/FAIL"""
    with pytest.raises(ValueError, match="strictly positive"):
        settlement_ratio(10.0, -25.0)

def test_ratio_negative_settlement_raises():
    with pytest.raises(ValueError, match="non-negative"):
        settlement_ratio(-5.0, 25.0)

def test_ratio_at_limit():
    """ratio == 1.0 exactly — boundary condition"""
    assert settlement_ratio(25.0, 25.0) == pytest.approx(1.0)

# ── differential_slope ────────────────────────────────────

def test_slope_normal():
    """settlements [5, 20] mm, spacing 3 m → 15/3 = 5 mm/m"""
    assert differential_slope([5.0, 20.0], 3.0) == pytest.approx(5.0)

def test_slope_zero_spacing_raises():
    """CRITICAL: would ZeroDivisionError in old code"""
    with pytest.raises(ValueError, match="strictly positive"):
        differential_slope([5.0, 20.0], 0.0)

def test_slope_single_point_raises():
    """Old code returned 0.0 — masks missing data"""
    with pytest.raises(ValueError, match="At least 2"):
        differential_slope([10.0], 5.0)

def test_slope_negative_spacing_raises():
    with pytest.raises(ValueError, match="strictly positive"):
        differential_slope([5.0, 20.0], -3.0)

def test_slope_negative_settlement_raises():
    with pytest.raises(ValueError, match="non-negative"):
        differential_slope([-5.0, 20.0], 3.0)

# ── status_from_ratio ─────────────────────────────────────

def test_status_pass():
    assert status_from_ratio(0.5) == "PASS"

def test_status_warning():
    """New marginal zone: 0.8 ≤ ratio < 1.0"""
    assert status_from_ratio(0.9) == "WARNING"

def test_status_fail():
    assert status_from_ratio(1.2) == "FAIL"

def test_status_exact_boundary():
    """ratio == 1.0 must be FAIL (not PASS)"""
    assert status_from_ratio(1.0) == "FAIL"

def test_status_exact_warning_lower():
    """ratio == 0.8 is the first WARNING value"""
    assert status_from_ratio(0.8) == "WARNING"

def test_status_negative_ratio_raises():
    with pytest.raises(ValueError, match="non-negative"):
        status_from_ratio(-0.1)
```

**Why these 13 tests and no more:**

| Risk covered | Tests |
|---|---|
| Zero-allowable false PASS (original bug) | `test_ratio_zero_allowable_raises` |
| Sign-flipped PASS (negative allowable/spacing) | `test_ratio_negative_allowable_raises`,
`test_slope_negative_spacing_raises` |
| ZeroDivision crash | `test_slope_zero_spacing_raises` |
| Silent zero on insufficient data | `test_slope_single_point_raises` |
| Boundary 1.0 FAIL vs PASS confusion | `test_status_exact_boundary`, `test_ratio_at_limit` |
| Normal happy-path correctness | `test_ratio_normal_pass`, `test_slope_normal`, `test_status_pass/warning/fail` |
| Negative physical values | `test_ratio_negative_settlement_raises`, `test_slope_negative_settlement_raises`,
`test_status_negative_ratio_raises` |
| New WARNING zone logic | `test_status_warning`, `test_status_exact_warning_lower` |

Each test targets a **distinct** failure mode — no redundant matrix, maximum signal per test.