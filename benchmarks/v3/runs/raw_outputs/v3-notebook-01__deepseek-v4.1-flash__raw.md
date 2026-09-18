# Raw Output

- task_id: `v3-notebook-01`
- model_id_used: `deepseek-v4.1-flash`
- api_model: `deepseek/deepseek-v4.1-flash` (OpenRouter)
- reasoning_effort: `high`
- run_route: `VS Code agent chat via OpenRouter, fresh chat per task, sandbox workspace on a separate drive holding the three task folders (prompts and context only; no evaluator or reference files)`
- run_date: `2026-09-18`
- thinking_mode_used: `yes (reasoning effort high)`

## Prompt Used

Same as in the prompt file (`tasks/notebook_01_pad_footing_sizing/prompt.md`), read by the agent from the task folder. The deliverable was written by the agent as `footing_sizing_notebook_draft.md` in that folder.

## Raw Model Output

# Square Pad Footing - Preliminary Sizing (Notebook Draft)

Task 1 deliverable. Ordered notebook outline: alternating Markdown and Python cells.
Standard-library Python only. Calculations are carried unrounded internally; rounding appears only at reporting time.

---

## Markdown Cell 1 - Assumptions, Exclusions, and Sign Conventions

### Scope of this draft

Preliminary sizing of one square pad footing (`B x B`, constant thickness, rigid) supporting one reinforced concrete column.
Output is a candidate width `B` in metres, chosen from a discrete set of sizes, plus the governing load case.

### Assumptions

1. **Rigid footing, planar soil pressure.** The footing is stiff enough relative to the soil that the contact pressure distribution remains planar (linear) over the base; the footing does not deform enough to redistribute pressure.
2. **Linear-elastic soil response.** Soil pressure is proportional to settlement over the loaded area, so pressure under axial load plus biaxial moment can be built by superposition of axial stress and bending stress.
3. **Service loads only.** Loads are unfactored. No load factors and no material resistance factors are applied. The check is against an allowable (working) net bearing pressure.
4. **Net bearing pressure.** `220 kPa` is treated as a *net allowable* value, i.e. the pressure available for the column load alone. This is consistent with ignoring footing self-weight (item 5).
5. **Full contact assumed for `qmax`.** `qmax` is computed from the planar distribution assuming the whole base is in compression. If `qmin < 0` the assumption is violated and the case is rejected (`no-uplift` rule), rather than re-analyzed as partial contact.
6. **Column load is concentric in plan except for the applied moments.** The column is taken at the footing centre; the given `Mx`, `My` are the only sources of eccentricity.
7. **Square base, so the elastic section modulus is identical about both plan axes.** `S_x = S_y = B^3 / 6`. This is what lets the biaxial corner check collapse to a single sum.
8. **One column, one footing.** No interaction between adjacent footings, no group effects, no raft action.
9. **Moments are transferred fully to the footing.** No reduction for column stiffness or frame action.

### Exclusions (deliberately not checked)

| Omitted item | Why it is out of scope here |
| --- | --- |
| Footing self-weight | `220 kPa` is a net allowable pressure; self-weight is carried by the displaced soil |
| Sliding | No horizontal loads given; would also need friction/interface data |
| Settlement (total and differential) | Serviceability check needing soil stiffness and consolidation data |
| Punching shear | Requires thickness, concrete strength, and load/column geometry |
| One-way (beam) shear | Same as punching shear |
| Reinforcement design | Requires thickness, cover, concrete/steel strengths, and moment at the column face |
| Overturning / stability under moment alone | Service-load no-uplift rule is used as the proxy at this stage |
| Groundwater, soil layering, local weak pockets | Geotechnical data not provided |
| Local bearing / column-to-footing connection | Separate design step |

### Sign conventions

- **Axial load `N`:** positive in compression (downward column load). All given `N` are positive.
- **Soil pressure `q`:** positive in compression (downward pressure on the soil, i.e. upward reaction on the footing). `1 kPa = 1 kN/m^2`.
- **Moments `Mx`, `My`:** applied moments about the plan axes `x` and `y` respectively, taken in the same rotational sense for the purposes of this check.
  - `Mx` varies the pressure **along the `y` direction** (i.e. it tilts the pressure plane about the `x` axis).
  - `My` varies the pressure **along the `x` direction** (i.e. it tilts the pressure plane about the `y` axis).
