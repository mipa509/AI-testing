# Raw Output

- task_id: `v2-medium-06`
- model_id_used: `minimax-m2.7-cloud`
- run_date: `2026-04-10`
- thinking_mode_used: `yes`

## Prompt Used

Same as in the prompt file

## Context Files Shared

- `context/foundation_settlement.py`

## Raw Model Output
# Review: `context/foundation_settlement.py`

---

## 1. Key Bugs or Risks

| Severity | Function | Issue |
|----------|----------|-------|
| **HIGH** | `differential_slope` | **Unit mismatch** — `delta_mm` (mm) is divided by `spacing_m` (meters) without unit conversion. The result is in
`mm/m`, not a dimensionless ratio. Example: 10mm differential over 5m returns `2.0` (mm/m) instead of the correct `0.002` (m/m) or `1:500`. |
| **MEDIUM** | `settlement_ratio` | Returns `0.0` when `allowable_mm == 0`, which silently masks a division-by-zero that should probably raise an error.
|
| **LOW** | `differential_slope` | No guard against `spacing_m == 0`. |
| **LOW** | All functions | No type hints or docstrings — unit conventions are implicit, inviting misuse. |

---

## 2. Minimum Code Fixes

```python
def settlement_ratio(settlement_mm, allowable_mm):
    """Compute settlement as a fraction of allowable.

    Args:
        settlement_mm: Observed settlement (mm, positive downward).
        allowable_mm:  Allowable settlement limit (mm, positive).

    Returns:
        Dimensionless ratio (settlement / allowable).

    Raises:
        ValueError: If allowable_mm is zero or if inputs are negative.
    """
    if allowable_mm == 0:
        raise ValueError("allowable_mm cannot be zero")
    if settlement_mm < 0:
        raise ValueError("settlement_mm must be non-negative (heave should use a separate function)")
    return settlement_mm / allowable_mm


def differential_slope(settlements_mm, spacing_m):
    """Compute differential settlement slope as a dimensionless ratio.

    Args:
        settlements_mm: List of settlement readings at each node (mm).
        spacing_m:      Uniform horizontal spacing between nodes (meters).

    Returns:
        Dimensionless slope (Δsettlement / spacing) in m/m.
        For example, 10mm over 5m → 0.002 (or 1:500).

    Raises:
        ValueError: If fewer than 2 points, or spacing_m <= 0.
    """
    if len(settlements_mm) < 2:
        raise ValueError("At least two settlement points are required")
    if spacing_m <= 0:
        raise ValueError("spacing_m must be positive")

    delta_mm = max(settlements_mm) - min(settlements_mm)
    delta_m  = delta_mm / 1000.0          # mm → m
    return delta_m / spacing_m             # m/m (dimensionless)


def status_from_ratio(ratio):
    """Determine PASS/FAIL based on settlement ratio.

    Args:
        ratio: Dimensionless settlement ratio (actual / allowable).

    Returns:
        "PASS" if ratio < 1.0, else "FAIL".

    Raises:
        ValueError: If ratio is not a finite number.
    """
    if not isinstance(ratio, (int, float)) or not (-float('inf') < ratio < float('inf')):
        raise ValueError(f"ratio must be a finite numeric value, got {type(ratio).__name__}")
    return "PASS" if ratio < 1.0 else "FAIL"
```

---

## 3. Focused Test Set

These tests target the hidden failures with explicit sign conventions and units.

