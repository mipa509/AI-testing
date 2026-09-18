# Raw Output

- task_id: `v3-notebook-01`
- model_id_used: `anon-2026-09-19`
- api_model: `undisclosed at scoring time (placeholder id; to be replaced when the user names the model)`
- reasoning_effort: `not recorded`
- run_route: `agentic CLI coding session (vendor undisclosed at scoring time), fresh session per task, sandbox workspace on a separate drive holding the task folder (prompt and context files only; no evaluator or reference files)`
- run_date: `2026-09-19`
- thinking_mode_used: `not recorded`

## Prompt Used

Same as in the prompt file (`tasks/notebook_01_pad_footing_sizing/prompt.md`), read by the agent from the task folder. The deliverable was written as `response.md` in that folder.

## Raw Model Output

# Square Pad Footing – Preliminary Sizing Notebook Draft

**Task:** Preliminary sizing of a square pad footing supporting one reinforced-concrete column (400 mm × 400 mm), service loads only, bearing-pressure and no-uplift checks.

**Status:** Draft for Chartered Engineer review. Not for construction.

---

## Markdown Cell 1 — Assumptions, exclusions and sign conventions

### 1.1 Scope of this check

Preliminary plan-size selection of a square pad footing under axial service load plus biaxial service moments. Two criteria only:

| Check | Criterion |
|---|---|
| Bearing pressure | `q_max ≤ q_allow = 220 kPa` (allowable **net** bearing pressure) |
| No uplift | `q_min ≥ 0 kPa` (full contact over the whole base) |

Service (unfactored, SLS-type) loads are used throughout, consistent with a permissible-pressure style check (BS 8004 / EN 1997-1 §6.5.2 serviceability-type verification). No partial factors are applied to actions or to soil resistance.

### 1.2 Assumptions

- Footing is **square**, width `B` (m), plan area `A = B²`.
- Footing is **rigid** relative to the soil, so the base pressure distribution is **linear** (planar) under `N + Mx + My`. This is the standard preliminary model (Navier / combined-stress approach) used in BS 8004, EN 1997-1 Annex D commentary and Bowles, *Foundation Analysis and Design*, and is justified while:
  - the footing thickness is of the same order as its cantilever projection (typical for pad footings, so the base does not deflect appreciably relative to the soil), and
  - the resultant remains within the middle-third **kern**, so the whole base stays in compression and the linear superposition of axial and bending stress is valid.
- The soil is treated as a linear-elastic bed of uniform stiffness. Real stress redistribution at the corners is ignored; this is conservative for `q_max`.
- Loads act at the column base and are transferred to the footing centroid without any additional eccentricity (column concentric on footing).
- Moments are applied about the footing centroidal axes; no shear-induced moments at underside are added (footing depth not defined).
- Column size 400 mm × 400 mm is for **reporting only**; it does not enter the two checks.
- Allowable net bearing pressure `q_allow = 220 kPa` is a given design parameter. Its derivation (SI, SLS/ULS basis) is outside this draft.

### 1.3 Exclusions (per brief)

Not checked here, must be covered in later design stages:

- footing self-weight and backfill surcharge (hence "net" pressure is compared directly with column loads),
- sliding,
- settlement,
- punching shear,
- one-way (beam) shear,
- reinforcement design,
- overturning stability factor (partially covered by the no-uplift check),
- ULS bearing resistance to EN 1997-1 §6.5.2 (DA1 combinations).

### 1.4 Sign convention and eccentricities

Right-handed axes at the footing centroid, `x` and `y` parallel to the footing sides, `z` downward.

| Symbol | Meaning | Unit |
|---|---|---|
| `N` | Axial column load, **compression positive** (downward) | kN |
| `Mx` | Moment **about the x-axis**; causes pressure variation along **y** | kNm |
| `My` | Moment **about the y-axis**; causes pressure variation along **x** | kNm |
| `ey = Mx / N` | Eccentricity of resultant along **y** | m |
| `ex = My / N` | Eccentricity of resultant along **x** | m |
| `q` | Soil contact pressure, **compression positive** | kPa (= kN/m²) |

Positive `Mx` shifts the resultant to `+y`; positive `My` shifts it to `+x`. Because the footing is square and doubly symmetric, the sign of each moment only selects which corner is most heavily loaded. The absolute values `|Mx|`, `|My|` are therefore used; `q_max` occurs at the corner `(+B/2, +B/2)` and `q_min` at the diagonally opposite corner `(−B/2, −B/2)`.

