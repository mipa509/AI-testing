# Raw Output

- task_id: `v2-anchor-07`
- model_id_used: `tencent-hy4-preview`
- api_model: `tencent/hy4-preview` (OpenRouter)
- reasoning_effort: `high`
- run_route: `VS Code agent chat via OpenRouter, fresh chat per task, sandbox workspace on a separate drive holding the three task folders (prompts and context only; no evaluator or reference files)`
- run_date: `2026-09-18`
- thinking_mode_used: `yes (reasoning effort high)`

## Prompt Used

Same as in the prompt file (`tasks/anchor_07_v1_task6_ec3/prompt.md`), read by the agent from the task folder including the two header lines above the `text` block. The response was written to `response.md` in that folder.

## Context Files Shared

- none

## Raw Model Output

# Task 7 — EC3 Bending Resistance Review: 254×102×28 UB

**Verdict: the section is NOT adequate.** The snippet contains two errors that are individually fatal and which, by coincidence, partially mask each other. Once corrected, the beam passes the *cross-section* bending check at 93% utilisation — but it fails **lateral-torsional buckling by a factor of ~2.9** and **deflection by a factor of ~2.5**. The original code's "PASS" is an artefact of a unit bug, not a real result.

---

## 1. Errors in the original snippet

### Error 1 — Wrong section property: minor-axis modulus used for major-axis bending (engineering logic)

```python
Wpl_z = 49.0e3   # mm^3   <- plastic modulus about z-z axis
```

A simply supported beam carrying vertical gravity load bends about its **major (y-y) axis**. The resistance must therefore use `Wpl,y`, not `Wpl,z`. For a UB the z-z axis is the weak axis; using it here understates the true capacity by a factor of ~7.

The value is also wrong even for the axis it names. Tabulated `Wpl,z` for a 254×102×28 is **54.8 cm³ = 54.8×10³ mm³**, not 49.0×10³ mm³ — the coded figure is ~11% low. (49.0 cm³ does not correspond to any published property of this section; it appears to be an invented or mis-transcribed number.)

Correct value: **`Wpl,y = 353 cm³ = 353.4×10³ mm³`**.

### Error 2 — Unit conversion missing: N·mm reported as kN·m (units)

```python
M_Rd = (Wpl_z * fy) / gamma_M0   # kN.m
```

`mm³ × N/mm² = N·mm`. To reach kN·m you must divide by **10⁶**. The comment claims kN·m but the arithmetic yields N·mm, so `M_Rd` is overstated by a factor of one million:

```
49.0e3 mm³ × 275 N/mm² = 13,475,000 N·mm  →  the code calls this 13,475,000 "kN.m"
                                          →  true value = 13.475 kN.m
```

### Why the two errors nearly cancel — and why the "PASS" is meaningless

| | Value |
|---|---|
| `M_Ed` (as coded) | 88.89 kN·m |
| `M_Rd` (as coded, N·mm mislabelled kN·m) | 13,475,000 |
| `util` (as printed) | **0.0000** → "PASS" |

The utilisation is `88.89 / 13,475,000 = 6.6 × 10⁻⁶`. The snippet prints `0.0000` and declares PASS purely because the denominator is a million times too large. **This is not a pass — it is a unit bug.** Had the units been right but the axis still wrong, the result would have been `88.89 / 13.475 = 6.60` → FAIL. The two errors happen to push in opposite directions, which is exactly why this class of bug survives casual review.

### Error 3 — Self-weight omitted

The beam weighs 28.3 kg/m ≈ **0.278 kN/m**, which at ULS (γ_G = 1.35) adds 0.375 kN/m — about 2% of the applied load. Small here, but it must be declared rather than silently dropped.

### Error 4 — No load factors, and the load basis is undefined

`w = 18.5` is used directly as the design load with no statement of whether it is characteristic or already factored. This is the single largest source of uncertainty in the result (see §4).

### Error 5 — Checks omitted entirely

The snippet performs only Cl. 6.2.5 bending. A real EC3 beam check also requires:

- **Cl. 5.5 / Table 5.2** — section classification (the "Class 1" claim is asserted, never verified)
- **Cl. 6.2.6** — shear resistance
- **Cl. 6.2.8** — shear/moment interaction
- **Cl. 6.3.2** — **lateral-torsional buckling** (governs here, decisively)
- **Cl. 7.2** — deflection (serviceability)

