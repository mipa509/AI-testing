# V3 Overall Ranking

## Cross-Task Average Scores

| Criterion | gemma4:31b-cloud | glm-5.1:cloud | gpt5.4-xhigh | qwen-3.6plus | minimax-m2.7-cloud | kimi-k2-thinking | deepseek-v3.2 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Calculation correctness | 4 | 5 | 5 | 4 | 5 | 5 | 5 |
| Code quality/executability | 4 | 5 | 5 | 4 | 5 | 5 | 5 |
| Engineering judgement | 3 | 5 | 5 | 3 | 4 | 4 | 4 |
| Unit/assumption handling | 4 | 5 | 5 | 5 | 4 | 4 | 3 |
| Notebook traceability/clarity | 3 | 4 | 5 | 4 | 4 | 4 | 4 |
| Completeness of deliverable | 4 | 5 | 5 | 4 | 5 | 5 | 5 |
| Practical usability | 4 | 4 | 4 | 4 | 4 | 3 | 3 |
| Overall average | 3.71 | 4.71 | 4.86 | 4.00 | 4.43 | 4.29 | 4.14 |

## Overall Ranking

1. `gpt5.4-xhigh`
2. `glm-5.1:cloud`
3. `minimax-m2.7-cloud`
4. `kimi-k2-thinking`
5. `deepseek-v3.2`
6. `qwen-3.6plus`
7. `gemma4:31b-cloud`

## Recommended Use Cases

- Best notebook drafter: `gpt5.4-xhigh`
- Best technically reliable result: `gpt5.4-xhigh`
- Best value under free-use constraints: `gemma4:31b-cloud` if local or no-cost access is available; fastest usable draft in this run, but it still needs manual QC on the governing-case conclusion.
- Biggest operational weakness observed: Long think time on several otherwise strong models, plus conclusion-level governing-case mistakes in some outputs that would need human review before use.