### 1.5 Bearing-pressure equations

Section properties of the square base:

```
A  = B²                     plan area                    [m²]
Ix = Iy = B⁴ / 12           second moment of area        [m⁴]
Zx = Zy = I / (B/2) = B³/6  elastic section modulus      [m³]
```

Combined-stress (Navier) pressure at any point `(x, y)` on the base:

```
q(x, y) = N/A + Mx·y/Ix + My·x/Iy
```

Evaluating at the corner `y = +B/2`, `x = +B/2`:

```
q_corner = N/A + Mx·(B/2)/(B⁴/12) + My·(B/2)/(B⁴/12)
         = N/B² + 6·Mx/B³ + 6·My/B³
```

Hence the edge (corner) pressures used for the checks:

```
q_max = N/B² + 6·(|Mx| + |My|) / B³
q_min = N/B² − 6·(|Mx| + |My|) / B³
```

i.e. axial stress `N/A` plus/minus bending stress `M/Z` in each direction, superposed. Units: `kN / m² = kPa`, `kNm / m³ = kPa`, so no conversion factors are required.

**Validity limit.** The linear formula holds only while `q_min ≥ 0`. Equivalently the resultant lies within the kern of a square:

```
|ex|/B + |ey|/B ≤ 1/6
```

If `q_min < 0` the base would partially lift off and the pressure would have to be recomputed on the compressed zone. In this task `q_min < 0` is itself a **failure** of the no-uplift criterion, so the partial-contact solution is not needed; the case is simply reported as failing.

---

## Markdown Cell 2 — Input data

All quantities in kN, kNm, m, kPa. Values are taken directly from the engineering brief.

```python
# Code Cell 1 — Input data (standard library only)

# Column (reporting only – not used in the checks)
COLUMN_SIZE_MM = (400, 400)                     # mm x mm

# Soil
Q_ALLOW_KPA = 220.0                             # allowable NET bearing pressure [kPa]

# Candidate footing widths: 2.4 m to 3.2 m in 0.1 m steps.
# Built from integers (decimetres) to avoid floating-point drift in the loop.
CANDIDATE_B_M = [i / 10 for i in range(24, 33)]  # [2.4, 2.5, ..., 3.2]

# Service load cases: N [kN] compression +ve, Mx [kNm] about x, My [kNm] about y
LOAD_CASES = {
    "LC1": {"N": 1100.0, "Mx": 90.0,  "My": 60.0},
    "LC2": {"N": 700.0,  "Mx": 200.0, "My": 140.0},
    "LC3": {"N": 1250.0, "Mx": 70.0,  "My": 110.0},
}

print(f"Column           : {COLUMN_SIZE_MM[0]} mm x {COLUMN_SIZE_MM[1]} mm (reporting only)")
print(f"Allowable q_net  : {Q_ALLOW_KPA:.0f} kPa")
print(f"Candidate widths : {CANDIDATE_B_M} m")
for name, lc in LOAD_CASES.items():
    print(f"{name}: N = {lc['N']:.0f} kN, Mx = {lc['Mx']:.0f} kNm, My = {lc['My']:.0f} kNm")
```

Expected output:

```
Column           : 400 mm x 400 mm (reporting only)
Allowable q_net  : 220 kPa
Candidate widths : [2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2] m
LC1: N = 1100 kN, Mx = 90 kNm, My = 60 kNm
LC2: N = 700 kN, Mx = 200 kNm, My = 140 kNm
LC3: N = 1250 kN, Mx = 70 kNm, My = 110 kNm
```

---

## Markdown Cell 3 — Calculation functions

The functions below implement the equations of §1.5. All internal arithmetic is left **unrounded**; rounding is applied only in the printing/reporting cells. Each function is small and pure so it can be unit-tested or hand-checked independently.

