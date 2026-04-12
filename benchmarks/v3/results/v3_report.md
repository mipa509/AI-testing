# V3 Benchmark Report

## Executive Summary

V3 benchmarked seven models on one deterministic notebook-style structural engineering task: preliminary sizing of a square pad footing under service loads using a rigid-footing linear-pressure model. The benchmark was designed to test whether a model could convert an engineering brief into a readable Markdown-plus-Python notebook draft while preserving calculation correctness, unit discipline, and engineering judgement.

The winning model was `gpt5.4-xhigh`, followed by `glm-5.1:cloud` and `minimax-m2.7-cloud`. Several models reached the correct footing size of `3.0 m x 3.0 m`, so the decisive separation came from auditability, handling of the `2.9 m` uplift trap, governing-case framing, and notebook usability rather than from final size alone.

## Benchmark Scope

- Benchmark round: `v3`
- Task count: `1`
- Task ID: `v3-notebook-01`
- Task title: `Square pad footing sizing notebook draft`
- Model slate:
  - `gpt5.4-xhigh`
  - `gemma4:31b-cloud`
  - `glm-5.1:cloud`
  - `qwen-3.6plus`
  - `minimax-m2.7-cloud`
  - `kimi-k2-thinking`
  - `deepseek-v3.2`

## Task Brief In One Paragraph

Models were asked to produce an ordered notebook-style Markdown draft with alternating Markdown and Python code cells for sizing a square pad footing supporting one reinforced concrete column. The design check was limited to service-load bearing pressure and no-uplift, using candidate footing widths from `2.4 m` to `3.2 m` in `0.1 m` steps. The correct outcome was to select `3.0 m x 3.0 m`, governed by `LC2`, because `2.9 m` still fails the no-uplift criterion with `qmin = -0.410 kPa`.

## Method And Scoring

Scoring used the completed v3 scorecard and manual engineering review against the checked reference solution. The seven criteria were:

1. Calculation correctness
2. Code quality and executability
3. Engineering judgement
4. Unit and assumption handling
5. Notebook traceability and clarity
6. Completeness of deliverable
7. Practical usability

Practical usability was treated as a light secondary factor. Latency and operational friction influenced scoring, but they did not override correctness and engineering quality.

## Reference Engineering Outcome

- Correct selected footing: `3.0 m x 3.0 m`
- Governing selection case: `LC2`
- Key failure trap: `2.9 m` is incorrect because `LC2` gives `qmin = -0.410 kPa`
- Important distinction:
  - `LC3` has the largest `qmax` at the selected size
  - `LC2` governs footing selection because it controls no-uplift

This distinction mattered materially in the benchmark because multiple models were able to compute correct pressures but still framed the governing case incorrectly in the final conclusion.

## Overall Ranking

| Rank | Model | Overall Average |
|---|---|---:|
| 1 | `gpt5.4-xhigh` | 4.86 |
| 2 | `glm-5.1:cloud` | 4.71 |
| 3 | `minimax-m2.7-cloud` | 4.43 |
| 4 | `kimi-k2-thinking` | 4.29 |
| 5 | `deepseek-v3.2` | 4.14 |
| 6 | `qwen-3.6plus` | 4.00 |
| 7 | `gemma4:31b-cloud` | 3.71 |

## Model-by-Model Review

### 1. `gpt5.4-xhigh`

Strengths:
- Strongest overall task fit
- Exact handling of the `2.9 m` uplift trap
- Best derivation from `q = N/A +/- Mx*y/Ix +/- My*x/Iy`
- Clear distinction between maximum-compression case and governing selection case
- Clean executable notebook structure with minimal cleanup required

Weaknesses:
- Long think time relative to the fastest runs

Why it won:
It combined correct mechanics, correct selection logic, clear notebook flow, and the most auditable engineering conclusion.

### 2. `glm-5.1:cloud`

Strengths:
- Very strong reference-aligned derivation
- Correct `3.0 m` selection
- Correct overall governing case `LC2`
- Good executable code and solid assumptions

Weaknesses:
- Slightly plainer notebook flow than the winner
- Less polished in presentation and traceability than `gpt5.4-xhigh`

Why it placed second:
Technically strong and reliable, but marginally less compelling as an assistant-engineer notebook draft.

### 3. `minimax-m2.7-cloud`

Strengths:
- Correct result
- Clear structure and good presentation
- Correct distinction between bearing-governing and uplift-governing cases
- Runnable code and complete deliverable

