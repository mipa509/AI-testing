# Raw Output

- task_id: `v2-medium-06`
- model_id_used: `gpt5.6-sol-xhigh`
- api_model: `gpt-5.6-sol`
- reasoning_effort: `xhigh`
- run_route: `Codex VS Code extension, fresh session, empty sandbox workspace; inputs from neutral copy (D:\bench-inputs\task7)`
- run_date: `2026-09-17`
- thinking_mode_used: `yes (reasoning effort xhigh)`

## Prompt Used

Same as in the prompt file (`tasks/medium_06_review_plus_tests/prompt.md`), sent as message 1. `tasks/medium_06_review_plus_tests/context_combined.md` sent as message 2.

## Context Files Shared

- `context/foundation_settlement.py`

## Raw Model Output

Assuming settlement is **positive downward**, all settlement limits are positive magnitudes, spacing is in metres, and slope is returned as dimensionless angular distortion.

## 1. Key bugs and risks

- `allowable_mm == 0` returns `0.0`, producing a false PASS for an invalid or infinitely exceeded limit. Zero and negative allowables should be rejected.
- `status_from_ratio()` fails equality. Normally, settlement equal to the allowable limit is still acceptable, so `ratio <= 1.0` should PASS. Confirm this project convention.
- `differential_slope()` mixes millimetres and metres. `delta_mm / spacing_m` is **mm/m**, not dimensionless slope. For dimensionless angular distortion, divide by `spacing_m * 1000`.
- Zero or negative spacing is not rejected, causing division by zero or physically meaningless results.
- Returning zero for fewer than two measurements hides missing data.
- Signed settlement is not defined. With positive-downward settlement, negative inputs represent heave or a convention error and should not silently create a misleading ratio.
- For more than two settlements, `max - min` divided by one `spacing_m` is ambiguous. The maximum and minimum may not be separated by that distance. Either accept exactly two points or accept point coordinates and calculate slopes from actual separations.
- `NaN` can silently produce a PASS because comparisons with `NaN` are false in ways that undermine the current logic.

## 2. Minimum code fixes

This version deliberately treats `differential_slope` as a two-point calculation:

```py
import math


def settlement_ratio(settlement_mm, allowable_mm):
    """Utilisation ratio; settlement is positive downward, values are in mm."""
    if not math.isfinite(settlement_mm) or settlement_mm < 0:
        raise ValueError("settlement_mm must be finite and non-negative")
    if not math.isfinite(allowable_mm) or allowable_mm <= 0:
        raise ValueError("allowable_mm must be finite and greater than zero")

    return settlement_mm / allowable_mm


def differential_slope(settlements_mm, spacing_m):
    """
    Magnitude of two-point differential slope (dimensionless).

    Settlements are in mm, positive downward; spacing is in m.
    """
    if len(settlements_mm) != 2:
        raise ValueError("exactly two settlements are required")
    if not math.isfinite(spacing_m) or spacing_m <= 0:
        raise ValueError("spacing_m must be finite and greater than zero")
    if any(not math.isfinite(value) for value in settlements_mm):
        raise ValueError("settlements must be finite")

    delta_mm = abs(settlements_mm[1] - settlements_mm[0])
    return delta_mm / (spacing_m * 1000.0)


def status_from_ratio(ratio):
    """PASS means demand is no greater than the allowable value."""
    if not math.isfinite(ratio) or ratio < 0:
        raise ValueError("ratio must be finite and non-negative")

    return "PASS" if ratio <= 1.0 else "FAIL"
```

If the intended slope output is **mm/m**, retain `delta_mm / spacing_m` but rename it, for example, `differential_gradient_mm_per_m`, and document the unit. If multiple measurement points must be supported, pass their coordinates rather than a single spacing.

## 3. Focused high-value tests

```py
import math
import pytest

from context.foundation_settlement import (
    differential_slope,
    settlement_ratio,
    status_from_ratio,
)


def test_ratio_and_limit_boundary():
    assert settlement_ratio(20.0, 25.0) == pytest.approx(0.8)
    assert status_from_ratio(0.8) == "PASS"
    assert status_from_ratio(1.0) == "PASS"
    assert status_from_ratio(1.000001) == "FAIL"


@pytest.mark.parametrize("allowable", [0.0, -25.0])
def test_nonpositive_allowable_is_rejected(allowable):
    with pytest.raises(ValueError):
        settlement_ratio(10.0, allowable)


def test_differential_slope_converts_mm_and_m():
    # Positive-down settlements: 15 mm differential over 5 m.
    # 15 mm / 5000 mm = 0.003 dimensionless, equivalent to 3 mm/m.
    assert differential_slope([10.0, 25.0], 5.0) == pytest.approx(0.003)

    # Returned value is a magnitude and is independent of point order.
    assert differential_slope([25.0, 10.0], 5.0) == pytest.approx(0.003)


@pytest.mark.parametrize("spacing", [0.0, -5.0])
def test_nonpositive_spacing_is_rejected(spacing):
    with pytest.raises(ValueError):
        differential_slope([10.0, 25.0], spacing)


@pytest.mark.parametrize("values", [[], [10.0], [10.0, 20.0, 30.0]])
def test_ambiguous_or_insufficient_slope_inputs_are_rejected(values):
    with pytest.raises(ValueError):
        differential_slope(values, 5.0)


def test_nonfinite_values_are_rejected():
    with pytest.raises(ValueError):
        settlement_ratio(math.nan, 25.0)

    with pytest.raises(ValueError):
        differential_slope([10.0, math.nan], 5.0)

    with pytest.raises(ValueError):
        status_from_ratio(math.nan)
```

The most important hidden-failure tests are the zero allowable, equality boundary, millimetre-to-metre conversion, zero spacing, ambiguous multi-point input, and `NaN` cases.