- **`qmax` / `qmin`:** extreme *corner* pressures, taken at the most-compressed and least-compressed corners respectively. Because both bending terms are added with the same sign at one corner, the individual sign of each moment does not change the magnitude of `qmax` or `qmin` for a square base; only the corner at which they occur changes.
- **Eccentricity:** `e = M / N`, expressed in metres as an offset of the load resultant from the base centroid. `e_x` is associated with `My`, `e_y` with `Mx`.
- **Units:** `N` in kN, `M` in kNm, `B` in m, stress/pressure in kPa. Consistency is guaranteed by kN + m -> kPa (`kN/m^2`), so no conversion factors appear in the pressure equations.

---

## Markdown Cell 2 - Input Data

### Geometry and allowable pressure

| Quantity | Symbol | Value | Unit |
| --- | --- | --- | --- |
| Column size (reporting only, not used in the check) | `c` | 400 | mm |
| Candidate footing widths | `B` | 2.4 to 3.2 in 0.1 steps | m |
| Allowable net bearing pressure | `q_allow` | 220 | kPa |
| Minimum permitted edge pressure (no uplift) | `q_min,lim` | 0 | kPa |

### Service load cases (unfactored)

| Case | `N` (kN) | `Mx` (kNm) | `My` (kNm) |
| --- | --- | --- | --- |
| LC1 | 1100 | 90 | 60 |
| LC2 | 700 | 200 | 140 |
| LC3 | 1250 | 70 | 110 |

### Selection rule

Choose the **smallest** `B` in the candidate set for which **every** load case satisfies:

```
qmax <= 220 kPa      (bearing)
qmin >= 0   kPa      (no uplift / full contact)
```

Note that the column size is stated for reporting only and does not enter the bearing or no-uplift check in this draft.

---

## Markdown Cell 3 - Calculation Model and Pressure Equations

### Load-effect equations

For a square base of width `B`:

```
A  = B^2                       (base area, m^2)
S  = B^3 / 6                   (elastic section modulus about x or y, m^3)
q0 = N / A = N / B^2           (axial/average pressure, kPa)
qb = M / S = 6 M / B^3         (edge bending stress, kPa, per unit moment)
```

### Edge (corner) pressure expression

Superposing axial stress and biaxial bending stress at the critical corner:

```
qmax = N/B^2 + 6*Mx/B^3 + 6*My/B^3 = N/B^2 + 6*(Mx + My)/B^3
qmin = N/B^2 - 6*Mx/B^3 - 6*My/B^3 = N/B^2 - 6*(Mx + My)/B^3
```

Because the base is square, `S_x = S_y`, so the two bending contributions take the same coefficient and combine into a single `6*(Mx+My)/B^3` term.

### Derivation sketch

1. Axial only: pressure is uniform, `q0 = N/B^2`.
2. Moment about one axis only, say `Mx`: the pressure varies linearly across the base over the dimension `B`, with the neutral axis at middepth. Using `q = M/S` for the extreme fibre, the edge increment is `sigma_b = Mx/S = 6*Mx/B^3`. One edge gains `+sigma_b`, the opposite edge loses `sigma_b`. The slope of the pressure plane is set by `Mx`; the direction of variation is along `y`.
3. Adding `My` does the same thing along the `x` direction: one edge gains `+6*My/B^3`, the opposite loses it.
4. Both increments are positive at a common corner of a square base. That corner therefore carries

   `qmax = q0 + sigma_bx + sigma_by`, and the diagonally opposite corner carries `qmin = q0 - sigma_bx - sigma_by`.

5. Substituting gives the expressions above. This is a planar (bilinear in plan) pressure surface described by three numbers: `q0`, and the two slopes driven by `Mx` and `My`.

### Equivalent eccentricity form (used later as a cross-check)

Setting `qmin >= 0`:

```
N/B^2 >= 6*(Mx + My)/B^3   =>   B >= 6*(Mx + My)/N
```

Dividing through by `N` and writing `e_x = My/N`, `e_y = Mx/N`:

```
e_x + e_y <= B/6
```

This is exactly the condition that the load resultant lies within the kern of the square base - the classical no-uplift criterion. The planar-superposition formulation and the kern test therefore agree for a square base, which is a useful independent check of the code.

### Why this model is appropriate here

