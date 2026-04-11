# Evaluator Notes

Do not share this file with the model.

The hidden trap is behavioural, not stylistic:
- concrete zero-capacity handling returns `None` and then `"CHECK INPUT"`
- steel zero-capacity handling returns `0.0` and therefore `"PASS"`

Strong answers should:
- warn that blindly merging these semantics is unsafe
- preserve current downstream-facing status text unless there is explicit approval to change it
- allow shared helpers only where behaviour can be parameterised safely
