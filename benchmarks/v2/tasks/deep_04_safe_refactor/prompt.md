# Task 4 - Safe refactor with behaviour preservation constraints

You are reviewing a proposed refactor. The author wants to "deduplicate shared utilisation helpers" across steel and concrete modules.

Read the supplied files and return:
1. Whether the refactor is safe in principle.
2. Which logic may be shared and which behaviour must remain distinct.
3. A minimal refactor approach that preserves behaviour.
4. Tests or regression checks needed before merging.

Constraints:
- Assume downstream spreadsheets depend on current status text.
- Do not recommend a broad rewrite.
- Penalise any refactor that silently changes zero-denominator behaviour.

Context files to provide:
- `context/concrete_checks.py`
- `context/steel_checks.py`
- `context/common_formatting.py`

Wait for me to provide you with the py files code before proceeding to answer.