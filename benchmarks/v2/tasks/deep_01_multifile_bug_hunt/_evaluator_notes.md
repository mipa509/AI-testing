# Evaluator Notes

Do not share this file with the model.

Primary planted defect:
- `section_library.get_section_properties()` converts `cm3` to `mm3` using `1e2` instead of `1e3`.

Important secondary risks:
- `build_member_summary()` uses signed `max` instead of a major-axis envelope rule, so large hogging moments can be missed.
- Missing guard for unknown sections.
- The prompt asks for the smallest safe patch, so full rewrites should be penalised.

Strong answers should:
- identify the unit conversion bug as root cause
- call out the envelope issue as a real secondary risk
- propose targeted tests around units and governing moment selection
