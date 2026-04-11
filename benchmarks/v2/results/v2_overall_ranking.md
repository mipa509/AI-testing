# V2 Overall Ranking

This ranking covers the six new v2 tasks for `gemma4:31b-cloud`, `glm-5.1:cloud`, `gpt5.4-xhigh`, `qwen-3.6plus`, `minimax-m2.7-cloud`, `kimi-k2-thinking`, and `deepseek-v3.2`.

## Cross-Task Average Scores

| Criterion | gemma4:31b-cloud | glm-5.1:cloud | gpt5.4-xhigh | qwen-3.6plus | minimax-m2.7-cloud | kimi-k2-thinking | deepseek-v3.2 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Correctness | 4.00 | 3.83 | 4.33 | 4.00 | 3.67 | 3.50 | 2.67 |
| Repo comprehension | 4.00 | 3.83 | 4.50 | 4.17 | 4.00 | 3.50 | 2.83 |
| Change safety | 3.83 | 3.50 | 4.00 | 3.33 | 3.50 | 3.33 | 2.33 |
| Engineering judgement | 4.00 | 3.67 | 4.33 | 3.67 | 3.50 | 3.33 | 2.50 |
| Maintainability | 4.00 | 4.00 | 4.17 | 4.00 | 4.17 | 3.50 | 2.86 |
| Clarity | 4.17 | 4.50 | 4.83 | 4.00 | 4.17 | 4.17 | 3.17 |
| Economics/practicality | 4.67 | 3.83 | 2.83 | 3.00 | 3.00 | 4.33 | 2.17 |
| Overall average | 4.10 | 3.88 | 4.14 | 3.74 | 3.72 | 3.67 | 2.65 |

## Overall Ranking

1. `gpt5.4-xhigh`
2. `gemma4:31b-cloud`
3. `glm-5.1:cloud`
4. `qwen-3.6plus`
5. `minimax-m2.7-cloud`
6. `kimi-k2-thinking`
7. `deepseek-v3.2`

## Recommended Use Cases

- Best premium reference model: `gpt5.4-xhigh`
- Best primary coder: `gpt5.4-xhigh`
- Best reviewer: `gpt5.4-xhigh`
- Best value under free-use constraints: `gemma4:31b-cloud`
- Best grounded paid/API middle option: `qwen-3.6plus`
- Biggest operational weakness observed: Severe context-fidelity failures before or without the supplied files, especially on `kimi-k2-thinking` and `deepseek-v3.2`
