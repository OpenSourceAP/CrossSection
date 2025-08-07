---
description: Debug a predictor that is failing validation
allowed-tools: 
  # Run the validation script inside its venv
  - Bash(cd /Users/idrees/Desktop/CrossSection/Signals/pyCode && source .venv/bin/activate && python3 utils/test_predictors.py --predictors *)
  # Quick file‑existence check for guard clause
  - Bash(test -f Code/Predictors/*)
  # Create debug scipts
  - Write(ClaudeDebug/*.py)
  - Edit(ClaudeDebug/*.py)
  # Edit the py script
  - Edit(pyCode/Predictors/*.py)
examples: 
  - `/debug-predictor AccrualsBM`
---

# Context  

- Latest test output for **${ARGUMENTS}**:  
  !`cd /Users/idrees/Desktop/CrossSection/Signals/pyCode && \
    source .venv/bin/activate && \
    python3 utils/test_predictors.py --predictors ${ARGUMENTS}`

# Task  
Let's debug @pyCode/Predictors/${ARGUMENTS}.py. The tests above fail.  
- Select a specific observation that is causing the test to fail and bisect
    - Read the bisection strategy in Journal/2025-07-16_AnalystRevision_bisection_debugging.md
    - Look for the line of the py script that is causing this observation to be problematic
- Study recent entries in Journal/ for previous debugging lessons
- Think about the plan before writing code
- Read and carefully understand the Debugging philosophy from @CLAUDE.md. 
- Do not assume the code you have written is correct. 
- When recovering missing rows, just creating placeholder data or hard coding results to satisfy the condition is absolutely unacceptable. We want real fixes that mimic the original stata code's behavior, not hard coded fixes which mask the actual issue. 
- If the issue is truly a data issue, then point out which intermediate dataset + permnoyyyymm combinations are facing this issue. 
- Check both stata and python datasets before saying there are data discrepancies.

# Error Handling
- If **${ARGUMENTS}** is not a valid predictor, check with the user on the name of the predictor