```python
# Code Cell 2 — Section properties and corner pressures

from dataclasses import dataclass


@dataclass(frozen=True)
class PressureResult:
    """Bearing-pressure results for one footing size and one load case (unrounded)."""
    case: str
    B: float          # footing width [m]
    N: float          # axial load [kN]
    Mx: float         # moment about x [kNm]
    My: float         # moment about y [kNm]
    ex: float         # eccentricity along x = |My|/N [m]
    ey: float         # eccentricity along y = |Mx|/N [m]
    q_avg: float      # N/A [kPa]
    q_bend: float     # 6(|Mx|+|My|)/B^3 [kPa]
    q_max: float      # corner max pressure [kPa]
    q_min: float      # corner min pressure [kPa]
    kern_ratio: float # |ex|/B + |ey|/B  (<= 1/6 for full contact)
    ok_bearing: bool
    ok_uplift: bool

    @property
    def ok(self) -> bool:
        return self.ok_bearing and self.ok_uplift


def section_properties(B: float) -> tuple[float, float]:
    """Return (A, Z) for a square base of width B [m]: A = B^2 [m^2], Z = B^3/6 [m^3]."""
    if B <= 0:
        raise ValueError("Footing width B must be positive")
    A = B * B
    Z = B ** 3 / 6.0
    return A, Z


def corner_pressures(B: float, N: float, Mx: float, My: float) -> tuple[float, float]:
    """
    Linear (Navier) corner pressures for a rigid square footing.
        q_max = N/A + (|Mx| + |My|)/Z
        q_min = N/A - (|Mx| + |My|)/Z
    Units: N [kN], Mx, My [kNm], B [m]  ->  q [kPa].
    """
    if N <= 0:
        raise ValueError("N must be compressive (positive) for a bearing check")
    A, Z = section_properties(B)
    q_avg = N / A
    q_bend = (abs(Mx) + abs(My)) / Z
    return q_avg + q_bend, q_avg - q_bend


def check_case(case: str, B: float, N: float, Mx: float, My: float,
               q_allow: float) -> PressureResult:
    """Evaluate bearing and no-uplift criteria for one footing size and one load case."""
    A, Z = section_properties(B)
    q_max, q_min = corner_pressures(B, N, Mx, My)
    ex = abs(My) / N
    ey = abs(Mx) / N
    return PressureResult(
        case=case, B=B, N=N, Mx=Mx, My=My,
        ex=ex, ey=ey,
        q_avg=N / A,
        q_bend=(abs(Mx) + abs(My)) / Z,
        q_max=q_max, q_min=q_min,
        kern_ratio=ex / B + ey / B,
        ok_bearing=q_max <= q_allow,
        ok_uplift=q_min >= 0.0,
    )
```

```python
# Code Cell 3 — Hand check of the derivation on one case (LC1, B = 3.0 m)

B_chk, lc = 3.0, LOAD_CASES["LC1"]
A_chk, Z_chk = section_properties(B_chk)

# Long-hand version of §1.5 (axial stress + bending stress in each direction)
q_axial   = lc["N"] / B_chk**2                  # N / A
q_bend_x  = 6 * lc["Mx"] / B_chk**3             # Mx / Z
q_bend_y  = 6 * lc["My"] / B_chk**3             # My / Z
q_max_hand = q_axial + q_bend_x + q_bend_y
q_min_hand = q_axial - q_bend_x - q_bend_y

q_max_fn, q_min_fn = corner_pressures(B_chk, lc["N"], lc["Mx"], lc["My"])

print(f"A = {A_chk:.3f} m2, Z = {Z_chk:.4f} m3")
print(f"N/A     = {q_axial:.2f} kPa")
print(f"Mx/Z    = {q_bend_x:.2f} kPa")
print(f"My/Z    = {q_bend_y:.2f} kPa")
print(f"q_max   = {q_max_hand:.2f} kPa (function: {q_max_fn:.2f})")
print(f"q_min   = {q_min_hand:.2f} kPa (function: {q_min_fn:.2f})")
assert abs(q_max_hand - q_max_fn) < 1e-9 and abs(q_min_hand - q_min_fn) < 1e-9
print("Hand derivation and function agree.")
```

Expected output:

```
A = 9.000 m2, Z = 4.5000 m3
N/A     = 122.22 kPa
Mx/Z    = 20.00 kPa
My/Z    = 13.33 kPa
q_max   = 155.56 kPa (function: 155.56)
q_min   = 88.89 kPa (function: 88.89)
Hand derivation and function agree.
```

---

## Markdown Cell 4 — Search over candidate footing sizes

Widths are evaluated in ascending order. For each width all three load cases are checked. The selected footing is the **smallest** `B` for which *every* case satisfies both `q_max ≤ 220 kPa` and `q_min ≥ 0 kPa`. A full pass/fail matrix is printed so that the governing criterion and case are visible, not just the answer.

