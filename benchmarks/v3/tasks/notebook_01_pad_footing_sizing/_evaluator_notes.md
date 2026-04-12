# Evaluator Notes - v3-notebook-01

Do not show this file to the model.

## Objective

Check whether the model can convert a deterministic footing-sizing brief into a notebook-style deliverable with:
- explicit engineering assumptions
- correct unit handling
- working Python
- a stated and justified bearing-pressure model
- correct footing selection
- a readable engineering conclusion

## Exact Expected Outcome

- selected footing size: `3.0 m x 3.0 m`
- governing case: `LC2`
- critical rejection at `2.9 m`: `LC2` gives `qmin = -0.410 kPa`, so uplift occurs even though `qmax` is acceptable

## Reference Engineering Model

Preferred reference model for this benchmark:
- rigid square footing
- linear soil-pressure distribution under axial load plus biaxial moment
- service-level screening only

Preferred reference formulation:
- `ex = My / N`
- `ey = Mx / N`
- `qavg = N / B^2`
- `qmax = qavg * (1 + 6*ex/B + 6*ey/B)`
- `qmin = qavg * (1 - 6*ex/B - 6*ey/B)`

Why this is the preferred solution here:
- it matches the prompt's stated rigid-footing linear-pressure assumption
- it is a standard preliminary screening model for axial load plus biaxial moment
- it makes the uplift check explicit through `qmin`
- it is simple enough for a notebook-style benchmark while still exposing unit, sign, and logic errors

## Reference Values At B = 3.0 m

- `LC1`: `ex = 0.054545 m`, `ey = 0.081818 m`, `qavg = 122.222 kPa`, `qmax = 155.556 kPa`, `qmin = 88.889 kPa`
- `LC2`: `ex = 0.200000 m`, `ey = 0.285714 m`, `qavg = 77.778 kPa`, `qmax = 153.333 kPa`, `qmin = 2.222 kPa`
- `LC3`: `ex = 0.088000 m`, `ey = 0.056000 m`, `qavg = 138.889 kPa`, `qmax = 178.889 kPa`, `qmin = 98.889 kPa`

## Near-Miss Values At B = 2.9 m

- `LC1`: `qmax = 167.699 kPa`, `qmin = 93.895 kPa`
- `LC2`: `qmax = 166.879 kPa`, `qmin = -0.410 kPa`
- `LC3`: `qmax = 192.915 kPa`, `qmin = 104.350 kPa`

## Common Failure Modes To Penalise

- selects `2.9 m` by checking `qmax` only
- uses an inappropriate or unexplained pressure model for the stated footing assumption
- applies inconsistent units between `kN`, `kNm`, `m`, and `kPa`
- swaps or misstates `ex` and `ey`
- omits assumptions, exclusions, or sign conventions
- produces code without notebook-style explanation
- produces explanation without a working calculation core
- gives a correct final size but does not explain why smaller candidates fail

## Scoring Guidance

High-scoring outputs should:
- explicitly state the excluded checks
- state the rigid-footing linear-pressure model and justify it briefly
- show the preferred derivation path from `q = N/A ± Mx*y/Ix ± My*x/Iy` to the edge-pressure form used for a square footing
- state the sign convention used for moments and eccentricities
- state the equations actually used
- show a clear candidate-size search loop
- report the selected size and governing case
- provide code that would plausibly run with standard-library Python only

Alternative formulations:
- may be accepted if they are explicitly stated, technically coherent with the prompt assumptions, and produce a defensible pass/fail decision
- should be penalised if they are unexplained, incompatible with the stated rigid linear-pressure model, or hide the uplift check
- should not automatically be treated as correct just because the final footing size matches the reference answer

Allow minor rounding differences in displayed values if the selected footing and pass/fail logic remain correct.
