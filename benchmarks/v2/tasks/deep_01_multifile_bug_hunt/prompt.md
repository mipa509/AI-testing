# Task 1 - Multi-file bug hunt in a member check pipeline

You are reviewing a small structural engineering Python package that summarises beam bending checks from analysis results.

The team reports that some major-axis utilisation ratios look materially too high after a recent refactor.

Read the supplied files and do all of the following:
1. Identify the most likely root-cause defect.
2. Identify any secondary risks worth fixing in the same patch.
3. Propose the smallest safe multi-file fix.
4. State what tests you would add before merging.

Constraints:
- Do not rewrite the whole package.
- Assume this is a code-review and fix-design task, not a greenfield implementation.
- Be explicit about units and section-property conventions.
- Order findings by severity.

Context files to provide:
- `context/analysis_pipeline.py`
- `context/section_library.py`
- `context/reporting.py`