- The purpose is **preliminary sizing**, not final design. The dominant unknowns are soil parameters, not footing stiffness.
- RC pad footings sized for a single column are typically thick and short in span relative to the loaded area, so behaviour is close to rigid and planar contact pressure is a good idealization.
- The load resultants here are eccentric by at most about `0.49 m` on a base of nominal width `3 m`, i.e. order `B/6`. That is inside the full-contact regime, so the linear distribution applies rather than partial contact.
- The model is **conservative in the right direction**: it assumes no pressure redistribution to stiffer or deeper soil, no beneficial soil-structure interaction, and it enforces full contact as a hard requirement.
- It requires only `N`, `Mx`, `My`, and `B` - no soil stiffness, no footing thickness - which is what makes it usable at the sizing stage.

Where the model stops being appropriate: if `qmin` goes significantly negative, partial-contact (nonlinear, triangular or worse) behaviour governs and this formulation overstates `qmax` and cannot describe the real contact area. That regime is deliberately excluded by the selection rule rather than analyzed.

---

## Code Cell 1 - Service Load Cases

```python
# Code Cell 1 - Service (unfactored) load cases and unit conventions.
# Units used throughout: kN, kNm, m, kPa   (1 kPa == 1 kN/m^2)

LOAD_CASES = [
    {"name": "LC1", "N_kN": 1100.0, "Mx_kNm": 90.0, "My_kNm": 60.0},
    {"name": "LC2", "N_kN": 700.0, "Mx_kNm": 200.0, "My_kNm": 140.0},
    {"name": "LC3", "N_kN": 1250.0, "Mx_kNm": 70.0, "My_kNm": 110.0},
]

print("Service load cases (unfactored)")
print(f"{'Case':<6}{'N [kN]':>10}{'Mx [kNm]':>12}{'My [kNm]':>12}")
for lc in LOAD_CASES:
    print(f"{lc['name']:<6}{lc['N_kN']:>10.1f}{lc['Mx_kNm']:>12.1f}{lc['My_kNm']:>12.1f}")
```

---

## Code Cell 2 - Input Parameters

```python
# Code Cell 2 - Input data for the sizing search.

Q_ALLOW_KPA = 220.0          # allowable NET bearing pressure
Q_MIN_LIMIT_KPA = 0.0        # any negative edge pressure == uplift, rejected

B_MIN_M = 2.4
B_MAX_M = 3.2
B_STEP_M = 0.1

COLUMN_SIZE_M = 0.4          # 400 mm x 400 mm, reporting only

# Candidate sizes. Rounding to 0.1 m is a selection/display convenience so that
# float artefacts (e.g. 2.7000000000000002) cannot break equality comparisons.
B_CANDIDATES_M = []
_b = B_MIN_M
while _b <= B_MAX_M + 1e-9:
    B_CANDIDATES_M.append(round(_b, 1))
    _b += B_STEP_M

print(f"Allowable net bearing pressure : {Q_ALLOW_KPA:.0f} kPa")
print(f"No-uplift limit                : {Q_MIN_LIMIT_KPA:.0f} kPa")
print(f"Column size (reporting only)   : {COLUMN_SIZE_M * 1000:.0f} mm x {COLUMN_SIZE_M * 1000:.0f} mm")
print(f"Candidate footing widths [m]   : {B_CANDIDATES_M}")
```

---

## Code Cell 3 - Pressure Functions

