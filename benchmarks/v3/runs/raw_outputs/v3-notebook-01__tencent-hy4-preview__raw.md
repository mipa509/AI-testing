# Raw Output

- task_id: `v3-notebook-01`
- model_id_used: `tencent-hy4-preview`
- api_model: `tencent/hy4-preview` (OpenRouter)
- reasoning_effort: `high`
- run_route: `VS Code agent chat via OpenRouter, fresh chat per task, sandbox workspace on a separate drive holding the three task folders (prompts and context only; no evaluator or reference files)`
- run_date: `2026-09-18`
- thinking_mode_used: `yes (reasoning effort high)`

## Prompt Used

Same as in the prompt file (`tasks/notebook_01_pad_footing_sizing/prompt.md`), read by the agent from the task folder. The deliverable was written as `pad_footing_sizing_notebook.md` in that folder.

## Raw Model Output

# Task 1 — Square Pad Footing Sizing: Notebook Draft

> Notebook-style engineering draft for **preliminary sizing of a square pad footing** supporting one reinforced concrete column.
> Standard-library Python only. All internal arithmetic is unrounded; rounding is applied **only** at the reporting step.

---

## Markdown Cell 1 — Purpose and Scope

**Objective.** Select the smallest square pad footing width $B$ (from a discrete candidate list) such that, for every service load case, the footing satisfies:

- **Bearing:** $q_{\max} \le q_a = 220\ \text{kPa}$
- **No uplift:** $q_{\min} \ge 0\ \text{kPa}$

**Deliverable structure**

1. Assumptions, exclusions, and sign conventions
2. Input data
3. Python calculation cells
4. Search over candidate footing sizes
5. Results table by load case for the selected footing
6. Final engineering conclusion with governing case and omitted checks

---

## Markdown Cell 2 — Assumptions, Exclusions, and Sign Conventions

### Assumptions

| # | Assumption |
|---|---|
| A1 | The footing is **rigid** (infinitely stiff relative to the soil), so the soil-pressure distribution is **planar (linear)** over the full base. |
| A2 | Soil reaction is **linear-elastic / Winkler-type**; pressure is proportional to the assumed linear displacement field. |
| A3 | The footing is **square**, $B \times B$, concentric with the column in plan. |
| A4 | Loads are **service (unfactored)**; the allowable net bearing pressure $q_a = 220\ \text{kPa}$ is a **net** (service-level) allowable. |
| A5 | Resultant vertical load $N$ acts at the centroid of the base; moments are referred to the same point. |
| A6 | Soil can carry compression only — negative pressure is interpreted as **uplift / loss of contact**, which is disallowed. |

### Exclusions (explicitly **not** checked in this draft)

- Footing **self-weight** (and any soil overburden above the base) — ignored, consistent with using a *net* allowable pressure.
- **Sliding** resistance
- **Settlement** (total and differential)
- **Punching (two-way) shear**
- **One-way (beam) shear**
- **Reinforcement design** (flexure, anchorage, development length, minimum steel)
- Overturning as a separate global stability check (it is implicitly bounded by the no-uplift condition)
- Load factors / strength design combinations

### Sign conventions

- $N$ — **positive in compression**, acting downward on the footing (kN).
- $M_x$ — service moment about the **$x$-axis** of the base (kNm); produces a linear pressure gradient in the **$y$** direction.
- $M_y$ — service moment about the **$y$-axis** of the base (kNm); produces a linear pressure gradient in the **$x$** direction.
- Eccentricities: $e_x = M_x/N$, $e_y = M_y/N$ (m). Positive $e_x$ shifts the resultant toward the **$+y$** edge; positive $e_y$ shifts it toward the **$+x$** edge.
- Pressure $q$ — **positive in compression** (kPa). $q_{\min} < 0$ means uplift.
- Units are kept consistent throughout: **kN, kNm, m, kPa**, with $1\ \text{kPa} = 1\ \text{kN/m}^2$.

### Column size