### What the snippet got right

- `M_Ed = wL²/8` for a simply supported beam under UDL — correct.
- `γ_M0 = 1.0` — correct for cross-section resistance (EN 1993-1-1, UK NA).
- `f_y = 275 N/mm²` — correct for S275 with `t_f = 10 mm ≤ 16 mm` (EN 10025-2 Table 3.1). No thickness de-rating needed.
- **The "Class 1" claim is in fact correct** — verified in §3 below.

---

## 2. Section properties and their source

All values below are for **UB 254×102×28**, taken from **BS EN 10365:2017** (the current dimensional/properties standard, which superseded BS 4-1:2005), as tabulated in the **SCI P363 "Blue Book"** (Steel Construction Institute / Tata Steel). Cross-checked against two independent published tables (CivilAxis, tabulated from BS EN 10365:2017 / SCI P363; Structolution, EN 10365). Values agree to within rounding.

| Property | Symbol | Value | Unit |
|---|---|---|---|
| Depth | `h` | 260.4 | mm |
| Width | `b` | 102.2 | mm |
| Web thickness | `t_w` | 6.3 | mm |
| Flange thickness | `t_f` | 10.0 | mm |
| Root radius | `r` | 7.6 | mm |
| Area | `A` | 36.1 | cm² |
| Mass | — | 28.3 | kg/m |
| 2nd moment, major | `I_y` | 4000 | cm⁴ |
| 2nd moment, minor | `I_z` | 179 | cm⁴ |
| Elastic modulus, major | `W_el,y` | 308 | cm³ |
| **Plastic modulus, major** | **`W_pl,y`** | **353** | **cm³** |
| Elastic modulus, minor | `W_el,z` | 34.9 | cm³ |
| Plastic modulus, minor | `W_pl,z` | 54.8 | cm³ |
| Torsion constant | `I_t` | 9.57 | cm⁴ |
| Warping constant | `I_w` | 0.028 | dm⁶ |

Material/analysis constants: `E = 210,000 N/mm²`, `G = 81,000 N/mm²`, `f_y = 275 N/mm²`, `γ_M0 = γ_M1 = 1.0`.

**Independent sanity check on `W_pl,y`** — computed from bare geometry (ignoring fillets):

```
W_pl,y = b·t_f·(h − t_f) + t_w·(h − 2t_f)²/4
       = 102.2 × 10.0 × 250.4 + 6.3 × 240.4²/4
       = 255,909 + 91,022 = 346,931 mm³
```

Adding ~2% for root fillets gives **353,870 mm³ ≈ 354 cm³**, matching the tabulated 353 cm³. The property is confirmed. (The same check on the minor axis gives 54,610 mm³ → ~55.7 cm³ with fillets, again confirming that 49.0 cm³ is wrong.)

---

## 3. Corrected calculation — full working

### 3.1 Classification (EN 1993-1-1 Cl. 5.5, Table 5.2)

```
ε = √(235 / f_y) = √(235 / 275) = 0.9244
```

**Outstand flange (compression):**
```
c = (b − t_w − 2r) / 2 = (102.2 − 6.3 − 2×7.6) / 2 = 40.35 mm
c / t_f = 40.35 / 10.0 = 4.04
Class 1 limit = 9ε = 8.32        →  4.04 < 8.32  ✓ Class 1
```

**Web (pure bending):**
```
c = h − 2t_f − 2r = 260.4 − 20.0 − 15.2 = 225.2 mm
c / t_w = 225.2 / 6.3 = 35.7
Class 1 limit = 72ε = 66.6       →  35.7 < 66.6  ✓ Class 1
```

**Section is Class 1.** The colleague's assertion was right, but it should be demonstrated, not assumed. Class 1 permits the plastic modulus `W_pl,y` to be used.

### 3.2 Design moment

Taking `w = 18.5 kN/m` as an **already-factored ULS load** (the most favourable reading; see §4 for the alternative):

```
self-weight        = 28.3 kg/m × 9.81 / 1000 = 0.278 kN/m
w_Ed               = 18.5 + 1.35 × 0.278 = 18.875 kN/m
M_Ed               = w_Ed · L² / 8 = 18.875 × 6.2² / 8 = 90.69 kN·m
```

### 3.3 Bending resistance (Cl. 6.2.5)

