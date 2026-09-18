# Raw Output

- task_id: `v2-deep-02`
- model_id_used: `tencent-hy4-preview`
- api_model: `tencent/hy4-preview` (OpenRouter)
- reasoning_effort: `high`
- run_route: `VS Code agent chat via OpenRouter, fresh chat per task, sandbox workspace on a separate drive holding the three task folders (prompts and context only; no evaluator or reference files)`
- run_date: `2026-09-18`
- thinking_mode_used: `yes (reasoning effort high)`

## Prompt Used

Same as in the prompt file (`tasks/deep_02_repo_review_traps/prompt.md`), read by the agent from the task folder together with the three `context/*.py` files, instead of receiving `context_combined.md` as a second message. The review was written to `code_review.md` in that folder as asked.

## Context Files Shared

- `context/load_factors.py`
- `context/beam_capacity.py`
- `context/reporting.py`

## Raw Model Output

# Code Review — `v2 deep 02` beam screening package

**Scope:** pre-release review of a small internal package for **major-axis steel beam ULS screening**.
**Files reviewed:** `context/load_factors.py`, `context/beam_capacity.py`, `context/reporting.py`.
**Mode:** review only — no code rewritten. Findings ordered by severity, each with *why it matters* and a *minimum fix direction*.

---

## Executive summary

The package is not releasable. There are **three blocking defects**, and they interact badly:

1. Variable load is never factored (`ULS_GAMMA_Q` is defined but unused).
2. The plastic moment resistance is **1000× too small** due to a cm³ → mm³ conversion error.
3. The reporting function returns **exactly one row — the least critical one** — and silently discards every governing case.

Defects 1 and 2 push the utilisation in *opposite* directions, so the net result is "everything FAILs by ~3 orders of magnitude." That is dangerous in review terms: the loud, obvious failure invites a one-character "fix" to the divisor, which would then **expose and hide** defect 1 behind plausible-looking numbers. Both must be fixed together, with a unit test pinning the arithmetic.

| # | Severity | Location | Finding |
|---|----------|----------|---------|
| F1 | **Critical** | `load_factors.py` | Variable action `Q` is not multiplied by `ULS_GAMMA_Q` |
| F2 | **Critical** | `beam_capacity.py` | `Wpl_y_cm3 × fy_MPa / 1e6` is 1000× too small (cm³→mm³ missing) |
| F3 | **Critical** | `reporting.py` | `build_review_table` returns `output[:1]` — one row, the *lowest* utilisation |
| F4 | **High** | `reporting.py` / `load_factors.py` | No governing-combination logic; no ψ₀, no γ_G,fav, no accidental case |
| F5 | **High** | `beam_capacity.py` | Plastic resistance applied unconditionally — no section classification, no γ_M0 |
| F6 | **Medium** | `reporting.py` | Rounding to 2 dp happens *before* the PASS/FAIL decision and before sorting |
| F7 | **Medium** | all three | No input validation or unit contracts; `KeyError` / `ZeroDivisionError` paths |
| F8 | **Low** | all three | Flat intra-package imports, no package marker, no tests |

---

## F1 — Critical: variable load is never factored

```python
ULS_GAMMA_G = 1.35
ULS_GAMMA_Q = 1.50

def factored_line_load(row: dict) -> float:
    return (row["G_kN_per_m"] * ULS_GAMMA_G) + row["Q_kN_per_m"]   # Q missing * ULS_GAMMA_Q
```

**Why it matters.** `ULS_GAMMA_Q` is declared and never used — a dead constant sitting next to a live one is the classic signature of an incomplete edit. Every ULS result is unconservative by a factor that depends on the G:Q ratio. For a Q-dominated row (e.g. G = 2, Q = 10 kN/m) the design load is understated by **~38%**; for G = Q = 10 kN/m it is understated by **~17.5%**. This is not a rounding issue — it is a systematic non-conservative bias in the primary output of the package, and it will not be caught by eyeballing results because the numbers look reasonable.

**Minimum fix direction.**

```python
return (row["G_kN_per_m"] * ULS_GAMMA_G) + (row["Q_kN_per_m"] * ULS_GAMMA_Q)
```

Then add a regression test asserting `factored_line_load({"G_kN_per_m": 10.0, "Q_kN_per_m": 10.0}) == 28.5`, and a lint/CI rule or unit test that fails if a module-level `ULS_GAMMA_*` constant is unreferenced.

---

## F2 — Critical: unit conversion error — resistance is 1000× too small

