# Raw Output

- task_id: `v2-deep-01`
- model_id_used: `kimi-k2-thinking`
- run_date: `2026-04-09`
- thinking_mode_used: `yes`

## Prompt Used

Same as in the prompt file

## Context Files Shared

All files from context folder

## Raw Model Output
----------------------------------------------------------------------------------------------
**1. Most Likely Root-Cause Defect (Critical)**

In `analysis_pipeline.py`, the `calculate_utilisation()` function incorrectly uses **elastic section modulus (Zx,
Zy)** instead of **plastic section modulus (Sx, Sy)** for major and minor axis bending capacity calculations:

```python
# WRONG - underestimates capacity by ~10-30% for steel I-sections
bending_capacity_major = section.Zx * section.fy  # mm³ × MPa = N·mm
bending_capacity_minor = section.Zy * section.fy
```

**Why this causes high utilisation ratios:**
- For typical steel I-sections, **Sx ≈ 1.1–1.3 × Zx** (plastic modulus is significantly larger)
- Using Z underestimates true bending capacity, inflating utilisation ratios by the same factor
- The Section dataclass explicitly provides both values, but the refactor likely introduced this regression by
mistakenly using the more conservative elastic modulus
- This explains why utilisations look "materially too high" post-refactor

---

**2. Secondary Risks (Ordered by Severity)**

**High Severity:**
- **Fragile global state dependency**: `process_load_case()` directly accesses the `SECTION_LIBRARY` global
without validation. If `load_sections()` isn't called first, it raises an opaque `KeyError` or `NameError`.
- **Missing error handling**: No checks for missing `section_id` or zero capacity (division by zero). A typo in a
section name causes silent failure or crashes.

**Medium Severity:**
- **Overly simplistic interaction formula**: The linear sum `axial_util + bending_major_util + bending_minor_util`
doesn't match any modern design code (EC3, AISC use exponent-based interaction with reduction factors). This is
unconservative for dominant axial loads and overly conservative for pure bending.
- **No units validation**: Assumes consistent units (N, mm, MPa) but no assertions or documentation guarantees
this. A mismatched results file could silently produce wrong utilisations.

**Low Severity:**
- **Hard-coded reporting threshold**: `plot_utilisation()` flags utilisation > 0.9 as red without justification.
Should be configurable or based on code-specific limits.
- **Sign convention ignored**: Using `abs()` masks potential analysis sign errors that might indicate model
issues.

---

**3. Smallest Safe Multi-File Fix**

Change only the capacity calculations and add minimal guardrails:

**File: `analysis_pipeline.py`**
```python
def calculate_utilisation(result: AnalysisResult, section: Section) -> float:
    """Calculate the utilisation ratio for a member."""
    # Axial capacity (force)
    axial_capacity = section.A * section.fy  # N = mm² × MPa

    # BENDING CAPACITY FIX: Use plastic modulus (Sx, Sy) not elastic (Zx, Zy)
    # This corrects the post-refactor regression where Z was mistakenly used
    bending_capacity_major = section.Sx * section.fy  # N·mm = mm³ × MPa
    bending_capacity_minor = section.Sy * section.fy  # N·mm = mm³ × MPa

    # Interaction (unchanged for minimal fix)
    axial_util = abs(result.axial_force) / axial_capacity
    bending_major_util = abs(result.major_axis_bending) / bending_capacity_major
    bending_minor_util = abs(result.minor_axis_bending) / bending_capacity_minor

    return axial_util + bending_major_util + bending_minor_util

def process_load_case(load_case_data: dict) -> dict[str, float]:
    """Process a single load case and return utilisation ratios."""
    utilisations = {}

    for member_id, result_dict in load_case_data.items():
        result = AnalysisResult(**result_dict)

        # MINIMAL SAFETY: Explicit error for missing sections
        if result.section_id not in SECTION_LIBRARY:
            raise KeyError(
                f"Section '{result.section_id}' not found for member '{member_id}'. "
                f"Available sections: {list(SECTION_LIBRARY.keys())}"
            )

        section = SECTION_LIBRARY[result.section_id]
        util = calculate_utilisation(result, section)
        utilisations[member_id] = util

    return utilisations
```