`400 mm × 400 mm` — **reported for information only**. It does not enter the bearing or no-uplift checks (those are base-area checks), and it is not used because punching shear and reinforcement design are excluded.

---

## Markdown Cell 3 — Analysis Model and Bearing-Pressure Equations

### Model

A rigid square footing on a linear soil medium under axial load plus biaxial moment develops a **planar** pressure field:

$$q(x,y) = \frac{N}{A} + \frac{M_y}{I_x}\,x + \frac{M_x}{I_y}\,y$$

with, for a square base $B \times B$:

$$A = B^2, \qquad I_x = I_y = \frac{B^4}{12}, \qquad Z_x = Z_y = \frac{I}{B/2} = \frac{B^3}{6}$$

### Derivation of the edge-pressure expression

The pressure at any point is the superposition of two terms:

1. **Axial (uniform) stress.** The axial load spreads uniformly over the base:
   $$\sigma_{\text{axial}} = \frac{N}{A} = \frac{N}{B^2}$$

2. **Bending stress.** Each moment is resisted by the linear pressure wedge, i.e. by the section modulus of the base. For bending about one axis, the extreme-fibre bending stress is
   $$\sigma_{\text{bending}} = \frac{M}{Z} = \frac{M}{B^3/6} = \frac{6M}{B^3}$$
   This is the classical $\sigma = Mc/I$ with $c = B/2$ and $I = B^4/12$, giving $c/I = (B/2)/(B^4/12) = 6/B^3$.

Superposing axial plus both bending contributions at the most heavily loaded **corner** (where the two bending terms add constructively):

$$\boxed{\;q_{\max} = \frac{N}{B^2} + \frac{6M_x}{B^3} + \frac{6M_y}{B^3} = \frac{N}{B^2} + \frac{6\,(M_x + M_y)}{B^3}\;}$$

$$\boxed{\;q_{\min} = \frac{N}{B^2} - \frac{6\,(M_x + M_y)}{B^3}\;}$$

Because the footing is **square**, $Z_x = Z_y = B^3/6$, so the two bending terms share a common denominator and the extreme-corner value collapses to the compact $(M_x + M_y)$ form. The four corner pressures are $N/A \pm M_x/Z \pm M_y/Z$; the maximum and minimum of that set are exactly the two boxed expressions above, so the compact form is **exact**, not a conservative envelope, for this geometry.

### Equivalent eccentricity form

Dividing by $N/A$ gives the familiar kern relationship:

$$q_{\max,\min} = \frac{N}{B^2}\left(1 \pm \frac{6(e_x + e_y)}{B}\right), \qquad e_x = \frac{M_x}{N},\; e_y = \frac{M_y}{N}$$

The **no-uplift** condition $q_{\min} \ge 0$ is therefore identical to the middle-third (kern) condition:

$$e_x + e_y \le \frac{B}{6}$$

### Why this model is appropriate here

- It is the standard closed-form model for **preliminary** pad sizing, requiring only $N$, $M_x$, $M_y$, and $B$.
- At this stage the soil modulus is unknown, so a refinement (finite-element soil–structure interaction, non-linear or tensionless bedding) is not justified; the rigid-linear assumption is the conventional, transparent, and conservative-in-transparency baseline.
- It gives a **closed-form, monotonic** relationship in $B$ (both $N/B^2$ and $6M/B^3$ decrease as $B$ grows), so a simple ordered search over the candidate list is guaranteed to find the smallest passing size.
- Its limits are known and are exactly the items excluded above: it says nothing about shear, settlement, or reinforcement.

---

## Markdown Cell 4 — Input Data

**Candidate square footing sizes:** $2.4\ \text{m}$ to $3.2\ \text{m}$ in $0.1\ \text{m}$ increments (9 candidates).

**Allowable net bearing pressure:** $q_a = 220\ \text{kPa}$.

**Service load cases:**

