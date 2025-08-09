---
description: Debug failures of the Precision1 test for a given predictor. 
  - Trying to make debugging more systematic.
allowed-tools:
  # TBC: allow only the predictor in $ARGUMENTS to be edited
  - Edit(Predictors/*.py)
  - Write(Debug/*.py)
  - Edit(Debug/*.py)
  - Bash(touch:*)
examples:
  - `/debug-prec1 AccrualsBM`
---

# Set the Context
- Make sure you are in the `Signals/` folder
    - use `pwd` to check the current directory
    - always return to the `Signals/` folder after each command
- Run the test
    - `cd pyCode && python3 utils/test_predictors.py --predictors $ARGUMENTS && cd ..`
- Make sure you can write to `Debug/`
    - `touch Debug/test.py`

# Debug: fix the Precision1 test problems for $ARGUMENTS
- Find the exact python commands that are causing the problem
    - Pick a specific observation from the "Largest Differences" in test output
        - Example: `permno=76995, yyyymm=200003` 
        - Focus on ONE observation for clarity
    - Find the bad line
        - Write a debug script in `../Debug/` that focuses on the year where the observation has largest difference, to make the debugging faster and cleaner.
        - Find the exact line of code where the observation starts to diverge
            - It is likely when the signal is first calculated
    - Identify suspect python commands based on the bad line
- Compare the problematic python commands with the corresponding stata 
    - Compare with the Stata counterpart to the python predictor creation script
        - e.g. compare `code/Predictors/AccrualsBM.do` with `pyCode/Predictors/AccrualsBM.`        
    - Search for relevant documentation in `DocsForClaude/stata_*.md`
    - Search for relevant Journal entries in `Journal/`
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