# V2 Per-Task Results

Current scored slate: `gemma4:31b-cloud`, `glm-5.1:cloud`, `gpt5.4-xhigh`, `qwen-3.6plus`, `minimax-m2.7-cloud`, `kimi-k2-thinking`, and `deepseek-v3.2`.

| Task | Winner | Difference size | Notes |
|---|---|---|---|
| Task 1 - Multi-file bug hunt | `gemma4:31b-cloud` | Small | `gemma` found the real conversion bug and paired it with the strongest repo-grounded secondary risk. `qwen` and `minimax` were grounded but both missed the signed-moment envelope trap, while `kimi` hallucinated a different repo. |
| Task 2 - Repo review traps | `gemma4:31b-cloud` | Small | `gemma`, `kimi`, and `qwen` all caught the three real blockers. `minimax` found only two of them because it missed the actual resistance unit defect. |
| Task 3 - Scoped feature design | `gpt5.4-xhigh` | Small | GPT-5.4 produced the clearest compatibility-preserving opt-in SLS design: it kept existing ULS interfaces stable and avoided widening `report_rows()` by default. |
| Task 4 - Safe refactor | `kimi-k2-thinking` | Very small | `kimi`, `glm`, `gemma`, `gpt`, `qwen`, and `minimax` were all strong; the gap here is mostly presentation and practicality rather than core technical quality. |
| Task 5 - Large dataset pipeline | `kimi-k2-thinking` | Small | All seven recognised the vectorisation need, but `kimi` still best balanced performance improvement with a stable output contract. |
| Task 6 - Review plus tests | `glm-5.1:cloud` | Small | No model was ideal. `glm` stayed closest to the real helper semantics overall; `gpt` and `minimax` were more grounded than most, while `qwen` missed the hidden unit-consistency bug. |
