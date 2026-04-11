# Raw Output

- task_id: `v2-medium-06`
- model_id_used: `qwen-3.6plus`
- run_date: `2026-04-10`
- thinking_mode_used: `yes`

## Prompt Used

Same as in the prompt file

## Context Files Shared

- `context/foundation_settlement.py`

## Raw Model Output
Here's my review of the `foundation_settlement.py` helper.

---

## 1. Key Bugs and Risks

### Critical

| # | Issue | Function | Impact |
|---|-------|----------|--------|
| C1 | **Zero allowable returns `0.0`** | `settlement_ratio` | When `allowable_mm == 0`, any settlement is unacceptable, yet the function returns `0.0` — which `status_from_ratio` classifies as `"PASS"`. This silently masks a dangerous condition. |
| C2 | **Zero spacing causes `ZeroDivisionError`** | `differential_slope` | No guard against `spacing_m == 0`. The function will crash rather than return a safe value. |

### Moderate

| # | Issue | Function | Impact |
|---|-------|----------|--------|
| M1 | **No validation for negative inputs** | All functions | Negative settlement, allowable, or spacing values are physically meaningless but accepted without warning. |
| M2 | **No type hints or docstrings** | All functions | Units (mm, m) and sign conventions (positive = downward settlement) are implicit. Easy for downstream users to misuse. |
| M3 | **Single-element list returns `0.0` silently** | `differential_slope` | A single settlement cannot produce a differential slope. Returning `0.0` masks insufficient data. |

### Minor

| # | Issue | Function | Impact |
|---|-------|----------|--------|
| m1 | **No handling for `NaN` or `None`** | All functions | Could propagate silently through calculations. |
| m2 | **Boundary at exactly `1.0`** | `status_from_ratio` | Ratio of exactly `1.0` returns `"FAIL"`. This is defensible but should be documented. |

---

## 2. Minimum Code Fixes

```python
"""Foundation settlement helpers.

Sign convention:
    Positive settlement = downward (compression).
    All lengths in mm unless stated otherwise.
    Spacing in metres.
"""

from typing import Sequence


def settlement_ratio(settlement_mm: float, allowable_mm: float) -> float:
    """Return settlement / allowable ratio.

    Raises ValueError if either argument is negative or if allowable is zero.
    """
    if allowable_mm <= 0:
        raise ValueError(
            f"allowable_mm must be positive, got {allowable_mm}"
        )
    if settlement_mm < 0:
        raise ValueError(
            f"settlement_mm must be non-negative, got {settlement_mm}"
        )
    return settlement_mm / allowable_mm


def differential_slope(
    settlements_mm: Sequence[float], spacing_m: float
) -> float:
    """Return differential slope as a dimensionless ratio (mm/m).

    Requires at least two settlement values and positive spacing.
    """
    if len(settlements_mm) < 2:
        raise ValueError(
            f"Need at least 2 settlements, got {len(settlements_mm)}"
        )
    if spacing_m <= 0:
        raise ValueError(
            f"spacing_m must be positive, got {spacing_m}"
        )
    delta_mm = max(settlements_mm) - min(settlements_mm)
    return delta_mm / spacing_m


def status_from_ratio(ratio: float) -> str:
    """Return 'PASS' if ratio < 1.0, else 'FAIL'."""
    return "PASS" if ratio < 1.0 else "FAIL"
```

**Summary of changes:**
- **C1 fixed**: `settlement_ratio` now raises `ValueError` for zero or negative allowable (instead of returning a misleading `0.0`).
- **C2 fixed**: `differential_slope` now raises `ValueError` for zero or negative spacing.
- **M1 fixed**: Negative inputs are rejected with clear messages.
- **M2 fixed**: Type hints and docstrings document units and sign conventions.
- **M3 fixed**: Single-element list now raises `ValueError` instead of silently returning `0.0`.

---

## 3. Focused Test Set

Six high-value tests that catch the hidden failures:

```python
import pytest
from foundation_settlement import (
    settlement_ratio,
    differential_slope,
    status_from_ratio,
)


class TestSettlementRatio:
    """Units: settlement_mm (mm), allowable_mm (mm). Ratio is dimensionless."""

    def test_normal_pass(self):
        # 10 mm settlement against 25 mm allowable → 0.4 → PASS
        assert settlement_ratio(10.0, 25.0) == pytest.approx(0.4)
        assert status_from_ratio(settlement_ratio(10.0, 25.0)) == "PASS"

    def test_zero_allowable_raises(self):
        # Critical: must NOT return 0.0 (which would be classified as PASS)
        with pytest.raises(ValueError, match="allowable_mm must be positive"):
            settlement_ratio(5.0, 0.0)

    def test_negative_settlement_raises(self):
        # Negative settlement = uplift, not valid for this helper
        with pytest.raises(ValueError, match="settlement_mm must be non-negative"):
            settlement_ratio(-1.0, 25.0)


class TestDifferentialSlope:
    """Units: settlements (mm), spacing (m). Result is mm/m (dimensionless slope)."""

    def test_normal_slope(self):
        # 20 mm differential over 6 m spacing → 3.33 mm/m
        assert differential_slope([10.0, 30.0], 6.0) == pytest.approx(
            3.333, abs=0.01
        )

    def test_zero_spacing_raises(self):
        # Critical: must NOT crash with ZeroDivisionError
        with pytest.raises(ValueError, match="spacing_m must be positive"):
            differential_slope([10.0, 20.0], 0.0)

    def test_single_settlement_raises(self):
        # Cannot compute differential from one point
        with pytest.raises(ValueError, match="Need at least 2 settlements"):
            differential_slope([10.0], 6.0)


class TestStatusFromRatio:
    def test_boundary_exactly_one(self):
        # Ratio == 1.0 is FAIL (at the limit, not under)
        assert status_from_ratio(1.0) == "FAIL"

    def test_just_under_one(self):
        assert status_from_ratio(0.999) == "PASS"
```

### Why these six tests?

| Test | Catches |
|------|---------|
| `test_zero_allowable_raises` | **C1** — the most dangerous silent bug (zero allowable → false PASS) |
| `test_zero_spacing_raises` | **C2** — prevents ZeroDivisionError crash |
| `test_negative_settlement_raises` | **M1** — guards against physically meaningless inputs |
| `test_single_settlement_raises` | **M3** — prevents silent masking of insufficient data |
| `test_boundary_exactly_one` | **m2** — documents the pass/fail threshold behavior |
| `test_normal_pass` / `test_normal_slope` | Baseline correctness — verifies the happy path still works |

This is a minimal set. Each test targets a specific bug or risk identified above, with no redundant coverage.