# Structural Engineering AI Model Benchmark Report (Expanded, 3 Models, Tasks 1-6)

Models compared:
- Qwen3.5 27B
- Qwen3-Coder-Next
- gemma4:31b-cloud

Scope:
- Tasks 1-6 from `benchmarks/v1/structural_engineering_model_benchmark.md` and `benchmarks/v1/Evaluation 6.md`
- Raw first-pass outputs only (no post-hoc fixes in model code)

Review context:
- Tasks 1-5 baseline for Qwen3.5 27B and Qwen3-Coder-Next is retained from the prior dual-review averaged benchmark.
- gemma4:31b-cloud was added using the same rubric across tasks.
- Task 6 was scored in this rerun for all three models using the planted-error guidance.

Scoring criteria (1-5):
1. Correctness
2. Robustness to messy real-world engineering data
3. Code quality and readability
4. Maintainability / modularity
5. Engineering suitability and judgement
6. Clarity of presented information (explanations, assumptions, references, traceability)

Model key:
- A = Qwen3.5 27B
- B = Qwen3-Coder-Next
- C = gemma4:31b-cloud

---

## Task 1 - Results cleanup and envelope extraction

| Criterion | A | B | C | Winner |
|---|---:|---:|---:|---|
| Correctness | 4.0 | 3.0 | 3.0 | A |
| Robustness | 4.0 | 3.0 | 3.0 | A |
| Readability | 4.0 | 4.0 | 4.0 | Tie |
| Maintainability | 4.0 | 4.0 | 4.0 | Tie |
| Engineering suitability | 4.0 | 3.0 | 3.0 | A |
| Clarity | 4.0 | 4.5 | 5.0 | C |

Overall winner: **Qwen3.5 27B**  
Difference size: **Moderate**

Detailed comments:
- A: Strongest technical baseline on this task due to safer governing-index handling and pragmatic data cleanup flow.
- B: Well-presented but less safe for all-NaN governing-index edge cases and schema assumptions.
- C: Strong explanation quality and useful narrative, but less rigorous governing-row traceability than A.

---

## Task 2 - Eurocode-style slab check function

| Criterion | A | B | C | Winner |
|---|---:|---:|---:|---|
| Correctness | 4.0 | 2.0 | 3.0 | A |
| Robustness | 4.0 | 3.0 | 3.0 | A |
| Readability | 4.0 | 3.5 | 4.0 | Tie (A/C) |
| Maintainability | 4.0 | 3.5 | 4.0 | Tie (A/C) |
| Engineering suitability | 4.0 | 2.0 | 3.0 | A |
| Clarity | 4.0 | 4.5 | 5.0 | C |

Overall winner: **Qwen3.5 27B**  
Difference size: **Large**

Detailed comments:
- A: Best alignment to requested K-definition and practical engineering utility structure.
- B: Major technical miss by changing K basis and adding non-requested assumptions that reduce trust.
- C: Good balance and strong explanations, but treatment when beyond singly reinforced limit is less conservative/explicit than A.

---

## Task 3 - Pile/column geometry assignment

| Criterion | A | B | C | Winner |
|---|---:|---:|---:|---|
| Correctness | 2.0 | 2.0 | 4.0 | C |
| Robustness | 3.0 | 2.0 | 3.0 | Tie (A/C) |
| Readability | 4.0 | 4.0 | 4.0 | Tie |
| Maintainability | 4.0 | 3.5 | 4.0 | Tie (A/C) |
| Engineering suitability | 3.0 | 3.0 | 4.0 | C |
| Clarity | 4.0 | 5.0 | 5.0 | Tie (B/C) |

Overall winner: **gemma4:31b-cloud**  
Difference size: **Large**

Detailed comments:
- A: Good defensive cleaning and vectorized distance logic, but summary merge bug blocks reliability.
- B: Clear write-up, but summary-stage column/merge logic defect remains critical.
- C: Clean nearest-assignment flow without the blocking summary bug; practical and scalable with KDTree.
- Caveat for C: introduces scipy dependency and could use stronger numeric coercion/validation.

---

## Task 4 - Rules engine classification

| Criterion | A | B | C | Winner |
|---|---:|---:|---:|---|
| Correctness | 4.0 | 4.0 | 4.0 | Tie |
| Robustness | 3.0 | 3.0 | 3.0 | Tie |
| Readability | 4.0 | 5.0 | 4.0 | B |
| Maintainability | 4.0 | 5.0 | 4.0 | B |
| Engineering suitability | 4.0 | 4.0 | 4.0 | Tie |
| Clarity | 4.0 | 5.0 | 5.0 | Tie (B/C) |

Overall winner: **Qwen3-Coder-Next**  
Difference size: **Minor to Moderate**

Detailed comments:
- A: Correct and practical.
- B: Best modularity and readability for future expansion.
- C: Solid implementation with good explanation, but not stronger than B on maintainability pattern.
- Shared weakness: XD/XS subclass handling remains simplistic in all models.

---

## Task 5 - Large dataset summary and plotting

