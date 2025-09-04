---
description: Streamline a py script
allowed-tools: 
  - Bash(cd pyCode && source .venv/bin/activate && python3 utils/test_predictors.py --predictors *)
  - Bash(cd pyCode && python3 Predictors/*.py)
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
    - make sure `sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))` is used before importing from `utils/`
- Make sure the script still runs    

# DO NOT
- edit any other files