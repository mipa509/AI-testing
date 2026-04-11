# Evaluator Notes

Do not share this file with the model.

Primary findings expected:
- `load_factors.factored_line_load()` omits the `1.50` factor on imposed load.
- `major_axis_resistance_kNm()` treats `cm3` as if it were `mm3`.
- `build_review_table()` returns only the lowest utilisation row because it sorts ascending and slices `[:1]`.

Secondary details:
- Early rounding before status is not the main bug.
- Good answers should prioritise engineering correctness over style.
