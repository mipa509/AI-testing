# Structural Engineering Coding Model Benchmark Pack

Use this file to compare **Qwen3.5 27B** vs **Qwen3-Coder-Next** on realistic structural-engineering coding tasks.

## How to use this pack

1. Use a **fresh session** for each model on each task.
2. Paste the **same task prompt** into both models.
3. Do **not** correct or guide either model on the first pass.
4. Paste each raw output into the matching section below.
5. After both outputs are pasted, either:
   - send the filled file back to me for evaluation, or
   - use the evaluation prompt included after each task.

## Suggested scoring

Score each solution from **1 to 5** on:
- Correctness
- Robustness to messy real-world engineering data
- Code quality and readability
- Maintainability / modularity
- Engineering suitability and judgement
- Clarity of presented information (i.e. markdown or explanations, references etc)

---

# Evaluator system prompt

Use this in a dedicated evaluation window if you want consistent judging:

```text
You are acting as a strict coding evaluator for structural engineering automation tasks.

Your role is to compare candidate model outputs for Python coding tasks fairly and critically.

Rules:
1. Do not rewrite the solutions unless asked.
2. Evaluate the outputs based on correctness, robustness, code quality, engineering suitability, maintainability, and likely real-world usefulness.
3. Be skeptical of hidden assumptions, incorrect units, fragile pandas logic, inefficient loops, missing validation, and invented engineering logic.
4. Prefer solutions that are production-oriented, readable, modular, and safe for messy real engineering data.
5. For structural engineering tasks, pay close attention to:
   - units and conversions
   - preservation of engineering meaning
   - handling of missing or bad data
   - edge cases
   - whether the logic would be trustworthy in practice
6. When comparing two outputs, score each from 1 to 5 for:
   - correctness
   - robustness
   - readability
   - maintainability
   - engineering judgement
7. Then give:
   - winner by category
   - overall winner
   - short explanation of why
   - key weaknesses in each output
8. Be concise but specific. Prefer direct technical critique over generic praise.
9. If both are flawed, say so clearly.
10. Do not assume code is correct just because it looks polished.
11. Do not reward unnecessary complexity. Prefer the simplest solution that is correct, robust, and maintainable.
```

---

# Task 1 — SCIA / analysis results cleanup and envelope extraction

## Task prompt

```text
I am a structural engineer working with analysis results exported from software into CSV files.
Write Python code using pandas to process a results table with columns like:

Member
Case
Combination
Position_m
N_kN
Vy_kN
Vz_kN
Mx_kNm
My_kNm
Mz_kNm

Requirements:
1. Load the CSV.
2. Clean column names.
3. Convert numeric columns safely, coercing bad data to NaN.
4. Create a new column called ResultCase which uses Combination if present, otherwise Case.
5. For each Member, find:
   - max and min Mz_kNm
   - max absolute Vy_kN
   - max absolute N_kN
6. Also return the row where each governing value occurs.
7. Output two DataFrames:
   - a summary table by Member
   - a governing rows table
8. Make the code robust and readable, with comments and clear function structure.

Assume there may be blank strings, duplicated rows, and mixed numeric/string values.
```

## Output — Qwen3.5 27B

```python
[PASTE OUTPUT HERE]
```

## Output — Qwen3-Coder-Next

```python
[PASTE OUTPUT HERE]
```

## Evaluation prompt

```text
Compare the following two model outputs for the same structural engineering Python task.

TASK:
[PASTE TASK PROMPT HERE]

OUTPUT A:
[PASTE QWEN 3.5 OUTPUT HERE]

OUTPUT B:
[PASTE QWEN3-CODER-NEXT OUTPUT HERE]

Evaluate both outputs against these criteria:
1. Correctness
2. Robustness to messy real-world engineering data
3. Code quality and readability
4. Maintainability / modularity
5. Engineering suitability and judgement

Return in this format:

Task summary:
[one short sentence]

Scores:
Criterion | Output A | Output B | Winner
Correctness | x/5 | x/5 | A/B/Tie
Robustness | x/5 | x/5 | A/B/Tie
Readability | x/5 | x/5 | A/B/Tie
Maintainability | x/5 | x/5 | A/B/Tie
Engineering suitability | x/5 | x/5 | A/B/Tie

Top weaknesses of Output A:
1.
2.
3.

Top weaknesses of Output B:
1.
2.
3.

Overall winner:
[Output A / Output B / Tie]

Practical significance:
[State whether the difference is minor, moderate, or large for real engineering coding work]
```

---

# Task 2 — Eurocode-style slab check function with formula logic

## Task prompt