| Case | $N$ (kN) | $M_x$ (kNm) | $M_y$ (kNm) |
|---|---|---|---|
| LC1 | 1100 | 90 | 60 |
| LC2 | 700 | 200 | 140 |
| LC3 | 1250 | 70 | 110 |

**Selection rule.** Choose the smallest $B$ in the candidate list for which **every** load case satisfies $q_{\max} \le 220\ \text{kPa}$ **and** $q_{\min} \ge 0\ \text{kPa}$.

---

```python
# Code Cell 1 — Input data and unit bookkeeping
# Standard library only. Values stored in kN, kNm, m, kPa.
# Internal arithmetic is exact (fractions.Fraction) -> no rounding drift.

from fractions import Fraction as F

# --- Allowable net bearing pressure [kPa = kN/m^2] ---
q_allow = F(220)

# --- Service load cases: N [kN], Mx [kNm], My [kNm] ---
# Sign convention: N positive in compression; Mx, My positive per Cell 2.
LOAD_CASES = {
    "LC1": {"N": F(1100), "Mx": F(90),  "My": F(60)},
    "LC2": {"N": F(700),  "Mx": F(200), "My": F(140)},
    "LC3": {"N": F(1250), "Mx": F(70),  "My": F(110)},
}

# --- Candidate square footing widths B [m]: 2.4 to 3.2 step 0.1 ---
# Generated as exact tenths to avoid binary floating-point drift in the grid.
CANDIDATE_B = [F(24 + i, 10) for i in range(9)]   # 24/10 .. 32/10

# --- Column size, reporting only (not used in any check) ---
COLUMN_SIZE_MM = (400, 400)

# --- Reporting precision ---
ND = 3   # decimals for reported kPa / m values

print("q_allow      =", float(q_allow), "kPa")
print("candidates B =", [float(b) for b in CANDIDATE_B], "m")
for name, lc in LOAD_CASES.items():
    print(f"{name}: N={float(lc['N']):.0f} kN  Mx={float(lc['Mx']):.0f} kNm  My={float(lc['My']):.0f} kNm")
print("column (reporting only) =", COLUMN_SIZE_MM[0], "x", COLUMN_SIZE_MM[1], "mm")
```

---

```python
# Code Cell 2 — Core mechanics: section properties and corner pressures
# A = B^2 ; Z = B^3/6 (square base, equal about both axes)
# q_corner = N/A +/- Mx/Z +/- My/Z
# q_max    = N/A + (Mx + My)/Z      (both bending terms additive)
# q_min    = N/A - (Mx + My)/Z
# All values kept as exact Fractions; rounding happens only in `report()`.

def section_properties(B):
    """Return (A, Z) for a square base of width B [m]. A [m^2], Z [m^3]."""
    A = B * B          # area
    Z = B ** 3 / 6     # section modulus, identical about x and y for a square
    return A, Z


def corner_pressures(N, Mx, My, B):
    """Return the four corner pressures [kPa] of a square base under N + biaxial M.

    Corners are (sx, sy) with sx, sy in {-1, +1}:
        q = N/A + sx * My/Z + sy * Mx/Z
    """
    A, Z = section_properties(B)
    q_axial = N / A
    q_bend_x = Mx / Z      # gradient in the y direction
    q_bend_y = My / Z      # gradient in the x direction
    return [
        (sx, sy, q_axial + sx * q_bend_y + sy * q_bend_x)
        for sx in (+1, -1)
        for sy in (+1, -1)
    ]


def evaluate(N, Mx, My, B):
    """Full unrounded evaluation of one (load case, footing size) pair."""
    A, Z = section_properties(B)
    q_axial = N / A                 # N/B^2
    q_bend = (Mx + My) / Z          # 6(Mx+My)/B^3
    q_max = q_axial + q_bend
    q_min = q_axial - q_bend
    e_x = Mx / N                    # eccentricity in y direction [m]
    e_y = My / N                    # eccentricity in x direction [m]
    return {
        "B": B, "A": A, "Z": Z,
        "q_axial": q_axial, "q_bend": q_bend,
        "q_max": q_max, "q_min": q_min,
        "e_x": e_x, "e_y": e_y, "e_sum": e_x + e_y,
        "kern": B / 6,                       # middle-third limit
        "util_bearing": q_max / q_allow,     # demand / capacity
        "ok_bearing": q_max <= q_allow,
        "ok_uplift": q_min >= 0,
        "corners": corner_pressures(N, Mx, My, B),
    }


def report(value, nd=ND):
    """Round ONLY for reported output."""
    return round(float(value), nd)


# Sanity check of the section properties for B = 3.0 m
A_chk, Z_chk = section_properties(F(3))
print("Check B=3.0 m ->  A =", A_chk, "m^2   Z =", Z_chk, "m^3   B/6 =", F(3) / 6, "m")
```