```python
def major_axis_resistance_kNm(section: dict) -> float:
    return section["Wpl_y_cm3"] * section["fy_MPa"] / 1e6
```

**Why it matters.** Trace the units:

- `Wpl_y_cm3` is cm³; **1 cm³ = 1000 mm³** — this conversion is missing.
- `fy_MPa` is N/mm² (= MPa).
- `mm³ × N/mm² = N·mm`, and **1 kN·m = 10⁶ N·mm**.

So the correct expression is `Wpl_cm3 × 1000 × fy / 1e6 = Wpl_cm3 × fy / 1000`. The code divides by `1e6` instead of `1e3`, making the resistance **1000× too small** and therefore the utilisation **1000× too large**.

Worked check, UB 305×165×40 (Wpl,y ≈ 625 cm³, fy = 355 MPa):

| | Value |
|---|---|
| Correct `M_pl,Rd` | 625 × 355 / 1000 = **221.9 kN·m** |
| As coded | 625 × 355 / 1e6 = **0.222 kN·m** |

Combined with F1 on a 6 m span (G = Q = 10 kN/m): true utilisation ≈ 0.58 (PASS); as coded ≈ 476 (FAIL). Every member in every run reports FAIL, which is why this has survived to release review — the failure is so extreme it reads as "the sections are wrong" rather than "the formula is wrong."

**Minimum fix direction.** Make the conversion explicit rather than folding it into a magic divisor, and name the partial factor:

```python
GAMMA_M0 = 1.0

def major_axis_resistance_kNm(section: dict) -> float:
    wpl_mm3 = section["Wpl_y_cm3"] * 1e3          # cm^3 -> mm^3
    mpl_nmm = wpl_mm3 * section["fy_MPa"]          # mm^3 * N/mm^2 -> N*mm
    return mpl_nmm / 1e6 / GAMMA_M0                # N*mm -> kN*m
```

Add a golden-value test (625 cm³ / 355 MPa → 221.9 kN·m ±0.1%). Better still, carry units explicitly (`pint`) or rename keys to `Wpl_y_mm3` so the conversion cannot be silently dropped again.

---

## F3 — Critical: the report returns one row, and it is the least critical one

```python
output.sort(key=lambda item: item["utilisation"])
return output[:1]
```

**Why it matters.** This is the most serious finding from a *reporting integrity* standpoint, because it fails silently and produces output that looks well-formed.

- The function is named `build_review_table` but returns a single-element list. Any caller that renders it as a table will show one member and no indication that others existed.
- The sort is **ascending**, so `[:1]` keeps the **lowest** utilisation — the *least* critical member. The governing case is thrown away. A reviewer reading the output sees a comfortable PASS and concludes the design is fine.
- There is no row count, no truncation flag, no warning. Silent data loss in an engineering report is worse than a crash: a crash gets investigated, a plausible-looking one-row table gets signed off.

**Minimum fix direction.** Return the full table; if a "worst case" view is wanted, make it a separate, explicitly named function and sort **descending**:

```python
def build_review_table(load_rows, section_lookup) -> list:
    ...                                  # no slicing
    output.sort(key=lambda item: item["utilisation"], reverse=True)
    return output

def governing_case(load_rows, section_lookup) -> dict:
    return max(build_review_table(load_rows, section_lookup),
               key=lambda item: item["utilisation"])
```

Also assert `len(output) == len(load_rows)` before returning, so any future filtering is loud.

---

## F4 — High: no governing-combination logic

**What the code does.** `row["combination"]` is read from the input and echoed straight into the output. Nothing validates it, nothing groups by it, and nothing takes an envelope. Each row is evaluated independently and then (per F3) all but one are discarded.

**Why it matters.** ULS screening is defined by the *governing* combination, not by any single one:

- **No envelope.** If `load_rows` contains several combinations for the same `member_id` (e.g. EN 1990 eq. 6.10a / 6.10b, or each variable action taken in turn as leading), the correct answer is `max(utilisation)` **per member**. The current code has no concept of a member-level maximum.
- **No ψ₀.** Only one variable action is supported. Accompanying variable actions must be reduced by ψ₀ (and leading ones may use ψ₀ under 6.10b). A single `Q_kN_per_m` field cannot express this.
- **No favourable permanent factor.** `ULS_GAMMA_G = 1.35` is applied unconditionally. Where G is favourable (e.g. counteracting uplift, or a permanent load that reduces the net moment), γ_G,fav = 1.0 applies. Always-unfavourable is conservative for simple gravity beams but wrong for any case with counteracting effects, and it will produce spurious failures there.
- **No accidental / seismic branch.** γ = 1.0 combinations are not representable.
- **Unvalidated label.** A typo such as `"ULS-6.10b"` vs `"6.10b"` propagates into the report unchecked, so the output can claim a combination that was never actually evaluated.