```python
import pytest
from context.foundation_settlement import settlement_ratio, differential_slope, status_from_ratio


# ─── settlement_ratio ────────────────────────────────────────────────────────

class TestSettlementRatio:
    """Sign convention: settlement_mm is positive downward; allowable_mm is positive."""

    def test_nominal(self):
        assert settlement_ratio(25.0, 50.0) == pytest.approx(0.5)

    def test_at_limit_returns_one(self):
        """At the exact allowable limit the ratio is 1.0."""
        assert settlement_ratio(50.0, 50.0) == pytest.approx(1.0)

    def test_zero_actual_raises(self):
        """Zero observed settlement is valid and returns 0."""
        assert settlement_ratio(0.0, 50.0) == 0.0

    def test_negative_settlement_raises(self):
        """Heave (negative settlement) is a different mechanism — raise."""
        with pytest.raises(ValueError, match="non-negative"):
            settlement_ratio(-5.0, 50.0)

    def test_zero_allowable_raises(self):
        """Division by zero is not silently swallowed."""
        with pytest.raises(ValueError, match="cannot be zero"):
            settlement_ratio(10.0, 0.0)


# ─── differential_slope ───────────────────────────────────────────────────────

class TestDifferentialSlope:
    """Sign convention: result is dimensionless m/m (delta_m / spacing_m)."""

    def test_nominal(self):
        # 10 mm over 5 m → 0.01 m / 5 m = 0.002 m/m
        assert differential_slope([0.0, 10.0], 5.0) == pytest.approx(0.002)

    def test_three_points(self):
        # settlements = [0, 10, 5] mm; max-min = 10 mm; over 2 m
        assert differential_slope([0.0, 10.0, 5.0], 2.0) == pytest.approx(0.005)

    def test_single_point_raises(self):
        with pytest.raises(ValueError, match="at least two"):
            differential_slope([10.0], 2.0)

    def test_empty_list_raises(self):
        with pytest.raises(ValueError, match="at least two"):
            differential_slope([], 2.0)

    def test_zero_spacing_raises(self):
        with pytest.raises(ValueError, match="spacing_m must be positive"):
            differential_slope([0.0, 10.0], 0.0)

    def test_negative_spacing_raises(self):
        with pytest.raises(ValueError, match="spacing_m must be positive"):
            differential_slope([0.0, 10.0], -2.0)

    def test_no_differential_returns_zero(self):
        """Uniform settlement (no differential) yields zero slope."""
        assert differential_slope([10.0, 10.0, 10.0], 3.0) == pytest.approx(0.0)

    def test_result_is_dimensionless_m_per_m(self):
        """Verify the output is in m/m, not mm/m (the original bug)."""
        slope = differential_slope([0.0, 10.0], 5.0)
        # If the bug were present, slope would be 2.0 (mm/m).
        # Correct value is 0.002 (m/m).
        assert slope < 1.0, "Slope must be << 1 (m/m), not in mm/m"


# ─── status_from_ratio ────────────────────────────────────────────────────────

class TestStatusFromRatio:
    """Boundary: ratio == 1.0 is FAIL (at or beyond allowable)."""

    @pytest.mark.parametrize("ratio, expected", [
        (0.0,   "PASS"),
        (0.5,   "PASS"),
        (0.999, "PASS"),
        (1.0,   "FAIL"),   # exactly at limit → FAIL
        (1.5,   "FAIL"),
    ])
    def test_threshold(self, ratio, expected):
        assert status_from_ratio(ratio) == expected

    def test_non_numeric_raises(self):
        with pytest.raises(ValueError, match="finite numeric"):
            status_from_ratio("0.5")

    def test_infinity_raises(self):
        with pytest.raises(ValueError, match="finite numeric"):
            status_from_ratio(float('inf'))
```

---

### Why these tests?

| Test | Catches |
|------|---------|
| `test_nominal` (differential) | Baseline correctness |
| `test_result_is_dimensionless` | **The mm/m vs m/m unit bug** — the single highest-value check |
| `test_negative_spacing_raises` | Zero/negative spacing crash |
| `test_negative_settlement_raises` | Heave passed as settlement |
| `test_zero_allowable_raises` | Silent 0 → masked error |
| `test_at_limit_returns_one` + parametrised thresholds | Boundary `ratio == 1.0` is FAIL (not ambiguous) |

This set is deliberately small (≈15 test cases) while hitting every hidden failure.