**File: `section_library.py`** (add type-checked getter)
```python
def get_section(section_id: str) -> Section:
    """Type-safe section retrieval with clear error messages."""
    if not SECTION_LIBRARY:
        raise RuntimeError("Section library not loaded. Call load_sections() first.")
    try:
        return SECTION_LIBRARY[section_id]
    except KeyError:
        raise KeyError(
            f"Section '{section_id}' not found. Available: {list(SECTION_LIBRARY.keys())}"
        )
```

Then update `process_load_case` to use it:
```python
from .section_library import get_section

def process_load_case(load_case_data: dict) -> dict[str, float]:
    utilisations = {}
    for member_id, result_dict in load_case_data.items():
        result = AnalysisResult(**result_dict)
        section = get_section(result.section_id)  # Now with validation
        utilisations[member_id] = calculate_utilisation(result, section)
    return utilisations
```

---

**4. Tests to Add Before Merging**

**Priority 1 - Regression Test (Prevents this exact bug):**
```python
def test_calculate_utilisation_uses_plastic_modulus():
    """Verify Sx/Sy are used, not Zx/Zy."""
    # Create a mock section where Sx is 20% larger than Zx
    section = Section(
        name="TEST_UB",
        A=5000, fy=355,
        Zx=500e3, Zy=100e3,  # Elastic moduli
        Sx=600e3, Sy=120e3,  # Plastic moduli (20% higher)
        Ix=1e8, Iy=5e6
    )
    result = AnalysisResult(
        member_id="M1", section_id="TEST_UB",
        axial_force=0, major_axis_bending=177.5e6, minor_axis_bending=0
    )

    util = calculate_utilisation(result, section)
    # With Sx=600e3: capacity = 600e3 × 355 = 213e6 N·mm
    # Moment = 177.5e6 N·mm → util = 177.5/213 ≈ 0.833
    # If Zx=500e3 was used: util would be 177.5/177.5 = 1.0

    assert abs(util - 0.833) < 0.01, f"Expected ~0.833, got {util}"
```

**Priority 2 - Integration Test:**
```python
def test_end_to_end_with_real_section():
    """Test with actual steel section data."""
    load_sections("tests/fixtures/sections.json")
    load_cases = load_analysis_results("tests/fixtures/results.json")

    # Use a UB 305x165x46 (Sx=720e3 mm³, fy=355 MPa)
    # Apply moment of 200 kN·m = 200e6 N·mm
    # Expected util = 200e6 / (720e3 × 355) ≈ 0.78

    all_utils = process_all_load_cases(
        "tests/fixtures/results.json",
        "tests/fixtures/sections.json"
    )
    assert all_utils["Beam_1"][0] < 0.85  # Should pass with Sx, fail with Zx
```

**Priority 3 - Error Handling:**
```python
def test_missing_section_raises_clear_error():
    """Verify meaningful error for missing section."""
    load_sections("tests/fixtures/sections.json")

    invalid_data = {
        "M1": {
            "member_id": "M1",
            "section_id": "NONEXISTENT_SECTION",  # Not in library
            "axial_force": 0, "major_axis_bending": 0, "minor_axis_bending": 0
        }
    }

    with pytest.raises(KeyError, match="NONEXISTENT_SECTION not found"):
        process_load_case(invalid_data)
```

**Priority 4 - Edge Cases:**
```python
def test_zero_capacity_raises_zero_division_error():
    """Detect division by zero from bad data."""
    section = Section("TEST", A=0, fy=0, Zx=1, Zy=1, Sx=1, Sy=1, Ix=1, Iy=1)
    result = AnalysisResult("M1", "TEST", 0, 0, 0)

    with pytest.raises(ZeroDivisionError):
        calculate_utilisation(result, section)
```

**Priority 5 - Units Contract:**
```python
def test_units_consistency():
    """Document expected units through test."""
    # 1 kN·m moment on 355 MPa steel with Sx=1000e3 mm³
    # Expected util = 1e6 N·mm / (1000e3 × 355) ≈ 0.0028
    section = Section("UNITS_TEST", A=1, fy=355,
                     Zx=1, Zy=1, Sx=1000e3, Sy=1, Ix=1, Iy=1)
    result = AnalysisResult("M1", "UNITS_TEST", 0, 1e6, 0)

    util = calculate_utilisation(result, section)
    assert abs(util - 0.0028) < 0.0001
```

-----------------------------------------------------------------------------------------------------