```python
# Code Cell 3 - Rigid-footing, planar (linear) soil pressure under N + Mx + My.
# All functions return UNROUNDED values.

def base_area_m2(B):
    """Plan area of a square base, m^2."""
    return B * B


def section_modulus_m3(B):
    """Elastic section modulus about a plan axis, m^3. Equal for x and y (square base)."""
    return B ** 3 / 6.0


def average_pressure_kpa(B, N):
    """Axial (uniform) component of contact pressure, kPa."""
    return N / base_area_m2(B)


def edge_pressures_kpa(B, N, Mx, My):
    """
    Extreme corner pressures, kPa. Compression positive.

    qmax = N/B^2 + 6*Mx/B^3 + 6*My/B^3
    qmin = N/B^2 - 6*Mx/B^3 - 6*My/B^3
    """
    q_axial = average_pressure_kpa(B, N)
    q_bending = (abs(Mx) + abs(My)) / section_modulus_m3(B)
    return q_axial + q_bending, q_axial - q_bending


def resultant_eccentricity_sum_m(N, Mx, My):
    """e_x + e_y, the kern ordinate: e_x = My/N, e_y = Mx/N. Units: m."""
    return (abs(Mx) + abs(My)) / N


def kern_limit_m(B):
    """Kern boundary for a square base: e_x + e_y <= B/6."""
    return B / 6.0


def check_case(B, case):
    """
    Run bearing + no-uplift checks for one load case at one width.
    Returns a result dict with unrounded values.
    """
    N, Mx, My = case["N_kN"], case["Mx_kNm"], case["My_kNm"]
    qmax, qmin = edge_pressures_kpa(B, N, Mx, My)

    bearing_ok = qmax <= Q_ALLOW_KPA
    uplift_ok = qmin >= Q_MIN_LIMIT_KPA
    kern_ok = resultant_eccentricity_sum_m(N, Mx, My) <= kern_limit_m(B) + 1e-12

    return {
        "name": case["name"],
        "N_kN": N,
        "Mx_kNm": Mx,
        "My_kNm": My,
        "q_axial_kpa": average_pressure_kpa(B, N),
        "q_bending_kpa": (abs(Mx) + abs(My)) / section_modulus_m3(B),
        "qmax_kpa": qmax,
        "qmin_kpa": qmin,
        "e_sum_m": resultant_eccentricity_sum_m(N, Mx, My),
        "kern_m": kern_limit_m(B),
        "bearing_ok": bearing_ok,
        "uplift_ok": uplift_ok,
        "kern_ok": kern_ok,
        "pass": bearing_ok and uplift_ok,
    }


def check_size(B, cases):
    """Check every load case at one width. Returns (passes_everything, results)."""
    results = [check_case(B, c) for c in cases]
    return all(r["pass"] for r in results), results
```

---

## Code Cell 4 - Search Over Candidate Footing Sizes

```python
# Code Cell 4 - Sweep the candidate widths and find the smallest that passes all cases.
# Internals stay unrounded; formatting/rounding happens only when printing.

SEARCH = []
for B in B_CANDIDATES_M:
    ok, results = check_size(B, LOAD_CASES)
    worst_qmax = max(r["qmax_kpa"] for r in results)
    worst_qmin = min(r["qmin_kpa"] for r in results)
    SEARCH.append({
        "B_m": B,
        "pass": ok,
        "worst_qmax_kpa": worst_qmax,
        "worst_qmin_kpa": worst_qmin,
    })

print("Search over candidate square footing sizes")
print(f"{'B [m]':>7}{'max qmax [kPa]':>17}{'min qmin [kPa]':>17}{'result':>9}")
print("-" * 50)
for row in SEARCH:
    print(f"{row['B_m']:>7.1f}{row['worst_qmax_kpa']:>17.3f}"
          f"{row['worst_qmin_kpa']:>17.3f}{'PASS' if row['pass'] else 'FAIL':>9}")

passing = [row["B_m"] for row in SEARCH if row["pass"]]
if not passing:
    raise ValueError("No candidate width satisfies both checks; widen the search range.")

SELECTED_B_M = min(passing)
print()
print(f"Smallest passing width  B = {SELECTED_B_M:.1f} m")
print(f"Rejected widths         : {[row['B_m'] for row in SEARCH if not row['pass']]}")
```

---

## Markdown Cell 4 - Results Table by Load Case for the Selected Footing

The table below reports, for the selected width only, the governing pressures for each load case, the axial and bending components separately, the eccentricity check against the kern, and the pass/fail status of each criterion.

---

## Code Cell 5 - Results Table by Load Case (Selected Footing)