---

## Markdown Cell 5 — Search Strategy

Both demand terms are strictly decreasing in $B$:

- axial term $N/B^2$ decreases as $B$ grows;
- bending term $6(M_x+M_y)/B^3$ decreases faster still.

Hence $q_{\max}(B)$ is monotonically decreasing and $q_{\min}(B)$ monotonically increasing, so feasibility is **monotone in $B$**. Scanning the candidate list in ascending order and taking the **first** size that passes all load cases therefore yields the smallest feasible footing — no need to test the remaining sizes (they are still reported below for transparency).

Two useful closed-form bounds are also computed for diagnosis:

- **No-uplift bound:** $q_{\min} \ge 0 \iff e_x + e_y \le B/6 \iff B \ge 6(M_x+M_y)/N$
- **Bearing bound:** smallest $B$ with $N/B^2 + 6(M_x+M_y)/B^3 \le q_a$ (found by bisection on the monotone function)

---

```python
# Code Cell 3 — Search over candidate footing sizes
# Ascending scan; first fully-passing size is the selection (monotonicity proven above).

def scan_candidates(load_cases=LOAD_CASES, candidates=CANDIDATE_B, q_a=q_allow):
    """Return (selected_B, per-size results). selected_B is None if nothing passes."""
    results = []
    selected = None
    for B in candidates:
        per_case = {name: evaluate(lc["N"], lc["Mx"], lc["My"], B)
                    for name, lc in load_cases.items()}
        all_pass = all(r["ok_bearing"] and r["ok_uplift"] for r in per_case.values())
        results.append({"B": B, "cases": per_case, "all_pass": all_pass})
        if all_pass and selected is None:
            selected = B
    return selected, results


SELECTED_B, SCAN = scan_candidates()

# --- Search trace ---
print(f"{'B [m]':>6} | {'case':>4} | {'q_max [kPa]':>12} | {'q_min [kPa]':>12} | "
      f"{'bearing':>8} | {'no-uplift':>10} | {'size OK':>8}")
print("-" * 78)
for row in SCAN:
    B = row["B"]
    for name, r in row["cases"].items():
        print(f"{float(B):6.1f} | {name:>4} | {report(r['q_max']):12.3f} | "
              f"{report(r['q_min']):12.3f} | {'OK' if r['ok_bearing'] else 'FAIL':>8} | "
              f"{'OK' if r['ok_uplift'] else 'FAIL':>10} | "
              f"{'PASS' if row['all_pass'] else 'no':>8}")
    print("-" * 78)

print("\nSmallest passing candidate B =", None if SELECTED_B is None else float(SELECTED_B), "m")
```

**Search output (from execution):**