```
M_pl,Rd = W_pl,y · f_y / γ_M0
        = 353.4×10³ mm³ × 275 N/mm² / 1.0
        = 97,185,000 N·mm
        = 97.19 kN·m          ← note the ÷10⁶
```

### 3.4 Cross-section utilisation

```
util = M_Ed / M_pl,Rd = 90.69 / 97.19 = 0.933
```

**Cross-section bending: PASS at 93%.** But this is only valid if the compression flange is fully laterally restrained. It is not — see §3.6.

### 3.5 Shear (Cl. 6.2.6)

```
A_v = A − 2b·t_f + (t_w + 2r)·t_f
    = 3610 − 2×102.2×10.0 + (6.3 + 2×7.6)×10.0 = 1781 mm²
    (min. A_v = (h − 2t_f)·t_w = 1515 mm² — not governing)

V_pl,Rd = A_v · f_y / (√3 · γ_M0) = 1781 × 275 / (1.732 × 1.0) = 282.8 kN
V_Ed    = w_Ed · L / 2 = 18.875 × 6.2 / 2 = 58.5 kN
util    = 58.5 / 282.8 = 0.21        ✓ PASS
```

Web slenderness `h_w/t_w = 38.2 < 72ε = 66.6` → no shear buckling check needed.
`V_Ed = 58.5 kN < 0.5 V_pl,Rd = 141 kN` → **no reduction of `M_pl,Rd` for shear** (Cl. 6.2.8). The bending check above stands unreduced.

### 3.6 Lateral-torsional buckling (Cl. 6.3.2) — **GOVERNING FAILURE**

The snippet omits this entirely. For an unrestrained 6.2 m span it dominates by a wide margin.

**Elastic critical moment** (Cl. 6.3.2.2, general expression; `C₁ = 1.132`, `C₂ = 0.459` for UDL on a simply supported span, `z_g = 0` for load at shear centre):

```
M_cr = C₁ · (π²EI_z / L²) · √[ I_w/I_z + L²GI_t/(π²EI_z) + (C₂z_g)² ]
     = 1.132 × (π² × 210000 × 179×10⁴ / 6200²) × √[ 2.79×10¹⁰/179×10⁴
                                                    + 6200² × 81000 × 9.57×10⁴ / (π² × 210000 × 179×10⁴) ]
     = 33.8 kN·m
```

**Slenderness and reduction factor:**

```
λ̅_LT = √(M_pl,Rd / M_cr) = √(97.19 / 33.8) = 1.695
h/b = 260.4/102.2 = 2.55 > 2  →  α_LT = 0.49  (curve c, Table 6.5)

Φ_LT = 0.5 [1 + α_LT(λ̅_LT − 0.4) + 0.75λ̅_LT²]
     = 0.5 [1 + 0.49(1.695 − 0.4) + 0.75 × 1.695²] = 1.895

χ_LT = 1 / (Φ_LT + √(Φ_LT² − 0.75λ̅_LT²)) = 1 / (1.895 + √(3.591 − 2.155)) = 0.323   (≤ 1.0 ✓)

M_b,Rd = χ_LT · M_pl,Rd = 0.323 × 97.19 = 31.4 kN·m
```

**Utilisation = 90.69 / 31.4 = 2.89 → FAIL by a factor of ~2.9.**

If the load is applied at the top flange (destabilising, `z_g = +h/2`), `M_cr` drops to 27.9 kN·m, `χ_LT = 0.278`, `M_b,Rd = 27.0 kN·m`, and utilisation rises to **3.36**.

**How much restraint would be needed?** `M_b,Rd` vs unrestrained length:

| `L_b` (m) | `M_cr` (kN·m) | `λ̅_LT` | `χ_LT` | `M_b,Rd` (kN·m) | Utilisation |
|---|---|---|---|---|---|
| 1.0 | 558.4 | 0.42 | 0.990 | 96.3 | 0.94 ✓ |
| 1.5 | 265.9 | 0.60 | 0.883 | 85.8 | 1.06 ✗ |
| 2.0 | 162.5 | 0.77 | 0.780 | 75.8 | 1.20 ✗ |
| 2.5 | 113.7 | 0.92 | 0.686 | 66.6 | 1.36 ✗ |
| 3.0 | 86.5 | 1.06 | 0.603 | 58.6 | 1.55 ✗ |
| 4.0 | 58.1 | 1.29 | 0.478 | 46.4 | 1.95 ✗ |
| 6.2 | 33.8 | 1.69 | 0.323 | 31.4 | 2.89 ✗ |