```python
# Code Cell 5 - Detailed results for the selected footing, one row per load case.

B = SELECTED_B_M
ok, results = check_size(B, LOAD_CASES)

A = base_area_m2(B)
S = section_modulus_m3(B)

print(f"Selected footing  B x B = {B:.1f} m x {B:.1f} m")
print(f"Base area A = B^2       = {A:.3f} m^2")
print(f"Section modulus S = B^3/6 = {S:.4f} m^3")
print(f"Allowable net pressure  = {Q_ALLOW_KPA:.0f} kPa")
print()

hdr = (f"{'Case':<6}{'N':>8}{'Mx':>7}{'My':>7}"
       f"{'q_axial':>10}{'q_bend':>9}{'qmax':>9}{'qmin':>9}"
       f"{'(e_x+e_y)':>11}{'B/6':>8}{'bearing':>9}{'uplift':>8}")
print("Pressures in kPa, moments in kNm, loads in kN, lengths in m")
print(hdr)
print("-" * len(hdr))

for r in results:
    print(f"{r['name']:<6}{r['N_kN']:>8.0f}{r['Mx_kNm']:>7.0f}{r['My_kNm']:>7.0f}"
          f"{r['q_axial_kpa']:>10.3f}{r['q_bending_kpa']:>9.3f}"
          f"{r['qmax_kpa']:>9.3f}{r['qmin_kpa']:>9.3f}"
          f"{r['e_sum_m']:>11.4f}{r['kern_m']:>8.4f}"
          f"{'PASS' if r['bearing_ok'] else 'FAIL':>9}"
          f"{'PASS' if r['uplift_ok'] else 'FAIL':>8}")

print()
print("Cross-check: planar superposition (qmin >= 0) vs kern criterion (e_x + e_y <= B/6)")
for r in results:
    agree = r["uplift_ok"] == r["kern_ok"]
    print(f"  {r['name']}: superposition={'OK' if r['uplift_ok'] else 'UPLIFT'}"
          f"  kern={'OK' if r['kern_ok'] else 'OUT'}"
          f"  -> {'consistent' if agree else 'INCONSISTENT (investigate)'}")
```

---

## Code Cell 6 - Governing Case and Final Summary

```python
# Code Cell 6 - Identify the governing load case and summarise the outcome.

B = SELECTED_B_M
ok, results = check_size(B, LOAD_CASES)
prev_row = [row for row in SEARCH if row["B_m"] < B][-1]

# Governing case against each limit, unrounded internally.
# Bearing: the case with the highest qmax has the smallest margin to q_allow.
# No-uplift: the case with the lowest qmin has the smallest margin to zero.
# (Both are direct comparisons of the limiting pressure, so no normalisation is
# needed - and no ratio that could be inverted by mistake.)
def bearing_margin_kpa(r):
    return Q_ALLOW_KPA - r["qmax_kpa"]


def uplift_margin_kpa(r):
    return r["qmin_kpa"] - Q_MIN_LIMIT_KPA


gov_bearing = min(results, key=bearing_margin_kpa)   # smallest bearing margin
gov_uplift = min(results, key=uplift_margin_kpa)     # smallest no-uplift margin

# Guard: at the selected width every case must pass, and the governing case must
# be the one that was critical at the rejected width just below it.
assert gov_uplift["uplift_ok"], "Governing no-uplift case must actually pass at the selected width."
assert gov_uplift["name"] == min(
    results, key=lambda r: r["qmin_kpa"]
)["name"]

print(f"Selected footing width        : B = {B:.1f} m")
print(f"Previously rejected width     : B = {prev_row['B_m']:.1f} m"
      f"  (qmin = {prev_row['worst_qmin_kpa']:.3f} kPa -> uplift, rejected)")
print(f"Governing case for size choice: {gov_uplift['name']} "
      f"(no-uplift governs the required width)")
print(f"  no-uplift margin at B={B:.1f} m: qmin = {gov_uplift['qmin_kpa']:.3f} kPa"
      f"  vs limit {Q_MIN_LIMIT_KPA:.0f} kPa"
      f"  -> margin {uplift_margin_kpa(gov_uplift):.3f} kPa")
print(f"Highest bearing utilisation   : {gov_bearing['name']} "
      f"qmax = {gov_bearing['qmax_kpa']:.2f} kPa vs {Q_ALLOW_KPA:.0f} kPa "
      f"({gov_bearing['qmax_kpa'] / Q_ALLOW_KPA * 100:.1f}% of allowable)")
print()

print("Per-case status at the selected width:")
for r in results:
    print(f"  {r['name']}: qmax = {r['qmax_kpa']:.2f} kPa, qmin = {r['qmin_kpa']:.2f} kPa"
          f"  -> {'PASS' if r['pass'] else 'FAIL'}")

print()
print("Final outcome:")
print(f"  ADOPT square pad footing B x B = {B:.1f} m x {B:.1f} m (preliminary sizing)")
print(f"  GOVERNING LOAD CASE = {gov_uplift['name']} (controls the no-uplift requirement)")
```

