# Raw Output

- task_id: `v3-notebook-01`
- model_id_used: `qwen-3.6plus`
- run_date: `2026-04-11`
- thinking_mode_used: `yes`

## Prompt Used

[Paste the exact prompt text from `tasks/notebook_01_pad_footing_sizing/prompt.md`.]

## Raw Model Output

<VSCode.Cell language="markdown">
# Square Pad Footing — Preliminary Sizing

## Assumptions, Exclusions, and Sign Conventions

### Assumptions
- **Rigid footing**: The pad footing is assumed rigid relative to the supporting soil, giving a linear soil-pressure distribution.
- **Linear elastic soil response**: Bearing pressure varies linearly across the footing base under combined axial load and biaxial moment.
- **Service loads only**: All loads are unfactored service-level loads.
- **Square footing**: Footing width `B` equals footing length `L`.

### Exclusions
The following checks are **not** performed in this preliminary sizing:
- Footing self-weight (conservative — actual self-weight increases bearing pressure)
- Sliding resistance
- Settlement (immediate or consolidation)
- Punching shear
- One-way (beam) shear
- Reinforcement design

### Sign Conventions
- **Axial load `N`**: Positive in compression (downward into the soil).
- **Moments `Mx`, `My`**: Positive moments produce compression on the positive face of the respective axis.
- **Eccentricities**: `ex = My / N` and `ey = Mx / N`. Positive eccentricities shift the resultant away from the centroid toward the positive axis direction.
- **Bearing pressure**: `q` is positive in compression (soil reaction upward).
- **No-uplift criterion**: `qmin >= 0` ensures the entire footing base remains in contact with the soil.

### Units
All calculations use consistent units:
- Force: **kN**
- Moment: **kNm**
- Length: **m**
- Pressure: **kPa** (= kN/m²)
</VSCode.Cell>

<VSCode.Cell language="markdown">
## Input Data

The following cell defines all input parameters: column dimensions, candidate footing sizes, allowable bearing pressure, and the three service load cases.
</VSCode.Cell>

<VSCode.Cell language="python">
# ============================================================
# Input Data
# ============================================================

# Column dimensions (for reporting only)
col_width = 0.400   # m
col_depth = 0.400   # m

# Candidate square footing sizes: 2.4 m to 3.2 m in 0.1 m increments
B_candidates = [round(2.4 + 0.1 * i, 1) for i in range(9)]  # [2.4, 2.5, ..., 3.2]

# Allowable net bearing pressure
q_allow = 220.0  # kPa

# Service load cases: (N_kN, Mx_kNm, My_kNm)
load_cases = {
    "LC1": {"N": 1100.0, "Mx": 90.0,  "My": 60.0},
    "LC2": {"N":  700.0, "Mx": 200.0, "My": 140.0},
    "LC3": {"N": 1250.0, "Mx": 70.0,  "My": 110.0},
}

print("Column size:", col_width, "m x", col_depth, "m")
print("Candidate footing sizes (m):", B_candidates)
print("Allowable bearing pressure (kPa):", q_allow)
print("Number of load cases:", len(load_cases))
</VSCode.Cell>

<VSCode.Cell language="markdown">
## Bearing Pressure Calculation Model

### Governing Equations

For a rigid square footing of width `B` under axial load `N` and biaxial moments `Mx`, `My`, the soil pressure at any point `(x, y)` on the footing base is:

```
q(x, y) = N / A + Mx * y / Ix + My * x / Iy
```

where:
- `A = B²` is the footing area
- `Ix = Iy = B⁴ / 12` is the second moment of area about each axis
- `x` and `y` are measured from the footing centroid, ranging from `-B/2` to `+B/2`

### Edge Pressures

The maximum and minimum pressures occur at the corners. Substituting `x = ±B/2` and `y = ±B/2`:

```
q_max = N / B² + 6 * Mx / B³ + 6 * My / B³
q_min = N / B² - 6 * Mx / B³ - 6 * My / B³
```

More precisely, using eccentricities `ex = My / N` and `ey = Mx / N`:

```
q_max = (N / B²) * (1 + 6*ex/B + 6*ey/B)
q_min = (N / B²) * (1 - 6*ex/B - 6*ey/B)
```

### Why This Model Is Appropriate

This linear elastic model is standard for preliminary footing sizing because:
1. It gives a quick, conservative estimate of peak bearing pressure.
2. It identifies whether uplift occurs (`qmin < 0`), which would require a nonlinear analysis.
3. It is the basis for most code-based preliminary checks before detailed geotechnical analysis.

