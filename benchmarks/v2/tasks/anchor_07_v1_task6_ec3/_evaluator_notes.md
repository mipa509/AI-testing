# Evaluator Notes

Do not share this file with the model.

This anchor preserves the planted v1 objective:
- planted fault 1: wrong axis property (`Wpl_z` used instead of major-axis `Wpl_y`)
- planted fault 2: unit conversion error from `N.mm` to `kN.m`

Scoring guidance:
- reward direct identification and correction of those two faults
- reward clear corrected adequacy conclusion
- penalise answers that drift into extra assumptions and replace the planted objective with a different design problem
