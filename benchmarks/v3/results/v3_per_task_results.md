# V3 Per-Task Results

| Task | Winner | Difference size | Notes |
|---|---|---|---|
| Task 1 - Square pad footing sizing notebook draft | `gpt5.4-xhigh` | `moderate` | Several models found `3.0 m`, but `gpt5.4-xhigh` gave the cleanest derivation, clearest explanation of why `2.9 m` fails on uplift in `LC2`, and the strongest notebook traceability with minimal cleanup. |

September 2026 refresh: the winner is unchanged. `gpt5.6-sol-xhigh` scored 4.29 overall (correct `3.0 m` and `LC2`, executable, but no derivation or eccentricity definitions) and `gpt5.6-luna-max` scored 3.57 (correct narrative answer, but the code fails its own consistency assert at code cell 4 and produces no result).

DeepSeek V4.1 Flash addendum (2026-09-18): the winner is unchanged. `deepseek-v4.1-flash` scored 4.71 overall (correct `3.0 m` and `LC2`, runs end to end, kern-rule cross-check; loose cell alternation and a section-modulus derivation), level with `glm-5.1:cloud`.

GLM 5.3 Flash addendum (2026-09-18): the winner is unchanged. `glm-5.3-flash` scored 4.00 overall (correct `3.0 m` and `LC2` in the Markdown with a full derivation and sweep, but the code prints `LC3` as governing and the middle-third equivalence claim is wrong for biaxial loading).

Tencent Hy4 Preview addendum (2026-09-18): the winner is unchanged. `tencent-hy4-preview` scored 4.71 overall (correct `3.0 m` and `LC2`, runs end to end, explicit `M*c/I` derivation, corner pressures and closed-form bounds; eccentricity naming reversed relative to the reference and stated as such).

Claude Fable 5.1 addendum (2026-09-19): the winner is unchanged. `claude-fable-5.1-high` scored 4.36 overall (two-judge mean; 4.71 on the Claude judge alone) (correct `3.0 m` and `LC2`, runs end to end, Navier derivation with the kern limit, full pass/fail matrix and a closed-form width cross-check; 5.00 on the technical criteria, 3 on practicality for the slowest and most expensive v3 run recorded).

Gemma 4 26B local addendum (2026-09-19): the winner is unchanged. `gemma4:26b-local` scored 2.86 overall (revised from 2.00 under the September offset) (correct derivation, but the code does not run and the conclusion states `2.9 m` with `LC1` governing; 2.83 on the technical criteria after the offset, 3 on practicality as a free local run whose notebook needs fixing before it executes).
