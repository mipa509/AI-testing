# Evaluator Notes

Do not share this file with the model.

Expected issues:
- `settlement_ratio()` returning `0.0` for zero allowable is unsafe
- `differential_slope()` mixes `mm` and `m`, so the output is numerically inconsistent
- strong answers should propose targeted tests around zero allowable, unit conversion, and borderline pass/fail thresholds
