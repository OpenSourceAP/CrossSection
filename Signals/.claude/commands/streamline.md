---
description: Streamline a py script
allowed-tools: 
  # Run the validation script inside its venv
  - Bash(cd pyCode && source .venv/bin/activate && python3 utils/test_predictors.py --predictors *)
  # Quick file‑existence check for guard clause
  - Bash(test -f Code/Predictors/*)
  # Create debug scipts
  - Write(Debug/*.py)
  - Edit(Debug/*.py)
  # Edit the py script
  - Edit(pyCode/Predictors/*.py)
examples: 
  - `/streamline pyCode/Predictors/ZZ1_FR_FRbook.py`
---

# Task  
Streamline ${ARGUMENTS}.
- Remove any unnecessary calculations or data loading
- Use functions from `pyCode/utils/` to simplify
    - e.g. `stata_multi_lag`, `save_predictor`, `save_placebo`
- Make sure the script still runs    