# Evaluator Notes

Do not share this file with the model.

Expected issues:
- row-wise `iterrows()` loop is a poor choice at scale
- direct `float()` casts will break on messy values instead of coercing safely
- no handling for zero or missing lengths
- otherwise the core ratio idea is valid

Strong answers should improve performance without making the solution unnecessarily complex.
