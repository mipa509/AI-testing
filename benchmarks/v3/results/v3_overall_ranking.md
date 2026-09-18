# V3 Overall Ranking

## Cross-Task Average Scores

| Criterion | gemma4:31b-cloud | glm-5.1:cloud | gpt5.4-xhigh | qwen-3.6plus | minimax-m2.7-cloud | kimi-k2-thinking | deepseek-v3.2 | gpt5.6-sol-xhigh | gpt5.6-luna-max |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Calculation correctness | 4 | 5 | 5 | 4 | 5 | 5 | 5 | 5 | 3 |
| Code quality/executability | 4 | 5 | 5 | 4 | 5 | 5 | 5 | 5 | 3 |
| Engineering judgement | 3 | 5 | 5 | 3 | 4 | 4 | 4 | 4 | 4 |
| Unit/assumption handling | 4 | 5 | 5 | 5 | 4 | 4 | 3 | 4 | 4 |
| Notebook traceability/clarity | 3 | 4 | 5 | 4 | 4 | 4 | 4 | 4 | 4 |
| Completeness of deliverable | 4 | 5 | 5 | 4 | 5 | 5 | 5 | 4 | 4 |
| Practical usability | 4 | 4 | 4 | 4 | 4 | 3 | 3 | 4 | 3 |
| Overall average | 3.71 | 4.71 | 4.86 | 4.00 | 4.43 | 4.29 | 4.14 | 4.29 | 3.57 |

## Overall Ranking

1. `gpt5.4-xhigh` - `4.86`
2. `glm-5.1:cloud` - `4.71`
3. `minimax-m2.7-cloud` - `4.43`
4. `kimi-k2-thinking` - `4.29`
5. `gpt5.6-sol-xhigh` - `4.29`
6. `deepseek-v3.2` - `4.14`
7. `qwen-3.6plus` - `4.00`
8. `gemma4:31b-cloud` - `3.71`
9. `gpt5.6-luna-max` - `3.57`

September 2026 note: `gpt5.6-sol-xhigh` and `gpt5.6-luna-max` were scored blind by a new judge alongside April anchor responses and shifted onto the April scale with a per-task calibration offset (see `benchmarks/refresh_2026-09_calibration.md`). Ties on the overall average are ordered by the six-criterion technical mean. April rows are unchanged.

## Recommended Use Cases

- Best notebook drafter: `gpt5.4-xhigh`
- Best technically reliable result: `gpt5.4-xhigh`
- Best value under free-use constraints: `gemma4:31b-cloud` if local or no-cost access is available; fastest usable draft in this run, but it still needs manual QC on the governing-case conclusion.
- Biggest operational weakness observed: Long think time on several otherwise strong models, plus conclusion-level governing-case mistakes in some outputs that would need human review before use.
- September 2026 note: `gpt5.6-sol-xhigh` (4.29) did not match its predecessor on this task because it quoted the compact pressure formula without the requested derivation or eccentricity definitions; `gpt5.6-luna-max` (3.57) stated the correct answer but its notebook stops on its own consistency assert until a one-line formula fix is applied.