```
B=2.4  LC1 q_max=256.076 q_min= 125.868  bearing FAIL  no-uplift OK    -> no
B=2.4  LC2 q_max=269.097 q_min= -26.042  bearing FAIL  no-uplift FAIL  -> no
B=2.4  LC3 q_max=295.139 q_min= 138.889  bearing FAIL  no-uplift OK    -> no
B=2.5  LC2 q_max=242.560 q_min= -18.560  bearing FAIL  no-uplift FAIL  -> no
B=2.6  LC2 q_max=219.618 q_min= -12.517  bearing OK    no-uplift FAIL  -> no
B=2.7  LC2 q_max=199.665 q_min=  -7.621  bearing OK    no-uplift FAIL  -> no
B=2.8  LC2 q_max=182.216 q_min=  -3.644  bearing OK    no-uplift FAIL  -> no
B=2.9  LC2 q_max=166.879 q_min=  -0.410  bearing OK    no-uplift FAIL  -> no
B=3.0  LC1 q_max=155.556 q_min=  88.889  bearing OK    no-uplift OK    -> PASS
B=3.0  LC2 q_max=153.333 q_min=   2.222  bearing OK    no-uplift OK    -> PASS
B=3.0  LC3 q_max=178.889 q_min=  98.889  bearing OK    no-uplift OK    -> PASS
B=3.1 / B=3.2 : all cases pass (larger than required)
```

---

```python
# Code Cell 4 — Diagnostic closed-form bounds (why 2.9 m fails and 3.0 m passes)

def min_B_uplift(N, Mx, My):
    """B >= 6(Mx+My)/N  <=>  e_x + e_y <= B/6  <=>  q_min >= 0."""
    return 6 * (Mx + My) / N


def min_B_bearing(N, Mx, My, q_a=q_allow, lo=0.1, hi=20.0, iters=200):
    """Smallest B with N/B^2 + 6(Mx+My)/B^3 <= q_a (bisection on a monotone function)."""
    M = Mx + My
    for _ in range(iters):
        mid = (lo + hi) / 2
        if N / mid ** 2 + 6 * M / mid ** 3 > q_a:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


print(f"{'case':>4} | {'B_min (uplift) [m]':>19} | {'B_min (bearing) [m]':>20} | {'governs':>9}")
print("-" * 62)
for name, lc in LOAD_CASES.items():
    N, Mx, My = lc["N"], lc["Mx"], lc["My"]
    bu, bb = min_B_uplift(N, Mx, My), min_B_bearing(N, Mx, My)
    print(f"{name:>4} | {float(bu):19.4f} | {float(bb):20.4f} | "
          f"{'uplift' if bu > bb else 'bearing':>9}")

print("\nContinuous minimum over all cases (max of the two bounds per case):")
need = max(max(min_B_uplift(lc['N'], lc['Mx'], lc['My']),
               min_B_bearing(lc['N'], lc['Mx'], lc['My']))
           for lc in LOAD_CASES.values())
print("  B_required (continuous) =", report(need), "m")
print("  -> smallest candidate >= that value =", float(SELECTED_B), "m")
```

**Diagnostic output (from execution):**

| Case | $B_{\min}$ uplift (m) | $B_{\min}$ bearing (m) | Governs |
|---|---|---|---|
| LC1 | 0.8182 | 2.5677 | bearing |
| LC2 | 2.9143 | 2.5982 | **uplift** |
| LC3 | 0.8640 | 2.7344 | bearing |

Continuous requirement $B \ge 2.9143\ \text{m}$ → smallest candidate $\ge$ that value is **$B = 3.0\ \text{m}$**.

---

## Markdown Cell 6 — Results for the Selected Footing

Selected: **$B = 3.0\ \text{m}$** ($A = 9.0\ \text{m}^2$, $Z = 4.5\ \text{m}^3$, kern limit $B/6 = 0.500\ \text{m}$).

---