```python
# Code Cell 4 — Search

def evaluate_width(B: float, load_cases: dict, q_allow: float) -> list[PressureResult]:
    return [check_case(name, B, lc["N"], lc["Mx"], lc["My"], q_allow)
            for name, lc in load_cases.items()]


def select_footing(candidates: list[float], load_cases: dict, q_allow: float):
    """Return (selected_B, results_by_B). selected_B is None if nothing passes."""
    results_by_B = {}
    selected = None
    for B in candidates:                      # ascending order
        res = evaluate_width(B, load_cases, q_allow)
        results_by_B[B] = res
        if selected is None and all(r.ok for r in res):
            selected = B
    return selected, results_by_B


B_SEL, RESULTS = select_footing(CANDIDATE_B_M, LOAD_CASES, Q_ALLOW_KPA)

# Pass/fail matrix (values rounded for display only)
hdr = f"{'B [m]':>6} | " + " | ".join(f"{n:^25}" for n in LOAD_CASES) + " | all OK"
print(hdr)
print("-" * len(hdr))
for B, res in RESULTS.items():
    cells = []
    for r in res:
        flag = "OK " if r.ok else ("BRG" if not r.ok_bearing else "UPL")
        cells.append(f"{r.q_max:7.1f}/{r.q_min:7.1f} {flag}")
    print(f"{B:>6.1f} | " + " | ".join(f"{c:^25}" for c in cells)
          + f" | {'YES' if all(r.ok for r in res) else 'no'}")

print()
print("Cell format: q_max / q_min [kPa]  flag  (BRG = bearing fails, UPL = uplift fails)")
if B_SEL is None:
    print("No candidate width satisfies all load cases – extend the search range.")
else:
    print(f"Smallest passing width: B = {B_SEL:.1f} m")
```

Expected output:

```
 B [m] |            LC1            |            LC2            |            LC3            | all OK
------------------------------------------------------------------------------------------------------
   2.4 |    256.1/  125.9 BRG      |    269.1/  -26.0 BRG      |    295.1/  138.9 BRG      | no
   2.5 |    233.6/  118.4 BRG      |    242.6/  -18.6 BRG      |    269.1/  130.9 BRG      | no
   2.6 |    213.9/  111.5 OK       |    219.6/  -12.5 UPL      |    246.4/  123.5 BRG      | no
   2.7 |    196.6/  105.2 OK       |    199.7/   -7.6 UPL      |    226.3/  116.6 BRG      | no
   2.8 |    181.3/   99.3 OK       |    182.2/   -3.6 UPL      |    208.6/  110.2 OK       | no
   2.9 |    167.7/   93.9 OK       |    166.9/   -0.4 UPL      |    192.9/  104.4 OK       | no
   3.0 |    155.6/   88.9 OK       |    153.3/    2.2 OK       |    178.9/   98.9 OK       | YES
   3.1 |    144.7/   84.3 OK       |    141.3/    4.4 OK       |    166.3/   93.8 OK       | YES
   3.2 |    134.9/   80.0 OK       |    130.6/    6.1 OK       |    155.0/   89.1 OK       | YES

Cell format: q_max / q_min [kPa]  flag  (BRG = bearing fails, UPL = uplift fails)
Smallest passing width: B = 3.0 m
```

Note: for `B = 2.4 m` and `2.5 m`, LC2 fails **both** criteria; the flag shows the bearing failure first. From `B = 2.6 m` upward the only remaining LC2 failure is uplift.

---

## Markdown Cell 5 — Results table by load case for the selected footing

Detailed results for `B = B_SEL`. Utilisation is `q_max / q_allow`. The uplift margin is `q_min` itself (kPa of residual compression at the least-loaded corner). The kern ratio `|ex|/B + |ey|/B` must be `≤ 1/6 ≈ 0.1667` for full contact and is reported as an independent check on `q_min ≥ 0`.