Even at **1.5 m** unrestrained the section fails. Full restraint (or very nearly full restraint, `L_b ≲ 1.0 m`) is required for the 93% cross-section result to be usable.

### 3.7 Deflection (Cl. 7.2) — **ALSO FAILS**

```
δ = 5 w_ser L⁴ / (384 E I_y)
  = 5 × 18.78 × 6200⁴ / (384 × 210000 × 4000×10⁴)
  = 43.0 mm  =  L/144
```

Against the usual limits: `L/360 = 17.2 mm`, `L/250 = 24.8 mm`. **43 mm fails both, by 2.5× against L/360.**

At this load the section could only span **4.57 m** before hitting L/360; conversely at 6.2 m the maximum serviceability load for L/360 is only **7.5 kN/m** — well below the 18.5 kN/m applied.

---

## 4. Sensitivity: what if 18.5 kN/m is characteristic, not factored?

The snippet never says. If `w = 18.5` is a **characteristic** load, the design moment rises and the section fails the cross-section check too:

| Assumption | `w_Ed` (kN/m) | `M_Ed` (kN·m) | Utilisation vs `M_pl,Rd` | Result |
|---|---|---|---|---|
| 18.5 already ULS, self-weight included | 18.88 | 90.69 | 0.933 | PASS |
| 18.5 already ULS, self-weight ignored | 18.50 | 88.89 | 0.915 | PASS |
| 18.5 characteristic, γ_G = 1.35 | 25.35 | 121.81 | 1.253 | **FAIL** |
| 18.5 characteristic, γ_Q = 1.5 | 28.12 | 135.14 | 1.391 | **FAIL** |

**This ambiguity must be resolved before any conclusion is drawn.** The 93% figure is only defensible if 18.5 kN/m is already a ULS combination value.

---

## 5. Summary of results

| Check | Clause | Demand | Capacity | Utilisation | Result |
|---|---|---|---|---|---|
| Classification | 5.5 | — | — | — | Class 1 ✓ |
| Bending (cross-section) | 6.2.5 | 90.69 kN·m | 97.19 kN·m | 0.93 | PASS |
| Shear | 6.2.6 | 58.5 kN | 282.8 kN | 0.21 | PASS |
| M–V interaction | 6.2.8 | — | — | — | Not applicable ✓ |
| **Lateral-torsional buckling** | **6.3.2** | **90.69 kN·m** | **31.4 kN·m** | **2.89** | **FAIL** |
| **Deflection** | **7.2** | **43.0 mm** | **17.2 mm (L/360)** | **2.50** | **FAIL** |

### Is the section adequate?

**No.**

- On **cross-section bending alone**, and only if the compression flange is fully restrained and 18.5 kN/m is already a ULS value, it passes at **93%** — but with almost no reserve.
- **Unrestrained over 6.2 m it carries only 31.4 kN·m against a demand of 90.7 kN·m** — a factor of ~2.9 short. This is the governing limit state and the snippet does not check it at all.
- **Deflection is 43 mm = L/144**, roughly 2.5× the L/360 limit. Even a perfectly restrained beam would be rejected on serviceability.
- If 18.5 kN/m is characteristic rather than factored, the section fails cross-section bending as well (utilisation 1.25–1.39).

The original snippet's "PASS" is spurious — it is the product of a 10⁶ unit error, not a genuine margin.

### Recommendations

1. **Provide full lateral restraint** to the compression flange, or reduce the unrestrained length to ≲1.0 m. Without this the beam cannot work at any practical load.
2. **Increase the section.** For an unrestrained 6.2 m span carrying this load, a much stockier section is needed. Indicative `M_b,Rd` at 6.2 m (S275, UDL, load at shear centre):

   | Section | `M_pl,Rd` | `M_cr` | `χ_LT` | `M_b,Rd` | Util. | δ (mm) |
   |---|---|---|---|---|---|---|
   | 254×102×28 | 97.1 | 33.8 | 0.324 | 31.4 | 2.89 ✗ | 43.0 ✗ |
   | 305×127×37 | 148.2 | 58.6 | 0.357 | 52.9 | 1.71 ✗ | 24.1 ✗ |
   | 356×127×39 | 179.8 | 68.2 | 0.346 | 62.1 | 1.46 ✗ | 17.0 ~ |
   | **305×165×40** | 172.2 | 186.1 | 0.663 | 114.1 | **0.80 ✓** | 20.4 ✗ |
   | **356×171×45** | 213.1 | 237.9 | 0.672 | 143.2 | **0.63 ✓** | **14.3 ✓** |
   | 406×178×54 | 289.0 | 318.6 | 0.668 | 193.1 | 0.47 ✓ | 9.3 ✓ |

   A **356×171×45** is the smallest of these that satisfies both LTB and L/360 deflection. Note the pattern: the narrow sections (102–127 mm flanges) all fail LTB regardless of depth — **flange width, not depth, is what buys LTB capacity here.**
