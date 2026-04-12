# Task 1 - Square pad footing sizing notebook draft

Write a notebook-style engineering draft for preliminary sizing of a square pad footing supporting one column.

Your output must be an ordered Markdown notebook outline with alternating Markdown and Python code cells. Do not output literal `.ipynb` JSON.

## Deliverable Requirements

Your notebook draft must contain these sections in this order:
1. Assumptions, exclusions, and sign conventions
2. Input data
3. Python calculation cells
4. Search over candidate footing sizes
5. Results table by load case for the selected footing
6. Final engineering conclusion with governing case and omitted checks

You must:
- use standard-library Python only
- include readable Markdown cells, not just code comments
- keep calculations unrounded internally and round only for reported outputs
- state a final selected footing size in metres
- state the governing load case clearly

## Engineering Brief

Design a notebook draft for preliminary sizing of a square pad footing supporting one reinforced concrete column.

Use service loads only.

Ignore:
- footing self-weight
- sliding
- settlement
- punching shear
- one-way shear
- reinforcement design

Check only:
- bearing pressure
- no-uplift

Column size for reporting only:
- `400 mm x 400 mm`

Candidate square footing sizes:
- `2.4 m` to `3.2 m` in `0.1 m` increments

Allowable net bearing pressure:
- `220 kPa`

## Service Load Cases

- `LC1`: `N = 1100 kN`, `Mx = 90 kNm`, `My = 60 kNm`
- `LC2`: `N = 700 kN`, `Mx = 200 kNm`, `My = 140 kNm`
- `LC3`: `N = 1250 kN`, `Mx = 70 kNm`, `My = 110 kNm`

## Analysis Model Note

Assume a rigid square footing with linear soil-pressure distribution under axial load plus biaxial moment.

You must:
- state the bearing-pressure equations you use
- explain briefly why that model is appropriate for this preliminary check
- show briefly how your edge-pressure expression is obtained from axial stress plus bending stress
- define your sign convention and eccentricity directions clearly
- keep units consistent between `kN`, `kNm`, `m`, and `kPa`

## Selection Rule

Choose the smallest footing width `B` for which every load case satisfies:
- `qmax <= 220 kPa`
- `qmin >= 0 kPa`

## Output Shape

Present the answer as a notebook draft using clearly labelled Markdown and code cells, for example:

````md
## Markdown Cell 1
...

```python
# Code Cell 1
...
```
````

Do not return prose only. Do not omit the calculation code.