```text
Write a Python function for a reinforced concrete slab bending check.

Inputs:
- b = width in mm
- d = effective depth in mm
- fck in MPa
- fyk in MPa
- Med in kNm
- As_provided in mm2

Requirements:
1. Convert units consistently.
2. Calculate K = MEd / (b * d^2 * fck), using consistent units.
3. Check whether K is within a reasonable singly reinforced range.
4. Calculate lever arm z using a standard simplified EC2-style expression, but cap z at 0.95d.
5. Calculate required tensile steel As_req.
6. Calculate utilisation = As_req / As_provided.
7. Return a dictionary with intermediate values and a clear pass/fail result.
8. Add basic validation for zero or negative inputs.
9. Structure the code so it is easy to expand later.

Do not overcomplicate it, but write it like production-quality engineering utility code.
```

## Output — Qwen3.5 27B

```python
[PASTE OUTPUT HERE]
```

## Output — Qwen3-Coder-Next

```python
[PASTE OUTPUT HERE]
```

## Evaluation prompt

```text
Compare the following two model outputs for the same structural engineering Python task.

TASK:
[PASTE TASK PROMPT HERE]

OUTPUT A:
[PASTE QWEN 3.5 OUTPUT HERE]

OUTPUT B:
[PASTE QWEN3-CODER-NEXT OUTPUT HERE]

Evaluate both outputs against these criteria:
1. Correctness
2. Robustness to messy real-world engineering data
3. Code quality and readability
4. Maintainability / modularity
5. Engineering suitability and judgement

Return in this format:

Task summary:
[one short sentence]

Scores:
Criterion | Output A | Output B | Winner
Correctness | x/5 | x/5 | A/B/Tie
Robustness | x/5 | x/5 | A/B/Tie
Readability | x/5 | x/5 | A/B/Tie
Maintainability | x/5 | x/5 | A/B/Tie
Engineering suitability | x/5 | x/5 | A/B/Tie

Top weaknesses of Output A:
1.
2.
3.

Top weaknesses of Output B:
1.
2.
3.

Overall winner:
[Output A / Output B / Tie]

Practical significance:
[State whether the difference is minor, moderate, or large for real engineering coding work]
```

---

# Task 3 — Pile/column geometry assignment

## Task prompt

```text
Write Python code using pandas and numpy to assign each column load to the nearest pile cap centre.

Input tables:
1. columns_df with:
   ColumnID, X_m, Y_m, Load_kN

2. pilecaps_df with:
   CapID, X_m, Y_m

Requirements:
1. Compute planar distance from each column to each pile cap.
2. Assign each column to the nearest pile cap.
3. Add AssignedCapID and DistanceToCap_m to the columns table.
4. Flag any column where the nearest cap is more than 1.5 m away.
5. Return:
   - updated columns_df
   - a summary table with total assigned load per pile cap
6. Use a method that is clear and scalable for a moderate dataset.
7. Include comments and make the code easy to adapt later.

Assume coordinates are in metres and some IDs may contain whitespace.
```

## Output — Qwen3.5 27B

```python
[PASTE OUTPUT HERE]
```

## Output — Qwen3-Coder-Next

```python
[PASTE OUTPUT HERE]
```

## Evaluation prompt

```text
Compare the following two model outputs for the same structural engineering Python task.

TASK:
[PASTE TASK PROMPT HERE]

OUTPUT A:
[PASTE QWEN 3.5 OUTPUT HERE]

OUTPUT B:
[PASTE QWEN3-CODER-NEXT OUTPUT HERE]

Evaluate both outputs against these criteria:
1. Correctness
2. Robustness to messy real-world engineering data
3. Code quality and readability
4. Maintainability / modularity
5. Engineering suitability and judgement

Return in this format:

Task summary:
[one short sentence]

Scores:
Criterion | Output A | Output B | Winner
Correctness | x/5 | x/5 | A/B/Tie
Robustness | x/5 | x/5 | A/B/Tie
Readability | x/5 | x/5 | A/B/Tie
Maintainability | x/5 | x/5 | A/B/Tie
Engineering suitability | x/5 | x/5 | A/B/Tie

Top weaknesses of Output A:
1.
2.
3.

Top weaknesses of Output B:
1.
2.
3.

Overall winner:
[Output A / Output B / Tie]

Practical significance:
[State whether the difference is minor, moderate, or large for real engineering coding work]
```

---

# Task 4 — Engineering rules engine with many if statements

## Task prompt

```text
Write Python code to classify structural members from a pandas DataFrame.

Input columns:
MemberID
MemberType
Material
Span_m
Util_Bending
Util_Shear
Util_Deflection
EnvironmentClass

Requirements:
1. Create a column GoverningUtil which is the max of the three utilisation columns.
2. Create a column Status using these rules:
   - CRITICAL if GoverningUtil > 1.0
   - REVIEW if GoverningUtil between 0.9 and 1.0 inclusive
   - OK otherwise
3. Create a column Priority using:
   - HIGH if Status = CRITICAL
   - HIGH if MemberType is Beam and Span_m > 10 and GoverningUtil > 0.85
   - MEDIUM if Status = REVIEW
   - LOW otherwise
4. Create a column Notes using logic such as:
   - if Material is Steel and Util_Deflection governs, note "Check serviceability stiffness"
   - if Material is Concrete and Util_Shear governs, note "Review shear reinforcement / depth"
   - if EnvironmentClass is XD or XS, append "Durability review required"
5. Write this cleanly and avoid fragile chained indexing.
6. Return the updated DataFrame.

Make the solution readable, maintainable, and suitable for later expansion into more rules.
```