```python
# Code Cell 5 — Results table for the selected footing

if B_SEL is None:
    raise SystemExit("No footing selected – see search above.")

res_sel = RESULTS[B_SEL]
A_sel, Z_sel = section_properties(B_SEL)

print(f"Selected footing: {B_SEL:.1f} m x {B_SEL:.1f} m square "
      f"(A = {A_sel:.2f} m2, Z = {Z_sel:.3f} m3), column {COLUMN_SIZE_MM[0]} x {COLUMN_SIZE_MM[1]} mm")
print()
cols = ["Case", "N [kN]", "Mx [kNm]", "My [kNm]", "ex [m]", "ey [m]",
        "N/A [kPa]", "M/Z [kPa]", "q_max [kPa]", "q_min [kPa]", "Util.", "Kern", "Bearing", "Uplift"]
print(" | ".join(f"{c:>11}" for c in cols))
print("-" * (14 * len(cols)))
for r in res_sel:
    row = [r.case, f"{r.N:.0f}", f"{r.Mx:.0f}", f"{r.My:.0f}",
           f"{r.ex:.3f}", f"{r.ey:.3f}",
           f"{r.q_avg:.1f}", f"{r.q_bend:.1f}",
           f"{r.q_max:.1f}", f"{r.q_min:.1f}",
           f"{r.q_max / Q_ALLOW_KPA:.2f}", f"{r.kern_ratio:.3f}",
           "PASS" if r.ok_bearing else "FAIL",
           "PASS" if r.ok_uplift else "FAIL"]
    print(" | ".join(f"{v:>11}" for v in row))

# Governing cases
gov_bearing = max(res_sel, key=lambda r: r.q_max)
gov_uplift  = min(res_sel, key=lambda r: r.q_min)
print()
print(f"Governing bearing case : {gov_bearing.case}  (q_max = {gov_bearing.q_max:.1f} kPa, "
      f"utilisation {gov_bearing.q_max / Q_ALLOW_KPA:.2f})")
print(f"Governing uplift case  : {gov_uplift.case}  (q_min = {gov_uplift.q_min:.1f} kPa, "
      f"kern ratio {gov_uplift.kern_ratio:.4f} vs limit {1/6:.4f})")
```

Expected output:

```
Selected footing: 3.0 m x 3.0 m square (A = 9.00 m2, Z = 4.500 m3), column 400 x 400 mm

       Case |      N [kN] |    Mx [kNm] |    My [kNm] |      ex [m] |      ey [m] |   N/A [kPa] |   M/Z [kPa] | q_max [kPa] | q_min [kPa] |       Util. |        Kern |     Bearing |      Uplift
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        LC1 |        1100 |          90 |          60 |       0.055 |       0.082 |       122.2 |        33.3 |       155.6 |        88.9 |        0.71 |       0.045 |        PASS |        PASS
        LC2 |         700 |         200 |         140 |       0.200 |       0.286 |        77.8 |        75.6 |       153.3 |         2.2 |        0.70 |       0.162 |        PASS |        PASS
        LC3 |        1250 |          70 |         110 |       0.088 |       0.056 |       138.9 |        40.0 |       178.9 |        98.9 |        0.81 |       0.048 |        PASS |        PASS

Governing bearing case : LC3  (q_max = 178.9 kPa, utilisation 0.81)
Governing uplift case  : LC2  (q_min = 2.2 kPa, kern ratio 0.1619 vs limit 0.1667)
```

Summary table for the report (rounded values, `B = 3.0 m`):

| Case | N (kN) | Mx (kNm) | My (kNm) | ex (m) | ey (m) | q_max (kPa) | q_min (kPa) | Utilisation | Bearing | Uplift |
|---|---|---|---|---|---|---|---|---|---|---|
| LC1 | 1100 | 90 | 60 | 0.055 | 0.082 | 155.6 | 88.9 | 0.71 | PASS | PASS |
| LC2 | 700 | 200 | 140 | 0.200 | 0.286 | 153.3 | 2.2 | 0.70 | PASS | PASS |
| LC3 | 1250 | 70 | 110 | 0.088 | 0.056 | 178.9 | 98.9 | 0.81 | PASS | PASS |

```python
# Code Cell 6 — Independent verification: closed-form minimum width from the kern rule

# Full contact requires (|ex| + |ey|)/B <= 1/6  ->  B >= 6 (|ex| + |ey|) = 6 (|Mx| + |My|) / N.
# Bearing requires N/B^2 + 6 (|Mx|+|My|)/B^3 <= q_allow; solve by bisection (q_max decreases with B).

def b_min_uplift(N, Mx, My):
    return 6.0 * (abs(Mx) + abs(My)) / N

def b_min_bearing(N, Mx, My, q_allow, lo=0.5, hi=20.0, tol=1e-9):
    def excess(B):
        return corner_pressures(B, N, Mx, My)[0] - q_allow
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if excess(mid) > 0:
            lo = mid
        else:
            hi = mid
        if hi - lo < tol:
            break
    return hi

def round_up_to_increment(x, step=0.1):
    import math
    return math.ceil(round(x / step, 9)) * step

print(f"{'Case':>5} | {'B_min uplift [m]':>17} | {'B_min bearing [m]':>18}")
overall = 0.0
for name, lc in LOAD_CASES.items():
    bu = b_min_uplift(lc["N"], lc["Mx"], lc["My"])
    bb = b_min_bearing(lc["N"], lc["Mx"], lc["My"], Q_ALLOW_KPA)
    overall = max(overall, bu, bb)
    print(f"{name:>5} | {bu:17.3f} | {bb:18.3f}")

B_closed = round_up_to_increment(overall, 0.1)
print(f"\nExact minimum width (all cases) = {overall:.3f} m -> next 0.1 m increment = {B_closed:.1f} m")
assert abs(B_closed - B_SEL) < 1e-9, "Search result disagrees with closed form"
print("Closed-form minimum agrees with the search.")
```