**Minimum fix direction.** Do not try to build a full combination engine for a screening tool. Instead: (a) group results by `member_id` and report `max(utilisation)` per member as the governing value, carrying the winning `combination` label with it; (b) validate `combination` against an explicit allow-list of supported cases and raise on anything unknown; (c) extend the row schema to `{"G_kN_per_m", "Q_leading_kN_per_m", "Q_accompanying_kN_per_m", "psi0", "gamma_G_favourable": bool}` — or, if the tool is deliberately single-variable, document that restriction in the docstring and enforce it with a schema check.

---

## F5 — High: plastic resistance applied unconditionally

```python
def major_axis_resistance_kNm(section: dict) -> float:
    return section["Wpl_y_cm3"] * section["fy_MPa"] / 1e6
```

**Why it matters.** `Wpl,y` is the **plastic** section modulus. It is only valid for **Class 1 or Class 2** sections. For a Class 3 (semi-compact) section the resistance must use the **elastic** modulus `Wel,y`, and for a Class 4 (slender) section an **effective** modulus accounting for local buckling. Feeding a Class 3/4 section through this function **overestimates capacity** — a non-conservative error in the opposite direction to F2, and one that is invisible because nothing in the code or the output records which modulus was used.

Secondary points in the same function:

- **γ_M0 is implicit.** EC3 uses γ_M0 = 1.0, so the number is currently right, but an unnamed assumption is an assumption that cannot be audited or changed for a different design code.
- **No lateral-torsional buckling, shear, or axial interaction.** See "Not escalated" below for why these are documented limitations rather than defects — but they must be documented.

**Minimum fix direction.** Require the classification to be supplied and branch on it:

```python
def major_axis_resistance_kNm(section: dict) -> float:
    cls = section["class"]                       # 1..4, required
    key = "Wpl_y_cm3" if cls in (1, 2) else "Wel_y_cm3"
    if cls == 4:
        key = "Weff_y_cm3"
    ...
```

Raise on a missing or unknown `class`. At minimum, if classification is out of scope, add a module-level docstring stating "Class 1/2 sections only" and validate that the section dict carries a `class` field of 1 or 2.

---

## F6 — Medium: rounding before the decision, and before the sort

```python
util = round(utilisation(row, section), 2)
...
"status": "PASS" if util < 1.0 else "FAIL",
```

**Why it matters.** Three distinct problems in two lines:

- **The PASS/FAIL decision is made on rounded data.** A true utilisation of 0.996 is reported and judged as 1.00 → FAIL. Here the rounding happens to be conservative, but that is luck, not design: the same pattern with `<=` or with a different rounding mode would be non-conservative. Decisions should be made on full precision; rounding is a *presentation* concern.
- **The sort key is the rounded value.** Two members at 0.994 and 0.996 both sort as 1.00, so their relative order is arbitrary — and with F3 fixed, "which member governs" becomes non-deterministic.
- **2 dp is too coarse for screening.** A screening tool exists to rank and triage; collapsing 0.004 and 0.00 into the same bucket destroys the ranking at the low end, which is exactly where "can we go down a section size?" decisions live.

The boundary itself (`util < 1.0` → PASS, so exactly 1.00 fails) is correct and conservative — keep it.

**Minimum fix direction.** Separate the value from its presentation:

```python
util = utilisation(row, section)                 # full precision
...
"utilisation": round(util, 3),
"status": "PASS" if util < 1.0 else "FAIL",
```

and sort on the unrounded value (keep it in the dict, e.g. `"_util_raw"`, or sort before rounding). Use 3 dp for display.

---

## F7 — Medium: no input validation or unit contracts

**Why it matters.** Every function indexes dicts directly with no contract:

- `section_lookup[row["section_name"]]` → bare `KeyError` with no member context. In a batch run over 200 members, the traceback does not tell you *which* member had the bad section name.
- `major_axis_resistance_kNm` → `ZeroDivisionError` (or a silent `inf`) if `Wpl_y_cm3` or `fy_MPa` is 0 or missing. A zero utilisation or an `inf` then propagates into the report and, with F3, can become the single returned row.
- `row["span_m"]` → no check for `span_m > 0`. A zero span yields `M = 0` and a spurious PASS; a negative span yields a positive moment because it is squared, so a sign error is silently absorbed.
- **Units are encoded only in key names** (`_kN_per_m`, `_m`, `_cm3`, `_MPa`). Nothing enforces them. A caller passing `Wpl_y` in mm³ — a very common convention in section tables — gets a result 1000× wrong with no error. This is the same class of defect as F2, and it will recur.
- **No self-weight.** Steel beam self-weight is a permanent action and is not added. If callers do not include it in `G_kN_per_m`, every result is unconservative. Undocumented either way.

**Minimum fix direction.** Add a thin validation layer at the entry point (`build_review_table`) rather than in every function: check required keys exist, `span_m > 0`, `Wpl_y_cm3 > 0`, `fy_MPa > 0`, and raise a `ValueError` that names the `member_id`. Document the unit contract in a module docstring. Consider a `dataclass` or `pydantic` model for `LoadRow` and `Section` so the contract is enforced by construction rather than by convention.

---

## F8 — Low: packaging and test scaffolding

- `from load_factors import ...` / `from beam_capacity import ...` are flat absolute imports with no `__init__.py`. This works only when the CWD happens to be `context/`. As soon as the package is installed or imported from elsewhere, it breaks.
- No tests at all. Given F1 and F2 are both single-token arithmetic errors that a two-line test would have caught, this is the root cause behind the root causes.

**Minimum fix direction.** Add `context/__init__.py`, switch to explicit relative imports (`from .load_factors import ...`), and add a `tests/` module with golden-value tests for each of the three functions plus one end-to-end case with a known hand-calculated utilisation.

---

## Interaction note — fix F1 and F2 together

The two critical arithmetic errors have opposite signs:

| Defect | Effect on utilisation |
|---|---|
| F1 (Q unfactored) | **understates** load → utilisation too low (up to ~38% for Q-dominated rows) |
| F2 (cm³→mm³ missing) | **overstates** utilisation by 1000× |

Net effect: every row fails by ~3 orders of magnitude. The risk is that a reviewer "fixes the obvious bug" by changing `1e6` to `1e3`, sees plausible numbers in the 0.4–0.9 range, and ships — with F1 still live and every result unconservative. **Land both fixes in one change with tests for each**, and add an end-to-end test with a hand-calculated expected utilisation so the two cannot cancel again.

---

## Issues deliberately not escalated

Recorded here so the decision is auditable, not because they are invisible.

| Issue | Why not escalated |
|---|---|
| **Lateral-torsional buckling not checked** | Real ULS limit state and often governing for unrestrained beams — but this is a *screening* tool, and adding LTB needs bracing length, moment gradient and imperfection factors that the current schema cannot express. Not a code defect. **Mitigation required before release:** document "fully restrained / LTB not checked" in the module docstring and in the report header, or add a required `restraint` input that raises when unbraced. |
| **Shear, axial force, and interaction** | Rarely governing for a gravity beam screen; out of scope by the stated intent. Note in limitations. |
| **Deflection / vibration (SLS)** | Explicitly out of scope — ULS screening only. |
| **`M = wL²/8` assumption** | Correct for a simply supported beam under UDL, which is the stated screening case. Not flagged as a defect, but the assumption is undocumented and unvalidated — add a `support_condition` field or a docstring line. Worth revisiting if cantilevers or point loads ever enter scope. |
| **Type hints, docstrings, naming, formatting** | Stylistic; explicitly deprioritised by the review brief. (The *absence* of docstrings stating the unit contract is F7, which is escalated.) |
| **Python's banker's rounding** | `round()` uses round-half-to-even. Irrelevant once F6 moves rounding to presentation only. |
| **`util < 1.0` boundary** | Exactly 1.00 → FAIL is the conservative direction. Correct as written. |
| **Mutable default / mutation of inputs** | None present; `output.sort()` only mutates the local list. |

---

## Recommended release gate

Blocking: **F1, F2, F3**. Required before release: **F4, F5**. Fast-follow: **F6, F7, F8**.

Minimum evidence to close the gate:

1. Golden-value unit test for `factored_line_load` (G = Q = 10 → 28.5 kN/m).
2. Golden-value unit test for `major_axis_resistance_kNm` (625 cm³, 355 MPa → 221.9 kN·m).
3. End-to-end test asserting the returned table has one row per input row, and that the governing case is the maximum utilisation, not the minimum.
4. A documented limitations block covering LTB, shear, SLS, and the Class 1/2 and simply-supported-UDL assumptions.
