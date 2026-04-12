# Raw Output

- task_id: `v3-notebook-01`
- model_id_used: `gemma4:31b-cloud`
- run_date: `2026-04-11`
- thinking_mode_used: `yes`

## Prompt Used

[Paste the exact prompt text from `tasks/notebook_01_pad_footing_sizing/prompt.md`.]

## Raw Model Output

# Preliminary Sizing of Square Pad Footing

## 1. Assumptions, Exclusions, and Sign Conventions

### Engineering Assumptions
- **Rigid Footing:** The footing is assumed to be infinitely rigid relative to the soil. This allows the use of a linear pressure distribution model, which is appropriate for preliminary sizing to determine if the footing dimensions are in the correct order of magnitude.
- **Linear Distribution:** Soil pressure varies linearly from the most compressed corner to the least compressed corner.
- **Serviceability:** Analysis is performed using service loads (unfactored).

### Exclusions
The following checks are omitted from this preliminary draft:
- Footing self-weight (net bearing pressure is checked).
- Sliding and overturning stability.
- Immediate and long-term settlement.
- Punching shear and one-way shear.
- Reinforcement design (steel area and detailing).

### Sign Conventions and Coordinates
- **Axial Load ($N$):** Positive acting downwards.
- **Moments ($M_x, M_y$):** Positive moments acting about the $x$ and $y$ axes, respectively.
- **Eccentricity:** $e_x = M_y/N$ and $e_y = M_x/N$.
- **Pressure ($q$):** Positive value indicates compression (bearing) on the soil.

---

```python
# Input Data
# Column dimensions (for reporting only)
COL_WIDTH = 0.40  # m
COL_DEPTH = 0.40  # m

# Allowable net bearing pressure (kPa)
ALLOWABLE_Q = 220.0

# Service Load Cases: (N [kN], Mx [kNm], My [kNm])
LOAD_CASES = {
    "LC1": {"N": 1100.0, "Mx": 90.0, "My": 60.0},
    "LC2": {"N": 700.0, "Mx": 200.0, "My": 140.0},
    "LC3": {"N": 1250.0, "Mx": 70.0, "My": 110.0},
}

# Candidate footing widths (B) in meters
CANDIDATE_WIDTHS = [round(2.4 + 0.1 * i, 1) for i in range(9)] # 2.4m to 3.2m
```

## 2. Analysis Model and Equations

The soil pressure at any point $(x, y)$ on a square footing is given by the superposition of the axial stress and the bending stresses:

$$q = \frac{N}{A} \pm \frac{M_x}{Z_x} \pm \frac{M_y}{Z_y}$$

Where:
- $A = B^2$ (Area of square footing)
- $Z = \frac{B^3}{6}$ (Elastic section modulus for a square)

For a square footing, the maximum pressure ($q_{max}$) occurs at the corner where both moments induce compression:
$$q_{max} = \frac{N}{B^2} + \frac{6(M_x + M_y)}{B^3}$$

The minimum pressure ($q_{min}$) occurs at the opposite corner:
$$q_{min} = \frac{N}{B^2} - \frac{6(M_x + M_y)}{B^3}$$

---

```python
def calculate_bearing_pressures(B, N, Mx, My):
    """
    Calculates max and min bearing pressures for a square footing.
    Returns: (q_max, q_min)
    """
    area = B**2
    section_modulus = (B**3) / 6.0
    
    # Superposition of axial and biaxial bending
    q_max = (N / area) + (Mx / section_modulus) + (My / section_modulus)
    q_min = (N / area) - (Mx / section_modulus) - (My / section_modulus)
    
    return q_max, q_min
```

## 3. Search over Candidate Footing Sizes

We will iterate through the candidate widths starting from $2.4\text{ m}$. The smallest width $B$ that satisfies both the maximum bearing capacity and the no-uplift condition ($q_{min} \ge 0$) for all load cases will be selected.

---

```python
selected_B = None

for B in CANDIDATE_WIDTHS:
    all_cases_pass = True
    
    for lc_name, loads in LOAD_CASES.items():
        q_max, q_min = calculate_bearing_pressures(B, loads["N"], loads["Mx"], loads["My"])
        
        # Selection Rule: q_max <= 220 kPa AND q_min >= 0 kPa
        if q_max > ALLOWABLE_Q or q_min < 0:
            all_cases_pass = False
            break
            
    if all_cases_pass:
        selected_B = B
        break

print(f"Selected Footing Width: {selected_B} m")
```

## 4. Results Table for Selected Footing

The following table summarizes the bearing pressures for the selected footing size across all service load cases.

---

```python
print(f"{'Load Case':<12} | {'q_max (kPa)':<15} | {'q_min (kPa)':<15} | {'Status':<10}")
print("-" * 58)

governing_case = ""
max_q_found = 0

for lc_name, loads in LOAD_CASES.items():
    q_max, q_min = calculate_bearing_pressures(selected_B, loads["N"], loads["Mx"], loads["My"])
    
    status = "PASS" if (q_max <= ALLOWABLE_Q and q_min >= 0) else "FAIL"
    print(f"{lc_name:<12} | {q_max:<15.2f} | {q_min:<15.2f} | {status:<10}")
    
    if q_max > max_q_found:
        max_q_found = q_max
        governing_case = lc_name
```

## 5. Final Engineering Conclusion

Based on the preliminary sizing analysis, the results are as follows:

- **Selected Footing Size:** `selected_B` metres (Square)
- **Governing Load Case:** `governing_case`
- **Maximum Bearing Pressure:** `max_q_found` kPa (within allowable $220\text{ kPa}$)
- **Minimum Bearing Pressure:** All cases $\ge 0\text{ kPa}$ (no uplift)

**Note:** This sizing is preliminary. The final design must include checks for punching shear, one-way shear, and reinforcement calculations. The self-weight of the footing should be added to the axial load $N$ in the final iteration to further stabilize the footing against uplift, although it will increase the maximum bearing pressure.

---

```python
# Final summary output for the conclusion section
print(f"Final Selected Width: {selected_B} m")
print(f"Governing Case: {governing_case}")
```
