# Reference Solution Review - v3-notebook-01

This is the checked engineering reference for manual review. Do not show it to the model before scoring.

## Problem Definition

Size the smallest square footing width `B` between `2.4 m` and `3.2 m` in `0.1 m` increments such that all service load cases satisfy:
- `qmax <= 220 kPa`
- `qmin >= 0 kPa`

## Reference Modelling Assumption

Reference modelling assumption:
- rigid square footing
- linear soil-pressure distribution under axial load plus biaxial moment
- service-level screening only

## Preferred Reference Formulation

Preferred formulation used for scoring review:
- `ex = My / N`
- `ey = Mx / N`
- `qavg = N / B^2`
- `qmax = qavg * (1 + 6*ex/B + 6*ey/B)`
- `qmin = qavg * (1 - 6*ex/B - 6*ey/B)`

Why this formulation is used as the benchmark reference:
- it is consistent with the stated rigid-footing linear-pressure assumption
- it gives direct visibility of both peak compression and uplift risk
- it is appropriate for a simple preliminary serviceability-style screening notebook
- it is deterministic enough for consistent cross-model scoring

## Preferred Derivation Path

Start from linear stress distribution under axial load plus biaxial bending:
- `q = N/A ± Mx*y/Ix ± My*x/Iy`

For a square footing of width `B`:
- `A = B^2`
- `Ix = Iy = B^4 / 12`
- at the edge, `x = B/2` and `y = B/2`

So the edge bending terms become:
- `Mx*y/Ix = Mx * (B/2) / (B^4/12) = 6*Mx/B^3`
- `My*x/Iy = My * (B/2) / (B^4/12) = 6*My/B^3`

Therefore:
- `q = N/B^2 ± 6*Mx/B^3 ± 6*My/B^3`

Using eccentricities:
- `ex = My/N`
- `ey = Mx/N`

This can be rearranged to:
- `qmax = qavg * (1 + 6*ex/B + 6*ey/B)`
- `qmin = qavg * (1 - 6*ex/B - 6*ey/B)`

This is the preferred explanation path for the benchmark because it shows the underlying mechanics rather than only quoting the compact final formula.

Alternative model responses may still be reviewable, but they should only score well if they:
- state their equations explicitly
- justify why the formulation matches the stated footing behaviour
- preserve a transparent uplift or tension check
- remain unit-consistent and technically coherent

Excluded checks:
- footing self-weight
- sliding
- settlement
- punching shear
- one-way shear
- reinforcement design

## Eccentricities By Load Case

### LC1

- `N = 1100 kN`
- `Mx = 90 kNm`
- `My = 60 kNm`
- `ex = 60 / 1100 = 0.054545 m`
- `ey = 90 / 1100 = 0.081818 m`

### LC2

- `N = 700 kN`
- `Mx = 200 kNm`
- `My = 140 kNm`
- `ex = 140 / 700 = 0.200000 m`
- `ey = 200 / 700 = 0.285714 m`

### LC3

- `N = 1250 kN`
- `Mx = 70 kNm`
- `My = 110 kNm`
- `ex = 110 / 1250 = 0.088000 m`
- `ey = 70 / 1250 = 0.056000 m`

## Governing Candidate Check

`LC2` governs the selection because it produces the smallest `qmin`.

### LC2 Sweep Across Candidate Sizes

| B (m) | qavg (kPa) | qmax (kPa) | qmin (kPa) | Status |
|---|---:|---:|---:|---|
| 2.4 | 121.528 | 269.097 | -26.042 | Fail |
| 2.5 | 112.000 | 242.560 | -18.560 | Fail |
| 2.6 | 103.550 | 219.618 | -12.517 | Fail |
| 2.7 | 96.022 | 199.665 | -7.621 | Fail |
| 2.8 | 89.286 | 182.216 | -3.644 | Fail |
| 2.9 | 83.234 | 166.879 | -0.410 | Fail |
| 3.0 | 77.778 | 153.333 | 2.222 | Pass |
| 3.1 | 72.841 | 141.318 | 4.364 | Pass |
| 3.2 | 68.359 | 130.615 | 6.104 | Pass |

This is the intended trap in the benchmark: models that check `qmax` only may incorrectly select `2.9 m`, but the correct answer is `3.0 m` because `qmin` is still negative at `2.9 m`.

## Final Checked Values At B = 3.0 m

### LC1

- `qavg = 1100 / 3.0^2 = 122.222 kPa`
- `qmax = 122.222 * (1 + 6*0.054545/3.0 + 6*0.081818/3.0) = 155.556 kPa`
- `qmin = 122.222 * (1 - 6*0.054545/3.0 - 6*0.081818/3.0) = 88.889 kPa`

### LC2

- `qavg = 700 / 3.0^2 = 77.778 kPa`
- `qmax = 77.778 * (1 + 6*0.200000/3.0 + 6*0.285714/3.0) = 153.333 kPa`
- `qmin = 77.778 * (1 - 6*0.200000/3.0 - 6*0.285714/3.0) = 2.222 kPa`

### LC3

- `qavg = 1250 / 3.0^2 = 138.889 kPa`
- `qmax = 138.889 * (1 + 6*0.088000/3.0 + 6*0.056000/3.0) = 178.889 kPa`
- `qmin = 138.889 * (1 - 6*0.088000/3.0 - 6*0.056000/3.0) = 98.889 kPa`

## Final Answer

- selected footing size: `3.0 m x 3.0 m`
- governing load case: `LC2`
- reason: `3.0 m` is the first candidate size for which all load cases satisfy both `qmax <= 220 kPa` and `qmin >= 0 kPa`
- omitted checks should be stated explicitly in the model answer