### Derivation of Edge-Pressure Expression

Starting from the general flexure formula for combined axial load and biaxial bending:

```
σ = P/A + Mx*y/Ix + My*x/Iy
```

For a square footing with `Ix = Iy = B⁴/12` and `A = B²`, at the corner `(x, y) = (B/2, B/2)`:

```
q_corner = N/B² + Mx*(B/2)/(B⁴/12) + My*(B/2)/(B⁴/12)
         = N/B² + 6*Mx/B³ + 6*My/B³
```

The four corners are evaluated, and `qmax` and `qmin` are taken as the extreme values.
</VSCode.Cell>

<VSCode.Cell language="python">
# ============================================================
# Bearing Pressure Calculation Functions
# ============================================================

def calc_bearing_pressure(N, Mx, My, B):
    """
    Calculate maximum and minimum bearing pressures for a square footing.
    
    Parameters
    ----------
    N : float
        Axial load (kN), positive in compression.
    Mx : float
        Moment about x-axis (kNm).
    My : float
        Moment about y-axis (kNm).
    B : float
        Footing width (m).
    
    Returns
    -------
    q_max : float
        Maximum bearing pressure (kPa).
    q_min : float
        Minimum bearing pressure (kPa).
    """
    A = B ** 2
    I = B ** 4 / 12.0
    
    # Eccentricities
    ex = My / N  # eccentricity about y-axis due to My
    ey = Mx / N  # eccentricity about x-axis due to Mx
    
    # Corner pressures: q = N/A + Mx*y/I + My*x/I
    # Evaluate at all four corners: (+-B/2, +-B/2)
    half_B = B / 2.0
    
    corners = []
    for sx in [-1, 1]:
        for sy in [-1, 1]:
            x = sx * half_B
            y = sy * half_B
            q = N / A + Mx * y / I + My * x / I
            corners.append(q)
    
    q_max = max(corners)
    q_min = min(corners)
    
    return q_max, q_min


def check_footing(N, Mx, My, B, q_allow):
    """
    Check if a footing size satisfies bearing pressure and no-uplift criteria.
    
    Returns
    -------
    passes : bool
        True if both qmax <= q_allow and qmin >= 0.
    q_max : float
        Maximum bearing pressure (kPa).
    q_min : float
        Minimum bearing pressure (kPa).
    """
    q_max, q_min = calc_bearing_pressure(N, Mx, My, B)
    passes = (q_max <= q_allow) and (q_min >= 0.0)
    return passes, q_max, q_min


# Quick verification with LC1 and B = 3.0 m
q_max, q_min = calc_bearing_pressure(1100, 90, 60, 3.0)
print(f"LC1, B=3.0m: q_max = {q_max:.2f} kPa, q_min = {q_min:.2f} kPa")
</VSCode.Cell>

<VSCode.Cell language="markdown">
## Search Over Candidate Footing Sizes

This cell iterates through all candidate footing sizes and checks each load case. The smallest footing that passes all load cases is selected.
</VSCode.Cell>

<VSCode.Cell language="python">
# ============================================================
# Search Over Candidate Footing Sizes
# ============================================================

print("=" * 70)
print("FOOTING SIZE SEARCH")
print("=" * 70)
print(f"{'B (m)':<8} {'LC':<6} {'q_max (kPa)':<14} {'q_min (kPa)':<14} {'Pass':<6}")
print("-" * 70)

all_pass_by_B = {}

for B in B_candidates:
    all_pass = True
    for lc_name, lc in load_cases.items():
        passes, q_max, q_min = check_footing(lc["N"], lc["Mx"], lc["My"], B, q_allow)
        status = "OK" if passes else "FAIL"
        if not passes:
            all_pass = False
        print(f"{B:<8.1f} {lc_name:<6} {q_max:<14.2f} {q_min:<14.2f} {status:<6}")
    all_pass_by_B[B] = all_pass
    print("-" * 70)

# Select the smallest footing that passes all load cases
selected_B = None
for B in B_candidates:
    if all_pass_by_B[B]:
        selected_B = B
        break

if selected_B is not None:
    print(f"\nSelected footing size: B = {selected_B} m x {selected_B} m")
else:
    print("\nNo candidate footing size satisfies all load cases.")
</VSCode.Cell>

<VSCode.Cell language="markdown">
## Results Table for Selected Footing