Weaknesses:
- Uses an `abs(Mx) + abs(My)` framing in the narrative, which is less rigorous than the explicit sign-convention path in the reference approach

Why it placed third:
Strong usable output with only a modest modelling-expression penalty.

### 4. `kimi-k2-thinking`

Strengths:
- Correct selected size and governing case
- Good assumptions and usable notebook structure
- Runnable code

Weaknesses:
- Pressure model is presented mostly through a section-modulus shortcut rather than the clearest reference derivation
- Governing-case logic is more heuristic than explicit
- Slow run

Why it placed fourth:
Technically good, but less transparent and less direct than the top three.

### 5. `deepseek-v3.2`

Strengths:
- Correct final size
- Runnable code
- Reasonably complete deliverable

Weaknesses:
- Written eccentricity definitions are swapped in the assumptions section
- Narrative precision is weaker than the stronger entries
- Slow run and weaker notebook pacing

Why it placed fifth:
Good calculation core, but weaker written engineering framing and lower practical usability.

### 6. `qwen-3.6plus`

Strengths:
- Strong derivation and correct size search
- Good unit discipline
- Underlying Python content runs and reaches the correct selected footing size

Weaknesses:
- Final conclusion reports `LC3` as governing instead of `LC2`
- Exported artifact used VS Code cell wrappers rather than clean benchmark notebook formatting
- Final Markdown retained unresolved placeholders

Scoring note:
Per review direction, this run was judged mainly on content rather than being heavily penalized for the wrapper-export format.

Why it placed sixth:
Strong mid-pack content, but the conclusion-level governing-case error mattered on a benchmark where the key discriminator was exactly that distinction.

### 7. `gemma4:31b-cloud`

Strengths:
- Fastest reported run in the slate
- Correct `3.0 m` selection
- Runnable code

Weaknesses:
- Final prose leaves unresolved placeholders
- Labels `LC3` as the governing case without separating maximum compression from governing selection
- Notebook traceability is weaker than most of the field

Why it placed seventh:
It solved the size selection, but the conclusion-level framing was weak and required the most manual interpretation relative to the rest of the slate.

## Cross-Model Patterns

### What Strong Models Did Well

- Stated the rigid-footing linear-pressure model clearly
- Explained why the model was appropriate for preliminary screening
- Derived or transparently justified the edge-pressure equations
- Preserved unit consistency between `kN`, `kNm`, `m`, and `kPa`
- Searched all candidate sizes explicitly
- Reported why `2.9 m` fails and why `3.0 m` is the first passing width
- Distinguished between the case with the largest `qmax` and the case that governs selection

### Common Failure Modes

- Correct final size but wrong governing-case wording
- Weak explanation of the uplift failure at `2.9 m`
- Shortcut formulas without enough derivation or sign-convention grounding
- Placeholder leakage in final prose
- Formatting/export artifacts that reduced direct usability as a notebook draft

## Practical Takeaways

- For notebook-style structural engineering drafting, the benchmark rewarded models that could make the reasoning auditable, not just numerically correct.
- The key benchmark trap was subtle enough that a model could appear strong while still failing the most important judgement distinction.
- Fast models still have value because they can be revised quickly, but if they blur governing-case logic, they demand closer human review.
- Several models are already usable as assistant-engineer drafting tools, but only the top group produced outputs that needed minimal correction before reuse.

## Recommended Use Cases

- Best notebook drafter: `gpt5.4-xhigh`
- Best technically reliable result: `gpt5.4-xhigh`
- Strong conservative runner-up: `glm-5.1:cloud`
- Best value under free-use constraints: `gemma4:31b-cloud`, with the caution that conclusion-level QC is still required

## Limitations Of V3

- V3 currently contains only one scored task, so the ranking is highly sensitive to this single notebook-style problem.
- The task intentionally emphasized one engineering trap, so future rounds should broaden the range of traps and deliverable styles.
- Operational observations were manually recorded and not normalized across platforms, so usability comparisons should remain secondary.

## Next Steps

1. Expand v3 with more notebook-style tasks that stress different engineering failure modes.
2. Add at least one task where the correct answer is not recovered by a simple search loop.
3. Record latency and interaction friction more systematically if practicality is going to remain a tracked metric.
4. Separate "maximum-demand case" from "governing selection case" explicitly in future scorecards, since that distinction clearly separated strong from merely adequate outputs.
