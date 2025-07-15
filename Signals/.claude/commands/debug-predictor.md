---
description: Debug a predictor that is failing validation
allowed-tools: 
  # Run the validation script inside its venv
  - Bash(cd /Users/chen1678/Dropbox/oap-ac/CrossSection/Signals/pyCode && source .venv/bin/activate && python3 utils/test_predictors.py --predictors *)
  # Quick file‑existence check for guard clause
  - Bash(test -f Code/Predictors/*)
  # Create debug scipts
  - Write(Debug/*.py)
  - Edit(Debug/*.py)
examples: 
  - `/debug-predictor AccrualsBM`
---

# Context  

- Latest test output for **$ARGUMENTS**:  
  !`cd /Users/chen1678/Dropbox/oap-ac/CrossSection/Signals/pyCode && \
    source .venv/bin/activate && \
    python3 utils/test_predictors.py --predictors $ARGUMENTS`

# Task  
Let's debug @pyCode/Predictors/$ARGUMENTS.py. The tests above fail.  

1. Summarise the failures and isolate the first breaking assertion.  
2. List hypotheses for root causes (data mismatch, index alignment, logic divergence, I/O issues, etc.).  
3. For each hypothesis, propose one quick check (diff, assert, or print).  
4. Emit small debug helpers or one‑off scripts as needed (shell or Python).  
5. Return an ordered action plan with estimated effort per step.

think about the plan.
