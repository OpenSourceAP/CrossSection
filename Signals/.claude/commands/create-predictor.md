---
description: create a predictor py script
allowed-tools: 
  # Run the validation script inside its venv
  - Bash(cd /Users/idrees/Desktop/CrossSection/Signals/pyCode && source .venv/bin/activate && python3 utils/test_predictors.py --predictors *)
  # Quick file‑existence check for guard clause
  - Bash(test -f Code/Predictors/*)
  # Create debug scipts
  - Write(Debug/*.py)
  - Edit(Debug/*.py)
  # Create a new predictor script
  - Write(pyCode/Predictors/*.py)
  - Edit(pyCode/Predictors/*.py)
examples: 
  - `/create-predictor BM`
---

# Context  
- We are working on the Predictors leg of the project.

# Task  
- Let's translate @Code/Predictors/$ARGUMENTS.do into python. 
- Goals
  - Replicate the logic in the do file, line by line
  - Use test_predictors.py to check the output

# Error handling
- if $ARGUMENTS is not a valid predictor, check with the user on the name of the predictor