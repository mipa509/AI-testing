# Raw Output

- task_id: `v2-deep-01`
- model_id_used: `glm-5.1-cloud`
- run_date: `2026-04-09`
- thinking_mode_used: `yes`

## Prompt Used

Same as in the prompt file

## Context Files Shared

All files from context folder

## Raw Model Output
----------------------------------------------------------------------------------------------
# Code Review: Root-Cause Analysis

## 1. Primary Defect — `1e2` instead of `1e3` in cm³→mm³ conversion

**File:** `section_library.py`, line in `get_section_properties`:

```python
"Wpl_y_mm3": section["Wpl_y_cm3"] * 1e2,   # ← BUG
```

1 cm = 10 mm → **1 cm³ = (10 mm)³ = 1 000 mm³**, so the factor must be `1e3`.

### Tracing the impact through the pipeline

| Step | With bug (`1e2`) | Correct (`1e3`) |
|---|---|---|
| `Wpl_y_mm3` (254×146×31 UB) | 366 × 100 = **36 600 mm³** | 366 × 1000 = **366 000 mm³** |
| `m_rd_kNm = W × f_y / 1e6` | 36 600 × 275 / 1e6 = **10.07 kNm** | 366 000 × 275 / 1e6 = **100.65 kNm** |
| `UR` for M_Ed = 80 kNm | 80 / 10.07 = **7.95** | 80 / 100.65 = **0.795** |

The bending resistance is **10× too low**, so every major-axis utilisation ratio is **10× too high**. This is the
root cause.

> The `1e6` divisor (N·mm → kN·m) in `analysis_pipeline.py` is correct: `mm³ × N/mm² = N·mm`, and `1 kN·m = 10⁶
N·mm`.

---

## 2. Secondary Risks (ordered by severity)

### 2a. 🔴 Axis-naming inconsistency: `Mz_kNm` vs `Wpl_y`

`analysis_pipeline.py` reads **`Mz_kNm`** as the applied moment but divides by `Wpl_y` resistance. In Eurocode
convention **y–y is the major axis** and **z–z is the minor axis**. In BS 5950 / some UK analysis software, z–z
*is* the major axis. The two naming conventions are opposites:

| Convention | Major axis | Minor axis |
|---|---|---|
| Eurocode / EN 1993 | y–y | z–z |
| BS 5950 / some UK software | z–z | y–y |

If the upstream analysis uses Eurocode labelling, **`Mz_kNm` is the minor-axis moment** and the code is checking
the wrong moment against the wrong resistance. This would typically *under-report* the major-axis UR and
*over-report* the minor-axis UR — a safety-critical error.

**Fix:** Add a comment documenting which convention is assumed, and rename the column at ingestion if necessary.

### 2b. 🟡 Missing partial factor γ_M0

```python
m_rd_kNm = props["Wpl_y_mm3"] * props["fy_MPa"] / 1e6
#                                              ^ no γ_M0
```

Per EN 1993-1-1 §6.2.5: `M_Rd = W_pl × f_y / γ_M0`. The UK NA sets `γ_M0 = 1.0`, so the result is numerically
correct *for the UK*, but the factor is invisible. If this code is ever used with a different National Annex
(e.g., Germany `γ_M0 = 1.0`, but some jurisdictions use `1.1` for existing structures), the result will be
silently non-conservative.

**Fix:** Make `gamma_M0` an explicit keyword argument defaulting to `1.0`.

### 2c. 🟡 No cross-section classification check

Using `W_pl` is only valid for **Class 1 or 2** sections. Class 3 sections require `W_el`; Class 4 require
`W_eff`. The current code applies a plastic check unconditionally. For compact UK UB sections this is usually
fine, but it will be **non-conservative** for any Class 3+ section added to the library in future.

### 2d. 🟢 `get_section_properties` will `KeyError` on unknown sections

No graceful handling if `row["Section"]` contains a name not in the dictionary — the whole `apply` bombs out with
an unhelpful error.

---

## 3. Smallest Safe Multi-File Fix

### `section_library.py` — fix the conversion, add a validation guard