---

## Markdown Cell 5 - Final Engineering Conclusion

### Selected footing

**Adopt a square pad footing `3.0 m x 3.0 m`** (preliminary sizing only). This is the smallest width in the candidate set `2.4 m` to `3.2 m` that satisfies both the bearing and the no-uplift requirement for every service load case.

### Governing load case

**`LC2` (`N = 700 kN`, `Mx = 200 kNm`, `My = 140 kNm`) governs the required footing size.**

The selection is driven by the **no-uplift** criterion, not by bearing pressure:

- `LC2` has the lowest axial load combined with the highest moments, so it produces the largest eccentricity relative to the base. At `B = 2.9 m` it gives `qmin = -0.41 kPa`, i.e. a small uplift at one edge, and is rejected. At `B = 3.0 m` it gives `qmin = +2.22 kPa`, just inside the kern boundary `e_x + e_y = 0.4857 m <= B/6 = 0.5000 m`.
- `LC2` is therefore the **critical** case for sizing; it is the last case to become acceptable as `B` increases, and every case at `B = 3.0 m` passes.
- `LC2` is also the technically uncomfortable case: it passes with only about `2 kPa` of compressive edge pressure remaining. In final design this should be recognized as a case where the planar-pressure assumption is marginal and a partial-contact check, plus the omitted stability, settlement, and shear checks, may well govern instead.

For completeness, the **highest bearing pressure** at `B = 3.0 m` comes from a different case:

- `LC3` (`N = 1250 kN`) gives `qmax = 178.89 kPa` (about `81%` of the `220 kPa` allowable), so bearing is comfortable.
- `LC1` gives `qmax = 155.56 kPa` / `qmin = 88.89 kPa`.

| Case | `qmax` (kPa) | `qmin` (kPa) | Bearing | No uplift | Comment |
| --- | --- | --- | --- | --- | --- |
| LC1 | 155.56 | 88.89 | PASS | PASS | Comfortable; well inside the kern |
| LC2 | 153.33 | 2.22 | PASS | PASS | **Governing for sizing**; kern marginal |
| LC3 | 178.89 | 98.89 | PASS | PASS | Highest `qmax`, still `81%` of allowable |

### Why `B = 3.0 m` and not `2.9 m`

`B = 2.9 m` fails `LC2` on no-uplift (`qmin = -0.41 kPa`). The next candidate, `3.0 m`, clears it. So the selected width is not set by bearing capacity but by the requirement that the load resultant remains inside the kern under the most eccentric service case.

### Checks performed

1. **Bearing pressure** - `qmax <= 220 kPa` for all three service cases at `B = 3.0 m`. Satisfied, maximum utilisation `81%` (`LC3`).
2. **No uplift / full contact** - `qmin >= 0 kPa` for all three cases. Satisfied, minimum `qmin = 2.22 kPa` (`LC2`).
3. **Cross-check** - the planar-superposition no-uplift criterion agrees with the independent kern criterion `e_x + e_y <= B/6` for every case, as expected for a square base.

### Checks deliberately omitted

Footing self-weight; sliding; settlement (total and differential); punching shear; one-way shear; reinforcement design; flexural design of the footing; column-to-footing connection and local bearing; overturning/stability under moment alone; groundwater and soil layering effects; long-term and cyclic soil behaviour.

### Limitations and next steps before this size is fixed

1. **Dimensional check.** Verify the `3.0 m` square suits the site, adjacent structures, and services.
2. **Add self-weight and overburden.** If the `220 kPa` figure is gross rather than net, re-run with `N + W_footing` and confirm the pressure sign convention; this will push the required width up.
3. **Partial contact.** Because `LC2` passes only marginally on `qmin`, assess the nonlinear partial-contact case explicitly for a slightly smaller base before assuming `3.0 m` is comfortably adequate.
4. **Thickness and shear.** Punching and one-way shear typically control pad thickness; these must be checked before the size is frozen, and a thinner/larger footing may be more economical than a thick `3.0 m` pad.
5. **Confirm geotechnical inputs.** The `220 kPa` allowable net bearing pressure, and whether it is a service, net, or gross value, must be confirmed against the geotechnical report.
6. **Load combinations.** Confirm that `LC1`-`LC3` are the complete set of service combinations, including any wind or seismic cases with larger moments.