Expected output:

```
 Case |  B_min uplift [m] |  B_min bearing [m]
  LC1 |             0.818 |              2.568
  LC2 |             2.914 |              2.598
  LC3 |             0.864 |              2.734

Exact minimum width (all cases) = 2.914 m -> next 0.1 m increment = 3.0 m
Closed-form minimum agrees with the search.
```

---

## Markdown Cell 6 — Final engineering conclusion

### Selected footing

**Square pad footing `B = 3.0 m × 3.0 m`** under the 400 mm × 400 mm column.

### Governing case and criterion

- **Governing criterion: no-uplift (`q_min ≥ 0`) under `LC2`** (`N = 700 kN`, `Mx = 200 kNm`, `My = 140 kNm`). This is the low-axial, high-moment case; the resultant eccentricity `|ex| + |ey| = 0.486 m` requires `B ≥ 2.914 m` to keep the resultant inside the middle-third kern. At `B = 2.9 m` the far corner goes to `q_min = −0.4 kPa` (fails); at `B = 3.0 m` it is `+2.2 kPa` (passes, kern ratio 0.162 vs limit 0.167).
- **Bearing pressure is governed by `LC3`** (`q_max = 178.9 kPa`, utilisation 0.81 of 220 kPa), but bearing alone would have been satisfied from `B = 2.8 m` upward. It is therefore **not** the governing criterion for size selection.
- All three load cases pass both checks at `B = 3.0 m`. The next smaller candidate (`2.9 m`) fails only the LC2 uplift check.

### Engineering observations for the reviewer

1. **Uplift margin is small.** `q_min = 2.2 kPa` under LC2 means the footing is only just in full contact. Any additional eccentricity (column setting-out tolerance, construction tolerance on the footing, a moment from horizontal shear acting over the footing depth) could put the corner into tension. Given the brief's exclusions this is reported, not resolved. Consider either accepting a partial-contact (redistributed) check at the detailed design stage or adopting `B = 3.1 m` (`q_min = 4.4 kPa`) if tolerances are significant.
2. **Self-weight omitted (per brief).** Including footing self-weight and backfill would *increase* `N` under LC2 and *improve* the uplift margin, while slightly increasing `q_max` under LC3. The result is therefore conservative for uplift and marginally unconservative for bearing; both effects are modest at 0.81 utilisation.
3. **Linear pressure model.** Appropriate at preliminary stage for a rigid square pad with resultant inside the kern. The selection rule (`q_min ≥ 0`) itself guarantees the model's validity for the chosen size.

### Checks omitted from this draft (must follow)

- ULS bearing resistance to EN 1997-1 §6.5.2 (Design Approach 1, Combinations 1 and 2) using the site-specific ground model — the 220 kPa allowable value is used here only as a preliminary permissible pressure.
- Settlement (total and differential) to EN 1997-1 §6.6.
- Sliding resistance (§6.5.3) — horizontal loads not provided.
- Overturning / EQU limit state with partial factors.
- Punching shear (EN 1992-1-1 §6.4) and one-way shear (§6.2) — govern footing depth.
- Flexural reinforcement design (EN 1992-1-1 §6.1, §9.8.2).
- Footing self-weight, backfill and any water-table effects on net pressure.
- Construction and setting-out tolerances on eccentricity.
- Column-base moment transfer / starter bar anchorage.

### Verification carried out within this draft

- Hand derivation of `q_max`, `q_min` from `N/A ± Mx/Z ± My/Z` reproduced by the coded function (Code Cell 3).
- Search result cross-checked against the closed-form kern limit `B ≥ 6(|Mx|+|My|)/N` and a bisection solve of the bearing inequality (Code Cell 6): exact minimum 2.914 m, rounded up to the 3.0 m increment.

**Chartered Engineer review required before this sizing is used for any further design or issued outside the design team.**
