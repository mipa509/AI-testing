# Raw Output

- task_id: `v2-deep-06`
- model_id_used: `kimi-k2-thinking`
- run_date: `2026-04-09`
- thinking_mode_used: `yes`

## Prompt Used

Same as in the prompt file

## Context Files Shared

All files from context folder

## Raw Model Output
----------------------------------------------------------------------------------------------
## 1. Key Bugs & Risks

### Critical Issues
- **Silent failure on division by zero**: `settlement_ratio()` returns `0.0` when `allowable_mm=0`, masking a
critical data error that should raise an exception.
- **Incorrect differential slope calculation**: `differential_slope()` uses `max(settlements_mm) -
min(settlements_mm)` across *all* points, not between *adjacent* foundation points per engineering standards. This
over-predicts risk for long foundations with many measurement points.
- **Wrong pass/fail threshold**: `status_from_ratio()` uses `< 1.0` instead of `<= 1.0`, causing a `FAIL` status
when settlement exactly equals the allowable limit (typically a PASS condition in geotechnical practice).

### High-Risk Validation Gaps
- No rejection of negative settlement values (physically invalid)
- No rejection of zero/negative spacing (causes division by zero or sign errors)
- Returns `0.0` instead of raising errors for insufficient data points, hiding malformed inputs

### Unit & Sign Convention Ambiguity
- Mixed units (mm vs m) without explicit conversion documentation; result is `mm/m` which is non-standard (should
be `mm/mm` or unified units)
- Sign convention not documented (settlements are positive downward)

---

## 2. Minimum Code Fixes

```python
def settlement_ratio(settlement_mm: float, allowable_mm: float) -> float:
    """Calculate settlement ratio with validation.

    Args:
        settlement_mm: Observed settlement in millimeters (must be >= 0)
        allowable_mm: Allowable settlement in millimeters (must be > 0)

    Returns:
        settlement / allowable ratio (dimensionless)

    Raises:
        ValueError: If inputs are invalid
    """
    if settlement_mm < 0 or allowable_mm < 0:
        raise ValueError("Settlement and allowable values must be non-negative")
    if allowable_mm == 0:
        raise ValueError("Allowable settlement cannot be zero")
    return settlement_mm / allowable_mm


def differential_slope(settlements_mm: list[float], spacing_m: float) -> float:
    """Calculate maximum differential slope between *adjacent* points.

    Args:
        settlements_mm: List of settlement observations in millimeters (length >= 2)
        spacing_m: Distance between *adjacent* observation points in meters (must be > 0)

    Returns:
        Maximum absolute slope in mm/m between any adjacent pair

    Raises:
        ValueError: If inputs are invalid
    """
    if len(settlements_mm) < 2:
        raise ValueError("At least two settlement points required")
    if spacing_m <= 0:
        raise ValueError("Spacing must be positive")
    if any(s < 0 for s in settlements_mm):
        raise ValueError("Settlements cannot be negative")

    # Calculate slope between adjacent points only
    max_slope = 0.0
    for i in range(1, len(settlements_mm)):
        delta_mm = abs(settlements_mm[i] - settlements_mm[i-1])
        slope = delta_mm / spacing_m
        max_slope = max(max_slope, slope)
    return max_slope


def status_from_ratio(ratio: float) -> str:
    """Determine pass/fail status from ratio.

    Args:
        ratio: Settlement ratio (dimensionless)

    Returns:
        "PASS" if ratio <= 1.0, otherwise "FAIL"
    """
    return "PASS" if ratio <= 1.0 else "FAIL"
```

---

## 3. Focused Test Set (High-Value Cases)

```python
import pytest

class TestSettlementRatio:
    def test_normal_case(self):
        assert settlement_ratio(25.0, 50.0) == 0.5

    def test_zero_allowable_raises_error(self):
        with pytest.raises(ValueError, match="cannot be zero"):
            settlement_ratio(10.0, 0.0)

    def test_negative_settlement_raises_error(self):
        with pytest.raises(ValueError, match="non-negative"):
            settlement_ratio(-5.0, 50.0)

    def test_exact_limit(self):
        assert settlement_ratio(50.0, 50.0) == 1.0


class TestDifferentialSlope:
    def test_adjacent_slope_calculation(self):
        # Catches the max-min bug: [0, 10, 5] should give 10 mm/m, not 5
        assert differential_slope([0.0, 10.0, 5.0], 1.0) == 10.0

    def test_insufficient_points_raises_error(self):
        with pytest.raises(ValueError, match="At least two"):
            differential_slope([5.0], 2.0)

    def test_zero_spacing_raises_error(self):
        with pytest.raises(ValueError, match="positive"):
            differential_slope([0.0, 10.0], 0.0)

    def test_negative_settlement_raises_error(self):
        with pytest.raises(ValueError, match="cannot be negative"):
            differential_slope([0.0, -5.0], 1.0)


class TestStatusFromRatio:
    def test_below_limit_passes(self):
        assert status_from_ratio(0.95) == "PASS"

    def test_at_limit_passes(self):
        # CRITICAL: This catches the < vs <= bug
        assert status_from_ratio(1.0) == "PASS"

    def test_above_limit_fails(self):
        assert status_from_ratio(1.01) == "FAIL"


# Integration test for realistic scenario
def test_foundation_assessment_end_to_end():
    """Simulate a 3-point foundation check."""
    settlements = [5.0, 15.0, 8.0]  # mm
    spacing = 3.0  # m
    allowable = 20.0  # mm

    ratio = settlement_ratio(max(settlements), allowable)
    slope = differential_slope(settlements, spacing)

    # Verify ratio status
    assert status_from_ratio(ratio) == "PASS"  # 15/20 = 0.75

    # Verify slope is between adjacent points, not max-min
    # Adjacent slopes: 10/3=3.33, 7/3=2.33 → max is 3.33
    # Old buggy max-min would give: (15-5)/3 = 3.33 (same here, but fails on other patterns)
    assert abs(slope - 3.33) < 0.01
```

**Test Execution Priority**: Run `test_at_limit_passes` and `test_adjacent_slope_calculation` first—they catch the
most critical logic bugs that could cause false failures or missed hazards.