# AI testing project: todo list

Ideas and follow-ups that are not yet scheduled. Add a date and a short rationale to each entry; move an entry out when it becomes a branch or a benchmark round.

## Planner plus coder workflow benchmark (added 2026-09-17)

Idea: test a two-model workflow instead of single-model runs. A strong model (GPT-5.6 Sol, or Astra when available) writes the plan; a cheap model (GPT-5.6 Luna at reasoning effort max) does the heavy-lifting coding against an existing app. Motivation: on the v2 tasks Luna matched Sol at roughly one tenth of Terra's price and one twenty-fifth of Sol's, so the split could be both strong and cheap.

Shape to work out before building (brainstorm first):

- Tasks that involve coding against an existing application rather than greenfield snippets, so the coder has to read and respect real code.
- Record token usage per stage (plan, code, any review pass) so the cost of the workflow is measured, not estimated; the run-record token fields and the dashboard usage chart already support per-model accounting and can be extended per stage.
- Make the grading more deterministic than the current rubric-based judging: for example executable acceptance tests, golden outputs, or diff-based checks that a script can score, with the rubric kept only for aspects a script cannot see.
- Decide the control: the same task run single-model with Sol, and single-model with Luna, so the workflow's gain is attributable.
