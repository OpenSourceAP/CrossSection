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
- Run the test
    - `python3 utils/test_predictors.py --predictors $ARGUMENTS`

# Debug: fix the superset test problems for $ARGUMENTS
- Find the exact python commands that are causing the problem
    - Pick a specific observation from the "missing observations sample" in test output
        - Example: `permno=11406, yyyymm=199009` 
        - Focus on ONE observation for clarity
    - Find the bad line
        - Write a debug script in `Debug/` that focuses on the year where the observation goes missing, to make the debugging faster and cleaner.
        - Find the exact line of code where the observation goes missing
    - Identify suspect python commands based on the bad line
- Compare the problematic python commands with the corresponding stata 
    - Compare with the Stata counterpart to the python predictor creation script
        - e.g. compare `code/Predictors/AccrualsBM.do` with `pyCode/Predictors/AccrualsBM.`        
    - Search for relevant documentation in `../DocsForClaude/stata_*.md`
    - Search for relevant Journal entries in `../Journal/`
    - If no relevant documentation on the stata command, search the web for info 
    - Check context7 to understand the python version
- Improve the predictor py script there is a significant improvement in the superset test   
    -  You do not need to fix all the problems. Take one step at a time.
- General strategy
    - Think about the plan before writing code
    - Do not assume the code you have written is correct. 
    - Do not hardcode data or use placeholders.
    - Write debugging code in `Debug/` 

# Document the Fix
- Document the lessons learned with an md file in `../Journal/    `
    - Make sure you are in the `pyCode` folder
    - Write a concise summary of the fix