3. **Confirm the load basis** for the 18.5 kN/m before finalising.
4. **Add deflection and LTB to the check routine.** A bending-only check gives false confidence on exactly this class of beam.

---

## 6. Corrected code

```python
"""EC3 bending + LTB + deflection check - UB 254x102x28, S275.
Section properties: BS EN 10365:2017 / SCI P363 (Blue Book).
"""
import math

# ---------------- Inputs ----------------
L      = 6.2          # m, span
w_uls  = 18.5         # kN/m, ULS uniform load (CONFIRM: characteristic or factored?)
w_ser  = 18.5         # kN/m, serviceability load for deflection
Lb     = 6.2          # m, unrestrained length of compression flange
restrained = False    # set True if compression flange is fully restrained

# ---------------- Section: UB 254x102x28 (BS EN 10365:2017 / SCI P363) ----------------
h, b, tw, tf, r = 260.4, 102.2, 6.3, 10.0, 7.6      # mm
A     = 36.1e2        # mm^2
Iy    = 4000e4        # mm^4
Iz    = 179e4         # mm^4
Wply  = 353.4e3       # mm^3  <- MAJOR axis (y-y). NOT Wpl,z.
Wely  = 308e3         # mm^3
It    = 9.57e4        # mm^4
Iw    = 2.79e10       # mm^6
mass  = 28.3          # kg/m

# ---------------- Material ----------------
fy, E, G = 275.0, 210000.0, 81000.0                 # N/mm^2
gM0, gM1 = 1.0, 1.0

# ---------------- Classification (Cl. 5.5) ----------------
eps = math.sqrt(235.0 / fy)
cf  = (b - tw - 2*r) / 2
cw  = h - 2*tf - 2*r
cls_f = 1 if cf/tf <= 9*eps  else (2 if cf/tf <= 10*eps  else 3)
cls_w = 1 if cw/tw <= 72*eps else (2 if cw/tw <= 83*eps  else 3)
cls  = max(cls_f, cls_w)
W_eff = Wply if cls <= 2 else Wely                  # plastic if Class 1/2, else elastic

# ---------------- Actions ----------------
sw   = mass * 9.81 / 1000.0                         # kN/m self-weight
wEd  = w_uls + 1.35 * sw
MEd  = wEd * L**2 / 8                               # kN.m
VEd  = wEd * L / 2                                  # kN

# ---------------- Bending resistance (Cl. 6.2.5) ----------------
Mpl_Rd = W_eff * fy / gM0 / 1e6                     # N.mm -> kN.m  (the /1e6 that was missing)

# ---------------- Shear (Cl. 6.2.6) ----------------
Av     = max(A - 2*b*tf + (tw + 2*r)*tf, (h - 2*tf)*tw)
Vpl_Rd = Av * fy / (math.sqrt(3) * gM0) / 1e3       # kN

# ---------------- Lateral-torsional buckling (Cl. 6.3.2.2) ----------------
C1, C2, zg = 1.132, 0.459, 0.0                      # UDL, simply supported, load at shear centre
Lbmm = Lb * 1e3
Mcr  = (C1 * math.pi**2 * E * Iz / Lbmm**2
        * math.sqrt(Iw/Iz + Lbmm**2 * G * It / (math.pi**2 * E * Iz) + (C2*zg)**2)
        - C1 * C2 * zg * math.pi**2 * E * Iz / Lbmm**2) / 1e6
lam_LT = math.sqrt(Mpl_Rd / Mcr)
aLT    = 0.49 if h/b > 2 else 0.21                  # Table 6.5: h/b>2 -> curve c
phi    = 0.5 * (1 + aLT*(lam_LT - 0.4) + 0.75*lam_LT**2)
chi_LT = min(1.0, 1.0 / (phi + math.sqrt(max(phi**2 - 0.75*lam_LT**2, 0.0))))
Mb_Rd  = chi_LT * Mpl_Rd

# ---------------- M-V interaction (Cl. 6.2.8) ----------------
M_Rd = Mpl_Rd if VEd <= 0.5*Vpl_Rd else Mpl_Rd      # no reduction below 0.5*Vpl,Rd

# ---------------- Deflection (Cl. 7.2) ----------------
delta = 5 * (w_ser + sw) * (L*1e3)**4 / (384 * E * Iy)
lim   = L*1e3 / 360

# ---------------- Report ----------------
print(f"Section class          : {cls}   (c/tf={cf/tf:.2f} vs 9eps={9*eps:.2f}; "
      f"c/tw={cw/tw:.2f} vs 72eps={72*eps:.2f})")
print(f"M_Ed   = {MEd:8.2f} kN.m   (w_Ed = {wEd:.2f} kN/m incl. self-weight)")
print(f"M_pl,Rd= {Mpl_Rd:8.2f} kN.m   -> util = {MEd/Mpl_Rd:.3f}")
print(f"V_Ed   = {VEd:8.2f} kN     V_pl,Rd = {Vpl_Rd:.1f} kN -> util = {VEd/Vpl_Rd:.3f}")
print(f"M_cr   = {Mcr:8.2f} kN.m   lambda_LT = {lam_LT:.3f}  chi_LT = {chi_LT:.3f}")
print(f"M_b,Rd = {Mb_Rd:8.2f} kN.m   -> util = {MEd/Mb_Rd:.2f}")
print(f"delta  = {delta:8.1f} mm    = L/{L*1e3/delta:.0f}   (limit L/360 = {lim:.1f} mm)")

ok_bend = MEd <= M_Rd
ok_ltb  = restrained or MEd <= Mb_Rd
ok_defl = delta <= lim
print("\nSTATUS:", "PASS" if (ok_bend and ok_ltb and ok_defl) else "FAIL")
print(f"  bending    : {'PASS' if ok_bend else 'FAIL'}")
print(f"  LTB        : {'PASS' if ok_ltb  else 'FAIL'}"
      + ("  (fully restrained)" if restrained else f"  (Lb = {Lb} m unrestrained)"))
print(f"  deflection : {'PASS' if ok_defl else 'FAIL'}")
```