| Criterion | A | B | C | Winner |
|---|---:|---:|---:|---|
| Correctness | 4.0 | 1.0 | 4.0 | Tie (A/C) |
| Robustness | 3.0 | 2.0 | 3.0 | Tie (A/C) |
| Readability | 4.0 | 5.0 | 4.0 | B |
| Maintainability | 3.5 | 4.0 | 3.0 | B |
| Engineering suitability | 4.0 | 2.0 | 4.0 | Tie (A/C) |
| Clarity | 4.0 | 4.5 | 5.0 | C |

Overall winner: **gemma4:31b-cloud**  
Difference size: **Minor**

Detailed comments:
- A: Reliable technical workflow and useful engineering plotting cues.
- B: Strong structure/readability but blocked by known column-name issue from earlier review.
- C: Technically solid for requested flow and strongest explanatory quality for this task.
- A remains close second on technical confidence.

---

## Task 6 - EC3 steel beam bending snippet review (planted trap test)

Task intent (as provided):
- Catch two planted faults:
  1. Axis error (`Wpl_z` used instead of major-axis `Wpl_y` for gravity bending)
  2. Unit error (N·mm result compared directly to kN·m demand)
- Show corrected working and explicit adequacy conclusion.

| Criterion | A | B | C | Winner |
|---|---:|---:|---:|---|
| Correctness | 4.0 | 1.0 | 4.5 | C |
| Robustness | 4.0 | 1.5 | 4.0 | Tie (A/C) |
| Readability | 4.5 | 2.5 | 4.5 | Tie (A/C) |
| Maintainability | 4.0 | 2.0 | 4.0 | Tie (A/C) |
| Engineering suitability | 4.0 | 1.0 | 4.5 | C |
| Clarity | 5.0 | 2.0 | 5.0 | Tie (A/C) |

Overall winner: **gemma4:31b-cloud**  
Difference size: **Moderate**

Detailed comments:
- A:
  - Correctly catches both planted errors (axis and units).
  - Strong references and working shown.
  - Deduction: introduces LTB as governing and flips final verdict to FAIL based on additional assumptions not defined in the original snippet setup; this weakens strict prompt-grounded correctness.
- B:
  - Catches unit inconsistency but fails to correctly resolve axis convention in the final correction.
  - Reasoning is internally inconsistent and heavily contradictory (multiple reversals on units and values).
  - Final corrected conclusion is not reliable for this test objective.
- C:
  - Cleanly identifies both planted errors with direct fixes.
  - Uses major-axis modulus and proper N·mm to kN·m conversion.
  - Provides clear corrected working and explicit adequacy verdict.

---

## Final Summary Table (Tasks 1-6)

| Task | Winner | Difference size | Notes |
|---|---|---|---|
| Task 1 - Results cleanup | Qwen3.5 27B | Moderate | Strongest technical reliability; C strongest explanatory clarity |
| Task 2 - Slab check | Qwen3.5 27B | Large | A best EC2-aligned implementation; C second-best |
| Task 3 - Geometry assignment | gemma4:31b-cloud | Large | A/B contain summary bugs; C is functionally cleaner |
| Task 4 - Rules engine | Qwen3-Coder-Next | Minor to Moderate | Best readability/maintainability pattern |
| Task 5 - Summary and plotting | gemma4:31b-cloud | Minor | C edges A on clarity with strong technical coverage |
| Task 6 - EC3 trap test | gemma4:31b-cloud | Moderate | Clean catch of both planted errors; B weakest on consistency |

---

## Cross-task Average Scores (Tasks 1-6)

| Criterion | Qwen3.5 27B | Qwen3-Coder-Next | gemma4:31b-cloud |
|---|---:|---:|---:|
| Correctness | 3.67 | 2.17 | 3.75 |
| Robustness | 3.50 | 2.42 | 3.17 |
| Readability | 4.08 | 4.08 | 4.08 |
| Maintainability | 3.92 | 3.67 | 3.83 |
| Engineering suitability | 3.83 | 2.50 | 3.75 |
| Clarity | 4.17 | 4.25 | 5.00 |
| **Overall average** | **3.86** | **3.18** | **3.93** |

Overall ranking (6-task view):
1. **gemma4:31b-cloud** (3.93)
2. **Qwen3.5 27B** (3.86)
3. **Qwen3-Coder-Next** (3.18)

Interpretation:
- Qwen3.5 27B remains very strong on technical engineering logic in core calculation tasks.
- gemma4:31b-cloud now leads overall after Task 6, combining strong technical outcomes with consistently top clarity.
- Qwen3-Coder-Next remains strongest stylistically in some tasks but trails on engineering reliability consistency.

---

## Updated Answers to Final Questions

1. Did Qwen3-Coder-Next feel materially better than Qwen3.5 27B on actual work?
   - Not on correctness-critical engineering checks; it remains stronger in formatting and presentation style.

2. Was the difference only in polish, or also in correctness and usefulness?
   - Both. Correctness differences remain material on several tasks, including the EC3 trap test.

3. Would this gap justify buying hardware around larger local model based on this test?
   - Not by itself. Model choice plus verification workflow still drives most value.

4. Is Qwen3.5 27B already good enough for most daily engineering coding tasks?
   - Yes, with review/checking discipline.

Additional takeaway after Task 6:
- `gemma4:31b-cloud` is now the strongest overall composite performer in this benchmark set.
