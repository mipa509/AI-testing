# Evaluator Notes

Do not share this file with the model.

Strong answers should preserve backward compatibility:
- existing ULS-only callers must continue to work unchanged
- existing `RESULT_COLUMNS` ordering is part of the current report contract
- serviceability data should be optional, not mandatory

Preferred design direction:
- add serviceability columns only when relevant data exists or via an optional flag
- avoid breaking `report_rows()` for downstream consumers expecting the current schema
- include tests for both ULS-only and ULS-plus-SLS flows