## Output — Qwen3.5 27B

```python
[PASTE OUTPUT HERE]
```

## Output — Qwen3-Coder-Next

```python
[PASTE OUTPUT HERE]
```

## Evaluation prompt

```text
Compare the following two model outputs for the same structural engineering Python task.

TASK:
[PASTE TASK PROMPT HERE]

OUTPUT A:
[PASTE QWEN 3.5 OUTPUT HERE]

OUTPUT B:
[PASTE QWEN3-CODER-NEXT OUTPUT HERE]

Evaluate both outputs against these criteria:
1. Correctness
2. Robustness to messy real-world engineering data
3. Code quality and readability
4. Maintainability / modularity
5. Engineering suitability and judgement

Return in this format:

Task summary:
[one short sentence]

Scores:
Criterion | Output A | Output B | Winner
Correctness | x/5 | x/5 | A/B/Tie
Robustness | x/5 | x/5 | A/B/Tie
Readability | x/5 | x/5 | A/B/Tie
Maintainability | x/5 | x/5 | A/B/Tie
Engineering suitability | x/5 | x/5 | A/B/Tie

Top weaknesses of Output A:
1.
2.
3.

Top weaknesses of Output B:
1.
2.
3.

Overall winner:
[Output A / Output B / Tie]

Practical significance:
[State whether the difference is minor, moderate, or large for real engineering coding work]
```

---

# Task 5 — Large dataset summary and plotting for engineering review

## Task prompt

```text
Write Python code to analyse a large structural results DataFrame and produce a concise engineering review output.

Input columns:
Project
Member
Storey
LoadCase
Mz_kNm
Vy_kN
Deflection_mm
Length_m
Material

Requirements:
1. Group by Storey and Material.
2. Calculate:
   - count of members
   - max absolute Mz_kNm
   - max absolute Vy_kN
   - max Deflection_mm
   - mean Deflection_mm
3. Create a utilisation-style metric called DeflectionRatio = Deflection_mm / (Length_m * 1000 / 250)
   and find the max DeflectionRatio per Storey.
4. Produce a summary DataFrame.
5. Plot:
   - bar chart of max absolute Mz by Storey
   - bar chart of max DeflectionRatio by Storey
6. Keep the code clean and structured, with reusable functions.

Assume the dataset may be large, so avoid unnecessary copies and inefficient loops.
```

## Output — Qwen3.5 27B

```python
[PASTE OUTPUT HERE]
```

## Output — Qwen3-Coder-Next

```python
[PASTE OUTPUT HERE]
```

## Evaluation prompt

```text
Compare the following two model outputs for the same structural engineering Python task.

TASK:
[PASTE TASK PROMPT HERE]

OUTPUT A:
[PASTE QWEN 3.5 OUTPUT HERE]

OUTPUT B:
[PASTE QWEN3-CODER-NEXT OUTPUT HERE]

Evaluate both outputs against these criteria:
1. Correctness
2. Robustness to messy real-world engineering data
3. Code quality and readability
4. Maintainability / modularity
5. Engineering suitability and judgement

Return in this format:

Task summary:
[one short sentence]

Scores:
Criterion | Output A | Output B | Winner
Correctness | x/5 | x/5 | A/B/Tie
Robustness | x/5 | x/5 | A/B/Tie
Readability | x/5 | x/5 | A/B/Tie
Maintainability | x/5 | x/5 | A/B/Tie
Engineering suitability | x/5 | x/5 | A/B/Tie

Top weaknesses of Output A:
1.
2.
3.

Top weaknesses of Output B:
1.
2.
3.

Overall winner:
[Output A / Output B / Tie]

Practical significance:
[State whether the difference is minor, moderate, or large for real engineering coding work]
```

---

# Results summary table template

Copy this section and fill it in once you complete the benchmark.

| Task | Winner | Difference size | Notes |
|---|---|---|---|
| Task 1 — Results cleanup |  |  |  |
| Task 2 — Slab check |  |  |  |
| Task 3 — Geometry assignment |  |  |  |
| Task 4 — Rules engine |  |  |  |
| Task 5 — Summary and plotting |  |  |  |

---

# Final questions to answer after testing

1. Did Qwen3-Coder-Next feel materially better than Qwen3.5 27B on your actual work?
2. Was the difference only in polish, or in correctness and usefulness?
3. Would the gap justify buying hardware around larger local models?
4. Is Qwen3.5 27B already good enough for most daily engineering coding tasks?