**Output for the case as given (unrestrained, 6.2 m):**

```
Section class          : 1   (c/tf=4.04 vs 9eps=8.32; c/tw=35.75 vs 72eps=66.56)
M_Ed   =    90.69 kN.m   (w_Ed = 18.88 kN/m incl. self-weight)
M_pl,Rd=    97.19 kN.m   -> util = 0.933
V_Ed   =    58.51 kN     V_pl,Rd = 282.8 kN -> util = 0.207
M_cr   =    33.83 kN.m   lambda_LT = 1.695  chi_LT = 0.323
M_b,Rd =    31.43 kN.m   -> util = 2.89
delta  =    43.0 mm    = L/144   (limit L/360 = 17.2 mm)

STATUS: FAIL
  bending    : PASS
  LTB        : FAIL  (Lb = 6.2 m unrestrained)
  deflection : FAIL
```

---

## 7. Key lessons for the colleague

1. **Always convert N·mm → kN·m (÷10⁶).** Better still, work in a single consistent unit system (N and mm) throughout and convert only at the point of output.
2. **Name the axis explicitly and check it against the load direction.** Gravity load on a beam → major axis → `W_pl,y`. A `W_pl,z` in a beam bending check is an immediate red flag.
3. **Never trust a utilisation of 0.0000.** A near-zero or absurdly large utilisation is almost always a unit error, not a genuine result. Sanity-check the order of magnitude: a 254-deep UB in S275 has `M_pl,Rd` of roughly 100 kN·m — if your answer is 13 or 13 million, something is wrong.
4. **Bending capacity is not beam capacity.** For an unrestrained slender UB, LTB typically governs and can reduce capacity by 70% or more. Deflection frequently governs before that.
5. **State the load basis.** "Characteristic" and "factored" differ by 35–50% and flip this design from PASS to FAIL.
