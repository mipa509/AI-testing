# V3 Per-Task Results

| Task | Winner | Difference size | Notes |
|---|---|---|---|
| Task 1 - Square pad footing sizing notebook draft | `gpt5.4-xhigh` | `moderate` | Several models found `3.0 m`, but `gpt5.4-xhigh` gave the cleanest derivation, clearest explanation of why `2.9 m` fails on uplift in `LC2`, and the strongest notebook traceability with minimal cleanup. |

September 2026 refresh: the winner is unchanged. `gpt5.6-sol-xhigh` scored 4.29 overall (correct `3.0 m` and `LC2`, executable, but no derivation or eccentricity definitions) and `gpt5.6-luna-max` scored 3.57 (correct narrative answer, but the code fails its own consistency assert at code cell 4 and produces no result).

DeepSeek V4.1 Flash addendum (2026-09-18): the winner is unchanged. `deepseek-v4.1-flash` scored 4.71 overall (correct `3.0 m` and `LC2`, runs end to end, kern-rule cross-check; loose cell alternation and a section-modulus derivation), level with `glm-5.1:cloud`.

GLM 5.3 Flash addendum (2026-09-18): the winner is unchanged. `glm-5.3-flash` scored 4.00 overall (correct `3.0 m` and `LC2` in the Markdown with a full derivation and sweep, but the code prints `LC3` as governing and the middle-third equivalence claim is wrong for biaxial loading).

Tencent Hy4 Preview addendum (2026-09-18): the winner is unchanged. `tencent-hy4-preview` scored 4.71 overall (correct `3.0 m` and `LC2`, runs end to end, explicit `M*c/I` derivation, corner pressures and closed-form bounds; eccentricity naming reversed relative to the reference and stated as such).
