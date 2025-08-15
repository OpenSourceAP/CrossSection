# Plan: use logs from do files to debug superset failures

## Context

Plan/0814n1-editdo-superset.md describes how we added do file log output to help trace superset failures.

## Task: use the logs to debug the superset failures

- Read the do file log in `Human/Logs/*.log`
- Run the corresponding python script in `pyCode/Predictors/*.py`
- Compare the output of the python script with the do file log
    - Identify the checkpoint where the missing observations disappears
- Think of up to three hypotheses for the problems and test them
    - Check `DocsForClaude/traps.md` for common pitfalls 
    - Write py scripts in `Debug/` to test the hypotheses
      - Do NOT edit the `py` script for the predictor in this step.
    - If your hypothesis is that the underlying data is different, check the underlying datasets that are being imported in the `do` file and the `py` script.
- Attempt to fix the problem in the `py` script
    - Once your hypothesis is confirmed, edit the `py` script to fix the problem
    - Test with `python3 utils/test_predictors.py --predictors [predictor_name]`
    - Iterate