```python
SECTIONS = {
    "254x146x31 UB": {"Wpl_y_cm3": 366.0, "fy_MPa": 275.0},
    "305x165x40 UB": {"Wpl_y_cm3": 649.0, "fy_MPa": 275.0},
}


def get_section_properties(name: str) -> dict:
    if name not in SECTIONS:
        raise KeyError(f"Section '{name}' not in library. "
                       f"Available: {list(SECTIONS.keys())}")
    section = SECTIONS[name]
    return {
        "fy_MPa": section["fy_MPa"],
        "Wpl_y_mm3": section["Wpl_y_cm3"] * 1e3,   # 1 cm³ = 1 000 mm³
    }
```

### `analysis_pipeline.py` — make γ_M0 explicit, document axis convention

```python
def major_axis_utilisation(row: pd.Series, gamma_M0: float = 1.0) -> float:
    props = get_section_properties(row["Section"])
    # EN 1993-1-1 §6.2.5: M_Rd = W_pl,y * f_y / γ_M0
    # Axis convention: y-y = major axis (EN 1993). Column "Mz_kNm" is
    # assumed to be the major-axis moment per BS 5950 convention (z = major).
    # If the upstream analysis uses EN 1993 labelling, rename at ingestion.
    m_rd_kNm = props["Wpl_y_mm3"] * props["fy_MPa"] / (1e6 * gamma_M0)
    return row["Mz_kNm"] / m_rd_kNm
```

> **Total lines changed:** 1 critical fix (`1e2`→`1e3`), ~6 lines of safety/docs. No API changes, no restructure.

---

## 4. Tests to Add Before Merging

### 4.1 — Golden-value regression test (catches the primary defect)

```python
def test_major_axis_utilisation_254x146x31():
    """Hand calc: Wpl,y=366 cm³, fy=275 MPa, γ_M0=1.0
    → M_Rd = 366e3 mm³ × 275 MPa / 1e6 = 100.65 kNm
    For M_Ed = 80 kNm → UR = 0.7950"""
    row = pd.Series({"Section": "254x146x31 UB", "Mz_kNm": 80.0})
    ur = major_axis_utilisation(row)
    assert ur == pytest.approx(0.7950, rel=1e-3)
```

### 4.2 — Unit-conversion symmetry test (catches any future cm/mm regression)

```python
def test_section_properties_unit_round_trip():
    props = get_section_properties("254x146x31 UB")
    # Wpl_y_cm3 from table = 366.0; Wpl_y_mm3 should be exactly 366 000
    assert props["Wpl_y_mm3"] == 366.0 * 1000
    # Sanity: M_Rd for this section should be O(100) kNm, not O(10)
    m_rd = props["Wpl_y_mm3"] * props["fy_MPa"] / 1e6
    assert 50 < m_rd < 200, f"M_Rd = {m_rd:.1f} kNm — possible unit error"
```

### 4.3 — All sections yield sensible resistances (catches typos in the table)

```python
@pytest.mark.parametrize("name", SECTIONS.keys())
def test_resistance_in_plausible_range(name):
    props = get_section_properties(name)
    m_rd = props["Wpl_y_mm3"] * props["fy_MPa"] / 1e6
    # No UK UB section should have M_Rd < 20 kNm or > 2000 kNm
    assert 20 < m_rd < 2000, f"{name}: M_Rd = {m_rd:.1f} kNm"
```

### 4.4 — Unknown section raises clear error

```python
def test_unknown_section_raises():
    with pytest.raises(KeyError, match="not in library"):
        get_section_properties("999x999x99 UB")
```

---

## Summary

| # | Finding | Severity | Fix location |
|---|---------|----------|-------------|
| **1** | `1e2` → should be `1e3` for cm³→mm³. M_Rd is **10× too low**, UR **10× too high** | 🔴 Critical |
`section_library.py` |
| **2** | `Mz_kNm` / `Wpl_y` mixes two axis conventions with no documentation | 🔴 High | `analysis_pipeline.py`
(comment + rename guard) |
| **3** | γ_M0 absent from formula | 🟡 Medium | `analysis_pipeline.py` (keyword arg, default 1.0) |
| **4** | No cross-section class check before using W_pl | 🟡 Medium | Future: add class check |
| **5** | Unknown section key gives raw `KeyError` | 🟢 Low | `section_library.py` (guard) |

-----------------------------------------------------------------------------------------------------