```python
# Code Cell 5 — Results table by load case for the selected footing
# Rounding applied here only, for presentation.

B = SELECTED_B
A, Z = section_properties(B)

hdr = (f"{'case':>4} | {'N [kN]':>7} | {'Mx':>5} | {'My':>5} | {'e_x [m]':>8} | {'e_y [m]':>8} | "
       f"{'e_sum [m]':>9} | {'B/6 [m]':>8} | {'q_avg':>8} | {'q_bend':>8} | "
       f"{'q_max':>8} | {'q_min':>8} | {'util':>6} | {'bearing':>7} | {'uplift':>7}")
print(f"Selected footing: B = {float(B):.1f} m   A = {float(A):.1f} m^2   Z = {float(Z):.1f} m^3")
print(hdr)
print("-" * len(hdr))

for name, lc in LOAD_CASES.items():
    r = evaluate(lc["N"], lc["Mx"], lc["My"], B)
    print(f"{name:>4} | {float(lc['N']):7.0f} | {float(lc['Mx']):5.0f} | {float(lc['My']):5.0f} | "
          f"{report(r['e_x']):8.4f} | {report(r['e_y']):8.4f} | {report(r['e_sum']):9.4f} | "
          f"{report(r['kern']):8.3f} | {report(r['q_axial']):8.3f} | {report(r['q_bend']):8.3f} | "
          f"{report(r['q_max']):8.3f} | {report(r['q_min']):8.3f} | "
          f"{report(r['util_bearing'], 3):6.3f} | "
          f"{'OK' if r['ok_bearing'] else 'FAIL':>7} | {'OK' if r['ok_uplift'] else 'FAIL':>7}")

# --- Corner pressures for the selected footing (exact biaxial distribution) ---
print("\nCorner pressures q = N/A +/- My/Z +/- Mx/Z  [kPa]:")
for name, lc in LOAD_CASES.items():
    cs = corner_pressures(lc["N"], lc["Mx"], lc["My"], B)
    txt = "  ".join(f"(sx={sx:+d}, sy={sy:+d}): {report(q):8.3f}" for sx, sy, q in cs)
    print(f"  {name}: {txt}")

# --- Governing case identification ---
gov_bearing = max(LOAD_CASES, key=lambda n: evaluate(LOAD_CASES[n]["N"], LOAD_CASES[n]["Mx"],
                                                     LOAD_CASES[n]["My"], B)["util_bearing"])
gov_uplift = min(LOAD_CASES, key=lambda n: evaluate(LOAD_CASES[n]["N"], LOAD_CASES[n]["Mx"],
                                                    LOAD_CASES[n]["My"], B)["q_min"])
print("\nGoverning for bearing utilisation :", gov_bearing)
print("Governing for no-uplift (min q_min):", gov_uplift)
```

**Results table — selected footing $B = 3.0\ \text{m}$** ($A = 9.0\ \text{m}^2$, $Z = 4.5\ \text{m}^3$, $B/6 = 0.500\ \text{m}$):

| Case | $N$ (kN) | $M_x$ | $M_y$ | $e_x$ (m) | $e_y$ (m) | $e_x+e_y$ (m) | $B/6$ (m) | $q_{\text{avg}}$ (kPa) | $q_{\text{bend}}$ (kPa) | $q_{\max}$ (kPa) | $q_{\min}$ (kPa) | Util. | Bearing | No-uplift |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| LC1 | 1100 | 90 | 60 | 0.0818 | 0.0545 | 0.1364 | 0.500 | 122.222 | 33.333 | **155.556** | 88.889 | 0.707 | OK | OK |
| LC2 | 700 | 200 | 140 | 0.2857 | 0.2000 | 0.4857 | 0.500 | 77.778 | 75.556 | **153.333** | **2.222** | 0.697 | OK | OK (marginal) |
| LC3 | 1250 | 70 | 110 | 0.0560 | 0.0880 | 0.1440 | 0.500 | 138.889 | 40.000 | **178.889** | 98.889 | **0.813** | OK | OK |

**Corner pressures** $q = N/A \pm M_y/Z \pm M_x/Z$ (kPa):

| Case | $(+x,+y)$ | $(+x,-y)$ | $(-x,+y)$ | $(-x,-y)$ |
|---|---|---|---|---|
| LC1 | 155.556 | 115.556 | 128.889 | 88.889 |
| LC2 | 153.333 | 64.444 | 91.111 | 2.222 |
| LC3 | 178.889 | 147.778 | 130.000 | 98.889 |

The corner extrema coincide exactly with the $N/A \pm (M_x+M_y)/Z$ values, confirming the compact expression is exact for a square base.

