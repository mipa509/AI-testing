# Task 3 - Scoped feature design on an existing package

You are asked to design a scoped feature addition to an internal structural design package. Do not write the full implementation. Produce a decision-complete implementation plan.

Feature request:
- Add an optional serviceability summary alongside existing ULS results.
- If deflection data is present, compute `DeflectionRatio = Deflection_mm / AllowableDeflection_mm`.
- Preserve existing callers that only use ULS outputs.
- Keep report output stable for existing downstream consumers.

Read the supplied files and return:
1. The files you would change and why.
2. Any public interface or schema changes.
3. The data-flow changes from input to report.
4. Backward-compatibility risks.
5. Targeted tests and acceptance criteria.

Context files to provide:
- `context/io_contract.py`
- `context/design_engine.py`
- `context/report_writer.py`

Wait for me to provide you with the py files code before proceeding to answer.