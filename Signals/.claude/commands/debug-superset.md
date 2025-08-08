---
description: Debug failures of the superset test for a given predictor. 
  - Trying to make debugging more systematic.
allowed-tools:
  # TBC: allow only the predictor in $ARGUMENTS to be edited
  - Edit(Predictors/*.py)
examples:
  - `/debug-superset AccrualsBM`
---

# Set the Context
- First orient yourself and set up the environment
    - `cd pyCode` (if not already there)
    - `source .venv/bin/activate` (if not already activated)
- Run the test
    - `python3 utils/test_predictors.py --predictors $ARGUMENTS`

# Debug Task
- Debug the superset test problems for $ARGUMENTS
    - Check DocsForClaude/debugging-philosophy.md for debugging strategy
    - Check DocsForClaude/stata_*.md to understand Stata's exact behavior. Use context7 to understand the python version. 
    - Study recent entries in Journal/ for relevant debugging lessons
    - Think about the plan before writing code
    - Do not assume the code you have written is correct. 
    - Do not hardcode data or use placeholders.
    - Write code in `Debug/` to trace exactly where the problematic observations go missing.

# Document the Fix
- Document the lessons learned with an md file in `../Journal/    `
    - Make sure you are in the `pyCode` folder
    - Write a concise summary of the fix