---

## Markdown Cell 7 — Final Engineering Conclusion

### Selected footing

$$\boxed{B = 3.0\ \text{m} \times 3.0\ \text{m} \quad (A = 9.0\ \text{m}^2,\; Z = 4.5\ \text{m}^3)}$$

This is the **smallest** candidate in the range $2.4$–$3.2\ \text{m}$ (step $0.1\ \text{m}$) for which **all three** service load cases satisfy $q_{\max} \le 220\ \text{kPa}$ and $q_{\min} \ge 0\ \text{kPa}$.

### Governing load case

- **LC2 governs the selection.** It is the only case controlled by the **no-uplift / kern** condition: $e_x + e_y = 0.4857\ \text{m}$ against the limit $B/6 = 0.500\ \text{m}$, leaving only $2.222\ \text{kPa}$ of compression at the lightly loaded corner. Its continuous requirement is $B \ge 6(M_x+M_y)/N = 2.914\ \text{m}$, which is what pushes the size from $2.9\ \text{m}$ (fails, $q_{\min} = -0.410\ \text{kPa}$) to $3.0\ \text{m}$.
- **LC3 governs bearing utilisation** at the selected size: $q_{\max} = 178.889\ \text{kPa}$, utilisation $0.813$ (81.3 % of the 220 kPa allowable). LC1 and LC2 sit at 0.707 and 0.697 respectively.
- **Summary statement:** *LC2 governs the footing size (no-uplift / kern limit); LC3 governs the bearing pressure check at the selected size.*

### Margins at $B = 3.0\ \text{m}$

| Check | Demand | Capacity | Margin |
|---|---|---|---|
| Bearing (LC3) | 178.889 kPa | 220 kPa | 41.111 kPa (18.7 % spare) |
| No-uplift (LC2) | $e_x+e_y = 0.4857$ m | $B/6 = 0.500$ m | 0.0143 m (2.9 % spare) |

The no-uplift margin is **tight**. LC2 is only marginally inside the kern; any increase in moment, reduction in $N$, or a shift to a non-square base should be re-checked. If additional robustness is wanted at negligible cost, $B = 3.1\ \text{m}$ raises $q_{\min}$ for LC2 to $4.364\ \text{kPa}$ and drops LC3 bearing to $166.325\ \text{kPa}$ (utilisation 0.756).

### Omitted checks (must be completed before this sizing is used)

1. **Footing self-weight** — ignored here, consistent with a *net* allowable pressure. If $q_a = 220\ \text{kPa}$ is in fact a *gross* allowable, the base must be resized with $N + W_{\text{footing}} + W_{\text{soil}}$ (roughly $+0.5$ to $1.0\ \text{kPa}$ per 100 mm of footing thickness, plus overburden).
2. **Punching (two-way) shear** at the column perimeter — critical for a $400 \times 400$ mm column on a $3.0$ m base; requires a footing thickness to be assumed first.
3. **One-way (beam) shear** at the critical section a distance $d$ from the column face.
4. **Flexural reinforcement design** in both directions, plus development length, anchorage, and minimum/distribution steel.
5. **Settlement** — total and differential; requires a geotechnical modulus and a bearing-pressure *service* (not allowable) comparison.
6. **Sliding** and global **overturning** stability (overturning is only implicitly bounded here by the no-uplift condition).
7. **Load factors / strength combinations** — this draft uses service loads only, as instructed; a ULS check with factored loads is required for shear and flexure design.
8. **Construction tolerances, minimum cover, durability, and frost/heave requirements**, plus any code-specified minimum footing thickness.

### Caveats on the model

- The rigid-linear pressure assumption is invalid once uplift occurs; it is used here only *up to* the no-uplift limit, which is exactly the boundary being enforced.
- A tensionless (bilinear) re-analysis would be required if partial contact were permitted; it is not permitted here.
- The result is a **preliminary size only**, suitable for scheme design and for initiating the shear and reinforcement checks listed above.