The following cell presents a detailed results table for the selected footing size, showing bearing pressures and utilization ratios for each load case.
</VSCode.Cell>

<VSCode.Cell language="python">
# ============================================================
# Results Table for Selected Footing
# ============================================================

if selected_B is not None:
    print("=" * 80)
    print(f"RESULTS FOR SELECTED FOOTING: B = {selected_B} m x {selected_B} m")
    print("=" * 80)
    print(f"{'Load Case':<12} {'N (kN)':<10} {'Mx (kNm)':<10} {'My (kNm)':<10} "
          f"{'q_max (kPa)':<14} {'q_min (kPa)':<14} {'Utilization':<14} {'Status':<8}")
    print("-" * 80)
    
    governing_lc = None
    max_util = -1.0
    
    for lc_name, lc in load_cases.items():
        q_max, q_min = calc_bearing_pressure(lc["N"], lc["Mx"], lc["My"], selected_B)
        utilization = q_max / q_allow
        status = "OK" if (q_max <= q_allow and q_min >= 0) else "FAIL"
        
        if utilization > max_util:
            max_util = utilization
            governing_lc = lc_name
        
        print(f"{lc_name:<12} {lc['N']:<10.0f} {lc['Mx']:<10.1f} {lc['My']:<10.1f} "
              f"{q_max:<14.2f} {q_min:<14.2f} {utilization:<14.3f} {status:<8}")
    
    print("-" * 80)
    print(f"\nAllowable bearing pressure: {q_allow} kPa")
    print(f"Maximum utilization: {max_util:.3f} ({governing_lc})")
</VSCode.Cell>

<VSCode.Cell language="markdown">
## Final Engineering Conclusion

### Selected Footing Size

**Square pad footing: `B = {selected_B} m × {selected_B} m`**

### Governing Load Case

The governing load case is **`{governing_lc}`** with a bearing pressure utilization of **`{max_util:.1%}`** of the allowable `220 kPa`.

### Summary of Checks Performed

| Check | Criterion | Result |
|-------|-----------|--------|
| Bearing pressure | q_max ≤ 220 kPa | Satisfied for all LCs |
| No uplift | q_min ≥ 0 kPa | Satisfied for all LCs |

### Omitted Checks (to be verified in detailed design)

The following items are **not** covered by this preliminary sizing and must be checked in the detailed design stage:

1. **Footing self-weight**: Including self-weight will increase bearing pressures slightly.
2. **Sliding resistance**: Lateral loads and friction/adhesion at the soil–footing interface.
3. **Settlement**: Immediate and long-term settlement must be within tolerable limits.
4. **Punching shear**: Critical around the column perimeter; typically governs footing depth.
5. **One-way (beam) shear**: Along critical sections at `d` from the column face.
6. **Reinforcement design**: Flexural reinforcement in both directions.
7. **Geotechnical verification**: Allowable bearing pressure should be confirmed by a geotechnical engineer based on site-specific soil investigation.
8. **Load combinations**: Factored (ULS) load combinations per the applicable design code.

### Notes

- This draft uses **service loads only** and a **linear elastic soil model**.
- All internal calculations are unrounded; values are rounded only for reporting.
- Units are consistent throughout: kN, kNm, m, and kPa.
</VSCode.Cell>

<VSCode.Cell language="python">
# ============================================================
# Final Engineering Conclusion — Printed Summary
# ============================================================

if selected_B is not None:
    print("=" * 70)
    print("FINAL ENGINEERING CONCLUSION")
    print("=" * 70)
    print()
    print(f"Selected square pad footing: {selected_B} m x {selected_B} m")
    print(f"Column size: {col_width} m x {col_depth} m (for reporting)")
    print()
    print(f"Governing load case: {governing_lc}")
    print(f"  q_max = {calc_bearing_pressure(load_cases[governing_lc]['N'], load_cases[governing_lc]['Mx'], load_cases[governing_lc]['My'], selected_B)[0]:.2f} kPa")
    print(f"  Utilization = {max_util:.1%} of {q_allow} kPa allowable")
    print()
    print("All load cases satisfy:")
    print("  - Bearing pressure: q_max <= 220 kPa")
    print("  - No uplift: q_min >= 0 kPa")
    print()
    print("OMITTED CHECKS (verify in detailed design):")
    print("  - Footing self-weight")
    print("  - Sliding resistance")
    print("  - Settlement")
    print("  - Punching shear")
    print("  - One-way shear")
    print("  - Reinforcement design")
    print("=" * 70)
</VSCode.Cell>

